"""
叫应模块 - Django Admin配置
"""
from django.contrib import admin
from .models import CallGroup, CallTarget, CallPerson, PolicyFile, PolicyDistribution, CallRecord


@admin.register(CallGroup)
class CallGroupAdmin(admin.ModelAdmin):
    """叫应分组管理"""
    list_display = ['id', 'group_code', 'group_name', 'group_type', 'status', 'created_at']
    list_filter = ['group_type', 'status', 'created_at']
    search_fields = ['group_code', 'group_name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CallTarget)
class CallTargetAdmin(admin.ModelAdmin):
    """叫应对象管理"""
    list_display = ['id', 'target_code', 'target_name', 'target_type', 'organization_id', 'status', 'created_at']
    list_filter = ['target_type', 'status', 'created_at']
    search_fields = ['target_code', 'target_name', 'contact_person', 'contact_phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CallPerson)
class CallPersonAdmin(admin.ModelAdmin):
    """叫应人员管理"""
    list_display = ['id', 'person_name', 'rank', 'organization_id', 'mobile_phone', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['person_name', 'mobile_phone', 'office_phone', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PolicyFile)
class PolicyFileAdmin(admin.ModelAdmin):
    """政策文件管理"""
    list_display = ['id', 'file_code', 'file_name', 'file_type', 'publish_status', 'publish_time', 'created_at']
    list_filter = ['file_type', 'publish_status', 'publish_time', 'created_at']
    search_fields = ['file_code', 'file_name', 'policy_content', 'policy_title']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(PolicyDistribution)
class PolicyDistributionAdmin(admin.ModelAdmin):
    """政策文件下发表管理"""
    list_display = ['id', 'distribution_code', 'policy_file_id', 'target_id', 'feedback_status', 'distribution_time']
    list_filter = ['feedback_status', 'distribution_time']
    search_fields = ['distribution_code', 'policy_file_id']
    readonly_fields = ['created_at', 'distribution_time']


@admin.register(CallRecord)
class CallRecordAdmin(admin.ModelAdmin):
    """叫应记录管理"""
    list_display = ['id', 'call_code', 'call_type', 'call_status', 'call_time', 'person_id']
    list_filter = ['call_type', 'call_status', 'call_time', 'created_at']
    search_fields = ['call_code', 'call_content', 'error_message']
    readonly_fields = ['created_at', 'updated_at', 'call_time']
