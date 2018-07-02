# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from orm.wcup import models as wcup_models
# Register your models here.


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_zh_cn', 'group', 'is_out')
    readonly_fields = ('create_time', )
    search_fields = ('name', 'name_zh_cn')
    list_per_page = 20


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'country_a', 'country_b', 'type', 'score_90min', 'start_time', 'processed')
    readonly_fields = ('create_time',)
    raw_id_fields = ('country_a', 'country_b')
    search_fields = ('id',)
    list_per_page = 20
    ordering = ('processed', 'start_time',)


class GuessConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'odds_a', 'odds_b', 'handicap_num', 'schedule')
    readonly_fields = ('create_time',)
    raw_id_fields = ('schedule',)
    search_fields = ('schedule_id', 'id')
    ordering = ('-update_time', '-create_time',)
    list_per_page = 20


admin.site.register(wcup_models.Country, CountryAdmin)
admin.site.register(wcup_models.Schedule, ScheduleAdmin)
admin.site.register(wcup_models.GuessCondition, GuessConditionAdmin)
admin.site.site_header = '世界杯竞猜后台'
admin.site.index_title = "Word Cup Quiz Management Platform"
