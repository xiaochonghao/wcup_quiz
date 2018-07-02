# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _
from django.db import models

from orm.account.models import User
from orm.constants import HANDICAP_TYPE
from utils import create_uuid
from .managers.guess_record_manager import GuessRecordManager
from .managers.transaction_manager import TransactionManager

# Create your models here.


class Country(models.Model):
    """
    国家队表
    """
    _GROUP = (
        ('A', 'A组'),
        ('B', 'B组'),
        ('C', 'C组'),
        ('D', 'D组'),
        ('E', 'E组'),
        ('F', 'F组'),
        ('G', 'G组'),
        ('H', 'H组'),
    )
    name = models.CharField(max_length=50, primary_key=True, help_text=_('国家英文名字'))
    name_zh_cn = models.CharField(max_length=50, help_text=_('国家中文名字'))
    group = models.CharField(max_length=10, choices=_GROUP, help_text=_('所属的小组'))
    is_out = models.BooleanField(default=False, help_text=_('是否被淘汰'))
    create_time = models.DateTimeField(auto_now_add=True, help_text=_('创建时间'))
    update_time = models.DateTimeField(auto_now=True, help_text=_('更新时间'))

    def __unicode__(self):
        return self.name_zh_cn

    class Meta:
        db_table = 'wcup_country'


class Schedule(models.Model):
    """
    赛程表
    """
    _TYPE = (
        ('warm', _('热身赛')),
        ('group', _('小组赛')),
        ('1/8', _('1/8决赛')),
        ('1/4', _('1/4决赛')),
        ('3RD', _('季军赛')),
        ('final', _('决赛')),
    )

    id = models.CharField(primary_key=True, max_length=36, default=create_uuid, help_text=_('id'))
    country_a = models.ForeignKey(Country, related_name='country_a', help_text=_('主队'))
    country_b = models.ForeignKey(Country, related_name='country_b', help_text=_('客队'))
    start_time = models.DateTimeField(help_text=_('开始时间'))
    score_90min = models.CharField(max_length=20, blank=True, help_text=_('90min比赛结果'))
    score_final = models.CharField(max_length=20, blank=True, help_text=_('最终比赛结果'))
    type = models.CharField(max_length=20, choices=_TYPE, help_text=_('比赛类型'))
    processed = models.BooleanField(default=False, help_text=_('是否结算过'))
    create_time = models.DateTimeField(auto_now_add=True, help_text=_('创建时间'))
    update_time = models.DateTimeField(auto_now=True, help_text=_('更新时间'))

    @property
    def guess_end_time(self):
        """
        竞猜截止时间
        :return:
        """
        guess_end_date = self.start_time - timedelta(hours=1)
        return guess_end_date

    @property
    def type_cn(self):
        return unicode(dict(self._TYPE).get(self.type))

    def __unicode__(self):
        return '%s VS %s' % (self.country_a.name_zh_cn, self.country_b.name_zh_cn)

    class Meta:
        db_table = 'wcup_schedule'


class Transaction(models.Model):
    """
    交易明细表
    """
    id = models.AutoField(primary_key=True)
    out_gold = models.IntegerField(null=True, help_text=_('支出金币'))
    in_gold = models.DecimalField(null=True, decimal_places=3, max_digits=12, help_text=_('收入金币'))
    user = models.ForeignKey(User)
    schedule = models.ForeignKey(Schedule)
    detail = models.TextField(null=True, blank=True, help_text=_('交易明细'))
    create_time = models.DateTimeField(auto_now_add=True, help_text=_('创建时间'))

    objects = TransactionManager()

    class Meta:
        db_table = 'wcup_transaction'


class GuessCondition(models.Model):
    """
    竞猜条件表
    """
    _IS_VALID = (
        (True, _('有效')),
        (False, _('无效')),
    )
    _IS_LAST = (
        (True, _('当前最新条件')),
        (False, _('之前的竞猜条件'))
    )
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, help_text=_('属于哪个赛程'))
    odds_a = models.FloatField(default=1, help_text=_('主队赔率'))
    odds_b = models.FloatField(default=1, help_text=_('客队赔率'))
    handicap_num = models.FloatField(default=0, choices=HANDICAP_TYPE, help_text=_('让球数'))
    is_valid = models.BooleanField(choices=_IS_VALID, default=True, help_text=_('是否有效'))
    create_time = models.DateTimeField(auto_now_add=True, help_text=_('创建时间'))
    update_time = models.DateTimeField(auto_now=True, help_text=_('更新时间'))

    @property
    def handicap_disc(self):
        """
        盘口描述
        :return:
        """
        return dict(HANDICAP_TYPE).get(self.handicap_num)

    class Meta:
        db_table = 'wcup_guess_condition'


class GuessRecord(models.Model):
    """
    竞猜记录表
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User)
    schedule = models.ForeignKey(Schedule)
    condition = models.ForeignKey(GuessCondition)
    pay_for = models.IntegerField(default=10, help_text=_('本金'))
    support_country = models.ForeignKey(Country, help_text=_('支持的国家队'))
    support_odds = models.FloatField(default=1.0, help_text=_('支持的国家对应的赔率'))
    pay_back = models.DecimalField(null=True, max_digits=12, decimal_places=3, help_text=_('到手的钱'))
    detail = models.TextField(blank=True, help_text=_('回报的计算明细'))
    processed = models.BooleanField(default=False, help_text=_('是否结算过'))
    create_time = models.DateTimeField(auto_now_add=True, help_text=_('创建时间'))
    update_time = models.DateTimeField(auto_now=True, help_text=_('更新时间'))

    objects = GuessRecordManager()

    class Meta:
        db_table = 'wcup_guess_record'
