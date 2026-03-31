"""
安全态势展示模块 - URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SafetyResourceViewSet, SafetyTargetViewSet, ShelterViewSet,
    IndustryStatusViewSet, RegionStatusViewSet, MonitorDataViewSet,
    WarningEventViewSet, HazardSourceViewSet, VideoMonitorViewSet
)

router = DefaultRouter()
router.register(r'resources', SafetyResourceViewSet, basename='safety-resource')
router.register(r'targets', SafetyTargetViewSet, basename='safety-target')
router.register(r'shelters', ShelterViewSet, basename='shelter')
router.register(r'industry-status', IndustryStatusViewSet, basename='industry-status')
router.register(r'region-status', RegionStatusViewSet, basename='region-status')
router.register(r'monitor-data', MonitorDataViewSet, basename='monitor-data')
router.register(r'warning-events', WarningEventViewSet, basename='warning-event')
router.register(r'hazard-sources', HazardSourceViewSet, basename='hazard-source')
router.register(r'video-monitors', VideoMonitorViewSet, basename='video-monitor')

urlpatterns = [
    path('', include(router.urls)),
]

