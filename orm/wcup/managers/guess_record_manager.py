# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
import logging
from django.db import models

logger = logging.getLogger(__name__)


class GuessRecordManager(models.Manager):
    """
    竞猜记录表管理类
    """
    def add_new(self, user_id, schedule_id, condition_id, pay_for, support_country_id, support_odds):
        """
        添加新记录
        :param user_id:
        :param schedule_id:
        :param condition_id:
        :param pay_for:
        :param support_country_id:
        :param support_odds:
        :return:
        """
        try:
            new_data_dict = {
                "user_id": user_id,
                "schedule_id": schedule_id,
                "condition_id": condition_id,
                "pay_for": pay_for,
                "support_country_id": support_country_id,
                "support_odds": support_odds
            }
            new_obj = self.model(**new_data_dict)
            new_obj.save(force_insert=True)
            return new_obj.pk
        except Exception as e:
            logger.error('insert one new record into wcup_guess_record failed: %s' % e.message, exc_info=True)
            raise e
