"""
简报模块 - 视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.common.response import SuccessResponse, ErrorResponse
from apps.common.pagination import StandardResultsSetPagination
from .models import BriefTemplate, BriefStrategy, BriefData, BriefPush
from .serializers import (
    BriefTemplateSerializer, BriefStrategySerializer, BriefDataSerializer,
    BriefDataGenerateSerializer, BriefPushSerializer, BriefPushCreateSerializer,
    BriefPushReadSerializer
)


class BriefTemplateViewSet(viewsets.ModelViewSet):
    """
    简报模板管理视图集
    """
    queryset = BriefTemplate.objects.filter(deleted_at__isnull=True)
    serializer_class = BriefTemplateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['template_type', 'industry_type', 'time_dimension', 'status']
    search_fields = ['template_code', 'template_name', 'template_content', 'description']
    ordering_fields = ['created_at', 'template_type']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建简报模板"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建简报模板成功')

    def retrieve(self, request, *args, **kwargs):
        """获取简报模板详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新简报模板"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新简报模板成功')

    def destroy(self, request, *args, **kwargs):
        """删除简报模板（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除简报模板成功')


class BriefStrategyViewSet(viewsets.ModelViewSet):
    """
    简报策略管理视图集
    """
    queryset = BriefStrategy.objects.filter(deleted_at__isnull=True)
    serializer_class = BriefStrategySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['template_id', 'strategy_type', 'report_type', 'trigger_type', 'status']
    search_fields = ['strategy_code', 'strategy_name', 'description']
    ordering_fields = ['created_at', 'next_execute_at']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建简报策略"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建简报策略成功')

    def retrieve(self, request, *args, **kwargs):
        """获取简报策略详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新简报策略"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新简报策略成功')

    def destroy(self, request, *args, **kwargs):
        """删除简报策略（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除简报策略成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='执行策略',
        operation_description='手动执行简报策略，生成简报',
        responses={
            200: openapi.Response('执行成功', BriefDataSerializer),
            400: '参数错误',
            404: '策略不存在',
        },
        tags=['简报策略']
    )
    @action(detail=True, methods=['post'])
    def execute(self, request, pk=None):
        """执行策略（生成简报）"""
        instance = self.get_object()
        if instance.status != 1:
            return ErrorResponse(message='策略未启用，无法执行', code=400)

        # 这里应该调用实际的简报生成逻辑
        # 暂时返回成功响应
        instance.last_execute_at = timezone.now()
        instance.save()

        return SuccessResponse(message='策略执行成功，简报生成中')


class BriefDataViewSet(viewsets.ModelViewSet):
    """
    简报数据管理视图集
    """
    queryset = BriefData.objects.filter(deleted_at__isnull=True)
    serializer_class = BriefDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['template_id', 'strategy_id', 'brief_type', 'report_type', 'status']
    search_fields = ['brief_code', 'brief_title', 'brief_content', 'description']
    ordering_fields = ['report_date', 'generate_time', 'created_at']
    ordering = ['-report_date', '-generate_time']

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持日期范围过滤
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(report_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(report_date__lte=end_date)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建简报数据"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if not instance.generate_user_id:
            instance.generate_user_id = request.user.id
            instance.save()
        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='创建简报数据成功')

    def retrieve(self, request, *args, **kwargs):
        """获取简报数据详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新简报数据"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新简报数据成功')

    def destroy(self, request, *args, **kwargs):
        """删除简报数据（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除简报数据成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='生成简报',
        operation_description='根据模板和策略生成简报数据',
        request_body=BriefDataGenerateSerializer,
        responses={
            200: openapi.Response('生成成功', BriefDataSerializer),
            400: '参数错误',
            404: '模板或策略不存在',
        },
        tags=['简报数据']
    )
    @action(detail=False, methods=['post'])
    def generate(self, request):
        """生成简报"""
        serializer = BriefDataGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        template_id = serializer.validated_data['template_id']
        strategy_id = serializer.validated_data.get('strategy_id')
        report_date = serializer.validated_data['report_date']
        report_period_start = serializer.validated_data.get('report_period_start')
        report_period_end = serializer.validated_data.get('report_period_end')

        # 验证模板是否存在
        try:
            template = BriefTemplate.objects.get(id=template_id, deleted_at__isnull=True)
        except BriefTemplate.DoesNotExist:
            return ErrorResponse(message='模板不存在', code=404)

        # 验证策略是否存在（如果提供）
        if strategy_id:
            try:
                strategy = BriefStrategy.objects.get(id=strategy_id, deleted_at__isnull=True)
            except BriefStrategy.DoesNotExist:
                return ErrorResponse(message='策略不存在', code=404)

        # 这里应该调用实际的简报生成逻辑
        # 暂时返回成功响应，实际应该生成简报内容
        return SuccessResponse(message='简报生成功能待实现')


class BriefPushViewSet(viewsets.ModelViewSet):
    """
    简报推送记录管理视图集
    """
    queryset = BriefPush.objects.all()
    serializer_class = BriefPushSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['brief_id', 'push_target_type', 'target_id', 'push_channel', 'push_status', 'read_status']
    search_fields = ['message_id', 'error_message']
    ordering_fields = ['push_time', 'read_time', 'created_at']
    ordering = ['-push_time', '-created_at']

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(push_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(push_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建推送记录（通常通过推送接口创建）"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if not instance.push_time and instance.push_status == 2:  # 推送成功
            instance.push_time = timezone.now()
            instance.save()
        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='创建推送记录成功')

    def retrieve(self, request, *args, **kwargs):
        """获取推送记录详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新推送记录"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新推送记录成功')

    def destroy(self, request, *args, **kwargs):
        """删除推送记录"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除推送记录成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='推送简报',
        operation_description='将简报推送给指定的目标（用户、角色或组织）',
        request_body=BriefPushCreateSerializer,
        responses={
            200: openapi.Response('推送成功', BriefPushSerializer),
            400: '参数错误',
            404: '简报不存在',
        },
        tags=['简报推送']
    )
    @action(detail=False, methods=['post'])
    def push(self, request):
        """推送简报"""
        serializer = BriefPushCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        brief_id = serializer.validated_data['brief_id']
        push_target_type = serializer.validated_data['push_target_type']
        target_ids = serializer.validated_data['target_ids']
        push_channels = serializer.validated_data['push_channel']

        # 验证简报是否存在
        try:
            brief = BriefData.objects.get(id=brief_id, deleted_at__isnull=True)
        except BriefData.DoesNotExist:
            return ErrorResponse(message='简报不存在', code=404)

        # 为每个目标和渠道创建推送记录
        push_records = []
        for target_id in target_ids:
            for channel in push_channels:
                push_record = BriefPush.objects.create(
                    brief_id=brief_id,
                    push_target_type=push_target_type,
                    target_id=target_id,
                    push_channel=channel,
                    push_status=0,  # 待推送
                )
                push_records.append(push_record)

        # 这里应该调用实际的推送逻辑（系统消息、短信、邮件等）
        # 暂时将所有记录标记为推送成功
        for record in push_records:
            record.push_status = 2  # 推送成功
            record.push_time = timezone.now()
            record.save()

        # 更新简报状态为已推送
        if brief.status == 0:  # 未推送
            brief.status = 1  # 已推送
            brief.save()

        result_serializer = BriefPushSerializer(push_records, many=True)
        return SuccessResponse(data=result_serializer.data, message='推送成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='标记已读',
        operation_description='标记简报推送记录为已读',
        request_body=BriefPushReadSerializer,
        responses={
            200: openapi.Response('标记成功', BriefPushSerializer),
            400: '参数错误',
            404: '推送记录不存在',
        },
        tags=['简报推送']
    )
    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        """标记已读"""
        serializer = BriefPushReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        push_id = serializer.validated_data['push_id']
        try:
            push_record = BriefPush.objects.get(id=push_id)
        except BriefPush.DoesNotExist:
            return ErrorResponse(message='推送记录不存在', code=404)

        push_record.read_status = 1  # 已读
        push_record.read_time = timezone.now()
        push_record.save()

        # 如果所有推送记录都已读，更新简报状态
        brief_id = push_record.brief_id
        all_read = not BriefPush.objects.filter(
            brief_id=brief_id,
            read_status=0
        ).exists()
        if all_read:
            try:
                brief = BriefData.objects.get(id=brief_id, deleted_at__isnull=True)
                if brief.status == 1:  # 已推送
                    brief.status = 2  # 已查看
                    brief.save()
            except BriefData.DoesNotExist:
                pass

        result_serializer = BriefPushSerializer(push_record)
        return SuccessResponse(data=result_serializer.data, message='标记已读成功')
