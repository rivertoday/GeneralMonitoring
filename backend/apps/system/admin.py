"""
系统管理模块 - Django Admin配置
"""
from django.contrib import admin
from .models import DataSource, MessageTemplate


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    """数据源管理"""
    list_display = ['id', 'source_code', 'source_name', 'source_type', 'status', 'last_sync_at']
    list_filter = ['source_type', 'status', 'created_at']
    search_fields = ['source_code', 'source_name', 'api_url', 'description']
    readonly_fields = ['created_at', 'updated_at', 'last_sync_at']


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    """消息模板管理"""
    list_display = ['id', 'template_code', 'template_name', 'template_type', 'message_type', 'status', 'created_at']
    list_filter = ['template_type', 'message_type', 'status', 'created_at']
    search_fields = ['template_code', 'template_name', 'content', 'description']
    readonly_fields = ['created_at', 'updated_at']
