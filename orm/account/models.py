# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

from django.db import models

logger = logging.getLogger(__name__)

# Create your models here.


class UserAccountManager(BaseUserManager):
    def create_user(self, user_id, mobile, password=None):
        if not user_id:
            raise ValueError('User_id must be set!')
        user = self.model(user_id=user_id, mobile=mobile)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, mobile, password=None):
        user = self.create_user(user_id, mobile, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, user_id):
        return self.get(pk=user_id)

    def add_new(self, sso_id, adAccount, employeeNo, idNo, phone, email, department, weChatId, token):
        """
        添加新的用户记录
        :param sso_id:
        :param adAccount:
        :param employeeNo:
        :param idNo:
        :param phone:
        :param department:
        :return:
        """
        try:
            new_data = {
                "user_id": sso_id,
                "name": adAccount,
                "employee_no": employeeNo,
                "id_no": idNo,
                "mobile": phone,
                "email": email,
                "department": department,
                "wechat_id": weChatId,
                "token": token
            }
            obj = self.model(**new_data)
            obj.save(force_insert=True)
            return obj
        except Exception as e:
            logger.error('insert one new record into account_user failed: %s' % e.message, exc_info=True)
            raise e


class User(AbstractBaseUser):
    """
    用户表
    """
    user_id = models.IntegerField(primary_key=True, help_text=_('sso 接口返回用户id'))
    name = models.CharField(unique=True, max_length=255, null=True, help_text=_('用户名称'))
    employee_no = models.CharField(max_length=255, null=True, help_text=_('员工编号'))
    id_no = models.CharField(max_length=255, null=True, help_text=_('身份证号'))
    mobile = models.CharField(max_length=50, null=True, help_text=_('手机号'))
    email = models.CharField(max_length=50, null=True, help_text=_('邮箱地址'))
    department = models.CharField(max_length=255, null=True, help_text=_('部门'))
    wechat_id = models.CharField(max_length=255, null=True, help_text=_('微信ID'))
    capital = models.DecimalField(max_digits=12, decimal_places=3, default=0, help_text=_('金币总数量'))
    token = models.CharField(u'sso token', max_length=255, null=True)
    register_time = models.DateTimeField(auto_now_add=True, help_text=_('注册时间'))
    update_time = models.DateTimeField(auto_now=True, help_text=_('更新时间'))
    is_admin = models.BooleanField(default=False)
    ext_data = models.CharField(max_length=255, help_text=u'用户第一次登录暂存')

    USERNAME_FIELD = 'user_id'
    REQUIRED_FIELDS = ['mobile']

    objects = UserAccountManager()

    @property
    def is_staff(self):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def has_perm(self, perm, ob=None):
        return self.is_admin

    def get_short_name(self):
        return self.mobile

    class Meta:
        db_table = 'account_user'

