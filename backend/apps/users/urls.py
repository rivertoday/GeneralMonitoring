"""
用户权限管理 - URL配置（用户、角色、权限、组织管理）
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RoleViewSet, PermissionViewSet, OrganizationViewSet

# 创建路由器
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'permissions', PermissionViewSet, basename='permission')
router.register(r'organizations', OrganizationViewSet, basename='organization')

urlpatterns = [
    # 路由器注册的路由
    path('', include(router.urls)),
]


