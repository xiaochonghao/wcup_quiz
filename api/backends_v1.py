# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
import logging
import requests
from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.db import transaction

from orm.account.models import User
from utils import gen_md5
from service.api_util import catch_order_exception

logger = logging.getLogger('account')


class UserAuthenBackend(ModelBackend):
    def authenticate(self, name=None, pw=None, user_id=None, device_id=None,
                     code=None, request=None, **kwargs):
        """Authenticate user."""
        sso = SSO()
        if name and pw:
            logger.info('backends, authenticate from username and password, name: %s' % name)
            sso._authen(name, pw, user_id, device_id)
        elif code:
            logger.info('backends, authenticate from wechat, code: %s' % code)
            result = sso._verify(code)
            if result:
                user_id, device_id = result
                user = User(ext_data={
                    'u_id': user_id,
                    'd_id': device_id
                })
                return user
        else:
            return
        if not sso.token:
            return
        user = sso._update_user()
        return user

    def get_user(self, user_id):
        """
        获取用户
        :param user_id:
        :return:
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class SSO(object):
    headers = {'Accept': 'Application/json',
               'Content-Type': 'Application/json'}

    def __init__(self):
        self.app_id = settings.CORP_SSO_APP_ID
        self.app_secret = settings.CORP_SSO_APP_SECRET
        self.token = None
        self.code = None

    @property
    def token_headers(self):
        _headers = self.headers
        _headers['Access-Token'] = self.token
        return _headers

    def _authen(self, username, password, user_id=None, device_id=None):
        """认证用户名密码，登录校验，并返回token

        :param username:
        :param password:
        :param user_id:
        :param device_id:
        :return:
        """
        logger.info('backends, authen from username and password, name: %s' % username)
        params = {
            'appId': self.app_id,
            'appSecret': self.app_secret,
            'username': username,
            'passwd': password,
        }
        if user_id and device_id:
            logger.info('backends, authen at first time, binding wechat, name: %s' % username)
            sign = gen_md5(
                str(device_id) +
                str(password) +
                str(user_id) +
                str(username) +
                gen_md5(str(device_id) + str(password) + str(user_id) +
                        str(username) + str(self.app_id)) +
                str(self.app_secret))
            params.update({
                'userId': user_id,
                'deviceId': device_id,
            })
        else:
            logger.info('backends, authen commonly name: %s' % username)
            sign = gen_md5(
                str(password) +
                str(username) +
                gen_md5(str(password) + str(username) + str(self.app_id)) +
                str(self.app_secret))
        params.update({'sign': sign})
        resp = requests.post(settings.CORP_SSO_AUTHEN_URL,
                             json=params,
                             headers=self.headers)
        try:
            data = resp.json()
            status = data.get('status')
            token = data.get('Access-Token')
            if status == 'success' and token:
                self.token = token
                logger.info('backends, authen success, name: %s' % username)
                return
            logger.info('backends, authen failed, response data: %s' % data)
        except Exception as e:
            logger.info('backends, authen exception')
            logger.exception(e)

    def _verify(self, code):
        """校验code

        :param code:
        :return:
        """
        logger.info('backends, verify code: %s' % code)
        sign = gen_md5(
            str(code) +
            gen_md5(str(code) + str(self.app_id)) +
            str(self.app_secret))

        resp = requests.post(settings.CORP_SSO_VERIFY_URL,
                             json={'appId': self.app_id,
                                   'appSecret': self.app_secret,
                                   'code': code,
                                   'sign': sign},
                             headers=self.headers)

        try:
            data = resp.json()
            status = data.get('code')
            token = data.get('Access-Token')

            if status == '200' and token:
                # 非第一次登录，返回token
                self.token = token
                logger.info('Not first login, verify code success, code: %s' % code)
                return

            # 第一次登录，只能获取到user_id，device_id
            user_id = data.get('userId')
            device_id = data.get('deviceId')
            if user_id and device_id:
                logger.info('First login, get user id: %s, device id: %s success' % (user_id, device_id))
                return user_id, device_id

            logger.info('Unknown error happens, verify failed, response data: %s' % data)
        except Exception as e:
            logger.error('verify exception: %s' % e.message, exc_info=True)
            raise e

    def _user_info(self):
        """获取用户信息

        :param token:
        :return:
        """
        headers = self.token_headers
        sign = gen_md5(
            self.token +
            gen_md5(self.token + self.app_id) +
            self.app_secret)
        headers.update({'appId': self.app_id, 'appSecret': self.app_secret, 'sign': sign})
        resp = requests.get(
            settings.CORP_SSO_USER_URL,
            headers=self.token_headers)
        try:
            data = resp.json()
            status = data.get('status')
            employee = data.get('employee')
            if status == 'success' and employee:
                logger.info('backends, user info success, user info: %s' %
                            data)
                return employee
            logger.info('backends, user info failed, user info: %s' % data)
            return {}
        except Exception as e:
            logger.info('backends, user info exception')
            logger.exception(e)
            return {}

    @catch_order_exception('更新用户信息')
    def _update_user(self, token=None):
        """获取并更新用户信息

        :param token:
        :return:
        """
        if not token:
            token = self.token
        user_info = self._user_info()
        if not user_info:
            return
        sso_id = user_info.get('id')
        if not sso_id:
            logger.info(
                'backends, get sso_id failed, employee: %s.' % user_info)
            return None
        else:
            logger.info(
                'backends, update user, employee: %s' % user_info)
            ad_acount = user_info.get('adAccount')
            employee_no = user_info.get('employeeNo')
            id_no = user_info.get('idNo')
            phone = user_info.get('phone')
            email = user_info.get('email')
            department = user_info.get('department')
            wechat_id = user_info.get('weChatId')

            # 检查sso_id在用户表中是否有用户对应
            with transaction.atomic():
                user = User.objects.filter(pk=sso_id).first()
                if not user:
                    logger.info('this user<sso_id=%s> does not exist in account_user table' % sso_id)
                    user = User.objects.add_new(sso_id, ad_acount, employee_no, id_no, phone, email, department, wechat_id, token)
                return user
