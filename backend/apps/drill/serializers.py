"""
演练监督模块 - 序列化器
"""
import json
import uuid
from rest_framework import serializers
from django.utils import timezone
from apps.users.models import User, Organization
from .models import DrillEvent, DrillEvaluation, DrillSummary, DrillAnalysis


class DrillEventSerializer(serializers.ModelSerializer):
    """演练事件序列化器"""
    event_type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    drill_status_display = serializers.CharField(source='get_drill_status_display', read_only=True)
    data_source_display = serializers.CharField(source='get_data_source_display', read_only=True)
    organization_name = serializers.SerializerMethodField()
    related_plan_name = serializers.SerializerMethodField()

    class Meta:
        model = DrillEvent
        fields = [
            'id', 'event_code', 'event_name', 'organization_id', 'organization_name',
            'drill_plan_name', 'drill_plan_id', 'event_type', 'event_type_display',
            'accident_type', 'longitude', 'latitude', 'street', 'address',
            'event_time', 'injured_count', 'death_count', 'accident_summary',
            'related_plan_id', 'related_plan_name', 'drill_status', 'drill_status_display',
            'data_source', 'data_source_display', 'external_id', 'description',
            'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_organization_name(self, obj):
        """获取事发单位名称"""
        if obj.organization_id:
            try:
                org = Organization.objects.get(id=obj.organization_id, deleted_at__isnull=True)
                return org.org_name
            except Organization.DoesNotExist:
                return None
        return None

    def get_related_plan_name(self, obj):
        """获取关联预案名称"""
        if obj.related_plan_id:
            try:
                from apps.plan.models import EmergencyPlan
                plan = EmergencyPlan.objects.get(id=obj.related_plan_id, deleted_at__isnull=True)
                return plan.plan_name
            except Exception:
                return None
        return None


class DrillEventUpdateStatusSerializer(serializers.Serializer):
    """演练事件状态更新序列化器"""
    drill_status = serializers.ChoiceField(choices=DrillEvent.DRILL_STATUS_CHOICES, required=True, help_text='演练状态')


class DrillEvaluationSerializer(serializers.ModelSerializer):
    """演练评价序列化器"""
    node_type_display = serializers.CharField(source='get_node_type_display', read_only=True)
    evaluation_level_display = serializers.CharField(source='get_evaluation_level_display', read_only=True)
    event_detail = serializers.SerializerMethodField()
    evaluator_name = serializers.SerializerMethodField()

    class Meta:
        model = DrillEvaluation
        fields = [
            'id', 'event_id', 'event_detail', 'node_name', 'node_type', 'node_type_display',
            'evaluation_item', 'evaluation_content', 'evaluation_score', 'evaluation_level',
            'evaluation_level_display', 'evaluator_id', 'evaluator_name', 'evaluation_time',
            'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'evaluation_time', 'created_at', 'updated_at']

    def get_event_detail(self, obj):
        """获取演练事件详情"""
        if obj.event_id:
            try:
                event = DrillEvent.objects.get(id=obj.event_id, deleted_at__isnull=True)
                return {
                    'id': event.id,
                    'event_code': event.event_code,
                    'event_name': event.event_name,
                    'drill_status': event.drill_status
                }
            except DrillEvent.DoesNotExist:
                return None
        return None

    def get_evaluator_name(self, obj):
        """获取评价人姓名"""
        if obj.evaluator_id:
            try:
                user = User.objects.get(id=obj.evaluator_id, deleted_at__isnull=True)
                return user.username
            except User.DoesNotExist:
                return None
        return None


class DrillSummarySerializer(serializers.ModelSerializer):
    """演练总结序列化器"""
    communication_status_display = serializers.SerializerMethodField()
    plan_familiarity_display = serializers.SerializerMethodField()
    plan_operability_display = serializers.SerializerMethodField()
    duty_clarity_display = serializers.SerializerMethodField()
    command_science_display = serializers.SerializerMethodField()
    disposal_appropriateness_display = serializers.SerializerMethodField()
    overall_level_display = serializers.CharField(source='get_overall_level_display', read_only=True)
    event_detail = serializers.SerializerMethodField()
    summary_user_name = serializers.SerializerMethodField()

    class Meta:
        model = DrillSummary
        fields = [
            'id', 'event_id', 'event_detail', 'summary_title',
            'communication_status', 'communication_status_display', 'communication_comment',
            'plan_familiarity', 'plan_familiarity_display', 'plan_familiarity_comment',
            'plan_operability', 'plan_operability_display', 'plan_operability_comment',
            'duty_clarity', 'duty_clarity_display', 'duty_clarity_comment',
            'command_science', 'command_science_display', 'command_science_comment',
            'disposal_appropriateness', 'disposal_appropriateness_display', 'disposal_appropriateness_comment',
            'problems_analysis', 'improvement_suggestions', 'overall_score', 'overall_level',
            'overall_level_display', 'enterprise_summary', 'supervisor_opinion',
            'summary_user_id', 'summary_user_name', 'summary_time', 'description',
            'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'summary_time', 'created_at', 'updated_at']

    def get_communication_status_display(self, obj):
        """获取内部沟通状态显示"""
        if obj.communication_status:
            choices = dict(DrillSummary.STATUS_CHOICES)
            return choices.get(obj.communication_status, '')
        return None

    def get_plan_familiarity_display(self, obj):
        """获取预案熟悉程度显示"""
        if obj.plan_familiarity:
            choices = dict(DrillSummary.STATUS_CHOICES)
            return choices.get(obj.plan_familiarity, '')
        return None

    def get_plan_operability_display(self, obj):
        """获取预案可操作性显示"""
        if obj.plan_operability:
            choices = dict(DrillSummary.STATUS_CHOICES)
            return choices.get(obj.plan_operability, '')
        return None

    def get_duty_clarity_display(self, obj):
        """获取职责定位显示"""
        if obj.duty_clarity:
            choices = dict(DrillSummary.STATUS_CHOICES)
            return choices.get(obj.duty_clarity, '')
        return None

    def get_command_science_display(self, obj):
        """获取应急指挥显示"""
        if obj.command_science:
            choices = dict(DrillSummary.STATUS_CHOICES)
            return choices.get(obj.command_science, '')
        return None

    def get_disposal_appropriateness_display(self, obj):
        """获取应急处置显示"""
        if obj.disposal_appropriateness:
            choices = dict(DrillSummary.STATUS_CHOICES)
            return choices.get(obj.disposal_appropriateness, '')
        return None

    def get_event_detail(self, obj):
        """获取演练事件详情"""
        if obj.event_id:
            try:
                event = DrillEvent.objects.get(id=obj.event_id, deleted_at__isnull=True)
                return {
                    'id': event.id,
                    'event_code': event.event_code,
                    'event_name': event.event_name,
                    'drill_status': event.drill_status
                }
            except DrillEvent.DoesNotExist:
                return None
        return None

    def get_summary_user_name(self, obj):
        """获取总结人姓名"""
        if obj.summary_user_id:
            try:
                user = User.objects.get(id=obj.summary_user_id, deleted_at__isnull=True)
                return user.username
            except User.DoesNotExist:
                return None
        return None


class DrillAnalysisSerializer(serializers.ModelSerializer):
    """演练分析序列化器"""
    stat_type_display = serializers.CharField(source='get_stat_type_display', read_only=True)
    drill_type_display = serializers.CharField(source='get_drill_type_display', read_only=True)
    organization_name = serializers.SerializerMethodField()
    analysis_data_dict = serializers.SerializerMethodField()

    class Meta:
        model = DrillAnalysis
        fields = [
            'id', 'stat_date', 'stat_type', 'stat_type_display', 'organization_id',
            'organization_name', 'drill_type', 'drill_type_display', 'accident_type',
            'drill_count', 'completed_count', 'excellent_count', 'good_count',
            'qualified_count', 'unqualified_count', 'avg_score', 'analysis_data',
            'analysis_data_dict', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_organization_name(self, obj):
        """获取演练单位名称"""
        if obj.organization_id:
            try:
                org = Organization.objects.get(id=obj.organization_id, deleted_at__isnull=True)
                return org.org_name
            except Organization.DoesNotExist:
                return None
        return None

    def get_analysis_data_dict(self, obj):
        """获取详细分析数据字典"""
        if obj.analysis_data:
            try:
                return json.loads(obj.analysis_data)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

