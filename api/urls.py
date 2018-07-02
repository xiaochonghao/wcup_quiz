# -*- coding: utf-8 -*-
from rest_framework.routers import DefaultRouter

from api.api_views.account_views import AccountViewSet
from api.api_views.wcup_views import WCupQuizViewSet
router = DefaultRouter(trailing_slash=True)

router.register(r'account', AccountViewSet, base_name='account')
router.register(r'wcup', WCupQuizViewSet, base_name='wcup')

urlpatterns = router.urls
