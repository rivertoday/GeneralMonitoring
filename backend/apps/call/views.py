"""
叫应模块 - 视图
"""
import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.common.response import SuccessResponse, ErrorResponse
from apps.common.pagination import StandardResultsSetPagination
from .models import (
    CallGroup, CallTarget, CallPerson, PolicyFile,
    PolicyDistribution, CallRecord
)
from .serializers import (
    CallGroupSerializer, CallTargetSerializer, CallPersonSerializer,
    PolicyFileSerializer, PolicyFilePublishSerializer, PolicyDistributionSerializer,
    PolicyDistributionFeedbackSerializer, PolicyDistributionSuperviseSerializer,
    CallRecordSerializer, CallRecordResponseSerializer, CallRecordRetrySerializer,
    EmergencyCallSerializer
)


class CallGroupViewSet(viewsets.ModelViewSet):
    """
    叫应分组管理视图集
    """
    queryset = CallGroup.objects.filter(deleted_at__isnull=True)
    serializer_class = CallGroupSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['group_type', 'event_level', 'status']
    search_fields = ['group_code', 'group_name', 'description']
    ordering_fields = ['sort_order', 'created_at']
    ordering = ['sort_order']

    @swagger_auto_schema(tags=['叫应分组'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['叫应分组'])
    def create(self, request, *args, **kwargs):
        """创建叫应分组"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建叫应分组成功')

    @swagger_auto_schema(tags=['叫应分组'])
    def retrieve(self, request, *args, **kwargs):
        """获取叫应分组详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['叫应分组'])
    def update(self, request, *args, **kwargs):
        """更新叫应分组"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新叫应分组成功')

    @swagger_auto_schema(tags=['叫应分组'])
    def destroy(self, request, *args, **kwargs):
        """删除叫应分组（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除叫应分组成功')


class CallTargetViewSet(viewsets.ModelViewSet):
    """
    叫应对象管理视图集
    """
    queryset = CallTarget.objects.filter(deleted_at__isnull=True)
    serializer_class = CallTargetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['target_type', 'organization_id', 'status']
    search_fields = ['target_code', 'target_name', 'enterprise_name', 'safety_person', 'contact_phone']
    ordering_fields = ['created_at', 'target_type']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['叫应对象'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['叫应对象'])
    def create(self, request, *args, **kwargs):
        """创建叫应对象"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建叫应对象成功')

    @swagger_auto_schema(tags=['叫应对象'])
    def retrieve(self, request, *args, **kwargs):
        """获取叫应对象详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['叫应对象'])
    def update(self, request, *args, **kwargs):
        """更新叫应对象"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新叫应对象成功')

    @swagger_auto_schema(tags=['叫应对象'])
    def destroy(self, request, *args, **kwargs):
        """删除叫应对象（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除叫应对象成功')


class CallPersonViewSet(viewsets.ModelViewSet):
    """
    叫应人员管理视图集
    """
    queryset = CallPerson.objects.filter(deleted_at__isnull=True)
    serializer_class = CallPersonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['group_id', 'event_level', 'organization_id', 'status']
    search_fields = ['person_code', 'person_name', 'rank', 'mobile_phone', 'office_phone']
    ordering_fields = ['created_at', 'event_level']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['叫应人员'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['叫应人员'])
    def create(self, request, *args, **kwargs):
        """创建叫应人员"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建叫应人员成功')

    @swagger_auto_schema(tags=['叫应人员'])
    def retrieve(self, request, *args, **kwargs):
        """获取叫应人员详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['叫应人员'])
    def update(self, request, *args, **kwargs):
        """更新叫应人员"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新叫应人员成功')

    @swagger_auto_schema(tags=['叫应人员'])
    def destroy(self, request, *args, **kwargs):
        """删除叫应人员（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除叫应人员成功')


class PolicyFileViewSet(viewsets.ModelViewSet):
    """
    政策文件管理视图集
    """
    queryset = PolicyFile.objects.filter(deleted_at__isnull=True)
    serializer_class = PolicyFileSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['file_type', 'upload_user_id', 'publish_status']
    search_fields = ['file_code', 'file_name', 'policy_title']
    ordering_fields = ['upload_time', 'publish_time', 'created_at']
    ordering = ['-upload_time']

    @swagger_auto_schema(tags=['政策文件'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(upload_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(upload_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['政策文件'])
    def create(self, request, *args, **kwargs):
        """创建政策文件"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 设置上传人
        serializer.save(upload_user_id=request.user.id)
        return SuccessResponse(data=serializer.data, message='创建政策文件成功')

    @swagger_auto_schema(tags=['政策文件'])
    def retrieve(self, request, *args, **kwargs):
        """获取政策文件详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['政策文件'])
    def update(self, request, *args, **kwargs):
        """更新政策文件"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新政策文件成功')

    @swagger_auto_schema(tags=['政策文件'])
    def destroy(self, request, *args, **kwargs):
        """删除政策文件（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除政策文件成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='发布政策文件',
        operation_description='发布政策文件，将发布状态更新为已发布',
        request_body=PolicyFilePublishSerializer,
        responses={
            200: openapi.Response('发布成功', PolicyFileSerializer),
            400: '参数错误',
            404: '政策文件不存在',
        },
        tags=['政策文件']
    )
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布政策文件"""
        instance = self.get_object()
        serializer = PolicyFilePublishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.publish_status = 1  # 已发布
        instance.publish_time = serializer.validated_data.get('publish_time') or timezone.now()
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='发布政策文件成功')


class PolicyDistributionViewSet(viewsets.ModelViewSet):
    """
    政策文件下发管理视图集
    """
    queryset = PolicyDistribution.objects.filter(deleted_at__isnull=True)
    serializer_class = PolicyDistributionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['policy_file_id', 'target_id', 'feedback_status', 'supervise_status']
    search_fields = ['distribution_code', 'description']
    ordering_fields = ['distribution_time', 'feedback_deadline', 'created_at']
    ordering = ['-distribution_time']

    @swagger_auto_schema(tags=['政策文件下发'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(distribution_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(distribution_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['政策文件下发'])
    def create(self, request, *args, **kwargs):
        """创建政策文件下发"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 设置下发人
        serializer.save(distribution_user_id=request.user.id)
        return SuccessResponse(data=serializer.data, message='创建政策文件下发成功')

    @swagger_auto_schema(tags=['政策文件下发'])
    def retrieve(self, request, *args, **kwargs):
        """获取政策文件下发详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['政策文件下发'])
    def update(self, request, *args, **kwargs):
        """更新政策文件下发"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新政策文件下发成功')

    @swagger_auto_schema(tags=['政策文件下发'])
    def destroy(self, request, *args, **kwargs):
        """删除政策文件下发（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除政策文件下发成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='反馈政策文件下发',
        operation_description='反馈政策文件下发，更新反馈状态和反馈内容',
        request_body=PolicyDistributionFeedbackSerializer,
        responses={
            200: openapi.Response('反馈成功', PolicyDistributionSerializer),
            400: '参数错误',
            404: '下发记录不存在',
        },
        tags=['政策文件下发']
    )
    @action(detail=True, methods=['post'])
    def feedback(self, request, pk=None):
        """反馈政策文件下发"""
        instance = self.get_object()
        serializer = PolicyDistributionFeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.feedback_status = 1  # 已反馈
        instance.feedback_time = timezone.now()
        instance.feedback_content_actual = serializer.validated_data['feedback_content_actual']
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='反馈成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='督办政策文件下发',
        operation_description='督办政策文件下发，更新督办状态和督办人',
        request_body=PolicyDistributionSuperviseSerializer,
        responses={
            200: openapi.Response('督办成功', PolicyDistributionSerializer),
            400: '参数错误',
            404: '下发记录不存在',
        },
        tags=['政策文件下发']
    )
    @action(detail=True, methods=['post'])
    def supervise(self, request, pk=None):
        """督办政策文件下发"""
        instance = self.get_object()
        serializer = PolicyDistributionSuperviseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.supervise_status = 2  # 已督办
        instance.supervise_time = timezone.now()
        instance.supervise_user_id = serializer.validated_data['supervise_user_id']
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='督办成功')


class CallRecordViewSet(viewsets.ModelViewSet):
    """
    叫应记录管理视图集
    """
    queryset = CallRecord.objects.filter(deleted_at__isnull=True)
    serializer_class = CallRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['call_type', 'call_source', 'call_channel', 'call_status', 'receive_status', 'response_status']
    search_fields = ['call_code', 'call_content', 'description']
    ordering_fields = ['call_time', 'created_at']
    ordering = ['-call_time']

    @swagger_auto_schema(tags=['叫应记录'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(call_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(call_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['叫应记录'])
    def create(self, request, *args, **kwargs):
        """创建叫应记录"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建叫应记录成功')

    @swagger_auto_schema(tags=['叫应记录'])
    def retrieve(self, request, *args, **kwargs):
        """获取叫应记录详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['叫应记录'])
    def update(self, request, *args, **kwargs):
        """更新叫应记录"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新叫应记录成功')

    @swagger_auto_schema(tags=['叫应记录'])
    def destroy(self, request, *args, **kwargs):
        """删除叫应记录（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除叫应记录成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='响应叫应',
        operation_description='响应叫应记录，更新响应状态和响应内容',
        request_body=CallRecordResponseSerializer,
        responses={
            200: openapi.Response('响应成功', CallRecordSerializer),
            400: '参数错误',
            404: '叫应记录不存在',
        },
        tags=['叫应记录']
    )
    @action(detail=True, methods=['post'])
    def response(self, request, pk=None):
        """响应叫应"""
        instance = self.get_object()
        serializer = CallRecordResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.response_status = 1  # 已响应
        instance.response_time = timezone.now()
        instance.response_content = serializer.validated_data['response_content']
        instance.receive_status = 1  # 已接收
        if not instance.receive_time:
            instance.receive_time = timezone.now()
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='响应成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='重试叫应',
        operation_description='重试发送叫应记录',
        request_body=CallRecordRetrySerializer,
        responses={
            200: openapi.Response('重试成功', CallRecordSerializer),
            400: '参数错误',
            404: '叫应记录不存在',
        },
        tags=['叫应记录']
    )
    @action(detail=True, methods=['post'])
    def retry(self, request, pk=None):
        """重试叫应"""
        instance = self.get_object()
        instance.call_status = 0  # 待发送
        instance.retry_count += 1
        instance.last_retry_time = timezone.now()
        instance.error_message = None
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='重试成功，已加入发送队列')

    @swagger_auto_schema(
        method='get',
        operation_summary='叫应统计',
        operation_description='获取叫应统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['叫应记录']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """叫应统计"""
        queryset = self.get_queryset()
        
        # 时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(call_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(call_time__lte=end_time)

        # 统计总数
        total_count = queryset.count()
        
        # 按叫应类型统计
        type_stats = queryset.values('call_type').annotate(count=Count('id'))
        
        # 按叫应来源统计
        source_stats = queryset.values('call_source').annotate(count=Count('id'))
        
        # 按叫应渠道统计
        channel_stats = queryset.values('call_channel').annotate(count=Count('id'))
        
        # 按叫应状态统计
        call_status_stats = queryset.values('call_status').annotate(count=Count('id'))
        
        # 按接收状态统计
        receive_status_stats = queryset.values('receive_status').annotate(count=Count('id'))
        
        # 按响应状态统计
        response_status_stats = queryset.values('response_status').annotate(count=Count('id'))

        statistics_data = {
            'total_count': total_count,
            'type_stats': list(type_stats),
            'source_stats': list(source_stats),
            'channel_stats': list(channel_stats),
            'call_status_stats': list(call_status_stats),
            'receive_status_stats': list(receive_status_stats),
            'response_status_stats': list(response_status_stats),
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')


class EmergencyCallViewSet(viewsets.ViewSet):
    """
    一键叫应视图集
    """
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(
        method='post',
        operation_summary='一键叫应',
        operation_description='一键叫应相关责任人，支持常态化叫应和非常态化叫应',
        request_body=EmergencyCallSerializer,
        responses={
            200: openapi.Response('叫应成功'),
            400: '参数错误',
        },
        tags=['一键叫应']
    )
    @action(detail=False, methods=['post'])
    def call(self, request):
        """一键叫应"""
        serializer = EmergencyCallSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        call_type = serializer.validated_data['call_type']
        call_source = serializer.validated_data.get('call_source', 2)
        call_channel = serializer.validated_data['call_channel']
        call_content = serializer.validated_data['call_content']
        warning_id = serializer.validated_data.get('warning_id')

        created_records = []

        if call_type == 1:  # 常态化叫应
            target_ids = serializer.validated_data.get('target_ids', [])
            if not target_ids:
                return ErrorResponse(message='常态化叫应必须指定叫应对象', code=400)

            for target_id in target_ids:
                try:
                    target = CallTarget.objects.get(id=target_id, deleted_at__isnull=True, status=1)
                except CallTarget.DoesNotExist:
                    continue

                # 生成叫应编码
                call_code = f'CALL_{uuid.uuid4().hex[:16].upper()}'

                # 创建叫应记录
                call_record = CallRecord.objects.create(
                    call_code=call_code,
                    call_type=call_type,
                    call_source=call_source,
                    warning_id=warning_id,
                    target_id=target_id,
                    call_channel=call_channel,
                    call_content=call_content,
                    call_status=0,  # 待发送
                    receive_status=0,  # 未接收
                    response_status=0,  # 未响应
                )
                created_records.append(call_record.id)

        elif call_type == 2:  # 非常态化叫应
            person_ids = serializer.validated_data.get('person_ids', [])
            group_ids = serializer.validated_data.get('group_ids', [])

            if not person_ids and not group_ids:
                return ErrorResponse(message='非常态化叫应必须指定叫应人员或分组', code=400)

            # 处理分组叫应
            for group_id in group_ids:
                try:
                    group = CallGroup.objects.get(id=group_id, deleted_at__isnull=True, status=1)
                    persons = CallPerson.objects.filter(
                        group_id=group_id, deleted_at__isnull=True, status=1
                    )
                    for person in persons:
                        if person.id not in person_ids:
                            person_ids.append(person.id)
                except CallGroup.DoesNotExist:
                    continue

            # 处理人员叫应
            for person_id in person_ids:
                try:
                    person = CallPerson.objects.get(id=person_id, deleted_at__isnull=True, status=1)
                except CallPerson.DoesNotExist:
                    continue

                # 生成叫应编码
                call_code = f'CALL_{uuid.uuid4().hex[:16].upper()}'

                # 创建叫应记录
                call_record = CallRecord.objects.create(
                    call_code=call_code,
                    call_type=call_type,
                    call_source=call_source,
                    warning_id=warning_id,
                    person_id=person_id,
                    group_id=person.group_id,
                    call_channel=call_channel,
                    call_content=call_content,
                    call_status=0,  # 待发送
                    receive_status=0,  # 未接收
                    response_status=0,  # 未响应
                )
                created_records.append(call_record.id)

        return SuccessResponse(
            data={
                'created_count': len(created_records),
                'record_ids': created_records
            },
            message=f'一键叫应成功，已创建{len(created_records)}条叫应记录'
        )

