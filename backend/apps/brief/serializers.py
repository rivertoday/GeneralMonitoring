"""
简报模块 - 序列化器
"""
import json
from rest_framework import serializers
from django.utils import timezone
from .models import BriefTemplate, BriefStrategy, BriefData, BriefPush


class BriefTemplateSerializer(serializers.ModelSerializer):
    """简报模板序列化器"""
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True)
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    region_dimension_dict = serializers.SerializerMethodField()
    industry_dimension_dict = serializers.SerializerMethodField()
    variables_dict = serializers.SerializerMethodField()
    data_config_dict = serializers.SerializerMethodField()

    class Meta:
        model = BriefTemplate
        fields = [
            'id', 'template_code', 'template_name', 'template_type', 'template_type_display',
            'industry_type', 'industry_type_display', 'time_dimension', 'region_dimension',
            'region_dimension_dict', 'industry_dimension', 'industry_dimension_dict',
            'template_content', 'variables', 'variables_dict', 'data_config', 'data_config_dict',
            'status', 'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_region_dimension_dict(self, obj):
        """将region_dimension从JSON字符串转换为字典"""
        if obj.region_dimension:
            try:
                return json.loads(obj.region_dimension)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_industry_dimension_dict(self, obj):
        """将industry_dimension从JSON字符串转换为字典"""
        if obj.industry_dimension:
            try:
                return json.loads(obj.industry_dimension)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_variables_dict(self, obj):
        """将variables从JSON字符串转换为字典"""
        if obj.variables:
            try:
                return json.loads(obj.variables)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_data_config_dict(self, obj):
        """将data_config从JSON字符串转换为字典"""
        if obj.data_config:
            try:
                return json.loads(obj.data_config)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def validate_region_dimension(self, value):
        """验证region_dimension是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('region_dimension必须是有效的JSON格式')
        return value

    def validate_industry_dimension(self, value):
        """验证industry_dimension是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('industry_dimension必须是有效的JSON格式')
        return value

    def validate_variables(self, value):
        """验证variables是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('variables必须是有效的JSON格式')
        return value

    def validate_data_config(self, value):
        """验证data_config是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('data_config必须是有效的JSON格式')
        return value


class BriefStrategySerializer(serializers.ModelSerializer):
    """简报策略序列化器"""
    template_detail = serializers.SerializerMethodField()
    template_id = serializers.IntegerField(write_only=True, required=True)
    strategy_type_display = serializers.CharField(source='get_strategy_type_display', read_only=True)
    trigger_type_display = serializers.CharField(source='get_trigger_type_display', read_only=True)
    push_target_type_display = serializers.CharField(source='get_push_target_type_display', read_only=True)
    trigger_config_dict = serializers.SerializerMethodField()
    warning_type_filter_list = serializers.SerializerMethodField()
    warning_level_filter_list = serializers.SerializerMethodField()
    industry_filter_list = serializers.SerializerMethodField()
    region_filter_list = serializers.SerializerMethodField()
    push_target_ids_list = serializers.SerializerMethodField()
    push_channel_list = serializers.SerializerMethodField()

    class Meta:
        model = BriefStrategy
        fields = [
            'id', 'strategy_code', 'strategy_name', 'template_id', 'template_detail',
            'strategy_type', 'strategy_type_display', 'report_type', 'trigger_type',
            'trigger_type_display', 'trigger_config', 'trigger_config_dict',
            'warning_type_filter', 'warning_type_filter_list', 'warning_level_filter',
            'warning_level_filter_list', 'industry_filter', 'industry_filter_list',
            'region_filter', 'region_filter_list', 'push_target_type', 'push_target_type_display',
            'push_target_ids', 'push_target_ids_list', 'push_channel', 'push_channel_list',
            'message_template_id', 'status', 'last_execute_at', 'next_execute_at',
            'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_execute_at', 'next_execute_at']

    def get_trigger_config_dict(self, obj):
        """将trigger_config从JSON字符串转换为字典"""
        if obj.trigger_config:
            try:
                return json.loads(obj.trigger_config)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_warning_type_filter_list(self, obj):
        """将warning_type_filter从JSON字符串转换为列表"""
        if obj.warning_type_filter:
            try:
                return json.loads(obj.warning_type_filter)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_warning_level_filter_list(self, obj):
        """将warning_level_filter从JSON字符串转换为列表"""
        if obj.warning_level_filter:
            try:
                return json.loads(obj.warning_level_filter)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_industry_filter_list(self, obj):
        """将industry_filter从JSON字符串转换为列表"""
        if obj.industry_filter:
            try:
                return json.loads(obj.industry_filter)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_region_filter_list(self, obj):
        """将region_filter从JSON字符串转换为列表"""
        if obj.region_filter:
            try:
                return json.loads(obj.region_filter)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_push_target_ids_list(self, obj):
        """将push_target_ids从JSON字符串转换为列表"""
        if obj.push_target_ids:
            try:
                return json.loads(obj.push_target_ids)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_push_channel_list(self, obj):
        """将push_channel从JSON字符串转换为列表"""
        if obj.push_channel:
            try:
                return json.loads(obj.push_channel)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_template_detail(self, obj):
        """获取模板详情"""
        if obj.template_id:
            try:
                template = BriefTemplate.objects.get(id=obj.template_id, deleted_at__isnull=True)
                return BriefTemplateSerializer(template).data
            except BriefTemplate.DoesNotExist:
                return None
        return None

    def validate_trigger_config(self, value):
        """验证trigger_config是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('trigger_config必须是有效的JSON格式')
        return value

    def validate_warning_type_filter(self, value):
        """验证warning_type_filter是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('warning_type_filter必须是有效的JSON格式')
        return value

    def validate_warning_level_filter(self, value):
        """验证warning_level_filter是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('warning_level_filter必须是有效的JSON格式')
        return value

    def validate_industry_filter(self, value):
        """验证industry_filter是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('industry_filter必须是有效的JSON格式')
        return value

    def validate_region_filter(self, value):
        """验证region_filter是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('region_filter必须是有效的JSON格式')
        return value

    def validate_push_target_ids(self, value):
        """验证push_target_ids是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('push_target_ids必须是有效的JSON格式')
        return value

    def validate_push_channel(self, value):
        """验证push_channel是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('push_channel必须是有效的JSON格式')
        return value


class BriefDataSerializer(serializers.ModelSerializer):
    """简报数据序列化器"""
    template_detail = serializers.SerializerMethodField()
    template_id = serializers.IntegerField(write_only=True, required=True)
    strategy_detail = serializers.SerializerMethodField()
    strategy_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    brief_type_display = serializers.CharField(source='get_brief_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    data_summary_dict = serializers.SerializerMethodField()
    industry_data_dict = serializers.SerializerMethodField()
    region_data_dict = serializers.SerializerMethodField()
    time_data_dict = serializers.SerializerMethodField()

    class Meta:
        model = BriefData
        fields = [
            'id', 'brief_code', 'template_id', 'template_detail', 'strategy_id', 'strategy_detail',
            'brief_type', 'brief_type_display', 'report_type', 'report_date', 'report_period_start',
            'report_period_end', 'brief_title', 'brief_content', 'data_summary', 'data_summary_dict',
            'alarm_count', 'warning_count', 'risk_count', 'industry_data', 'industry_data_dict',
            'region_data', 'region_data_dict', 'time_data', 'time_data_dict', 'attachment_url',
            'status', 'status_display', 'generate_user_id', 'generate_time', 'description',
            'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'generate_time']

    def get_data_summary_dict(self, obj):
        """将data_summary从JSON字符串转换为字典"""
        if obj.data_summary:
            try:
                return json.loads(obj.data_summary)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_industry_data_dict(self, obj):
        """将industry_data从JSON字符串转换为字典"""
        if obj.industry_data:
            try:
                return json.loads(obj.industry_data)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_region_data_dict(self, obj):
        """将region_data从JSON字符串转换为字典"""
        if obj.region_data:
            try:
                return json.loads(obj.region_data)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def get_time_data_dict(self, obj):
        """将time_data从JSON字符串转换为字典"""
        if obj.time_data:
            try:
                return json.loads(obj.time_data)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

    def validate_data_summary(self, value):
        """验证data_summary是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('data_summary必须是有效的JSON格式')
        return value

    def validate_industry_data(self, value):
        """验证industry_data是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('industry_data必须是有效的JSON格式')
        return value

    def validate_region_data(self, value):
        """验证region_data是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('region_data必须是有效的JSON格式')
        return value

    def validate_time_data(self, value):
        """验证time_data是否为有效的JSON格式"""
        if value:
            try:
                json.loads(value)
            except json.JSONDecodeError:
                raise serializers.ValidationError('time_data必须是有效的JSON格式')
        return value

    def get_template_detail(self, obj):
        """获取模板详情"""
        if obj.template_id:
            try:
                template = BriefTemplate.objects.get(id=obj.template_id, deleted_at__isnull=True)
                return BriefTemplateSerializer(template).data
            except BriefTemplate.DoesNotExist:
                return None
        return None

    def get_strategy_detail(self, obj):
        """获取策略详情"""
        if obj.strategy_id:
            try:
                strategy = BriefStrategy.objects.get(id=obj.strategy_id, deleted_at__isnull=True)
                return BriefStrategySerializer(strategy).data
            except BriefStrategy.DoesNotExist:
                return None
        return None


class BriefDataGenerateSerializer(serializers.Serializer):
    """简报生成序列化器"""
    template_id = serializers.IntegerField(required=True, help_text='模板ID')
    strategy_id = serializers.IntegerField(required=False, allow_null=True, help_text='策略ID（可选）')
    report_date = serializers.DateField(required=True, help_text='报告日期')
    report_period_start = serializers.DateTimeField(required=False, allow_null=True, help_text='报告周期开始时间')
    report_period_end = serializers.DateTimeField(required=False, allow_null=True, help_text='报告周期结束时间')


class BriefPushSerializer(serializers.ModelSerializer):
    """简报推送记录序列化器"""
    brief_detail = serializers.SerializerMethodField()
    brief_id = serializers.IntegerField(write_only=True, required=True)
    push_target_type_display = serializers.CharField(source='get_push_target_type_display', read_only=True)
    push_channel_display = serializers.CharField(source='get_push_channel_display', read_only=True)
    push_status_display = serializers.CharField(source='get_push_status_display', read_only=True)
    read_status_display = serializers.CharField(source='get_read_status_display', read_only=True)

    class Meta:
        model = BriefPush
        fields = [
            'id', 'brief_id', 'brief_detail', 'push_target_type', 'push_target_type_display',
            'target_id', 'push_channel', 'push_channel_display', 'push_status', 'push_status_display',
            'push_time', 'read_status', 'read_status_display', 'read_time', 'error_message',
            'message_id', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'push_time']

    def get_brief_detail(self, obj):
        """获取简报详情"""
        if obj.brief_id:
            try:
                brief = BriefData.objects.get(id=obj.brief_id, deleted_at__isnull=True)
                return BriefDataSerializer(brief).data
            except BriefData.DoesNotExist:
                return None
        return None


class BriefPushCreateSerializer(serializers.Serializer):
    """简报推送创建序列化器"""
    brief_id = serializers.IntegerField(required=True, help_text='简报ID')
    push_target_type = serializers.IntegerField(required=True, help_text='推送目标类型: 1-用户, 2-角色, 3-组织')
    target_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        help_text='目标ID列表（用户ID、角色ID或组织ID）'
    )
    push_channel = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        help_text='推送渠道列表: system-系统消息, sms-短信, email-邮件'
    )

    def validate_push_target_type(self, value):
        """验证推送目标类型"""
        if value not in [1, 2, 3]:
            raise serializers.ValidationError('推送目标类型必须为1、2或3')
        return value

    def validate_push_channel(self, value):
        """验证推送渠道"""
        valid_channels = ['system', 'sms', 'email']
        for channel in value:
            if channel not in valid_channels:
                raise serializers.ValidationError(f'推送渠道必须为: {", ".join(valid_channels)}')
        return value


class BriefPushReadSerializer(serializers.Serializer):
    """简报标记已读序列化器"""
    push_id = serializers.IntegerField(required=True, help_text='推送记录ID')
