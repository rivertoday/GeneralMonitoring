"""
预案模块 - 序列化器
"""
import json
import uuid
from rest_framework import serializers
from django.utils import timezone
from apps.users.models import User, Organization
from .models import (
    EmergencyPlan, PlanStructure, PlanFlow,
    PlanTask, PlanExecution, PlanTaskExecution
)


class EmergencyPlanSerializer(serializers.ModelSerializer):
    """应急预案序列化器"""
    plan_type_display = serializers.CharField(source='get_plan_type_display', read_only=True)
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    plan_status_display = serializers.CharField(source='get_plan_status_display', read_only=True)
    organization_name = serializers.SerializerMethodField()
    create_user_name = serializers.SerializerMethodField()
    approve_user_name = serializers.SerializerMethodField()

    class Meta:
        model = EmergencyPlan
        fields = [
            'id', 'plan_code', 'plan_name', 'plan_type', 'plan_type_display',
            'industry_type', 'industry_type_display', 'organization_id', 'organization_name',
            'version', 'plan_file_path', 'plan_file_name', 'plan_summary',
            'plan_status', 'plan_status_display', 'publish_time', 'effective_time',
            'expire_time', 'revision_reason', 'create_user_id', 'create_user_name',
            'approve_user_id', 'approve_user_name', 'approve_time', 'description',
            'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_organization_name(self, obj):
        """获取所属部门名称"""
        if obj.organization_id:
            try:
                org = Organization.objects.get(id=obj.organization_id, deleted_at__isnull=True)
                return org.org_name
            except Organization.DoesNotExist:
                return None
        return None

    def get_create_user_name(self, obj):
        """获取创建人姓名"""
        if obj.create_user_id:
            try:
                user = User.objects.get(id=obj.create_user_id, deleted_at__isnull=True)
                return user.username
            except User.DoesNotExist:
                return None
        return None

    def get_approve_user_name(self, obj):
        """获取审批人姓名"""
        if obj.approve_user_id:
            try:
                user = User.objects.get(id=obj.approve_user_id, deleted_at__isnull=True)
                return user.username
            except User.DoesNotExist:
                return None
        return None


class EmergencyPlanPublishSerializer(serializers.Serializer):
    """预案发布序列化器"""
    publish_time = serializers.DateTimeField(required=False, allow_null=True, help_text='发布时间，不传则使用当前时间')
    effective_time = serializers.DateTimeField(required=False, allow_null=True, help_text='生效时间')


class EmergencyPlanApproveSerializer(serializers.Serializer):
    """预案审批序列化器"""
    approve_user_id = serializers.IntegerField(required=True, help_text='审批人ID')
    approve_time = serializers.DateTimeField(required=False, allow_null=True, help_text='审批时间，不传则使用当前时间')


class EmergencyPlanReviseSerializer(serializers.Serializer):
    """预案修订序列化器"""
    revision_reason = serializers.CharField(required=True, help_text='修订原因')
    new_version = serializers.CharField(required=True, help_text='新版本号')


class EmergencyPlanAbandonSerializer(serializers.Serializer):
    """预案废止序列化器"""
    revision_reason = serializers.CharField(required=True, help_text='废止原因')


class PlanStructureSerializer(serializers.ModelSerializer):
    """预案结构序列化器"""
    node_type_display = serializers.CharField(source='get_node_type_display', read_only=True)
    plan_name = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = PlanStructure
        fields = [
            'id', 'plan_id', 'plan_name', 'node_code', 'node_name', 'parent_id',
            'node_type', 'node_type_display', 'node_level', 'node_content',
            'node_index', 'is_key_info', 'description', 'remark',
            'children', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_plan_name(self, obj):
        """获取预案名称"""
        if obj.plan_id:
            try:
                plan = EmergencyPlan.objects.get(id=obj.plan_id, deleted_at__isnull=True)
                return plan.plan_name
            except EmergencyPlan.DoesNotExist:
                return None
        return None

    def get_children(self, obj):
        """获取子节点（树形结构）"""
        children = PlanStructure.objects.filter(
            plan_id=obj.plan_id,
            parent_id=obj.id,
            deleted_at__isnull=True
        ).order_by('node_index')
        return PlanStructureSerializer(children, many=True).data


class PlanFlowSerializer(serializers.ModelSerializer):
    """预案流程序列化器"""
    flow_type_display = serializers.CharField(source='get_flow_type_display', read_only=True)
    plan_name = serializers.SerializerMethodField()
    flow_config_dict = serializers.SerializerMethodField()
    next_flow_ids_list = serializers.SerializerMethodField()
    condition_config_dict = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = PlanFlow
        fields = [
            'id', 'plan_id', 'plan_name', 'flow_code', 'flow_name', 'parent_id',
            'flow_type', 'flow_type_display', 'flow_level', 'flow_config',
            'flow_config_dict', 'next_flow_ids', 'next_flow_ids_list',
            'condition_config', 'condition_config_dict', 'sort_order',
            'description', 'remark', 'children', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_plan_name(self, obj):
        """获取预案名称"""
        if obj.plan_id:
            try:
                plan = EmergencyPlan.objects.get(id=obj.plan_id, deleted_at__isnull=True)
                return plan.plan_name
            except EmergencyPlan.DoesNotExist:
                return None
        return None

    def get_flow_config_dict(self, obj):
        """获取流程配置字典"""
        if obj.flow_config:
            try:
                return json.loads(obj.flow_config)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_next_flow_ids_list(self, obj):
        """获取下一流程ID列表"""
        if obj.next_flow_ids:
            try:
                return json.loads(obj.next_flow_ids)
            except (json.JSONDecodeError, TypeError):
                return []
        return []

    def get_condition_config_dict(self, obj):
        """获取条件配置字典"""
        if obj.condition_config:
            try:
                return json.loads(obj.condition_config)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_children(self, obj):
        """获取子流程（树形结构）"""
        children = PlanFlow.objects.filter(
            plan_id=obj.plan_id,
            parent_id=obj.id,
            deleted_at__isnull=True
        ).order_by('sort_order')
        return PlanFlowSerializer(children, many=True).data


class PlanTaskSerializer(serializers.ModelSerializer):
    """预案任务序列化器"""
    task_type_display = serializers.CharField(source='get_task_type_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    plan_name = serializers.SerializerMethodField()
    flow_name = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()
    assign_user_name = serializers.SerializerMethodField()
    assign_role_name = serializers.SerializerMethodField()

    class Meta:
        model = PlanTask
        fields = [
            'id', 'plan_id', 'plan_name', 'flow_id', 'flow_name', 'task_code',
            'task_name', 'task_type', 'task_type_display', 'organization_id',
            'organization_name', 'assign_user_id', 'assign_user_name',
            'assign_role_id', 'assign_role_name', 'task_description',
            'task_requirement', 'estimated_time', 'priority', 'priority_display',
            'sort_order', 'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_plan_name(self, obj):
        """获取预案名称"""
        if obj.plan_id:
            try:
                plan = EmergencyPlan.objects.get(id=obj.plan_id, deleted_at__isnull=True)
                return plan.plan_name
            except EmergencyPlan.DoesNotExist:
                return None
        return None

    def get_flow_name(self, obj):
        """获取流程名称"""
        if obj.flow_id:
            try:
                flow = PlanFlow.objects.get(id=obj.flow_id, deleted_at__isnull=True)
                return flow.flow_name
            except PlanFlow.DoesNotExist:
                return None
        return None

    def get_organization_name(self, obj):
        """获取负责组织名称"""
        if obj.organization_id:
            try:
                org = Organization.objects.get(id=obj.organization_id, deleted_at__isnull=True)
                return org.org_name
            except Organization.DoesNotExist:
                return None
        return None

    def get_assign_user_name(self, obj):
        """获取指定执行人姓名"""
        if obj.assign_user_id:
            try:
                user = User.objects.get(id=obj.assign_user_id, deleted_at__isnull=True)
                return user.username
            except User.DoesNotExist:
                return None
        return None

    def get_assign_role_name(self, obj):
        """获取指定角色名称"""
        if obj.assign_role_id:
            try:
                from apps.users.models import Role
                role = Role.objects.get(id=obj.assign_role_id, deleted_at__isnull=True)
                return role.role_name
            except Exception:
                return None
        return None


class PlanExecutionSerializer(serializers.ModelSerializer):
    """预案执行记录序列化器"""
    execution_type_display = serializers.CharField(source='get_execution_type_display', read_only=True)
    execution_status_display = serializers.CharField(source='get_execution_status_display', read_only=True)
    plan_name = serializers.SerializerMethodField()
    warning_detail = serializers.SerializerMethodField()
    current_flow_name = serializers.SerializerMethodField()
    command_user_name = serializers.SerializerMethodField()

    class Meta:
        model = PlanExecution
        fields = [
            'id', 'execution_code', 'plan_id', 'plan_name', 'warning_id', 'warning_detail',
            'execution_type', 'execution_type_display', 'execution_status',
            'execution_status_display', 'start_time', 'end_time', 'duration',
            'command_user_id', 'command_user_name', 'current_flow_id', 'current_flow_name',
            'execution_result', 'execution_summary', 'description', 'remark',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'execution_code', 'created_at', 'updated_at']

    def get_plan_name(self, obj):
        """获取预案名称"""
        if obj.plan_id:
            try:
                plan = EmergencyPlan.objects.get(id=obj.plan_id, deleted_at__isnull=True)
                return plan.plan_name
            except EmergencyPlan.DoesNotExist:
                return None
        return None

    def get_warning_detail(self, obj):
        """获取预警详情"""
        if obj.warning_id:
            try:
                from apps.risk.models import RiskWarning
                warning = RiskWarning.objects.get(id=obj.warning_id, deleted_at__isnull=True)
                return {'id': warning.id, 'warning_code': warning.warning_code, 'warning_title': warning.warning_title}
            except Exception:
                return None
        return None

    def get_current_flow_name(self, obj):
        """获取当前流程名称"""
        if obj.current_flow_id:
            try:
                flow = PlanFlow.objects.get(id=obj.current_flow_id, deleted_at__isnull=True)
                return flow.flow_name
            except PlanFlow.DoesNotExist:
                return None
        return None

    def get_command_user_name(self, obj):
        """获取指挥人姓名"""
        if obj.command_user_id:
            try:
                user = User.objects.get(id=obj.command_user_id, deleted_at__isnull=True)
                return user.username
            except User.DoesNotExist:
                return None
        return None


class PlanExecutionStartSerializer(serializers.Serializer):
    """预案执行启动序列化器"""
    warning_id = serializers.IntegerField(required=False, allow_null=True, help_text='关联预警ID')
    execution_type = serializers.ChoiceField(choices=PlanExecution.EXECUTION_TYPE_CHOICES, default=1, help_text='执行类型：1-演练执行，2-实战执行')
    start_time = serializers.DateTimeField(required=False, allow_null=True, help_text='开始时间，不传则使用当前时间')


class PlanExecutionUpdateStatusSerializer(serializers.Serializer):
    """预案执行状态更新序列化器"""
    execution_status = serializers.ChoiceField(choices=PlanExecution.EXECUTION_STATUS_CHOICES, required=True, help_text='执行状态')
    current_flow_id = serializers.IntegerField(required=False, allow_null=True, help_text='当前流程ID')
    execution_result = serializers.CharField(required=False, allow_blank=True, help_text='执行结果')


class PlanExecutionCompleteSerializer(serializers.Serializer):
    """预案执行完成序列化器"""
    end_time = serializers.DateTimeField(required=False, allow_null=True, help_text='结束时间，不传则使用当前时间')
    execution_result = serializers.CharField(required=False, allow_blank=True, help_text='执行结果')
    execution_summary = serializers.CharField(required=False, allow_blank=True, help_text='执行总结')


class PlanTaskExecutionSerializer(serializers.ModelSerializer):
    """预案任务执行记录序列化器"""
    task_status_display = serializers.CharField(source='get_task_status_display', read_only=True)
    execution_detail = serializers.SerializerMethodField()
    task_detail = serializers.SerializerMethodField()
    assign_user_name = serializers.SerializerMethodField()

    class Meta:
        model = PlanTaskExecution
        fields = [
            'id', 'execution_id', 'execution_detail', 'task_id', 'task_detail',
            'assign_user_id', 'assign_user_name', 'task_status', 'task_status_display',
            'assign_time', 'accept_time', 'start_time', 'end_time', 'duration',
            'task_result', 'feedback_content', 'feedback_time', 'description',
            'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_execution_detail(self, obj):
        """获取预案执行记录详情"""
        if obj.execution_id:
            try:
                execution = PlanExecution.objects.get(id=obj.execution_id, deleted_at__isnull=True)
                return {
                    'id': execution.id,
                    'execution_code': execution.execution_code,
                    'plan_id': execution.plan_id,
                    'execution_status': execution.execution_status
                }
            except PlanExecution.DoesNotExist:
                return None
        return None

    def get_task_detail(self, obj):
        """获取任务详情"""
        if obj.task_id:
            try:
                task = PlanTask.objects.get(id=obj.task_id, deleted_at__isnull=True)
                return {
                    'id': task.id,
                    'task_code': task.task_code,
                    'task_name': task.task_name,
                    'task_type': task.task_type
                }
            except PlanTask.DoesNotExist:
                return None
        return None

    def get_assign_user_name(self, obj):
        """获取执行人姓名"""
        if obj.assign_user_id:
            try:
                user = User.objects.get(id=obj.assign_user_id, deleted_at__isnull=True)
                return user.username
            except User.DoesNotExist:
                return None
        return None


class PlanTaskExecutionAcceptSerializer(serializers.Serializer):
    """任务执行接受序列化器"""
    accept_time = serializers.DateTimeField(required=False, allow_null=True, help_text='接受时间，不传则使用当前时间')


class PlanTaskExecutionStartSerializer(serializers.Serializer):
    """任务执行开始序列化器"""
    start_time = serializers.DateTimeField(required=False, allow_null=True, help_text='开始时间，不传则使用当前时间')


class PlanTaskExecutionCompleteSerializer(serializers.Serializer):
    """任务执行完成序列化器"""
    end_time = serializers.DateTimeField(required=False, allow_null=True, help_text='结束时间，不传则使用当前时间')
    task_result = serializers.CharField(required=False, allow_blank=True, help_text='任务结果')
    feedback_content = serializers.CharField(required=False, allow_blank=True, help_text='反馈内容')
    feedback_time = serializers.DateTimeField(required=False, allow_null=True, help_text='反馈时间，不传则使用当前时间')

