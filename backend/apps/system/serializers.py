"""
系统管理模块 - 序列化器
"""
import json
import uuid
from rest_framework import serializers
from django.utils import timezone
from .models import DataSource, MessageTemplate


class DataSourceSerializer(serializers.ModelSerializer):
    """数据源序列化器"""
    source_type_display = serializers.CharField(source='get_source_type_display', read_only=True)
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    api_params_dict = serializers.SerializerMethodField()

    class Meta:
        model = DataSource
        fields = [
            'id', 'source_code', 'source_name', 'source_type', 'source_type_display',
            'industry_type', 'industry_type_display', 'api_url', 'api_method',
            'api_params', 'api_params_dict', 'db_host', 'db_port', 'db_name',
            'db_user', 'db_password', 'db_table', 'sync_interval', 'last_sync_at',
            'status', 'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'last_sync_at', 'created_at', 'updated_at']
        extra_kwargs = {
            'db_password': {'write_only': True}  # 密码字段只写不读
        }

    def get_api_params_dict(self, obj):
        """获取API请求参数字典"""
        if obj.api_params:
            try:
                return json.loads(obj.api_params)
            except (json.JSONDecodeError, TypeError):
                return None
        return None


class MessageTemplateSerializer(serializers.ModelSerializer):
    """消息模板序列化器"""
    template_type_display = serializers.CharField(source='get_template_type_display', read_only=True)
    message_type_display = serializers.CharField(source='get_message_type_display', read_only=True)
    variables_dict = serializers.SerializerMethodField()

    class Meta:
        model = MessageTemplate
        fields = [
            'id', 'template_code', 'template_name', 'template_type', 'template_type_display',
            'message_type', 'message_type_display', 'subject', 'content', 'variables',
            'variables_dict', 'status', 'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_variables_dict(self, obj):
        """获取变量说明字典"""
        if obj.variables:
            try:
                return json.loads(obj.variables)
            except (json.JSONDecodeError, TypeError):
                return None
        return None

