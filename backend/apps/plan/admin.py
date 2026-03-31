"""
预案模块 - Django Admin配置
"""
from django.contrib import admin
from .models import (
    EmergencyPlan, PlanStructure, PlanFlow,
    PlanTask, PlanExecution, PlanTaskExecution
)


@admin.register(EmergencyPlan)
class EmergencyPlanAdmin(admin.ModelAdmin):
    """应急预案管理"""
    list_display = ['id', 'plan_code', 'plan_name', 'plan_type', 'plan_status', 'created_at']
    list_filter = ['plan_type', 'plan_status', 'created_at']
    search_fields = ['plan_code', 'plan_name', 'plan_summary', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PlanStructure)
class PlanStructureAdmin(admin.ModelAdmin):
    """预案结构管理"""
    list_display = ['id', 'plan_id', 'node_name', 'node_type', 'parent_id', 'node_level', 'node_index']
    list_filter = ['node_type', 'node_level', 'created_at']
    search_fields = ['node_name', 'node_content']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['plan_id', 'node_level', 'node_index']


@admin.register(PlanFlow)
class PlanFlowAdmin(admin.ModelAdmin):
    """预案流程管理"""
    list_display = ['id', 'plan_id', 'flow_name', 'flow_type', 'parent_id', 'flow_level', 'sort_order']
    list_filter = ['flow_type', 'flow_level', 'created_at']
    search_fields = ['flow_name', 'condition_config', 'flow_config']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['plan_id', 'sort_order']


@admin.register(PlanTask)
class PlanTaskAdmin(admin.ModelAdmin):
    """预案任务管理"""
    list_display = ['id', 'plan_id', 'task_name', 'task_type', 'priority', 'organization_id', 'assign_user_id']
    list_filter = ['task_type', 'priority', 'created_at']
    search_fields = ['task_name', 'task_description', 'task_requirement']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['plan_id', 'priority']


@admin.register(PlanExecution)
class PlanExecutionAdmin(admin.ModelAdmin):
    """预案执行记录管理"""
    list_display = ['id', 'execution_code', 'plan_id', 'execution_status', 'start_time', 'end_time', 'command_user_id']
    list_filter = ['execution_status', 'start_time', 'created_at']
    search_fields = ['execution_code', 'execution_result', 'execution_summary']
    readonly_fields = ['created_at', 'updated_at', 'start_time']


@admin.register(PlanTaskExecution)
class PlanTaskExecutionAdmin(admin.ModelAdmin):
    """预案任务执行记录管理"""
    list_display = ['id', 'execution_id', 'task_id', 'task_status', 'start_time', 'end_time', 'assign_user_id']
    list_filter = ['task_status', 'start_time', 'created_at']
    search_fields = ['task_result', 'feedback_content']
    readonly_fields = ['created_at', 'updated_at', 'start_time']
