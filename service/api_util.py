# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger(__name__)


class CodeMsg(object):
    """
    api错误码 MODULE CODE 1
    """
    SUCCESS = {'code': '0000', 'msg': 'success'}
    SUCCESS_CODE = SUCCESS['code']
    PARAM_ERROR = {'code': '10001', 'msg': u'参数错误'}
    UNKNOWN_ERROR = {'code': '9999', 'msg': u'未知异常'}
    UNKNOWN_ERROR_CODE = UNKNOWN_ERROR['code']

    AUTHE_ERROR = {'code': '11000', 'msg': 'success'}
    AUTHE_TOKEN_INVALID = {'code': '11001', 'msg': u'Token验证无效，请检查Token.'}
    AUTHE_TIME_EXPIRE = {'code': '11002', 'msg': u'请求已过期，请检查请求时间.'}
    AUTHE_TIME_AFTER_NOW = {'code': '11003', 'msg': u'请求时间戳不允许大于请求时间.'}
    AUTHE_SIGN_ERROR = {'code': '11004', 'msg': u'签名验证失败.'}
    AUTHE_AK_ERROR = {'code': '11005', 'msg': u'AccessKey验证失败.'}
    AUTHE_PARAM_ERROR = {'code': '11006', 'msg': u'鉴权参数异常，请检查认证参数.'}
    DATA_PRO_ERROR = {'code': '0102', 'msg': u'产品数据异常'}
    DATA_GOODS_ERROR = {'code': '0103', 'msg': u'商品数据异常'}

    GET_DATA_ERROR = {'code': '20001', 'msg': u'获取数据异常.'}
    ACCOUNT_AUTH_ERROR = {'code': '20303', 'msg': u'用户权限不足'}

    CREATE_ERROR = {'code': '30001', 'msg': u'创建失败.'}
    OPERATE_ERROR = {'code': '30002', 'msg': u'操作失败.'}

    ORDER_AUDIT = {'code': '40001', 'msg': u'订单审核.'}

    SUCCESS_AUTHEN = {'code': 201, 'status': 1, 'msg': u'认证成功'}
    FAILED_AUTHEN = {'code': 202, 'status': 1, 'msg': u'认证失败'}

    def __init__(self):
        pass


class CommonReturn(object):
    """
    返回数据
    """

    def __init__(self, order_code_msg, message=u'', data=None, api_return_data=None, response=None):
        self.order_code_msg = order_code_msg
        self.message = message
        self.data = data if data is not None else {}
        self.api_return_data = api_return_data if api_return_data else {}
        self.response = response

    @property
    def code(self):
        return self.order_code_msg['code']

    @property
    def code_msg(self):
        return self.order_code_msg['msg']

    def is_success(self):
        if self.code == CodeMsg.SUCCESS['code']:
            return True
        return False

    def is_unknown_error(self):
        if self.code == CodeMsg.UNKNOWN_ERROR['code']:
            return True
        return False


class CommonException(Exception):
    """
    订单异常
    """
    def __init__(self, order_code_msg, *args, **kwargs):
        self._code = order_code_msg.get('code', '9999')
        self._code_msg = order_code_msg.get('msg', u'未知异常')
        self.order_code_msg = order_code_msg
        super(CommonException, self).__init__(*args, **kwargs)

    @property
    def code(self):
        return self._code

    @property
    def msg(self):
        return '%s(%s):%s' % (self._code_msg, self.code, self.message)


def catch_order_exception(op_msg):
    def _wrapper(func):
        def deco(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CommonException as ex:
                msg = u'%s异常：%s' % (op_msg, ex)
                logger.error(msg, exc_info=True)
                return {'code': ex.code, 'message': ex.message, 'code_msg': ex.msg}
            except Exception as ex:
                msg = u'%s异常：%s' % (op_msg, ex)
                logger.error(msg, exc_info=True)
                return {'code': CodeMsg.UNKNOWN_ERROR_CODE, 'message': msg}
        return deco
    return _wrapper
