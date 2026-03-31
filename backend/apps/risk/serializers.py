"""
风险监测预警模块 - 序列化器
"""
import json
from rest_framework import serializers
from django.utils import timezone
from .models import (
    WarningLevel, WarningRule, RiskMonitor, AlarmRecord,
    RiskWarning, AlarmStatistics, RiskHiddenDanger, RiskRectification
)


class WarningLevelSerializer(serializers.ModelSerializer):
    """预警级别序列化器"""
    level_color_display = serializers.CharField(source='get_level_color_display', read_only=True)

    class Meta:
        model = WarningLevel
        fields = [
            'id', 'level_code', 'level_name', 'level_color', 'level_color_display',
            'severity', 'response_org', 'response_time', 'description', 'status',
            'sort_order', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WarningRuleSerializer(serializers.ModelSerializer):
    """预警规则序列化器"""
    warning_level_detail = WarningLevelSerializer(source='warning_level', read_only=True)
    warning_level_id = serializers.PrimaryKeyRelatedField(
        queryset=WarningLevel.objects.filter(deleted_at__isnull=True),
        source='warning_level',
        write_only=True,
        required=False,
        allow_null=True
    )
    rule_type_display = serializers.CharField(source='get_rule_type_display', read_only=True)
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    condition_config_dict = serializers.SerializerMethodField()
    action_config_dict = serializers.SerializerMethodField()

    class Meta:
        model = WarningRule
        fields = [
            'id', 'rule_code', 'rule_name', 'rule_type', 'rule_type_display',
            'industry_type', 'industry_type_display', 'warning_level',
            'warning_level_id', 'warning_level_detail', 'condition_config',
            'condition_config_dict', 'action_config', 'action_config_dict',
            'response_time', 'handle_time', 'feedback_time', 'status',
            'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_condition_config_dict(self, obj):
        """将condition_config从JSON字符串转换为字典"""
        if obj.condition_config:
            try:
                return json.loads(obj.condition_config)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_action_config_dict(self, obj):
        """将action_config从JSON字符串转换为字典"""
        if obj.action_config:
            try:
                return json.loads(obj.action_config)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def validate_condition_config(self, value):
        """验证condition_config是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('condition_config必须是有效的JSON格式')
        return value

    def validate_action_config(self, value):
        """验证action_config是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('action_config必须是有效的JSON格式')
        return value


class RiskMonitorSerializer(serializers.ModelSerializer):
    """风险监测点序列化器"""
    monitor_type_display = serializers.CharField(source='get_monitor_type_display', read_only=True)
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    online_status_display = serializers.SerializerMethodField()

    class Meta:
        model = RiskMonitor
        fields = [
            'id', 'monitor_code', 'monitor_name', 'monitor_type', 'monitor_type_display',
            'industry_type', 'industry_type_display', 'data_source_id', 'location',
            'longitude', 'latitude', 'street', 'address', 'monitor_value', 'monitor_unit',
            'threshold_min', 'threshold_max', 'online_status', 'online_status_display',
            'last_data_time', 'status', 'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_online_status_display(self, obj):
        """获取在线状态显示"""
        return '在线' if obj.online_status == 1 else '离线'


class AlarmRecordSerializer(serializers.ModelSerializer):
    """报警记录序列化器"""
    monitor_detail = RiskMonitorSerializer(source='monitor', read_only=True)
    monitor_id = serializers.PrimaryKeyRelatedField(
        queryset=RiskMonitor.objects.filter(deleted_at__isnull=True),
        source='monitor',
        write_only=True
    )
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    alarm_status_display = serializers.CharField(source='get_alarm_status_display', read_only=True)

    class Meta:
        model = AlarmRecord
        fields = [
            'id', 'alarm_code', 'monitor', 'monitor_id', 'monitor_detail',
            'industry_type', 'industry_type_display', 'alarm_type', 'alarm_value',
            'threshold_value', 'location', 'longitude', 'latitude', 'street', 'address',
            'alarm_time', 'alarm_duration', 'alarm_status', 'alarm_status_display',
            'handle_user_id', 'handle_time', 'handle_result', 'feedback_time',
            'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AlarmRecordHandleSerializer(serializers.Serializer):
    """报警处理序列化器"""
    handle_result = serializers.CharField(required=True, help_text='处理结果')
    alarm_status = serializers.IntegerField(required=True, help_text='报警状态: 0-未处理, 1-处理中, 2-已处理, 3-已忽略')

    def validate_alarm_status(self, value):
        """验证报警状态值"""
        if value not in [0, 1, 2, 3]:
            raise serializers.ValidationError('报警状态值必须为0、1、2或3')
        return value


class RiskWarningSerializer(serializers.ModelSerializer):
    """风险预警序列化器"""
    warning_level_detail = WarningLevelSerializer(source='warning_level', read_only=True)
    warning_level_id = serializers.PrimaryKeyRelatedField(
        queryset=WarningLevel.objects.filter(deleted_at__isnull=True),
        source='warning_level',
        write_only=True
    )
    warning_rule_detail = WarningRuleSerializer(source='warning_rule', read_only=True)
    warning_rule_id = serializers.PrimaryKeyRelatedField(
        queryset=WarningRule.objects.filter(deleted_at__isnull=True),
        source='warning_rule',
        write_only=True,
        required=False,
        allow_null=True
    )
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    warning_analysis_type_display = serializers.CharField(source='get_warning_analysis_type_display', read_only=True)
    warning_source_display = serializers.CharField(source='get_warning_source_display', read_only=True)
    warning_status_display = serializers.CharField(source='get_warning_status_display', read_only=True)

    class Meta:
        model = RiskWarning
        fields = [
            'id', 'warning_code', 'warning_level', 'warning_level_id', 'warning_level_detail',
            'warning_rule', 'warning_rule_id', 'warning_rule_detail', 'industry_type',
            'industry_type_display', 'warning_type', 'warning_analysis_type',
            'warning_analysis_type_display', 'warning_title', 'warning_content',
            'location', 'longitude', 'latitude', 'street', 'address', 'warning_time',
            'warning_source', 'warning_source_display', 'warning_status', 'warning_status_display',
            'response_org_id', 'response_user_id', 'response_time', 'handle_time',
            'handle_result', 'feedback_time', 'publish_time', 'related_plan_id',
            'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RiskWarningPublishSerializer(serializers.Serializer):
    """风险预警发布序列化器"""
    publish_time = serializers.DateTimeField(required=False, help_text='发布时间，不填则使用当前时间')

    def validate_publish_time(self, value):
        """验证发布时间"""
        if value and value > timezone.now():
            raise serializers.ValidationError('发布时间不能晚于当前时间')
        return value


class RiskWarningHandleSerializer(serializers.Serializer):
    """风险预警处置序列化器"""
    handle_result = serializers.CharField(required=True, help_text='处置结果')
    warning_status = serializers.IntegerField(required=True, help_text='预警状态: 2-处理中, 3-已处置, 4-已关闭')

    def validate_warning_status(self, value):
        """验证预警状态值"""
        if value not in [2, 3, 4]:
            raise serializers.ValidationError('预警状态值必须为2、3或4')
        return value


class AlarmStatisticsSerializer(serializers.ModelSerializer):
    """报警统计序列化器"""
    stat_type_display = serializers.CharField(source='get_stat_type_display', read_only=True)
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    stat_data_dict = serializers.SerializerMethodField()

    class Meta:
        model = AlarmStatistics
        fields = [
            'id', 'stat_date', 'stat_type', 'stat_type_display', 'industry_type',
            'industry_type_display', 'street', 'alarm_count', 'unhandled_count',
            'handling_count', 'handled_count', 'ignored_count', 'avg_handle_time',
            'stat_data', 'stat_data_dict', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_stat_data_dict(self, obj):
        """将stat_data从JSON字符串转换为字典"""
        if obj.stat_data:
            try:
                return json.loads(obj.stat_data)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def validate_stat_data(self, value):
        """验证stat_data是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('stat_data必须是有效的JSON格式')
        return value


class RiskHiddenDangerSerializer(serializers.ModelSerializer):
    """隐患排查序列化器"""
    monitor_detail = RiskMonitorSerializer(source='monitor', read_only=True)
    monitor_id = serializers.PrimaryKeyRelatedField(
        queryset=RiskMonitor.objects.filter(deleted_at__isnull=True),
        source='monitor',
        write_only=True
    )
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    danger_level_display = serializers.CharField(source='get_danger_level_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = RiskHiddenDanger
        fields = [
            'id', 'danger_code', 'danger_name', 'monitor', 'monitor_id', 'monitor_detail',
            'organization_id', 'industry_type', 'industry_type_display', 'location',
            'longitude', 'latitude', 'street', 'address', 'danger_level', 'danger_level_display',
            'danger_category', 'danger_description', 'discover_time', 'discover_user_id',
            'status', 'status_display', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RiskRectificationSerializer(serializers.ModelSerializer):
    """隐患整改序列化器"""
    danger_detail = RiskHiddenDangerSerializer(source='danger', read_only=True)
    danger_id = serializers.PrimaryKeyRelatedField(
        queryset=RiskHiddenDanger.objects.filter(deleted_at__isnull=True),
        source='danger',
        write_only=True
    )
    rectification_status_display = serializers.CharField(source='get_rectification_status_display', read_only=True)
    verification_status_display = serializers.CharField(source='get_verification_status_display', read_only=True)

    class Meta:
        model = RiskRectification
        fields = [
            'id', 'rectification_code', 'danger', 'danger_id', 'danger_detail',
            'rectification_plan', 'rectification_measures', 'responsible_user_id',
            'responsible_org_id', 'plan_start_time', 'plan_end_time', 'actual_start_time',
            'actual_end_time', 'rectification_status', 'rectification_status_display',
            'rectification_result', 'verification_status', 'verification_status_display',
            'verification_time', 'verification_user_id', 'verification_opinion',
            'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RiskRectificationVerifySerializer(serializers.Serializer):
    """隐患整改验收序列化器"""
    verification_opinion = serializers.CharField(required=True, help_text='验收意见')
    verification_status = serializers.IntegerField(required=True, help_text='验收状态: 1-验收通过, 2-验收不通过')

    def validate_verification_status(self, value):
        """验证验收状态值"""
        if value not in [1, 2]:
            raise serializers.ValidationError('验收状态值必须为1或2')
        return value
