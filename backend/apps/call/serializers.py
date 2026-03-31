"""
叫应模块 - 序列化器
"""
from rest_framework import serializers
from django.utils import timezone
from .models import (
    CallGroup, CallTarget, CallPerson, PolicyFile,
    PolicyDistribution, CallRecord
)


class CallGroupSerializer(serializers.ModelSerializer):
    """叫应分组序列化器"""
    group_type_display = serializers.CharField(source='get_group_type_display', read_only=True)
    event_level_display = serializers.SerializerMethodField()

    class Meta:
        model = CallGroup
        fields = [
            'id', 'group_code', 'group_name', 'group_type', 'group_type_display',
            'event_level', 'event_level_display', 'description', 'status',
            'sort_order', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_event_level_display(self, obj):
        """获取事件级别显示文本"""
        if obj.event_level:
            level_map = {
                1: '红色I级',
                2: '橙色Ⅱ级',
                3: '黄色Ⅲ级',
                4: '蓝色Ⅳ级',
            }
            return level_map.get(obj.event_level, '')
        return None


class CallTargetSerializer(serializers.ModelSerializer):
    """叫应对象序列化器"""
    target_type_display = serializers.CharField(source='get_target_type_display', read_only=True)

    class Meta:
        model = CallTarget
        fields = [
            'id', 'target_code', 'target_name', 'target_type', 'target_type_display',
            'organization_id', 'enterprise_name', 'enterprise_info', 'safety_person',
            'contact_phone', 'contact_address', 'description', 'status',
            'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CallPersonSerializer(serializers.ModelSerializer):
    """叫应人员序列化器"""
    group_name = serializers.SerializerMethodField()
    event_level_display = serializers.SerializerMethodField()

    class Meta:
        model = CallPerson
        fields = [
            'id', 'person_code', 'person_name', 'group_id', 'group_name',
            'rank', 'mobile_phone', 'office_phone', 'contact_address',
            'event_level', 'event_level_display', 'organization_id',
            'description', 'status', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_group_name(self, obj):
        """获取分组名称"""
        if obj.group_id:
            try:
                group = CallGroup.objects.get(id=obj.group_id, deleted_at__isnull=True)
                return group.group_name
            except CallGroup.DoesNotExist:
                return None
        return None

    def get_event_level_display(self, obj):
        """获取事件级别显示文本"""
        if obj.event_level:
            level_map = {
                1: '红色I级',
                2: '橙色Ⅱ级',
                3: '黄色Ⅲ级',
                4: '蓝色Ⅳ级',
            }
            return level_map.get(obj.event_level, '')
        return None


class PolicyFileSerializer(serializers.ModelSerializer):
    """政策文件序列化器"""
    publish_status_display = serializers.CharField(source='get_publish_status_display', read_only=True)
    upload_user_name = serializers.SerializerMethodField()

    class Meta:
        model = PolicyFile
        fields = [
            'id', 'file_code', 'file_name', 'file_path', 'file_size',
            'file_type', 'file_ext', 'policy_title', 'policy_content',
            'policy_requirement', 'upload_user_id', 'upload_user_name',
            'upload_time', 'publish_status', 'publish_status_display',
            'publish_time', 'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'upload_time', 'created_at', 'updated_at']

    def get_upload_user_name(self, obj):
        """获取上传人姓名"""
        if obj.upload_user_id:
            try:
                from apps.users.models import User
                user = User.objects.get(id=obj.upload_user_id, deleted_at__isnull=True)
                return user.username
            except User.DoesNotExist:
                return None
        return None


class PolicyFilePublishSerializer(serializers.Serializer):
    """政策文件发布序列化器"""
    publish_time = serializers.DateTimeField(required=False, allow_null=True, help_text='发布时间，不传则使用当前时间')


class PolicyDistributionSerializer(serializers.ModelSerializer):
    """政策文件下发序列化器"""
    feedback_status_display = serializers.CharField(source='get_feedback_status_display', read_only=True)
    supervise_status_display = serializers.CharField(source='get_supervise_status_display', read_only=True)
    policy_file_detail = serializers.SerializerMethodField()
    target_detail = serializers.SerializerMethodField()
    distribution_user_name = serializers.SerializerMethodField()
    supervise_user_name = serializers.SerializerMethodField()

    class Meta:
        model = PolicyDistribution
        fields = [
            'id', 'distribution_code', 'policy_file_id', 'policy_file_detail',
            'target_id', 'target_detail', 'feedback_content', 'feedback_deadline',
            'distribution_time', 'distribution_user_id', 'distribution_user_name',
            'feedback_status', 'feedback_status_display', 'feedback_time',
            'feedback_content_actual', 'supervise_status', 'supervise_status_display',
            'supervise_time', 'supervise_user_id', 'supervise_user_name',
            'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'distribution_time', 'created_at', 'updated_at']

    def get_policy_file_detail(self, obj):
        """获取政策文件详情"""
        if obj.policy_file_id:
            try:
                policy_file = PolicyFile.objects.get(id=obj.policy_file_id, deleted_at__isnull=True)
                return PolicyFileSerializer(policy_file).data
            except PolicyFile.DoesNotExist:
                return None
        return None

    def get_target_detail(self, obj):
        """获取叫应对象详情"""
        if obj.target_id:
            try:
                target = CallTarget.objects.get(id=obj.target_id, deleted_at__isnull=True)
                return CallTargetSerializer(target).data
            except CallTarget.DoesNotExist:
                return None
        return None

    def get_distribution_user_name(self, obj):
        """获取下发人姓名"""
        if obj.distribution_user_id:
            try:
                from apps.users.models import User
                user = User.objects.get(id=obj.distribution_user_id, deleted_at__isnull=True)
                return user.username
            except User.DoesNotExist:
                return None
        return None

    def get_supervise_user_name(self, obj):
        """获取督办人姓名"""
        if obj.supervise_user_id:
            try:
                from apps.users.models import User
                user = User.objects.get(id=obj.supervise_user_id, deleted_at__isnull=True)
                return user.username
            except User.DoesNotExist:
                return None
        return None



class PolicyDistributionFeedbackSerializer(serializers.Serializer):
    """政策文件下发反馈序列化器"""
    feedback_content_actual = serializers.CharField(required=True, help_text='实际反馈内容')


class PolicyDistributionSuperviseSerializer(serializers.Serializer):
    """政策文件下发督办序列化器"""
    supervise_user_id = serializers.IntegerField(required=True, help_text='督办人ID')


class CallRecordSerializer(serializers.ModelSerializer):
    """叫应记录序列化器"""
    call_type_display = serializers.CharField(source='get_call_type_display', read_only=True)
    call_source_display = serializers.CharField(source='get_call_source_display', read_only=True)
    call_status_display = serializers.CharField(source='get_call_status_display', read_only=True)
    receive_status_display = serializers.CharField(source='get_receive_status_display', read_only=True)
    response_status_display = serializers.CharField(source='get_response_status_display', read_only=True)
    target_detail = serializers.SerializerMethodField()
    person_detail = serializers.SerializerMethodField()
    group_detail = serializers.SerializerMethodField()
    policy_distribution_detail = serializers.SerializerMethodField()

    class Meta:
        model = CallRecord
        fields = [
            'id', 'call_code', 'call_type', 'call_type_display', 'call_source',
            'call_source_display', 'policy_distribution_id', 'policy_distribution_detail',
            'warning_id', 'target_id', 'target_detail', 'person_id', 'person_detail',
            'group_id', 'group_detail', 'call_channel', 'call_content', 'call_time',
            'call_status', 'call_status_display', 'receive_status', 'receive_status_display',
            'receive_time', 'response_status', 'response_status_display', 'response_time',
            'response_content', 'retry_count', 'last_retry_time', 'error_message',
            'external_call_id', 'description', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'call_time', 'created_at', 'updated_at']

    def get_target_detail(self, obj):
        """获取叫应对象详情"""
        if obj.target_id:
            try:
                target = CallTarget.objects.get(id=obj.target_id, deleted_at__isnull=True)
                return CallTargetSerializer(target).data
            except CallTarget.DoesNotExist:
                return None
        return None

    def get_person_detail(self, obj):
        """获取叫应人员详情"""
        if obj.person_id:
            try:
                person = CallPerson.objects.get(id=obj.person_id, deleted_at__isnull=True)
                return CallPersonSerializer(person).data
            except CallPerson.DoesNotExist:
                return None
        return None

    def get_group_detail(self, obj):
        """获取叫应分组详情"""
        if obj.group_id:
            try:
                group = CallGroup.objects.get(id=obj.group_id, deleted_at__isnull=True)
                return CallGroupSerializer(group).data
            except CallGroup.DoesNotExist:
                return None
        return None

    def get_policy_distribution_detail(self, obj):
        """获取政策文件下发详情"""
        if obj.policy_distribution_id:
            try:
                distribution = PolicyDistribution.objects.get(
                    id=obj.policy_distribution_id, deleted_at__isnull=True
                )
                return PolicyDistributionSerializer(distribution).data
            except PolicyDistribution.DoesNotExist:
                return None
        return None


class CallRecordResponseSerializer(serializers.Serializer):
    """叫应记录响应序列化器"""
    response_content = serializers.CharField(required=True, help_text='响应内容')


class CallRecordRetrySerializer(serializers.Serializer):
    """叫应记录重试序列化器"""
    pass  # 重试不需要额外参数


class EmergencyCallSerializer(serializers.Serializer):
    """一键叫应序列化器"""
    call_type = serializers.IntegerField(required=True, help_text='叫应类型：1-常态化叫应，2-非常态化叫应')
    call_source = serializers.IntegerField(default=2, help_text='叫应来源：1-政策文件下发，2-一键叫应，3-预警触发')
    # 常态化叫应参数
    target_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text='叫应对象ID列表（常态化叫应）'
    )
    # 非常态化叫应参数
    person_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text='叫应人员ID列表（非常态化叫应）'
    )
    group_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text='叫应分组ID列表（非常态化叫应）'
    )
    call_channel = serializers.CharField(required=True, help_text='叫应渠道：system-系统消息，sms-短信，phone-电话')
    call_content = serializers.CharField(required=True, help_text='叫应内容')
    warning_id = serializers.IntegerField(required=False, allow_null=True, help_text='预警ID（预警触发时）')

