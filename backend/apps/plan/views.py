"""
预案模块 - 视图
"""
import uuid
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.common.response import SuccessResponse, ErrorResponse
from apps.common.pagination import StandardResultsSetPagination
from .models import (
    EmergencyPlan, PlanStructure, PlanFlow,
    PlanTask, PlanExecution, PlanTaskExecution
)
from .serializers import (
    EmergencyPlanSerializer, EmergencyPlanPublishSerializer,
    EmergencyPlanApproveSerializer, EmergencyPlanReviseSerializer,
    EmergencyPlanAbandonSerializer, PlanStructureSerializer,
    PlanFlowSerializer, PlanTaskSerializer, PlanExecutionSerializer,
    PlanExecutionStartSerializer, PlanExecutionUpdateStatusSerializer,
    PlanExecutionCompleteSerializer, PlanTaskExecutionSerializer,
    PlanTaskExecutionAcceptSerializer, PlanTaskExecutionStartSerializer,
    PlanTaskExecutionCompleteSerializer
)


class EmergencyPlanViewSet(viewsets.ModelViewSet):
    """
    应急预案管理视图集
    """
    queryset = EmergencyPlan.objects.filter(deleted_at__isnull=True)
    serializer_class = EmergencyPlanSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['plan_type', 'industry_type', 'organization_id', 'plan_status']
    search_fields = ['plan_code', 'plan_name', 'plan_summary', 'description']
    ordering_fields = ['publish_time', 'created_at', 'plan_type']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['应急预案'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(created_at__gte=start_time)
        if end_time:
            queryset = queryset.filter(created_at__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['应急预案'])
    def create(self, request, *args, **kwargs):
        """创建应急预案"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成预案编码
        if not serializer.validated_data.get('plan_code'):
            serializer.validated_data['plan_code'] = f'PLAN_{uuid.uuid4().hex[:16].upper()}'
        # 设置创建人
        serializer.save(create_user_id=request.user.id)
        return SuccessResponse(data=serializer.data, message='创建应急预案成功')

    @swagger_auto_schema(tags=['应急预案'])
    def retrieve(self, request, *args, **kwargs):
        """获取应急预案详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['应急预案'])
    def update(self, request, *args, **kwargs):
        """更新应急预案"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新应急预案成功')

    @swagger_auto_schema(tags=['应急预案'])
    def destroy(self, request, *args, **kwargs):
        """删除应急预案（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除应急预案成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='发布预案',
        operation_description='发布应急预案，将状态更新为已发布',
        request_body=EmergencyPlanPublishSerializer,
        responses={
            200: openapi.Response('发布成功', EmergencyPlanSerializer),
            400: '参数错误',
            404: '预案不存在',
        },
        tags=['应急预案']
    )
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """发布预案"""
        instance = self.get_object()
        if instance.plan_status == 1:
            return ErrorResponse(message='预案已发布，无需重复发布', code=400)
        
        serializer = EmergencyPlanPublishSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.plan_status = 1  # 已发布
        instance.publish_time = serializer.validated_data.get('publish_time') or timezone.now()
        if serializer.validated_data.get('effective_time'):
            instance.effective_time = serializer.validated_data['effective_time']
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='发布预案成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='审批预案',
        operation_description='审批应急预案',
        request_body=EmergencyPlanApproveSerializer,
        responses={
            200: openapi.Response('审批成功', EmergencyPlanSerializer),
            400: '参数错误',
            404: '预案不存在',
        },
        tags=['应急预案']
    )
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """审批预案"""
        instance = self.get_object()
        serializer = EmergencyPlanApproveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.approve_user_id = serializer.validated_data['approve_user_id']
        instance.approve_time = serializer.validated_data.get('approve_time') or timezone.now()
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='审批预案成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='修订预案',
        operation_description='修订应急预案，创建新版本',
        request_body=EmergencyPlanReviseSerializer,
        responses={
            200: openapi.Response('修订成功', EmergencyPlanSerializer),
            400: '参数错误',
            404: '预案不存在',
        },
        tags=['应急预案']
    )
    @action(detail=True, methods=['post'])
    def revise(self, request, pk=None):
        """修订预案"""
        instance = self.get_object()
        serializer = EmergencyPlanReviseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 将原预案状态改为已修订
        instance.plan_status = 2  # 已修订
        instance.revision_reason = serializer.validated_data['revision_reason']
        instance.save()

        # 创建新版本预案
        new_plan_data = {
            'plan_code': f'PLAN_{uuid.uuid4().hex[:16].upper()}',
            'plan_name': instance.plan_name,
            'plan_type': instance.plan_type,
            'industry_type': instance.industry_type,
            'organization_id': instance.organization_id,
            'version': serializer.validated_data['new_version'],
            'plan_file_path': instance.plan_file_path,
            'plan_file_name': instance.plan_file_name,
            'plan_summary': instance.plan_summary,
            'plan_status': 0,  # 草稿
            'create_user_id': request.user.id,
            'description': instance.description,
        }
        new_plan = EmergencyPlan.objects.create(**new_plan_data)

        result_serializer = self.get_serializer(new_plan)
        return SuccessResponse(data=result_serializer.data, message='修订预案成功，已创建新版本')

    @swagger_auto_schema(
        method='post',
        operation_summary='废止预案',
        operation_description='废止应急预案',
        request_body=EmergencyPlanAbandonSerializer,
        responses={
            200: openapi.Response('废止成功', EmergencyPlanSerializer),
            400: '参数错误',
            404: '预案不存在',
        },
        tags=['应急预案']
    )
    @action(detail=True, methods=['post'])
    def abandon(self, request, pk=None):
        """废止预案"""
        instance = self.get_object()
        serializer = EmergencyPlanAbandonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.plan_status = 3  # 已废止
        instance.revision_reason = serializer.validated_data['revision_reason']
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='废止预案成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='预案统计',
        operation_description='获取预案统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['应急预案']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """预案统计"""
        queryset = self.get_queryset()
        
        # 时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(created_at__gte=start_time)
        if end_time:
            queryset = queryset.filter(created_at__lte=end_time)

        # 统计总数
        total_count = queryset.count()
        
        # 按预案类型统计
        type_stats = queryset.values('plan_type').annotate(count=Count('id'))
        
        # 按行业类型统计
        industry_stats = queryset.values('industry_type').annotate(count=Count('id'))
        
        # 按预案状态统计
        status_stats = queryset.values('plan_status').annotate(count=Count('id'))
        
        # 按部门统计
        org_stats = queryset.filter(organization_id__isnull=False).values('organization_id').annotate(count=Count('id'))

        statistics_data = {
            'total_count': total_count,
            'type_stats': list(type_stats),
            'industry_stats': list(industry_stats),
            'status_stats': list(status_stats),
            'org_stats': list(org_stats),
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')


class PlanStructureViewSet(viewsets.ModelViewSet):
    """
    预案结构管理视图集
    """
    queryset = PlanStructure.objects.filter(deleted_at__isnull=True)
    serializer_class = PlanStructureSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['plan_id', 'node_type', 'parent_id', 'is_key_info']
    search_fields = ['node_code', 'node_name', 'node_content']
    ordering_fields = ['node_level', 'node_index', 'created_at']
    ordering = ['plan_id', 'node_level', 'node_index']

    @swagger_auto_schema(tags=['预案结构'])
    def list(self, request, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 优先从URL路径参数获取plan_id（嵌套路由），如果没有则从query参数获取
        plan_id = kwargs.get('plan_pk') or request.query_params.get('plan_id', None)
        if plan_id:
            queryset = queryset.filter(plan_id=plan_id)
            # 如果指定了plan_id，只返回顶级节点，子节点通过children字段递归获取
            queryset = queryset.filter(parent_id=0)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预案结构'])
    def create(self, request, **kwargs):
        """创建预案结构节点"""
        # 如果从嵌套路由获取plan_id，自动设置到请求数据中
        plan_pk = kwargs.get('plan_pk')
        if plan_pk:
            request.data['plan_id'] = plan_pk
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建预案结构节点成功')

    @swagger_auto_schema(tags=['预案结构'])
    def retrieve(self, request, *args, **kwargs):
        """获取预案结构节点详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预案结构'])
    def update(self, request, *args, **kwargs):
        """更新预案结构节点"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新预案结构节点成功')

    @swagger_auto_schema(tags=['预案结构'])
    def destroy(self, request, *args, **kwargs):
        """删除预案结构节点（软删除）"""
        instance = self.get_object()
        # 检查是否有子节点
        children_count = PlanStructure.objects.filter(
            parent_id=instance.id, deleted_at__isnull=True
        ).count()
        if children_count > 0:
            return ErrorResponse(message='该节点存在子节点，无法删除', code=400)
        instance.delete()
        return SuccessResponse(message='删除预案结构节点成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='获取树形结构',
        operation_description='获取指定预案的完整树形结构',
        responses={
            200: openapi.Response('获取成功', PlanStructureSerializer(many=True)),
        },
        tags=['预案结构']
    )
    @action(detail=False, methods=['get'], url_path='tree')
    def tree(self, request, **kwargs):
        """获取树形结构"""
        # 优先从URL路径参数获取plan_id（嵌套路由），如果没有则从query参数获取
        plan_id = kwargs.get('plan_pk') or request.query_params.get('plan_id', None)
        if not plan_id:
            return ErrorResponse(message='请指定plan_id参数', code=400)
        
        # 验证预案是否存在
        from .models import EmergencyPlan
        try:
            EmergencyPlan.objects.get(pk=plan_id, deleted_at__isnull=True)
        except EmergencyPlan.DoesNotExist:
            return ErrorResponse(message='预案不存在', code=404)
        
        # 获取所有顶级节点
        root_nodes = PlanStructure.objects.filter(
            plan_id=plan_id, parent_id=0, deleted_at__isnull=True
        ).order_by('node_index')
        
        serializer = self.get_serializer(root_nodes, many=True)
        return SuccessResponse(data=serializer.data, message='获取树形结构成功')


class PlanFlowViewSet(viewsets.ModelViewSet):
    """
    预案流程管理视图集
    """
    queryset = PlanFlow.objects.filter(deleted_at__isnull=True)
    serializer_class = PlanFlowSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['plan_id', 'flow_type', 'parent_id']
    search_fields = ['flow_code', 'flow_name', 'description']
    ordering_fields = ['flow_level', 'sort_order', 'created_at']
    ordering = ['plan_id', 'sort_order']

    @swagger_auto_schema(tags=['预案流程'])
    def list(self, request, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 优先从URL路径参数获取plan_id（嵌套路由），如果没有则从query参数获取
        plan_id = kwargs.get('plan_pk') or request.query_params.get('plan_id', None)
        if plan_id:
            queryset = queryset.filter(plan_id=plan_id)
            # 只返回顶级流程，子流程通过children字段递归获取
            queryset = queryset.filter(parent_id=0)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预案流程'])
    def create(self, request, **kwargs):
        """创建预案流程"""
        # 如果从嵌套路由获取plan_id，自动设置到请求数据中
        plan_pk = kwargs.get('plan_pk')
        if plan_pk:
            request.data['plan_id'] = plan_pk
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成流程编码
        if not serializer.validated_data.get('flow_code'):
            serializer.validated_data['flow_code'] = f'FLOW_{uuid.uuid4().hex[:16].upper()}'
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建预案流程成功')

    @swagger_auto_schema(tags=['预案流程'])
    def retrieve(self, request, *args, **kwargs):
        """获取预案流程详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预案流程'])
    def update(self, request, *args, **kwargs):
        """更新预案流程"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新预案流程成功')

    @swagger_auto_schema(tags=['预案流程'])
    def destroy(self, request, *args, **kwargs):
        """删除预案流程（软删除）"""
        instance = self.get_object()
        # 检查是否有子流程
        children_count = PlanFlow.objects.filter(
            parent_id=instance.id, deleted_at__isnull=True
        ).count()
        if children_count > 0:
            return ErrorResponse(message='该流程存在子流程，无法删除', code=400)
        instance.delete()
        return SuccessResponse(message='删除预案流程成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='获取树形流程',
        operation_description='获取指定预案的完整树形流程',
        responses={
            200: openapi.Response('获取成功', PlanFlowSerializer(many=True)),
        },
        tags=['预案流程']
    )
    @action(detail=False, methods=['get'], url_path='tree')
    def tree(self, request, **kwargs):
        """获取树形流程"""
        # 优先从URL路径参数获取plan_id（嵌套路由），如果没有则从query参数获取
        plan_id = kwargs.get('plan_pk') or request.query_params.get('plan_id', None)
        if not plan_id:
            return ErrorResponse(message='请指定plan_id参数', code=400)
        
        # 验证预案是否存在
        from .models import EmergencyPlan
        try:
            EmergencyPlan.objects.get(pk=plan_id, deleted_at__isnull=True)
        except EmergencyPlan.DoesNotExist:
            return ErrorResponse(message='预案不存在', code=404)
        
        # 获取所有顶级流程
        root_flows = PlanFlow.objects.filter(
            plan_id=plan_id, parent_id=0, deleted_at__isnull=True
        ).order_by('sort_order')
        
        serializer = self.get_serializer(root_flows, many=True)
        return SuccessResponse(data=serializer.data, message='获取树形流程成功')


class PlanTaskViewSet(viewsets.ModelViewSet):
    """
    预案任务管理视图集
    """
    queryset = PlanTask.objects.filter(deleted_at__isnull=True)
    serializer_class = PlanTaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['plan_id', 'flow_id', 'task_type', 'organization_id', 'priority']
    search_fields = ['task_code', 'task_name', 'task_description', 'task_requirement']
    ordering_fields = ['priority', 'sort_order', 'created_at']
    ordering = ['plan_id', 'priority', 'sort_order']

    @swagger_auto_schema(tags=['预案任务'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预案任务'])
    def create(self, request, *args, **kwargs):
        """创建预案任务"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成任务编码
        if not serializer.validated_data.get('task_code'):
            serializer.validated_data['task_code'] = f'TASK_{uuid.uuid4().hex[:16].upper()}'
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建预案任务成功')

    @swagger_auto_schema(tags=['预案任务'])
    def retrieve(self, request, *args, **kwargs):
        """获取预案任务详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预案任务'])
    def update(self, request, *args, **kwargs):
        """更新预案任务"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新预案任务成功')

    @swagger_auto_schema(tags=['预案任务'])
    def destroy(self, request, *args, **kwargs):
        """删除预案任务（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除预案任务成功')


class PlanExecutionViewSet(viewsets.ModelViewSet):
    """
    预案执行记录管理视图集
    """
    queryset = PlanExecution.objects.filter(deleted_at__isnull=True)
    serializer_class = PlanExecutionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['plan_id', 'warning_id', 'execution_type', 'execution_status']
    search_fields = ['execution_code', 'execution_result', 'execution_summary']
    ordering_fields = ['start_time', 'end_time', 'created_at']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['预案执行记录'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(start_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(start_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预案执行记录'])
    def create(self, request, *args, **kwargs):
        """创建预案执行记录"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成执行编码
        if not serializer.validated_data.get('execution_code'):
            serializer.validated_data['execution_code'] = f'EXEC_{uuid.uuid4().hex[:16].upper()}'
        # 设置指挥人
        serializer.save(command_user_id=request.user.id)
        return SuccessResponse(data=serializer.data, message='创建预案执行记录成功')

    @swagger_auto_schema(tags=['预案执行记录'])
    def retrieve(self, request, *args, **kwargs):
        """获取预案执行记录详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预案执行记录'])
    def update(self, request, *args, **kwargs):
        """更新预案执行记录"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新预案执行记录成功')

    @swagger_auto_schema(tags=['预案执行记录'])
    def destroy(self, request, *args, **kwargs):
        """删除预案执行记录（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除预案执行记录成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='启动执行',
        operation_description='启动预案执行',
        request_body=PlanExecutionStartSerializer,
        responses={
            200: openapi.Response('启动成功', PlanExecutionSerializer),
            400: '参数错误',
            404: '预案不存在',
        },
        tags=['预案执行记录']
    )
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """启动执行"""
        instance = self.get_object()
        if instance.execution_status != 0:
            return ErrorResponse(message='预案执行已启动或已完成，无法重复启动', code=400)
        
        serializer = PlanExecutionStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.execution_status = 1  # 执行中
        instance.start_time = serializer.validated_data.get('start_time') or timezone.now()
        if serializer.validated_data.get('warning_id'):
            instance.warning_id = serializer.validated_data['warning_id']
        if serializer.validated_data.get('execution_type'):
            instance.execution_type = serializer.validated_data['execution_type']
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='启动预案执行成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='更新执行状态',
        operation_description='更新预案执行状态',
        request_body=PlanExecutionUpdateStatusSerializer,
        responses={
            200: openapi.Response('更新成功', PlanExecutionSerializer),
            400: '参数错误',
            404: '执行记录不存在',
        },
        tags=['预案执行记录']
    )
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """更新执行状态"""
        instance = self.get_object()
        serializer = PlanExecutionUpdateStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.execution_status = serializer.validated_data['execution_status']
        if serializer.validated_data.get('current_flow_id'):
            instance.current_flow_id = serializer.validated_data['current_flow_id']
        if serializer.validated_data.get('execution_result'):
            instance.execution_result = serializer.validated_data['execution_result']
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='更新执行状态成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='完成执行',
        operation_description='完成预案执行',
        request_body=PlanExecutionCompleteSerializer,
        responses={
            200: openapi.Response('完成成功', PlanExecutionSerializer),
            400: '参数错误',
            404: '执行记录不存在',
        },
        tags=['预案执行记录']
    )
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """完成执行"""
        instance = self.get_object()
        if instance.execution_status == 2:
            return ErrorResponse(message='预案执行已完成，无需重复完成', code=400)
        
        serializer = PlanExecutionCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.execution_status = 2  # 已完成
        instance.end_time = serializer.validated_data.get('end_time') or timezone.now()
        if serializer.validated_data.get('execution_result'):
            instance.execution_result = serializer.validated_data['execution_result']
        if serializer.validated_data.get('execution_summary'):
            instance.execution_summary = serializer.validated_data['execution_summary']
        
        # 计算执行时长
        if instance.start_time and instance.end_time:
            duration = (instance.end_time - instance.start_time).total_seconds() / 60
            instance.duration = int(duration)
        
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='完成预案执行成功')


class PlanTaskExecutionViewSet(viewsets.ModelViewSet):
    """
    预案任务执行记录管理视图集
    """
    queryset = PlanTaskExecution.objects.filter(deleted_at__isnull=True)
    serializer_class = PlanTaskExecutionSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['execution_id', 'task_id', 'assign_user_id', 'task_status']
    search_fields = ['task_result', 'feedback_content']
    ordering_fields = ['assign_time', 'start_time', 'end_time', 'created_at']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['预案任务执行记录'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(assign_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(assign_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预案任务执行记录'])
    def create(self, request, *args, **kwargs):
        """创建预案任务执行记录"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 设置分配时间
        serializer.save(assign_time=timezone.now())
        return SuccessResponse(data=serializer.data, message='创建预案任务执行记录成功')

    @swagger_auto_schema(tags=['预案任务执行记录'])
    def retrieve(self, request, *args, **kwargs):
        """获取预案任务执行记录详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预案任务执行记录'])
    def update(self, request, *args, **kwargs):
        """更新预案任务执行记录"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新预案任务执行记录成功')

    @swagger_auto_schema(tags=['预案任务执行记录'])
    def destroy(self, request, *args, **kwargs):
        """删除预案任务执行记录（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除预案任务执行记录成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='接受任务',
        operation_description='接受任务执行',
        request_body=PlanTaskExecutionAcceptSerializer,
        responses={
            200: openapi.Response('接受成功', PlanTaskExecutionSerializer),
            400: '参数错误',
            404: '任务执行记录不存在',
        },
        tags=['预案任务执行记录']
    )
    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        """接受任务"""
        instance = self.get_object()
        if instance.task_status != 0:
            return ErrorResponse(message='任务状态不正确，无法接受', code=400)
        
        serializer = PlanTaskExecutionAcceptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.accept_time = serializer.validated_data.get('accept_time') or timezone.now()
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='接受任务成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='开始执行任务',
        operation_description='开始执行任务',
        request_body=PlanTaskExecutionStartSerializer,
        responses={
            200: openapi.Response('开始成功', PlanTaskExecutionSerializer),
            400: '参数错误',
            404: '任务执行记录不存在',
        },
        tags=['预案任务执行记录']
    )
    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        """开始执行任务"""
        instance = self.get_object()
        if instance.task_status not in [0, 1]:
            return ErrorResponse(message='任务状态不正确，无法开始执行', code=400)
        
        serializer = PlanTaskExecutionStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.task_status = 1  # 执行中
        instance.start_time = serializer.validated_data.get('start_time') or timezone.now()
        if not instance.accept_time:
            instance.accept_time = instance.start_time
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='开始执行任务成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='完成任务',
        operation_description='完成任务执行',
        request_body=PlanTaskExecutionCompleteSerializer,
        responses={
            200: openapi.Response('完成成功', PlanTaskExecutionSerializer),
            400: '参数错误',
            404: '任务执行记录不存在',
        },
        tags=['预案任务执行记录']
    )
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """完成任务"""
        instance = self.get_object()
        if instance.task_status != 1:
            return ErrorResponse(message='任务未在执行中，无法完成', code=400)
        
        serializer = PlanTaskExecutionCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.task_status = 2  # 已完成
        instance.end_time = serializer.validated_data.get('end_time') or timezone.now()
        if serializer.validated_data.get('task_result'):
            instance.task_result = serializer.validated_data['task_result']
        if serializer.validated_data.get('feedback_content'):
            instance.feedback_content = serializer.validated_data['feedback_content']
        instance.feedback_time = serializer.validated_data.get('feedback_time') or timezone.now()
        
        # 计算执行时长
        if instance.start_time and instance.end_time:
            duration = (instance.end_time - instance.start_time).total_seconds() / 60
            instance.duration = int(duration)
        
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='完成任务成功')

