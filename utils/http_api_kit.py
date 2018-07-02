# -*- coding: utf-8 -*-
import json
import logging
from time import sleep

import httplib2 as http
import datetime

from django.conf import settings

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class RequestAPI():
    STATUS_CODE = {
        '200': '成功',
        '201': '成功',
        '404': '资源不存在',
        '409': '资源冲突，存在关键资源',
        '500': '服务不可用'
    }

    @classmethod
    def access_data(cls, url, method, body='', token='', timeout=None, access_headers=None):
        if url == '':
            return {'status': '2001', 'msg': 'path is empty!'}
        if method.upper() not in ('GET', 'POST', 'DELETE', 'PUT'):
            return {'status': '2002', 'msg': 'method is invalid!'}

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'User-IP': settings.USER_REAL_IP
        }
        if token:
            headers['Access-Token'] = token
        if access_headers:
            headers.update(access_headers)

        target = urlparse(url)

        print(target.geturl())
        logger.info('调用API url: %s', str(target.geturl()))

        h = http.Http(timeout=timeout)

        if not isinstance(body, str):
            body = json.dumps(body)
        body = '' if method in ['GET'] else body

        logger.info('调用底层参数: %s', body)

        try:
            response, content = h.request(target.geturl(), method, body, headers)
        except Exception as exc:
            logger.error('请求底层失败，error msg:%s' % exc.message, exc_info=True)
            sleep(2)
            response, content = h.request(target.geturl(), method, body, headers)
        logger.info('底层返回状态: %s, 结果: %s', str(response.status), content)
        # if method in ['POST', 'PUT']:
        #     response = requests.request(method, target.geturl(), json=body, headers=headers)
        # else:
        #     response = requests.request(method, target.geturl(), headers=headers)
        rtn_status = response.status

        try:
            try:
                data = json.loads(content)
            except Exception as exc:
                logger.error('json转化底层数据失败, raise Exception: %r' % exc)
                data = eval(content)
        except Exception as exc:
            logger.error('json转化底层数据失败, raise Exception: %r' % exc)
            data = content
        return {'status': rtn_status, 'data': data, 'msg': cls.STATUS_CODE.get(rtn_status, '')}


if __name__ == '__main__':
    try:
        data = RequestAPI.access_data('http://10.131.32.3:8489/v1/zones', 'GET')
        print(data)
    except Exception as exc:
        print(exc)



