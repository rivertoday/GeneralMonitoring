"""
演练监督模块 - Django Admin配置
"""
from django.contrib import admin
from .models import DrillEvent, DrillEvaluation, DrillSummary, DrillAnalysis


@admin.register(DrillEvent)
class DrillEventAdmin(admin.ModelAdmin):
    """演练事件管理"""
    list_display = ['id', 'event_code', 'event_name', 'event_type', 'drill_status', 'event_time', 'street']
    list_filter = ['event_type', 'drill_status', 'event_time', 'created_at']
    search_fields = ['event_code', 'event_name', 'street', 'address', 'organization_id']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DrillEvaluation)
class DrillEvaluationAdmin(admin.ModelAdmin):
    """演练评价管理"""
    list_display = ['id', 'event_id', 'evaluator_id', 'node_type', 'evaluation_score', 'evaluation_time']
    list_filter = ['node_type', 'evaluation_time', 'created_at']
    search_fields = ['evaluation_item', 'evaluation_content', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DrillSummary)
class DrillSummaryAdmin(admin.ModelAdmin):
    """演练总结管理"""
    list_display = ['id', 'event_id', 'summary_title', 'overall_level', 'summary_time', 'summary_user_id']
    list_filter = ['overall_level', 'summary_time', 'created_at']
    search_fields = ['summary_title', 'enterprise_summary', 'supervisor_opinion', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(DrillAnalysis)
class DrillAnalysisAdmin(admin.ModelAdmin):
    """演练分析管理"""
    list_display = ['id', 'stat_date', 'stat_type', 'organization_id', 'drill_type', 'drill_count', 'created_at']
    list_filter = ['stat_type', 'stat_date', 'created_at']
    search_fields = ['stat_date']
    readonly_fields = ['created_at']
    ordering = ['-stat_date']
