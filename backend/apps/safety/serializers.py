"""
安全态势展示模块 - 序列化器
"""
import json
import uuid
from rest_framework import serializers
from django.utils import timezone
from apps.users.models import User, Organization
from .models import (
    SafetyResource, SafetyTarget, Shelter, IndustryStatus,
    RegionStatus, MonitorData, WarningEvent, HazardSource, VideoMonitor
)


class SafetyResourceSerializer(serializers.ModelSerializer):
    """安全资源序列化器"""
    resource_type_display = serializers.CharField(source='get_resource_type_display', read_only=True)
    organization_name = serializers.SerializerMethodField()
    equipment_info_dict = serializers.SerializerMethodField()

    class Meta:
        model = SafetyResource
        fields = [
            'id', 'resource_code', 'resource_name', 'resource_type', 'resource_type_display',
            'sub_type', 'longitude', 'latitude', 'street', 'address', 'organization_id',
            'organization_name', 'contact_person', 'contact_phone', 'capacity',
            'equipment_info', 'equipment_info_dict', 'expert_field', 'expert_level',
            'quantity', 'unit', 'status', 'description', 'remark',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_organization_name(self, obj):
        """获取所属组织名称"""
        if obj.organization_id:
            try:
                org = Organization.objects.get(id=obj.organization_id, deleted_at__isnull=True)
                return org.org_name
            except Organization.DoesNotExist:
                return None
        return None

    def get_equipment_info_dict(self, obj):
        """获取装备信息字典"""
        if obj.equipment_info:
            try:
                return json.loads(obj.equipment_info)
            except (json.JSONDecodeError, TypeError):
                return None
        return None


class SafetyTargetSerializer(serializers.ModelSerializer):
    """防护目标序列化器"""
    target_type_display = serializers.CharField(source='get_target_type_display', read_only=True)
    risk_level_display = serializers.CharField(source='get_risk_level_display', read_only=True)

    class Meta:
        model = SafetyTarget
        fields = [
            'id', 'target_code', 'target_name', 'target_type', 'target_type_display',
            'longitude', 'latitude', 'street', 'address', 'population', 'area',
            'risk_level', 'risk_level_display', 'contact_person', 'contact_phone',
            'description', 'status', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ShelterSerializer(serializers.ModelSerializer):
    """避难场所序列化器"""
    shelter_type_display = serializers.CharField(source='get_shelter_type_display', read_only=True)
    facilities_dict = serializers.SerializerMethodField()

    class Meta:
        model = Shelter
        fields = [
            'id', 'shelter_code', 'shelter_name', 'shelter_type', 'shelter_type_display',
            'longitude', 'latitude', 'street', 'address', 'capacity', 'area',
            'facilities', 'facilities_dict', 'contact_person', 'contact_phone',
            'description', 'status', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_facilities_dict(self, obj):
        """获取设施信息字典"""
        if obj.facilities:
            try:
                return json.loads(obj.facilities)
            except (json.JSONDecodeError, TypeError):
                return None
        return None


class IndustryStatusSerializer(serializers.ModelSerializer):
    """行业态势序列化器"""
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    status_data_dict = serializers.SerializerMethodField()

    class Meta:
        model = IndustryStatus
        fields = [
            'id', 'stat_date', 'industry_type', 'industry_type_display',
            'alarm_count', 'warning_count', 'risk_count',
            'risk_level_1_count', 'risk_level_2_count', 'risk_level_3_count', 'risk_level_4_count',
            'status_data', 'status_data_dict', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_status_data_dict(self, obj):
        """获取详细态势数据字典"""
        if obj.status_data:
            try:
                return json.loads(obj.status_data)
            except (json.JSONDecodeError, TypeError):
                return None
        return None


class RegionStatusSerializer(serializers.ModelSerializer):
    """区域态势序列化器"""
    status_data_dict = serializers.SerializerMethodField()

    class Meta:
        model = RegionStatus
        fields = [
            'id', 'stat_date', 'street', 'alarm_count', 'warning_count', 'risk_count',
            'risk_level_1_count', 'risk_level_2_count', 'risk_level_3_count', 'risk_level_4_count',
            'risk_color', 'status_data', 'status_data_dict', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_status_data_dict(self, obj):
        """获取详细态势数据字典"""
        if obj.status_data:
            try:
                return json.loads(obj.status_data)
            except (json.JSONDecodeError, TypeError):
                return None
        return None


class MonitorDataSerializer(serializers.ModelSerializer):
    """监测数据序列化器"""
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    online_status_display = serializers.SerializerMethodField()
    monitor_name = serializers.SerializerMethodField()

    class Meta:
        model = MonitorData
        fields = [
            'id', 'monitor_id', 'monitor_name', 'industry_type', 'industry_type_display',
            'data_time', 'monitor_value', 'monitor_unit', 'online_status',
            'online_status_display', 'data_source', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_online_status_display(self, obj):
        """获取在线状态显示"""
        return '在线' if obj.online_status == 1 else '离线'

    def get_monitor_name(self, obj):
        """获取监测点名称"""
        if obj.monitor_id:
            try:
                from apps.risk.models import RiskMonitor
                monitor = RiskMonitor.objects.get(id=obj.monitor_id, deleted_at__isnull=True)
                return monitor.monitor_name
            except Exception:
                return None
        return None


class WarningEventSerializer(serializers.ModelSerializer):
    """预警事件序列化器"""
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    warning_status_display = serializers.CharField(source='get_warning_status_display', read_only=True)
    warning_detail = serializers.SerializerMethodField()
    warning_level_detail = serializers.SerializerMethodField()

    class Meta:
        model = WarningEvent
        fields = [
            'id', 'warning_id', 'warning_detail', 'warning_code', 'warning_level_id',
            'warning_level_detail', 'industry_type', 'industry_type_display',
            'warning_type', 'warning_title', 'longitude', 'latitude', 'street', 'address',
            'warning_time', 'warning_status', 'warning_status_display',
            'nearby_monitor_count', 'nearby_risk_count', 'nearby_resource_count',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_warning_detail(self, obj):
        """获取预警详情"""
        if obj.warning_id:
            try:
                from apps.risk.models import RiskWarning
                warning = RiskWarning.objects.get(id=obj.warning_id, deleted_at__isnull=True)
                return {
                    'id': warning.id,
                    'warning_code': warning.warning_code,
                    'warning_title': warning.warning_title,
                    'warning_level': warning.warning_level_id
                }
            except Exception:
                return None
        return None

    def get_warning_level_detail(self, obj):
        """获取预警级别详情"""
        if obj.warning_level_id:
            try:
                from apps.risk.models import WarningLevel
                level = WarningLevel.objects.get(id=obj.warning_level_id, deleted_at__isnull=True)
                return {
                    'id': level.id,
                    'level_code': level.level_code,
                    'level_name': level.level_name,
                    'level_color': level.level_color
                }
            except Exception:
                return None
        return None


class HazardSourceSerializer(serializers.ModelSerializer):
    """危险源序列化器"""
    source_type_display = serializers.CharField(source='get_source_type_display', read_only=True)
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    risk_level_display = serializers.CharField(source='get_risk_level_display', read_only=True)
    organization_name = serializers.SerializerMethodField()
    emergency_plan_name = serializers.SerializerMethodField()

    class Meta:
        model = HazardSource
        fields = [
            'id', 'source_code', 'source_name', 'source_type', 'source_type_display',
            'industry_type', 'industry_type_display', 'organization_id', 'organization_name',
            'longitude', 'latitude', 'street', 'address', 'risk_level', 'risk_level_display',
            'material_type', 'material_quantity', 'material_unit', 'safety_measures',
            'emergency_plan_id', 'emergency_plan_name', 'contact_person', 'contact_phone',
            'description', 'status', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_organization_name(self, obj):
        """获取所属企业名称"""
        if obj.organization_id:
            try:
                org = Organization.objects.get(id=obj.organization_id, deleted_at__isnull=True)
                return org.org_name
            except Organization.DoesNotExist:
                return None
        return None

    def get_emergency_plan_name(self, obj):
        """获取关联应急预案名称"""
        if obj.emergency_plan_id:
            try:
                from apps.plan.models import EmergencyPlan
                plan = EmergencyPlan.objects.get(id=obj.emergency_plan_id, deleted_at__isnull=True)
                return plan.plan_name
            except Exception:
                return None
        return None


class VideoMonitorSerializer(serializers.ModelSerializer):
    """视频监控设施序列化器"""
    monitor_type_display = serializers.CharField(source='get_monitor_type_display', read_only=True)
    industry_type_display = serializers.CharField(source='get_industry_type_display', read_only=True)
    online_status_display = serializers.SerializerMethodField()
    organization_name = serializers.SerializerMethodField()

    class Meta:
        model = VideoMonitor
        fields = [
            'id', 'monitor_code', 'monitor_name', 'monitor_type', 'monitor_type_display',
            'industry_type', 'industry_type_display', 'longitude', 'latitude',
            'street', 'address', 'video_url', 'rtsp_url', 'coverage_radius',
            'camera_angle', 'online_status', 'online_status_display',
            'organization_id', 'organization_name', 'description', 'status',
            'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_online_status_display(self, obj):
        """获取在线状态显示"""
        return '在线' if obj.online_status == 1 else '离线'

    def get_organization_name(self, obj):
        """获取所属组织名称"""
        if obj.organization_id:
            try:
                org = Organization.objects.get(id=obj.organization_id, deleted_at__isnull=True)
                return org.org_name
            except Organization.DoesNotExist:
                return None
        return None

