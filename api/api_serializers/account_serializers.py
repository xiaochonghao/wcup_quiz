# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    user_name = serializers.CharField(max_length=255, allow_null=False, allow_blank=False, help_text='用户名')
    password = serializers.CharField(max_length=255, allow_null=False, allow_blank=False, help_text='密码')
    user_id = serializers.CharField(max_length=255, required=False, help_text='oa user_id')
    device_id = serializers.CharField(max_length=255, required=False, help_text='oa device_id')

class AuthenSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=255, required=False, allow_null=True, help_text='wechat code')