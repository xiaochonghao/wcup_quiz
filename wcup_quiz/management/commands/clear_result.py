# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from orm.wcup.models import GuessRecord, Schedule, Transaction
from orm.constants import WATER_RATE, WIN_FLAG, FAIL_FLAG, DRAW_FLAG

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    定时结算每个比赛日的竞猜结果
    """
    help = 'Clear the results of everyday matches quiz.'

    def handle(self, *args, **options):
        ClearMatchResult.do_clear()


class ClearMatchResult(object):
    """
    结算每天比赛的操作类
    """

    def __init__(self):
        self._unprocessed_schedules = None

    @property
    def unprocessed_schedules(self):
        """
        获取有结果，但未处理过的赛程
        :return:
        """
        if not self._unprocessed_schedules:
            conditions = Q(score_90min__isnull=True) and Q(score_90min='')
            self._unprocessed_schedules = Schedule.objects.filter(processed=False).exclude(conditions)
        return self._unprocessed_schedules

    @staticmethod
    def get_unprocessed_records(schedule_id):
        """
        获取属于某赛程，但是没有处理过的竞猜记录
        :param schedule_id:
        :return:
        """
        records = GuessRecord.objects.select_related('schedule', 'condition').filter(schedule_id=schedule_id,
                                                                                     processed=False)
        return records

    @staticmethod
    def calcute_integer(score_a, country_a_name, score_b, country_b_name, handicap_num, support_country, support_odds,
                        pay_for):
        """
        计算整型盘口
        :param score_a:
        :param country_a_name:
        :param score_b:
        :param country_b_name:
        :param handicap_num: -3, -2, -1, 0, 1, 2, 3
        :param support_country:
        :param support_odds: 支持的队伍的赔率
        :param pay_for: integer
        :return: pay_back
        """
        logger.info(vars())
        detail_tpl = '90分钟比分%s:%s，盘口类型%s，赔率%s, 结算最终结果：%s {0} %s。您支持%s，支付了%s，盈利结果：{1}{2}' % (
            score_a, score_b, handicap_num, support_odds, country_a_name, country_b_name, support_country, pay_for)
        if handicap_num < 0:
            _score_a = score_a
            _score_b = score_b + abs(handicap_num)
        else:
            _score_a = score_a + abs(handicap_num)
            _score_b = score_b

        win_all = pay_for * support_odds
        if _score_a == _score_b:
            logger.info('打平，扣本金比例%s' % WATER_RATE)
            pay_back = pay_for * (1 - WATER_RATE)
            detail = detail_tpl.format('平', '走盘庄家扣除%s本金，收回本金' % WATER_RATE, pay_back)
            result = 'draw'
        else:
            if _score_a > _score_b:
                pay_back_dict = {
                    country_a_name: {
                        'back': win_all,
                        'detail': detail_tpl.format('胜', '获取奖金', win_all),
                        'result': WIN_FLAG
                    },
                    country_b_name: {
                        'back': 0.0,
                        'detail': detail_tpl.format('胜', '没有奖金。', ''),
                        'result': FAIL_FLAG
                    }
                }
            else:
                pay_back_dict = {
                    country_a_name: {
                        'back': 0.0,
                        'detail': detail_tpl.format('负', '没有奖金。', ''),
                        'result': FAIL_FLAG
                    },
                    country_b_name: {
                        'back': win_all,
                        'detail': detail_tpl.format('负', '获取奖金', win_all),
                        'result': WIN_FLAG
                    },
                }
            pay_back = pay_back_dict.get(support_country).get('back')
            detail = pay_back_dict.get(support_country).get('detail')
            result = pay_back_dict.get(support_country).get('result')
        logger.info('pay_back=%s, detail="%s", result="%s"' % (pay_back, detail, result))
        return pay_back, detail, result

    @staticmethod
    def calcute_half(score_a, country_a_name, score_b, country_b_name, handicap_num, support_country, support_odds,
                     pay_for):
        """
        计算半球盘口
        :param score_a:
        :param country_a_name:
        :param score_b:
        :param country_b_name:
        :param handicap_num: -2.5, -1.5, -0.5, 0.5, 1.5, 2.5
        :param support_country:
        :param support_odds: 支持的队伍的赔率
        :param pay_for:
        :return:
        """
        logger.info(vars())
        detail_tpl = '90分钟比分%s:%s，盘口类型%s，赔率%s, 结算最终结果：%s {0} %s。您支持%s，支付了%s，盈利结果：{1}{2}' % (
            score_a, score_b, handicap_num, support_odds, country_a_name, country_b_name, support_country, pay_for)

        win_all = pay_for * support_odds
        if handicap_num < 0:
            _score_a = score_a
            _score_b = score_b + abs(handicap_num)
        else:
            _score_a = score_a + abs(handicap_num)
            _score_b = score_b

        if _score_a > _score_b:
            pay_back_dict = {
                country_a_name: {
                    'back': win_all,
                    'detail': detail_tpl.format('胜', '获取奖金', win_all),
                    'result': WIN_FLAG
                },
                country_b_name: {
                    'back': 0.0,
                    'detail': detail_tpl.format('胜', '没有奖金。', ''),
                    'result': FAIL_FLAG
                }
            }
        else:
            pay_back_dict = {
                country_a_name: {
                    'back': 0.0,
                    'detail': detail_tpl.format('负', '没有奖金。', ''),
                    'result': FAIL_FLAG
                },
                country_b_name: {
                    'back': win_all,
                    'detail': detail_tpl.format('负', '获取奖金', win_all),
                    'result': WIN_FLAG
                }
            }
        pay_back = pay_back_dict.get(support_country).get('back')
        detail = pay_back_dict.get(support_country).get('detail')
        result = pay_back_dict.get(support_country).get('result')
        logger.info('pay_back=%s, detail="%s", result="%s"' % (pay_back, detail, result))
        return pay_back, detail, result

    @staticmethod
    def get_25_dict(score_a, score_b, handicap_num, win_half, fail_half, win_all, country_a_name, country_b_name,
                    detail_tpl):
        """
        获取0.25做余数的分差的明细
        :param score_a: 没有经过让球处理的结果
        :param score_b: 没有经过让球处理的结果
        :param handicap_num: 让球数
        :param win_half: 赢一半的金额
        :param fail_half: 输一半的金额
        :param win_all: 全赢的金额
        :param country_a_name: 国家a名字
        :param country_b_name: 国家b名字
        :param detail_tpl: 明细模板
        :return:
        """
        if handicap_num < 0:
            _score_a = score_a
            _score_b = score_b + abs(handicap_num)
            if abs(_score_b - _score_a) == 0.25:
                pay_back_dict = {
                    country_a_name: {
                        'back': fail_half,
                        'detail': detail_tpl.format('平', '输一半，获取一半本金', fail_half),
                        'result': DRAW_FLAG
                    },
                    country_b_name: {
                        'back': win_half,
                        'detail': detail_tpl.format('平', '赢一半，获取彩头一半奖金', win_half),
                        'result': DRAW_FLAG
                    },
                }
            elif _score_b - _score_a > 0.25:
                pay_back_dict = {
                    country_a_name: {
                        'back': 0.0,
                        'detail': detail_tpl.format('负', '没有奖金', ''),
                        'result': FAIL_FLAG
                    },
                    country_b_name: {
                        'back': win_all,
                        'detail': detail_tpl.format('负', '获取奖金', win_all),
                        'result': WIN_FLAG
                    },
                }
            else:
                pay_back_dict = {
                    country_a_name: {
                        'back': win_all,
                        'detail': detail_tpl.format('胜', '获取奖金', win_all),
                        'result': WIN_FLAG
                    },
                    country_b_name: {
                        'back': 0.0,
                        'detail': detail_tpl.format('胜', '没有奖金', ''),
                        'result': FAIL_FLAG
                    },
                }
        else:
            _score_a = score_a + abs(handicap_num)
            _score_b = score_b
            if abs(_score_a - _score_b) == 0.25:
                pay_back_dict = {
                    country_b_name: {
                        'back': fail_half,
                        'detail': detail_tpl.format('平', '输一半，获取一半本金', fail_half),
                        'result': DRAW_FLAG
                    },
                    country_a_name: {
                        'back': win_half,
                        'detail': detail_tpl.format('平', '赢一半，获取彩头一半奖金', win_half),
                        'result': DRAW_FLAG
                    },
                }
            elif _score_a - _score_b > 0.25:
                pay_back_dict = {
                    country_b_name: {
                        'back': 0.0,
                        'detail': detail_tpl.format('胜', '没有奖金', ''),
                        'result': FAIL_FLAG
                    },
                    country_a_name: {
                        'back': win_all,
                        'detail': detail_tpl.format('胜', '获取奖金', win_all),
                        'result': WIN_FLAG
                    },
                }
            else:
                pay_back_dict = {
                    country_b_name: {
                        'back': win_all,
                        'detail': detail_tpl.format('负', '获取奖金', win_all),
                        'result': WIN_FLAG
                    },
                    country_a_name: {
                        'back': 0.0,
                        'detail': detail_tpl.format('负', '没有奖金', ''),
                        'result': FAIL_FLAG
                    },
                }
        return pay_back_dict

    @staticmethod
    def get_75_dict(score_a, score_b, handicap_num, win_half, fail_half, win_all, country_a_name, country_b_name,
                    detail_tpl):
        """
        获取0.75做余数的分差的明细
        :param score_a: 没有经过让球处理的结果
        :param score_b: 没有经过让球处理的结果
        :param handicap_num: 让球数
        :param win_half: 赢一半的金额
        :param fail_half: 输一半的金额
        :param win_all: 全赢的金额
        :param country_a_name: 国家a名字
        :param country_b_name: 国家b名字
        :param detail_tpl: 明细模板
        :return:
        """
        if handicap_num < 0:
            _score_a = score_a
            _score_b = score_b + abs(handicap_num)
            if abs(_score_b - _score_a) == 0.25:
                pay_back_dict = {
                    country_b_name: {
                        'back': fail_half,
                        'detail': detail_tpl.format('平', '输一半，获取一半本金', fail_half),
                        'result': DRAW_FLAG
                    },
                    country_a_name: {
                        'back': win_half,
                        'detail': detail_tpl.format('平', '赢一半，获取彩头一半奖金', win_half),
                        'result': DRAW_FLAG
                    },
                }
            elif _score_b - _score_a > 0.25:
                pay_back_dict = {
                    country_a_name: {
                        'back': 0.0,
                        'detail': detail_tpl.format('负', '没有奖金', ''),
                        'result': FAIL_FLAG
                    },
                    country_b_name: {
                        'back': win_all,
                        'detail': detail_tpl.format('负', '获取奖金', win_all),
                        'result': WIN_FLAG
                    },
                }
            else:
                pay_back_dict = {
                    country_a_name: {
                        'back': win_all,
                        'detail': detail_tpl.format('胜', '获取奖金', win_all),
                        'result': WIN_FLAG
                    },
                    country_b_name: {
                        'back': 0.0,
                        'detail': detail_tpl.format('胜', '没有奖金', ''),
                        'result': FAIL_FLAG
                    },
                }
        else:
            _score_a = score_a + abs(handicap_num)
            _score_b = score_b
            if abs(_score_a - _score_b) == 0.25:
                pay_back_dict = {
                    country_a_name: {
                        'back': fail_half,
                        'detail': detail_tpl.format('平', '输一半，获取一半本金', fail_half),
                        'result': DRAW_FLAG
                    },
                    country_b_name: {
                        'back': win_half,
                        'detail': detail_tpl.format('平', '赢一半，获取彩头一半奖金', win_half),
                        'result': DRAW_FLAG
                    },
                }
            elif _score_a - _score_b > 0.25:
                pay_back_dict = {
                    country_b_name: {
                        'back': 0.0,
                        'detail': detail_tpl.format('胜', '没有奖金', ''),
                        'result': FAIL_FLAG
                    },
                    country_a_name: {
                        'back': win_all,
                        'detail': detail_tpl.format('胜', '获取奖金', win_all),
                        'result': WIN_FLAG
                    },
                }
            else:
                pay_back_dict = {
                    country_b_name: {
                        'back': win_all,
                        'detail': detail_tpl.format('负', '获取奖金', win_all),
                        'result': WIN_FLAG
                    },
                    country_a_name: {
                        'back': 0.0,
                        'detail': detail_tpl.format('负', '没有奖金', ''),
                        'result': FAIL_FLAG
                    },
                }
        return pay_back_dict

    @staticmethod
    def calcute_quater(score_a, country_a_name, score_b, country_b_name, handicap_num, support_country, support_odds,
                       pay_for):
        """
        计算平半盘口
        :param score_a:
        :param country_a_name:
        :param score_b:
        :param country_b_name:
        :param handicap_num:-2.75, -2.25, -1.75, -1.25, -0.75, -0.25, 0.25, 0.75, 1.25, 1.75, 2.25, 2.75
        :param support_country:
        :param support_odds: 支持的队伍的赔率
        :param pay_for:
        :return:
        """
        logger.info(vars())
        detail_tpl = '90分钟比分%s:%s，盘口类型%s，赔率%s, 结算最终结果：%s {0} %s。您支持%s，支付了%s，盈利结果：{1}{2}' % (
            score_a, score_b, handicap_num, support_odds, country_a_name, country_b_name, support_country, pay_for)

        win_half = pay_for * ((support_odds - 1) * 0.5 + 1)
        fail_half = pay_for * 0.5
        win_all = pay_for * support_odds

        if abs(handicap_num) % 1 == 0.25:
            pay_back_dict = ClearMatchResult.get_25_dict(score_a, score_b, handicap_num, win_half, fail_half, win_all,
                                                         country_a_name, country_b_name, detail_tpl)
        else:
            pay_back_dict = ClearMatchResult.get_75_dict(score_a, score_b, handicap_num, win_half, fail_half, win_all,
                                                         country_a_name, country_b_name, detail_tpl)

        pay_back = pay_back_dict.get(support_country).get('back')
        detail = pay_back_dict.get(support_country).get('detail')
        result = pay_back_dict.get(support_country).get('result')
        logger.info('pay_back=%s, detail="%s", result="%s"' % (pay_back, detail, result))
        return pay_back, detail, result

    @classmethod
    def do_clear(cls):
        try:
            logger.info('开始本轮结算工作.')

            instance = cls()
            with transaction.atomic():
                for schedule in instance.unprocessed_schedules:
                    # 遍历有结果、但是未处理的赛程
                    logger.info('------ begin to deal schedule: "%s" ------' % schedule.pk)
                    score_90min = schedule.score_90min.split(':')
                    score_a = int(score_90min[0].strip())
                    score_b = int(score_90min[1].strip())

                    unprocessed_records = instance.get_unprocessed_records(schedule.pk)
                    for record in unprocessed_records:
                        # 遍历属于该赛程、但是未处理的竞猜记录
                        logger.info('****** begin to deal guess record: "%s" ******' % record.pk)
                        h_num = record.condition.handicap_num
                        if abs(h_num) % 1 == 0:
                            pay_back, detail, result = instance.calcute_integer(score_a,
                                                                                schedule.country_a.name_zh_cn,
                                                                                score_b,
                                                                                schedule.country_b.name_zh_cn,
                                                                                h_num,
                                                                                record.support_country.name_zh_cn,
                                                                                record.support_odds,
                                                                                record.pay_for)
                        elif abs(h_num) % 0.5 == 0:
                            pay_back, detail, result = instance.calcute_half(score_a,
                                                                             schedule.country_a.name_zh_cn,
                                                                             score_b,
                                                                             schedule.country_b.name_zh_cn,
                                                                             h_num,
                                                                             record.support_country.name_zh_cn,
                                                                             record.support_odds,
                                                                             record.pay_for)
                        else:
                            pay_back, detail, result = instance.calcute_quater(score_a,
                                                                               schedule.country_a.name_zh_cn,
                                                                               score_b,
                                                                               schedule.country_b.name_zh_cn,
                                                                               h_num,
                                                                               record.support_country.name_zh_cn,
                                                                               record.support_odds,
                                                                               record.pay_for)

                        new_trans_id = Transaction.objects.add_new(record.user_id, schedule.pk, detail,
                                                                   in_gold=pay_back)
                        logger.info('增加新的交易明细记录：new_trans_id=%s' % new_trans_id)

                        logger.info('更新竞猜记录的pay_back -> %s, detail -> %s' % (pay_back, result))
                        record.pay_back = pay_back
                        record.processed = True
                        record.detail = result
                        record.save(force_update=True)

                        user = record.user
                        logger.info('更新用户<%s>的capital字段：%s -> %s'
                                    % (record.user_id, user.capital, float(user.capital) + pay_back))
                        user.capital = float(user.capital) + pay_back
                        user.save(force_update=True)
                        logger.info('****** success end deal guess record: "%s" ******' % record.pk)

                    logger.info('更新schedule<%s>处理结果为True' % schedule.pk)
                    schedule.processed = True
                    schedule.save(force_update=True)
                    logger.info('------success end deal schedule: "%s" ------' % schedule.pk)

            logger.info('结束本轮结算工作.')
        except Exception as e:
            logger.error('do clear result happens error: %s' % e.message, exc_info=True)
            raise e
