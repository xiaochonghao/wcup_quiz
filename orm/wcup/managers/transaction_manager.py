# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db import models

logger = logging.getLogger(__name__)


class TransactionManager(models.Manager):
    """
    交易明细表管理类
    """
    def add_new(self, user_id, schedule_id, detail, in_gold=None, out_gold=None):
        """
        增加交易明细
        :param user_id:
        :param schedule_id:
        :param detail:
        :param in_gold:
        :param out_gold:
        :return:
        """
        try:
            new_data_dict = {
                "user_id": user_id,
                "schedule_id": schedule_id,
                "detail": detail,
                "in_gold": in_gold,
                "out_gold": out_gold
            }
            new_obj = self.model(**new_data_dict)
            new_obj.save(force_insert=True)
            return new_obj.pk
        except Exception as e:
            logger.error('insert one new record into wcup_transaction failed: %s' % e.message, exc_info=True)
            raise e
