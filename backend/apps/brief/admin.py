"""
简报模块 - Django Admin配置
"""
from django.contrib import admin
from .models import BriefTemplate, BriefStrategy, BriefData, BriefPush


@admin.register(BriefTemplate)
class BriefTemplateAdmin(admin.ModelAdmin):
    """简报模板管理"""
    list_display = ['id', 'template_code', 'template_name', 'template_type', 'status', 'created_at']
    list_filter = ['template_type', 'status', 'created_at']
    search_fields = ['template_code', 'template_name', 'template_content']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BriefStrategy)
class BriefStrategyAdmin(admin.ModelAdmin):
    """简报策略管理"""
    list_display = ['id', 'strategy_name', 'template_id', 'trigger_type', 'status', 'created_at']
    list_filter = ['trigger_type', 'status', 'created_at']
    search_fields = ['strategy_name', 'trigger_config', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(BriefData)
class BriefDataAdmin(admin.ModelAdmin):
    """简报数据管理"""
    list_display = ['id', 'brief_code', 'template_id', 'brief_type', 'status', 'generate_time']
    list_filter = ['brief_type', 'status', 'generate_time']
    search_fields = ['brief_code', 'brief_title', 'brief_content']
    readonly_fields = ['created_at', 'updated_at', 'generate_time']


@admin.register(BriefPush)
class BriefPushAdmin(admin.ModelAdmin):
    """简报推送记录管理"""
    list_display = ['id', 'brief_id', 'push_channel', 'push_status', 'push_time', 'error_message']
    list_filter = ['push_channel', 'push_status', 'push_time']
    search_fields = ['brief_id', 'target_id', 'error_message']
    readonly_fields = ['created_at', 'push_time']
