# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers


class SupportCountrySerializer(serializers.Serializer):
    schedule_id = serializers.CharField(max_length=36, allow_null=False, allow_blank=False, help_text='赛程id')
    country_name = serializers.CharField(max_length=50, allow_null=False, allow_blank=False, help_text='国家名字')
    condition_id = serializers.IntegerField(allow_null=False, help_text='竞猜时对应的条件id')
    pay_for = serializers.IntegerField(max_value=500, min_value=10, default=10, help_text='支付的押金')

