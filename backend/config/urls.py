"""
风险监测预警系统 - 主URL配置
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger/OpenAPI schema视图
schema_view = get_schema_view(
    openapi.Info(
        title=settings.API_INFO['title'],
        default_version=settings.API_INFO['default_version'],
        description=settings.API_INFO['description'],
        terms_of_service=settings.API_INFO.get('terms_of_service', ''),
        contact=openapi.Contact(**settings.API_INFO.get('contact', {})),
        license=openapi.License(**settings.API_INFO.get('license', {})),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # 根路径重定向到API文档
    path('', lambda request: redirect('swagger/'), name='home'),
    
    # Django管理后台
    path('admin/', admin.site.urls),
    
    # API接口
    path('api/v1/', include('api.urls')),
    
    # Swagger/OpenAPI文档
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui-alt'),
]

# 开发环境静态文件和媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # 静态文件由Django的staticfiles自动从STATICFILES_DIRS提供，无需手动配置
