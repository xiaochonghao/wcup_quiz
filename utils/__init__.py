# coding=utf-8
from __future__ import unicode_literals
from decimal import *
import re, os, sys, datetime, socket, logging, types, json, urllib, uuid, random, hashlib
from requests import post
from json import dumps

from django.conf import settings
from django.db import models
from django import forms
from django.core.serializers.json import DjangoJSONEncoder
import logging

logger = logging.getLogger(__name__)


def GetResponse(url):
    try:
        response = urllib.urlopen(url).read()
        return response
    except:
        return 'REQUEST ERROR'


def log(msg):
    if (settings.DEBUG):
        logger.debug(msg)


regex_unsafe_charset = re.compile(settings.UNSAFE_CHARSET)


def import_all_path(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def clean_unsafe_char(s):
    return regex_unsafe_charset.sub('', s)


def create_uuid(name=''):
    '''
    自动生成36位uuid
    :param name:
    :return:
    '''
    return str(uuid.uuid1())


def create_order_code():
    '''
    自动生成uuid
    :param name:
    :return:
    '''
    return datetime.datetime.now().strftime('%Y%m%d%H%S') + create_random_No(6)


def create_email_active_code(id, name):
    '''
    邮箱验证码生成
    :param id:
    :param name:
    :return:
    '''
    return hashlib.md5("%s%s%s" % (id, name, datetime.datetime.now().strftime('%Y%m%d%H'))).hexdigest()


def gen_token():
    '''
    自定义token每小时变化一次
    :return:
    '''
    str = settings.SECRET_KEY + datetime.datetime.now().strftime('%Y%m%d%H')
    token = hashlib.md5(str).hexdigest()
    return token


def gen_md5(str):
    """
    将str->md5_str
    :param str:
    :return:
    """
    m2 = hashlib.md5()
    m2.update(str)
    return m2.hexdigest()


def create_random_No(len_=6):
    '''
    生成随机数字
    :param len_:默认长度6
    :return:len_长度的随机数字
    '''
    num = ''
    for i in range(len_):
        num += str(random.randrange(10))
    logger.debug(num)
    return num


def get_user_ip_by_request(request):
    '''
    获取用户的IP地址
    :param request:
    :return:
    '''
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    return ip


def json_encode(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to a object dynamically are being ignored (and it also has
    problems with some models).
    """

    def _any(data):
        ret = None
        if type(data) is types.ListType:
            ret = _list(data)
        elif type(data) is types.DictType:
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        elif isinstance(data, models.base.ModelState):
            ret = _model(data)
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        fields = dir(data.__class__) + ret.keys()
        add_ons = [k for k in dir(data) if k not in fields]
        for k in add_ons:
            ret[k] = _any(getattr(data, k))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k, v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)

    return json.dumps(ret, cls=DjangoJSONEncoder)


def gen_discount_code():
    from django.utils.crypto import get_random_string

    return get_random_string(settings.DISCOUNT_CODE_LENGTH, "23456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def process_order_price(old_price):
    day_price = old_price * settings.SET_PAYMENT_SHOW_DATE
    new_price = Decimal(day_price / 100).quantize(Decimal('0.01'))
    logger.debug("old_price:%d day_price:%d new_price:%d" % (old_price, day_price, new_price))
    return new_price

def process_order_time_price(old_price):
    new_price = Decimal(old_price / 100).quantize(Decimal('0.01'))
    logger.debug("old_price:%d time_price:%d new_price:%d" % (old_price, old_price, new_price))
    return new_price


def process_price(old_price):
    if old_price is not None:
        new_price = Decimal(old_price).quantize(Decimal('0.01'))
    else:
        old_price = Decimal('0.00')
        new_price = Decimal('0.00')
    logger.debug("old_price:%d day_price:%d new_price:%d" % (old_price, old_price, new_price))
    return new_price


def is_ajax_request(request):
    """
    检查用户是ajax清清
    :param request:
    :return:
    """
    if request.META.get("HTTP_X_REQUESTED_WITH", ""):
        return True
    else:
        return False


def get_cost_format(cost, account_type):
    if account_type == 'CN':
        return "%.2f 元" % cost
    else:
        return "$ %.2f" % cost


def _check_password_strength(password):
    data = dumps({'password': password})
    headers = {'content-type': 'application/json'}
    result = post(
        settings.PASSWORD_STRENGTH_SERVICE_ADDRESS,
        data=data,
        headers=headers,
    )
    return result.json()


def make_float_shorter(f, weishu=4):
    # format float as shot as possible
    # 1.234567 => 1.2346
    # 1.100 => 1.1
    # 1.0 => 1
    f = round(f, weishu)
    if f.is_integer():
        f = int(f)
    return f


def make_price_shorter(f, weishu=4):
    # 分变成元，并且去掉末尾的0
    return make_float_shorter(float(f)/100, weishu)


def get_area_id(req):
    return 'CN'


def parse_ipadress(request):
    """获取用户的IP地址."""
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip_addr = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip_addr = request.META['REMOTE_ADDR']
    return ip_addr