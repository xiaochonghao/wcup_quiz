# -*- encoding:utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _


HANDICAP_TYPE = (
    (-0.25, _('平手/半球')),
    (-0.5, _('半球')),
    (-0.75, _('半球/一球')),
    (-1, _('一球')),
    (-1.25, _('一球/球半')),
    (-1.5, _('球半')),
    (-1.75, _('球半/两球')),
    (-2, _('两球')),
    (-2.25, _('两球/两球半')),
    (-2.5, _('两球半')),
    (-2.75, _('两球半/三球')),
    (-3, _('三球')),
    (0, _('平手')),
    (+0.25, _('受让平手/半球')),
    (+0.5, _('受让半球')),
    (+0.75, _('受让半球/一球')),
    (+1, _('受让一球')),
    (+1.25, _('受让一球/球半')),
    (+1.5, _('受让球半')),
    (+1.75, _('受让球半/两球')),
    (+2, _('受让两球')),
    (+2.25, _('受让两球/两球半')),
    (+2.5, _('受让两球半')),
    (+2.75, _('受让两球半/三球')),
    (+3, _('受让三球')),
)

# 整数盘口，踢平之后的扣的本机比率
WATER_RATE = 0.1

# 胜负平的标志
WIN_FLAG = 'win'
FAIL_FLAG = 'failed'
DRAW_FLAG = 'draw'
OTHER_FLAG = 'unknown'
