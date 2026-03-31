"""
系统管理模块 - URL配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DataSourceViewSet, MessageTemplateViewSet

router = DefaultRouter()
router.register(r'data-sources', DataSourceViewSet, basename='data-source')
router.register(r'message-templates', MessageTemplateViewSet, basename='message-template')

urlpatterns = [
    path('', include(router.urls)),
]

