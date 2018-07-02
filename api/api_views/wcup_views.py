# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
from datetime import datetime, timedelta

from rest_framework import viewsets
from rest_framework.decorators import list_route
from django.db import transaction
from rest_framework.authentication import BasicAuthentication

from api.api_serializers import wcup_serializers
from service.api_util import CodeMsg, CommonReturn
from api import api_serializer_deco, CsrfExemptSessionAuthentication
from orm.account.models import User
from orm.wcup import models as wcup_models
from utils.date_kit import dateTimeToStr
import utils as ut
from orm.constants import WIN_FLAG, FAIL_FLAG, DRAW_FLAG, OTHER_FLAG

logger = logging.getLogger(__name__)


# Create your views here.


class WCupQuizViewSet(viewsets.GenericViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @list_route(methods=['GET'],
                url_path='list_current')
    @api_serializer_deco('本期竞猜的赛程信息')
    def list_current(self, request):
        """
        列出本期竞猜的赛程信息
        :param request:
        :return:
        """
        # 开盘时间是当日10:00，用当前时间与今天10:00做比较，限定当今比赛日的开始结束时间
        now_date = datetime.now()
        today_time = now_date.strftime("%Y-%m-%d 00:00:00")
        today_date = datetime.strptime(today_time, "%Y-%m-%d 00:00:00")
        today_10date = today_date + timedelta(hours=10)
        yesterday_10date = today_10date - timedelta(days=1)
        tomorrow_10date = today_10date + timedelta(days=1)
        if now_date >= today_10date:
            start_time = today_10date.strftime("%Y-%m-%d 10:00:00")
            end_time = tomorrow_10date.strftime("%Y-%m-%d 10:00:00")
        else:
            start_time = yesterday_10date.strftime("%Y-%m-%d 10:00:00")
            end_time = today_10date.strftime("%Y-%m-%d 10:00:00")
        logger.info('now_time="%s" -> today start_time="%s", end_time="%s"' % (dateTimeToStr(now_date), start_time, end_time))
        schedules = wcup_models.Schedule.objects.select_related('country_a', 'country_b').filter(
            start_time__gte=start_time,
            start_time__lte=end_time).order_by('start_time')
        schedule_list = list()
        for schedule in schedules:
            res = {
                "schedule_id": schedule.pk,
                "country_a": schedule.country_a.name,
                "country_a_cn": schedule.country_a.name_zh_cn,
                "country_b": schedule.country_b.name,
                "country_b_cn": schedule.country_b.name_zh_cn,
                "start_time": dateTimeToStr(schedule.start_time),
                "guess_end_time": dateTimeToStr(schedule.guess_end_time),
                "type": schedule.type_cn,
                "pay_for": 0.0,
            }

            join_record = wcup_models.GuessRecord.objects.select_related(
                'condition').filter(
                schedule_id=schedule.pk, user_id=request.user.pk).first()
            if join_record:
                # 已经参与此场竞猜
                res.update({
                    "flag": 'joined',
                    "pay_for": ut.json_encode(join_record.pay_for),
                    "support_country_cn": join_record.support_country.name_zh_cn,
                    "support_odds": join_record.support_odds,
                    "odds_a": join_record.condition.odds_a,
                    "odds_b": join_record.condition.odds_b,
                    "handicap_num": join_record.condition.handicap_num,
                    "handicap_disc": join_record.condition.handicap_disc,
                    "condition_id": join_record.condition.pk,
                })
            else:
                # 没有参与竞猜
                last_condition = wcup_models.GuessCondition.objects.filter(schedule_id=schedule.pk,
                                                                           is_valid=1).order_by('-create_time').first()
                res.update({
                    "odds_a": last_condition.odds_a,
                    "odds_b": last_condition.odds_b,
                    "handicap_num": last_condition.handicap_num,
                    "handicap_disc": last_condition.handicap_disc,
                    "condition_id": last_condition.pk,
                })
                if now_date > schedule.guess_end_time:
                    # 时间介于结束竞猜时间~比赛开始时间，不能再竞猜
                    res.update({"flag": "cannot_join"})
                else:
                    # 还没有到竞猜截止时间，可以竞猜
                    res.update({"flag": "unjoined"})

            schedule_list.append(res)

        return CommonReturn(CodeMsg.SUCCESS, '成功获取本期赛程信息', {"schedules": schedule_list})

    @list_route(methods=['POST'],
                url_path='support_country',
                serializer_class=wcup_serializers.SupportCountrySerializer)
    @api_serializer_deco('提交竞猜支持的球队')
    def support_country(self, request, serializer_data=None):
        """
        提交竞猜支持的球队
        :param request:
        :param serializer_data:
        :return:
        """
        schedule_id = serializer_data.get('schedule_id')
        condition_id = serializer_data.get('condition_id')
        country_name = serializer_data.get('country_name')
        pay_for = serializer_data.get('pay_for', 10)
        now_date = datetime.now()

        condition = wcup_models.GuessCondition.objects.filter(pk=condition_id,
                                                              schedule_id=schedule_id,
                                                              is_valid=1).first()
        schedule = wcup_models.Schedule.objects.select_related('country_a', 'country_b').filter(pk=schedule_id).first()
        # condition_id || schedule_id不存在，拒绝
        if not condition:
            msg = '提交的条件"%s"不存在' % condition_id
            logger.error(msg, exc_info=True)
            return CommonReturn(CodeMsg.UNKNOWN_ERROR, msg)
        if not schedule:
            msg = '提交的赛程"%s"不存在' % schedule_id
            logger.error(msg, exc_info=True)
            return CommonReturn(CodeMsg.UNKNOWN_ERROR, msg)

        # 支持的国家不在赛程里面，拒绝
        if country_name not in (schedule.country_a.name, schedule.country_b.name):
            msg = '支持的国家"%s"不在该赛程' % country_name
            logger.error(msg, exc_info=True)
            return CommonReturn(CodeMsg.UNKNOWN_ERROR, msg)
        else:
            country_name_zh_cn = schedule.country_a.name_zh_cn if country_name == schedule.country_a.name \
                else schedule.country_b.name_zh_cn

        # 已经竞猜过该赛程，拒绝
        if wcup_models.GuessRecord.objects.filter(user_id=request.user.pk,
                                                  schedule_id=schedule_id).exists():
            msg = '已经竞猜过赛程"%s"，不能重复提交' % schedule_id
            logger.error(msg, exc_info=True)
            return CommonReturn(CodeMsg.DATA_PRO_ERROR, msg)

        # 提交时的时间已经过了截止时间，拒绝
        if now_date >= schedule.guess_end_time:
            msg = '已经过了竞猜截止时间"%s"，不能再参与竞猜' % schedule.guess_end_time
            logger.error(msg, exc_info=True)
            return CommonReturn(CodeMsg.DATA_PRO_ERROR, msg)

        odds = condition.odds_a if country_name == schedule.country_a.pk else condition.odds_b
        with transaction.atomic():
            # 添加竞猜记录
            record_id = wcup_models.GuessRecord.objects.add_new(request.user.pk,
                                                                schedule_id,
                                                                condition_id,
                                                                pay_for,
                                                                country_name,
                                                                odds)
            # 增加交易明细
            detail = '您参与了{0}开始进行的{1}: {2} VS {3}的竞猜，比赛采用盘口{4}，支持球队{5}（赔率{6}），支付了{7}金币'. \
                format(dateTimeToStr(schedule.start_time),
                       schedule.type_cn,
                       schedule.country_a.name_zh_cn,
                       schedule.country_b.name_zh_cn,
                       condition.handicap_disc,
                       country_name_zh_cn,
                       odds,
                       pay_for)
            trans_id = wcup_models.Transaction.objects.add_new(request.user.pk,
                                                               schedule_id,
                                                               detail,
                                                               out_gold=pay_for)
            # 更新用户总资产
            user = User.objects.filter(pk=request.user.pk).first()
            logger.info('update user<%s> capital: %s -> %s' % (user.pk, user.capital, user.capital - pay_for))
            user.capital -= pay_for
            user.save(force_update=True)
            logger.info('success insert guess record into db: record_id=%s' % record_id)
        return CommonReturn(CodeMsg.SUCCESS, '成功提交支持信息', {'transaction_id': trans_id, 'record_id': record_id})

    @list_route(methods=['GET'],
                url_path='list_history')
    @api_serializer_deco('列出用户往期参加的赛程信息')
    def list_history(self, request):
        """
        列出用户往期参加的赛程信息
        :param request:
        :return:
        """
        # 开盘时间是当日10:00，用当前时间与今天10:00做比较，限定往期的截止时间
        now_date = datetime.now()
        today_time = now_date.strftime("%Y-%m-%d 00:00:00")
        today_date = datetime.strptime(today_time, "%Y-%m-%d 00:00:00")
        today_10date = today_date + timedelta(hours=10)
        yesterday_10date = today_10date - timedelta(days=1)
        if now_date >= today_10date:
            limit_time = today_10date.strftime("%Y-%m-%d 10:00:00")
        else:
            limit_time = yesterday_10date.strftime("%Y-%m-%d 10:00:00")
        logger.info('now_time="%s", limit_time="%s"' % (dateTimeToStr(now_date), limit_time))
        records = wcup_models.GuessRecord.objects.select_related('schedule', 'condition', 'support_country').filter(
            user_id=request.user.pk, schedule__start_time__lt=limit_time).order_by('-create_time')
        schedules = list()
        for record in records:
            if (record.pay_back is None) or (record.detail not in (WIN_FLAG, FAIL_FLAG, DRAW_FLAG)):
                # 本场比赛还没有结算
                support_result = OTHER_FLAG
                coins = 0.0
                logger.error('==== record<record_id=%s> has no pay_back' % record.pk)
            else:
                support_result = record.detail
                coins = float(record.pay_back - record.pay_for)

            res = {
                "guess_id": record.pk,
                "country_a": record.schedule.country_a.pk,
                "country_a_cn": record.schedule.country_a.name_zh_cn,
                "odds_a": record.condition.odds_a,
                "country_b": record.schedule.country_b.pk,
                "country_b_cn": record.schedule.country_b.name_zh_cn,
                "odds_b": record.condition.odds_b,
                "start_time": dateTimeToStr(record.schedule.start_time),
                "handicap_num": record.condition.handicap_num,
                "handicap_disc": record.condition.handicap_disc,
                "score_90min": record.schedule.score_90min,
                "score_final": record.schedule.score_final,
                "pay_for": record.pay_for,
                "pay_back": coins,
                "type": record.schedule.type_cn,
                "support_country_cn": record.support_country.name_zh_cn,
                "support_odds": record.support_odds,
                "join_time": dateTimeToStr(record.create_time),
                "support_result": support_result
            }

            schedules.append(res)

        return CommonReturn(CodeMsg.SUCCESS, '成功列出用户的往期竞猜记录', {"schedules": schedules})

    @list_route(methods=['GET'],
                url_path='ranking')
    @api_serializer_deco('获取排行榜')
    def ranking(self, request):
        """
        获取排行榜
        :param request:
        :return:
        """
        ordered_user = User.objects.filter().order_by('-capital')[:10]
        ranking = list()
        for user in ordered_user:
            ranking.append({
                "user_id": user.pk,
                "user_name": user.name,
                "coins": float(user.capital),
            })
        return CommonReturn(CodeMsg.SUCCESS, '成功获取总排行榜', {"ranking": ranking})
