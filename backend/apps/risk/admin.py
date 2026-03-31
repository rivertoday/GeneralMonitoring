"""
风险监测预警模块 - Django Admin配置
"""
from django.contrib import admin
from .models import (
    WarningLevel, WarningRule, RiskMonitor, AlarmRecord,
    RiskWarning, AlarmStatistics, RiskHiddenDanger, RiskRectification
)


@admin.register(WarningLevel)
class WarningLevelAdmin(admin.ModelAdmin):
    """预警级别管理"""
    list_display = ['id', 'level_code', 'level_name', 'level_color', 'severity', 'status', 'sort_order']
    list_filter = ['level_color', 'severity', 'status', 'created_at']
    search_fields = ['level_code', 'level_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['severity']


@admin.register(WarningRule)
class WarningRuleAdmin(admin.ModelAdmin):
    """预警规则管理"""
    list_display = ['id', 'rule_name', 'rule_type', 'warning_level', 'status', 'created_at']
    list_filter = ['rule_type', 'warning_level', 'status', 'created_at']
    search_fields = ['rule_code', 'rule_name', 'condition_config', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RiskMonitor)
class RiskMonitorAdmin(admin.ModelAdmin):
    """风险监测数据管理"""
    list_display = ['id', 'monitor_code', 'monitor_name', 'industry_type', 'monitor_value', 'last_data_time']
    list_filter = ['industry_type', 'last_data_time', 'created_at']
    search_fields = ['monitor_code', 'monitor_name', 'location']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AlarmRecord)
class AlarmRecordAdmin(admin.ModelAdmin):
    """报警记录管理"""
    list_display = ['id', 'alarm_code', 'alarm_type', 'industry_type', 'alarm_status', 'alarm_time', 'handle_time']
    list_filter = ['alarm_type', 'industry_type', 'alarm_status', 'alarm_time']
    search_fields = ['alarm_code', 'description', 'location', 'handle_user_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RiskWarning)
class RiskWarningAdmin(admin.ModelAdmin):
    """风险预警管理"""
    list_display = ['id', 'warning_code', 'warning_type', 'warning_level', 'warning_analysis_type', 'warning_status', 'warning_time']
    list_filter = ['warning_type', 'warning_level', 'warning_analysis_type', 'warning_status', 'warning_time']
    search_fields = ['warning_code', 'warning_title', 'warning_content', 'location']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AlarmStatistics)
class AlarmStatisticsAdmin(admin.ModelAdmin):
    """报警统计管理"""
    list_display = ['id', 'stat_date', 'stat_type', 'industry_type', 'alarm_count', 'handled_count']
    list_filter = ['stat_date', 'stat_type', 'industry_type']
    search_fields = ['stat_date', 'street']
    ordering = ['-stat_date']


@admin.register(RiskHiddenDanger)
class RiskHiddenDangerAdmin(admin.ModelAdmin):
    """隐患排查管理"""
    list_display = ['id', 'danger_code', 'danger_name', 'industry_type', 'danger_level', 'status', 'discover_time', 'location']
    list_filter = ['industry_type', 'danger_level', 'status', 'discover_time']
    search_fields = ['danger_code', 'danger_name', 'location', 'discover_user_id', 'organization_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(RiskRectification)
class RiskRectificationAdmin(admin.ModelAdmin):
    """隐患整改管理"""
    list_display = ['id', 'rectification_code', 'danger', 'rectification_status', 'plan_end_time', 'responsible_user_id']
    list_filter = ['rectification_status', 'plan_end_time', 'created_at']
    search_fields = ['rectification_code', 'rectification_plan', 'rectification_measures', 'responsible_user_id', 'responsible_org_id']
    readonly_fields = ['created_at', 'updated_at']
