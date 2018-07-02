# -*- encoding:utf-8 -*-
import logging
from orm.account.models import User


logger = logging.getLogger(__name__)


class DjangoAdminUserPWBackend(object):

    def authenticate(self, username=None, password=None):
        """
        如果验证不通过，返回None
        :param username:
        :param password:
        :return:
        """
        logger.info('username="%s", password="%s"' % (username, password))
        if username not in (None, '') and password not in (None, ''):
            try:
                user = User.objects.get(user_id=username)
                valid_user = user.check_password(password)
                if not valid_user:
                    return None
            except User.DoesNotExist:
                logger.info('has no this user, add one new user')
                return None
            return user

        return None

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
