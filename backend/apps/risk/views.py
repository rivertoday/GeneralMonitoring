"""
风险监测预警模块 - 视图
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
from .models import (
    WarningLevel, WarningRule, RiskMonitor, AlarmRecord,
    RiskWarning, AlarmStatistics, RiskHiddenDanger, RiskRectification
)
from .serializers import (
    WarningLevelSerializer, WarningRuleSerializer, RiskMonitorSerializer,
    AlarmRecordSerializer, AlarmRecordHandleSerializer, RiskWarningSerializer,
    RiskWarningPublishSerializer, RiskWarningHandleSerializer, AlarmStatisticsSerializer,
    RiskHiddenDangerSerializer, RiskRectificationSerializer, RiskRectificationVerifySerializer
)


class WarningLevelViewSet(viewsets.ModelViewSet):
    """
    预警级别管理视图集
    """
    queryset = WarningLevel.objects.filter(deleted_at__isnull=True)
    serializer_class = WarningLevelSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['level_color', 'severity', 'status']
    search_fields = ['level_code', 'level_name', 'description']
    ordering_fields = ['severity', 'sort_order', 'created_at']
    ordering = ['severity']

    @swagger_auto_schema(tags=['预警级别'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预警级别'])
    def create(self, request, *args, **kwargs):
        """创建预警级别"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建预警级别成功')

    @swagger_auto_schema(tags=['预警级别'])
    def retrieve(self, request, *args, **kwargs):
        """获取预警级别详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预警级别'])
    def update(self, request, *args, **kwargs):
        """更新预警级别"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新预警级别成功')

    @swagger_auto_schema(tags=['预警级别'])
    def destroy(self, request, *args, **kwargs):
        """删除预警级别（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除预警级别成功')


class WarningRuleViewSet(viewsets.ModelViewSet):
    """
    预警规则管理视图集
    """
    queryset = WarningRule.objects.filter(deleted_at__isnull=True)
    serializer_class = WarningRuleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rule_type', 'industry_type', 'warning_level', 'status']
    search_fields = ['rule_code', 'rule_name', 'description']
    ordering_fields = ['created_at', 'rule_type']
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
        """创建预警规则"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建预警规则成功')

    def retrieve(self, request, *args, **kwargs):
        """获取预警规则详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新预警规则"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新预警规则成功')

    def destroy(self, request, *args, **kwargs):
        """删除预警规则（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除预警规则成功')


class RiskMonitorViewSet(viewsets.ModelViewSet):
    """
    风险监测点管理视图集
    """
    queryset = RiskMonitor.objects.filter(deleted_at__isnull=True)
    serializer_class = RiskMonitorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['monitor_type', 'industry_type', 'data_source_id', 'online_status', 'status', 'street']
    search_fields = ['monitor_code', 'monitor_name', 'address', 'description']
    ordering_fields = ['created_at', 'last_data_time', 'monitor_type']
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
        """创建监测点"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建监测点成功')

    def retrieve(self, request, *args, **kwargs):
        """获取监测点详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新监测点"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新监测点成功')

    def destroy(self, request, *args, **kwargs):
        """删除监测点（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除监测点成功')

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """更新监测点在线状态"""
        instance = self.get_object()
        online_status = request.data.get('online_status')
        if online_status not in [0, 1]:
            return ErrorResponse(message='在线状态值必须为0或1', code=400)
        instance.online_status = online_status
        if online_status == 1:
            instance.last_data_time = timezone.now()
        instance.save()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data, message='更新状态成功')


class AlarmRecordViewSet(viewsets.ModelViewSet):
    """
    报警记录管理视图集
    """
    queryset = AlarmRecord.objects.filter(deleted_at__isnull=True)
    serializer_class = AlarmRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['monitor', 'industry_type', 'alarm_type', 'alarm_status', 'street']
    search_fields = ['alarm_code', 'description', 'address']
    ordering_fields = ['alarm_time', 'created_at']
    ordering = ['-alarm_time']

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(alarm_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(alarm_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建报警记录"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建报警记录成功')

    def retrieve(self, request, *args, **kwargs):
        """获取报警记录详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新报警记录"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新报警记录成功')

    def destroy(self, request, *args, **kwargs):
        """删除报警记录（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除报警记录成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='处理报警',
        operation_description='处理指定的报警记录，更新报警状态和处理结果',
        request_body=AlarmRecordHandleSerializer,
        responses={
            200: openapi.Response('处理成功', AlarmRecordSerializer),
            400: '参数错误',
            404: '报警记录不存在',
        },
        tags=['报警记录']
    )
    @action(detail=True, methods=['post'])
    def handle(self, request, pk=None):
        """处理报警"""
        instance = self.get_object()
        serializer = AlarmRecordHandleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.alarm_status = serializer.validated_data['alarm_status']
        instance.handle_result = serializer.validated_data['handle_result']
        instance.handle_user_id = request.user.id
        instance.handle_time = timezone.now()
        if instance.alarm_status in [2, 3]:  # 已处理或已忽略
            instance.feedback_time = timezone.now()
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='处理报警成功')


class RiskWarningViewSet(viewsets.ModelViewSet):
    """
    风险预警管理视图集
    """
    queryset = RiskWarning.objects.filter(deleted_at__isnull=True)
    serializer_class = RiskWarningSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['warning_level', 'warning_rule', 'industry_type', 'warning_type',
                       'warning_analysis_type', 'warning_source', 'warning_status', 'street']
    search_fields = ['warning_code', 'warning_title', 'warning_content', 'address']
    ordering_fields = ['warning_time', 'publish_time', 'created_at']
    ordering = ['-warning_time']

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(warning_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(warning_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建风险预警"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建风险预警成功')

    def retrieve(self, request, *args, **kwargs):
        """获取风险预警详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新风险预警"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新风险预警成功')

    def destroy(self, request, *args, **kwargs):
        """删除风险预警（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除风险预警成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='发布预警',
        operation_description='发布风险预警，将预警状态更新为已发布',
        request_body=RiskWarningPublishSerializer,
        responses={
            200: openapi.Response('发布成功', RiskWarningSerializer),
            400: '参数错误',
            404: '预警不存在',
        },
        tags=['风险预警']
    )
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布预警"""
        instance = self.get_object()
        serializer = RiskWarningPublishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.warning_status = 1  # 已发布
        instance.publish_time = serializer.validated_data.get('publish_time') or timezone.now()
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='发布预警成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='处置预警',
        operation_description='处置风险预警，更新预警状态和处置结果',
        request_body=RiskWarningHandleSerializer,
        responses={
            200: openapi.Response('处置成功', RiskWarningSerializer),
            400: '参数错误',
            404: '预警不存在',
        },
        tags=['风险预警']
    )
    @action(detail=True, methods=['post'])
    def handle(self, request, pk=None):
        """处置预警"""
        instance = self.get_object()
        serializer = RiskWarningHandleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.warning_status = serializer.validated_data['warning_status']
        instance.handle_result = serializer.validated_data['handle_result']
        instance.response_user_id = request.user.id
        if instance.warning_status == 2:  # 处理中
            if not instance.response_time:
                instance.response_time = timezone.now()
        if instance.warning_status in [3, 4]:  # 已处置或已关闭
            instance.handle_time = timezone.now()
            if not instance.response_time:
                instance.response_time = timezone.now()
            instance.feedback_time = timezone.now()
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='处置预警成功')


class AlarmStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    报警统计视图集（只读）
    """
    queryset = AlarmStatistics.objects.all()
    serializer_class = AlarmStatisticsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['stat_type', 'industry_type', 'street']
    search_fields = ['stat_date']
    ordering_fields = ['stat_date']
    ordering = ['-stat_date']

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持日期范围过滤
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(stat_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(stat_date__lte=end_date)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取统计详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)


class RiskHiddenDangerViewSet(viewsets.ModelViewSet):
    """
    隐患排查管理视图集
    """
    queryset = RiskHiddenDanger.objects.filter(deleted_at__isnull=True)
    serializer_class = RiskHiddenDangerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['monitor', 'organization_id', 'industry_type', 'danger_level',
                       'danger_category', 'status', 'street']
    search_fields = ['danger_code', 'danger_name', 'address', 'danger_description']
    ordering_fields = ['discover_time', 'created_at', 'danger_level']
    ordering = ['-discover_time']

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(discover_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(discover_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建隐患排查"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if not instance.discover_user_id:
            instance.discover_user_id = request.user.id
            instance.save()
        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='创建隐患排查成功')

    def retrieve(self, request, *args, **kwargs):
        """获取隐患排查详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新隐患排查"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新隐患排查成功')

    def destroy(self, request, *args, **kwargs):
        """删除隐患排查（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除隐患排查成功')


class RiskRectificationViewSet(viewsets.ModelViewSet):
    """
    隐患整改管理视图集
    """
    queryset = RiskRectification.objects.filter(deleted_at__isnull=True)
    serializer_class = RiskRectificationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['danger', 'responsible_user_id', 'responsible_org_id',
                       'rectification_status', 'verification_status']
    search_fields = ['rectification_code', 'rectification_plan', 'rectification_measures']
    ordering_fields = ['plan_start_time', 'plan_end_time', 'created_at']
    ordering = ['-created_at']

    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(plan_start_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(plan_end_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    def create(self, request, *args, **kwargs):
        """创建隐患整改"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        if instance.rectification_status == 1:  # 进行中
            if not instance.actual_start_time:
                instance.actual_start_time = timezone.now()
                instance.save()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data, message='创建隐患整改成功')

    def retrieve(self, request, *args, **kwargs):
        """获取隐患整改详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """更新隐患整改"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        
        # 自动处理状态变更
        new_status = serializer.validated_data.get('rectification_status', instance.rectification_status)
        if new_status == 1 and not instance.actual_start_time:  # 开始整改
            instance.actual_start_time = timezone.now()
        elif new_status == 2 and not instance.actual_end_time:  # 完成整改
            instance.actual_end_time = timezone.now()
        
        serializer.save()
        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='更新隐患整改成功')

    def destroy(self, request, *args, **kwargs):
        """删除隐患整改（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除隐患整改成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='验收整改',
        operation_description='验收隐患整改，更新验收状态和验收意见',
        request_body=RiskRectificationVerifySerializer,
        responses={
            200: openapi.Response('验收成功', RiskRectificationSerializer),
            400: '参数错误',
            404: '整改记录不存在',
        },
        tags=['隐患整改']
    )
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """验收整改"""
        instance = self.get_object()
        serializer = RiskRectificationVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.verification_status = serializer.validated_data['verification_status']
        instance.verification_opinion = serializer.validated_data['verification_opinion']
        instance.verification_user_id = request.user.id
        instance.verification_time = timezone.now()
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='验收整改成功')
