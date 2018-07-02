# -*- coding: utf-8 -*-
import logging

from rest_framework.response import Response
from service.api_util import CodeMsg
from rest_framework.authentication import SessionAuthentication

logger = logging.getLogger(__name__)


def api_serializer_deco(api_msg, ignore_login=False):
    """
    统一处理接口序列化及返回数据
    :param api_msg:
    :param ignore_login: 是否忽略用户登录
    :return:
    """

    def _wrapper(func):
        def deco(*args, **kwargs):
            try:
                obj = args[0]
                req = args[1]
                if not ignore_login:
                    if req.user.is_authenticated():
                        user_id = req.user.user_id
                        logger.info('request user id: %s' % user_id)
                    else:
                        # login_url = settings.LOGIN_URL + "?referer="
                        res = Response({"status": 0, "code": 401, "msg": "not login"})
                        res.status_code = 200
                        return res

                    logger.info('user_id: %s' % req.user.user_id)

                req_dict = {
                    "GET": req.GET.dict(),
                    "POST": req.data,
                    "PUT": req.data
                }

                obj_serializer = None
                if obj.serializer_class:
                    obj_serializer = obj.get_serializer(data=req_dict.get(req.method))
                if not obj_serializer or obj_serializer.is_valid():
                    if obj_serializer:
                        serializer_data = obj_serializer.data
                        kwargs['serializer_data'] = serializer_data
                        logger.info('request parameters: %s' % serializer_data)
                    order_res = func(*args, **kwargs)
                    if order_res.response:
                        return order_res.response
                    if order_res.api_return_data:
                        res = order_res.api_return_data
                    else:
                        status = 1
                        code = 200
                        if not order_res.is_success():
                            status = 0
                            code = order_res.code
                        res = {
                            'code': code,
                            'msg': order_res.message,
                            'data': order_res.data,
                            'status': status
                        }
                else:
                    res = {
                        'code': CodeMsg.PARAM_ERROR['code'],
                        'msg': obj_serializer.errors,
                        'status': 0
                    }
            except Exception as ex:
                msg = u'%s异常：%s' % (api_msg, ex)
                logger.error(msg, exc_info=True)
                res = {
                    'code': CodeMsg.UNKNOWN_ERROR['code'],
                    'status': 0,
                    'msg': msg
                }
            try:
                logger.info(u'%s返回结果:%s' % (api_msg, res))
            except Exception as ex:
                logger.exception(ex, exc_info=True)
            res = Response(res)
            res.set_cookie("new_gic_flag", 1)
            return res

        return deco
    return _wrapper


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening