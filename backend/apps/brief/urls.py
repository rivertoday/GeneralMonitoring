"""
平急两用简报 - URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BriefTemplateViewSet, BriefStrategyViewSet,
    BriefDataViewSet, BriefPushViewSet
)

# 创建路由器
router = DefaultRouter()
router.register(r'templates', BriefTemplateViewSet, basename='brief-template')
router.register(r'strategies', BriefStrategyViewSet, basename='brief-strategy')
router.register(r'data', BriefDataViewSet, basename='brief-data')
router.register(r'pushes', BriefPushViewSet, basename='brief-push')

urlpatterns = [
    # 路由器注册的路由
    path('', include(router.urls)),
]
