"""
API接口路由配置
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 创建路由器
router = DefaultRouter()

# 注册各个模块的路由
# router.register(r'users', UserViewSet, basename='user')
# router.register(r'risk', RiskViewSet, basename='risk')
# ... 其他路由将在各app中注册

# 认证相关路由（直接在这里定义，避免模块导入问题）
from apps.users.auth_views import login, refresh_token, logout, user_info

urlpatterns = [
    # 认证相关（仅登录、刷新token等）
    path('auth/login/', login, name='auth-login'),
    path('auth/refresh/', refresh_token, name='auth-refresh'),
    path('auth/logout/', logout, name='auth-logout'),
    path('auth/user-info/', user_info, name='auth-user-info'),
    
    # 用户权限管理（用户、角色、权限、组织）
    path('users/', include('apps.users.urls')),
    
    # 风险监测预警
    path('risk/', include('apps.risk.urls')),
    
    # 简报
    path('brief/', include('apps.brief.urls')),
    
    # 叫应
    path('call/', include('apps.call.urls')),
    
    # 预案
    path('plan/', include('apps.plan.urls')),
    
    # 安全态势
    path('safety/', include('apps.safety.urls')),
    
    # 演练
    path('drill/', include('apps.drill.urls')),
    
    # 系统管理
    path('system/', include('apps.system.urls')),
    
    # 路由器注册的路由
    path('', include(router.urls)),
]


