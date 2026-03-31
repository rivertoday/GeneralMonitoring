"""
安全态势展示模块 - Django Admin配置
"""
from django.contrib import admin
from .models import (
    SafetyResource, SafetyTarget, Shelter, IndustryStatus,
    RegionStatus, MonitorData, WarningEvent, HazardSource, VideoMonitor
)


@admin.register(SafetyResource)
class SafetyResourceAdmin(admin.ModelAdmin):
    """安全资源管理"""
    list_display = ['id', 'resource_code', 'resource_name', 'resource_type', 'status', 'street', 'created_at']
    list_filter = ['resource_type', 'status', 'created_at']
    search_fields = ['resource_code', 'resource_name', 'street', 'address', 'contact_person', 'contact_phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(SafetyTarget)
class SafetyTargetAdmin(admin.ModelAdmin):
    """防护目标管理"""
    list_display = ['id', 'target_code', 'target_name', 'target_type', 'risk_level', 'status', 'street']
    list_filter = ['target_type', 'risk_level', 'status', 'created_at']
    search_fields = ['target_code', 'target_name', 'street', 'address', 'contact_person', 'contact_phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Shelter)
class ShelterAdmin(admin.ModelAdmin):
    """避难场所管理"""
    list_display = ['id', 'shelter_code', 'shelter_name', 'shelter_type', 'capacity', 'status', 'street']
    list_filter = ['shelter_type', 'status', 'created_at']
    search_fields = ['shelter_code', 'shelter_name', 'street', 'address', 'contact_person', 'contact_phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(IndustryStatus)
class IndustryStatusAdmin(admin.ModelAdmin):
    """行业态势管理"""
    list_display = ['id', 'stat_date', 'industry_type', 'alarm_count', 'warning_count', 'risk_count', 'updated_at']
    list_filter = ['stat_date', 'industry_type', 'updated_at']
    search_fields = ['stat_date']
    ordering = ['-stat_date', 'industry_type']


@admin.register(RegionStatus)
class RegionStatusAdmin(admin.ModelAdmin):
    """区域态势管理"""
    list_display = ['id', 'stat_date', 'street', 'alarm_count', 'warning_count', 'risk_count', 'updated_at']
    list_filter = ['stat_date', 'updated_at']
    search_fields = ['stat_date', 'street']
    ordering = ['-stat_date', 'street']


@admin.register(MonitorData)
class MonitorDataAdmin(admin.ModelAdmin):
    """监测数据管理"""
    list_display = ['id', 'monitor_id', 'industry_type', 'data_time', 'monitor_value', 'online_status']
    list_filter = ['industry_type', 'data_time', 'online_status']
    search_fields = ['monitor_id', 'data_source']
    readonly_fields = ['created_at']
    ordering = ['-data_time']


@admin.register(WarningEvent)
class WarningEventAdmin(admin.ModelAdmin):
    """预警事件管理"""
    list_display = ['id', 'warning_code', 'warning_type', 'warning_level_id', 'warning_status', 'warning_time', 'street']
    list_filter = ['warning_type', 'warning_level_id', 'warning_status', 'warning_time']
    search_fields = ['warning_code', 'warning_title', 'street', 'address']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(HazardSource)
class HazardSourceAdmin(admin.ModelAdmin):
    """危险源管理"""
    list_display = ['id', 'source_code', 'source_name', 'source_type', 'industry_type', 'risk_level', 'status', 'street']
    list_filter = ['source_type', 'industry_type', 'risk_level', 'status', 'created_at']
    search_fields = ['source_code', 'source_name', 'street', 'address', 'contact_person', 'contact_phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(VideoMonitor)
class VideoMonitorAdmin(admin.ModelAdmin):
    """视频监控设施管理"""
    list_display = ['id', 'monitor_code', 'monitor_name', 'monitor_type', 'industry_type', 'status', 'street', 'created_at']
    list_filter = ['monitor_type', 'industry_type', 'status', 'created_at']
    search_fields = ['monitor_code', 'monitor_name', 'street', 'address', 'video_url', 'rtsp_url']
    readonly_fields = ['created_at', 'updated_at']
