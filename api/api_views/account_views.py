# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.contrib.auth import authenticate, logout, login
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.authentication import BasicAuthentication

from api.api_serializers import account_serializers
from service.api_util import CodeMsg, CommonReturn
from api import api_serializer_deco, CsrfExemptSessionAuthentication
from utils import parse_ipadress

logger = logging.getLogger(__name__)


# Create your views here.


class AccountViewSet(viewsets.GenericViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    @list_route(methods=['POST'],
                url_path='login',
                serializer_class=account_serializers.LoginSerializer)
    def login(self, request):
        """
        登陆接口
        :param request:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            res = {
                "code": CodeMsg.PARAM_ERROR['code'],
                "msg": serializer.errors,
                "status": 0
            }
            return Response(res)
        user_name = serializer.data.get('user_name')
        password = serializer.data.get('password')
        user_id = serializer.data.get('user_id', None)
        device_id = serializer.data.get('device_id', None)
        user = authenticate(name=user_name, pw=password, user_id=user_id, device_id=device_id)
        if user and user.is_authenticated():
            login(request, user)
            res = {"status": 1, "code": 200, "msg": CodeMsg.SUCCESS}
        else:
            res = {"status": 0, "code": 401, "msg": "用户名或密码错误"}
        return Response(res)

    @list_route(methods=['GET'],
                url_path='logout')
    @api_serializer_deco('登出')
    def logout(self, request):
        """
        退出登陆
        :param request:
        :return:
        """
        logout(request)
        return CommonReturn(CodeMsg.SUCCESS, '登出成功')

    @list_route(methods=['GET'],
                url_path='user_info')
    @api_serializer_deco('获取用户信息')
    def user_info(self, request):
        """
        获取用户信息
        :param request:
        :return:
        """
        user_id = request.user.pk
        if not user_id:
            logger.error('request user is empty', exc_info=True)
            return CommonReturn(CodeMsg.UNKNOWN_ERROR, '获取用户信息失败')
        coins = request.user.capital if request.user.capital else 0
        res = {
            "user_id": user_id,
            "user_name": request.user.name,
            "coins": float(coins)
        }
        return CommonReturn(CodeMsg.SUCCESS, 'success', res)

    @list_route(methods=['POST'],
                url_path='authen',
                serializer_class=account_serializers.AuthenSerializer)
    @api_serializer_deco('code认证', ignore_login=True)
    def authen(self, request, serializer_data=None):
        """
        code认证api
        :param request:
        :param serializer_data:
        :return:
        """
        code = serializer_data.get('code')
        if not code:
            return CommonReturn(CodeMsg.FAILED_AUTHEN, u'认证失败', {})

        current_user = authenticate(code=code, request=request)
        if current_user and current_user.is_authenticated() and not current_user.ext_data:
            # 当用户非第一次登录，并且code认证通过，直接登录
            logger.info('account login with code, user id: %s,  ip: %s' % (current_user.pk, parse_ipadress(request)))
            login(request, current_user)
            return CommonReturn(CodeMsg.SUCCESS_AUTHEN, '认证成功')

        u_id = current_user.ext_data.get('u_id')
        d_id = current_user.ext_data.get('d_id')
        if not u_id or not d_id:
            # 用户第一次登录，但是没有获取到user_id，device_id
            return CommonReturn(CodeMsg.FAILED_AUTHEN, '认证失败', {})
        if u_id and d_id:
            # 用户第一次登录，获取到了user_id，device_id. 重定向login界面，绑定微信信息和用户信息
            logger.info('prepare binding wechat, wechat_user_id: %s, device_id: %s' % (u_id, d_id))
            res = {
                "user_id": u_id,
                "device_id": d_id
            }
            return CommonReturn(CodeMsg.FAILED_AUTHEN, '认证失败', res)
        return CommonReturn(CodeMsg.FAILED_AUTHEN, '认证失败', {})