"""
叫应模块 - URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CallGroupViewSet, CallTargetViewSet, CallPersonViewSet,
    PolicyFileViewSet, PolicyDistributionViewSet, CallRecordViewSet,
    EmergencyCallViewSet
)

router = DefaultRouter()
router.register(r'groups', CallGroupViewSet, basename='call-group')
router.register(r'targets', CallTargetViewSet, basename='call-target')
router.register(r'persons', CallPersonViewSet, basename='call-person')
router.register(r'policy-files', PolicyFileViewSet, basename='policy-file')
router.register(r'policy-distributions', PolicyDistributionViewSet, basename='policy-distribution')
router.register(r'records', CallRecordViewSet, basename='call-record')
router.register(r'emergency', EmergencyCallViewSet, basename='emergency-call')

urlpatterns = [
    path('', include(router.urls)),
]


