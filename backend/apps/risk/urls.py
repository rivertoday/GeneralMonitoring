"""
风险监测预警 - URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WarningLevelViewSet, WarningRuleViewSet, RiskMonitorViewSet,
    AlarmRecordViewSet, RiskWarningViewSet, AlarmStatisticsViewSet,
    RiskHiddenDangerViewSet, RiskRectificationViewSet
)

# 创建路由器
router = DefaultRouter()
router.register(r'warning-levels', WarningLevelViewSet, basename='warning-level')
router.register(r'warning-rules', WarningRuleViewSet, basename='warning-rule')
router.register(r'monitors', RiskMonitorViewSet, basename='monitor')
router.register(r'alarm-records', AlarmRecordViewSet, basename='alarm-record')
router.register(r'warnings', RiskWarningViewSet, basename='warning')
router.register(r'alarm-statistics', AlarmStatisticsViewSet, basename='alarm-statistic')
router.register(r'hidden-dangers', RiskHiddenDangerViewSet, basename='hidden-danger')
router.register(r'rectifications', RiskRectificationViewSet, basename='rectification')

urlpatterns = [
    # 路由器注册的路由
    path('', include(router.urls)),
]