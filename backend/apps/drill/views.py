"""
演练监督模块 - 视图
"""
import uuid
from django.db.models import Count, Q, Avg
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.common.response import SuccessResponse, ErrorResponse
from apps.common.pagination import StandardResultsSetPagination
from .models import DrillEvent, DrillEvaluation, DrillSummary, DrillAnalysis
from .serializers import (
    DrillEventSerializer, DrillEventUpdateStatusSerializer,
    DrillEvaluationSerializer, DrillSummarySerializer, DrillAnalysisSerializer
)


class DrillEventViewSet(viewsets.ModelViewSet):
    """
    演练事件管理视图集
    """
    queryset = DrillEvent.objects.filter(deleted_at__isnull=True)
    serializer_class = DrillEventSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['organization_id', 'event_type', 'accident_type', 'drill_status', 'data_source']
    search_fields = ['event_code', 'event_name', 'description']
    ordering_fields = ['event_time', 'created_at']
    ordering = ['-event_time', '-created_at']

    @swagger_auto_schema(tags=['演练事件'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(event_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(event_time__lte=end_time)
        
        # 支持地理位置范围过滤
        min_lng = request.query_params.get('min_lng', None)
        max_lng = request.query_params.get('max_lng', None)
        min_lat = request.query_params.get('min_lat', None)
        max_lat = request.query_params.get('max_lat', None)
        if min_lng and max_lng:
            queryset = queryset.filter(longitude__gte=min_lng, longitude__lte=max_lng)
        if min_lat and max_lat:
            queryset = queryset.filter(latitude__gte=min_lat, latitude__lte=max_lat)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['演练事件'])
    def create(self, request, *args, **kwargs):
        """创建演练事件"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成事件编码
        if not serializer.validated_data.get('event_code'):
            serializer.validated_data['event_code'] = f'DRILL_{uuid.uuid4().hex[:16].upper()}'
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建演练事件成功')

    @swagger_auto_schema(tags=['演练事件'])
    def retrieve(self, request, *args, **kwargs):
        """获取演练事件详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['演练事件'])
    def update(self, request, *args, **kwargs):
        """更新演练事件"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新演练事件成功')

    @swagger_auto_schema(tags=['演练事件'])
    def destroy(self, request, *args, **kwargs):
        """删除演练事件（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除演练事件成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='更新演练状态',
        operation_description='更新演练事件状态',
        request_body=DrillEventUpdateStatusSerializer,
        responses={
            200: openapi.Response('更新成功', DrillEventSerializer),
            400: '参数错误',
            404: '演练事件不存在',
        },
        tags=['演练事件']
    )
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """更新演练状态"""
        instance = self.get_object()
        serializer = DrillEventUpdateStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.drill_status = serializer.validated_data['drill_status']
        instance.save()

        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='更新演练状态成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='演练事件统计',
        operation_description='获取演练事件统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['演练事件']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """演练事件统计"""
        queryset = self.get_queryset()
        
        # 时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(event_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(event_time__lte=end_time)
        
        # 按事件类型统计
        type_stats = queryset.values('event_type').annotate(count=Count('id'))
        
        # 按事故类型统计
        accident_stats = queryset.values('accident_type').annotate(count=Count('id')).exclude(accident_type__isnull=True)
        
        # 按演练状态统计
        status_stats = queryset.values('drill_status').annotate(count=Count('id'))
        
        # 按数据来源统计
        source_stats = queryset.values('data_source').annotate(count=Count('id')).exclude(data_source__isnull=True)
        
        # 总受伤人数和死亡人数
        total_injured = queryset.aggregate(total=Count('injured_count'))['total'] or 0
        total_death = queryset.aggregate(total=Count('death_count'))['total'] or 0

        statistics_data = {
            'total_count': queryset.count(),
            'type_stats': list(type_stats),
            'accident_stats': list(accident_stats),
            'status_stats': list(status_stats),
            'source_stats': list(source_stats),
            'total_injured': total_injured,
            'total_death': total_death,
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')


class DrillEvaluationViewSet(viewsets.ModelViewSet):
    """
    演练评价管理视图集
    """
    queryset = DrillEvaluation.objects.filter(deleted_at__isnull=True)
    serializer_class = DrillEvaluationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['event_id', 'node_type', 'evaluation_level', 'evaluator_id']
    search_fields = ['node_name', 'evaluation_item', 'evaluation_content']
    ordering_fields = ['evaluation_time', 'created_at']
    ordering = ['-evaluation_time', '-created_at']

    @swagger_auto_schema(tags=['演练评价'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(evaluation_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(evaluation_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['演练评价'])
    def create(self, request, *args, **kwargs):
        """创建演练评价"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 设置评价人
        serializer.save(evaluator_id=request.user.id)
        return SuccessResponse(data=serializer.data, message='创建演练评价成功')

    @swagger_auto_schema(tags=['演练评价'])
    def retrieve(self, request, *args, **kwargs):
        """获取演练评价详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['演练评价'])
    def update(self, request, *args, **kwargs):
        """更新演练评价"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新演练评价成功')

    @swagger_auto_schema(tags=['演练评价'])
    def destroy(self, request, *args, **kwargs):
        """删除演练评价（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除演练评价成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='演练评价统计',
        operation_description='获取演练评价统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['演练评价']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """演练评价统计"""
        queryset = self.get_queryset()
        
        # 按节点类型统计
        node_stats = queryset.values('node_type').annotate(count=Count('id'))
        
        # 按评价等级统计
        level_stats = queryset.values('evaluation_level').annotate(count=Count('id')).exclude(evaluation_level__isnull=True)
        
        # 平均得分
        avg_score = queryset.exclude(evaluation_score__isnull=True).aggregate(avg=Avg('evaluation_score'))['avg']
        if avg_score:
            avg_score = float(avg_score)

        statistics_data = {
            'total_count': queryset.count(),
            'node_stats': list(node_stats),
            'level_stats': list(level_stats),
            'avg_score': avg_score,
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')


class DrillSummaryViewSet(viewsets.ModelViewSet):
    """
    演练总结管理视图集
    """
    queryset = DrillSummary.objects.filter(deleted_at__isnull=True)
    serializer_class = DrillSummarySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['event_id', 'overall_level', 'summary_user_id']
    search_fields = ['summary_title', 'description']
    ordering_fields = ['summary_time', 'created_at']
    ordering = ['-summary_time', '-created_at']

    @swagger_auto_schema(tags=['演练总结'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(summary_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(summary_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['演练总结'])
    def create(self, request, *args, **kwargs):
        """创建演练总结"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 检查是否已存在该事件的总结
        event_id = serializer.validated_data.get('event_id')
        if event_id:
            existing = DrillSummary.objects.filter(event_id=event_id, deleted_at__isnull=True).first()
            if existing:
                return ErrorResponse(message='该演练事件已存在总结，请更新现有总结', code=400)
        # 设置总结人
        serializer.save(summary_user_id=request.user.id)
        return SuccessResponse(data=serializer.data, message='创建演练总结成功')

    @swagger_auto_schema(tags=['演练总结'])
    def retrieve(self, request, *args, **kwargs):
        """获取演练总结详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['演练总结'])
    def update(self, request, *args, **kwargs):
        """更新演练总结"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新演练总结成功')

    @swagger_auto_schema(tags=['演练总结'])
    def destroy(self, request, *args, **kwargs):
        """删除演练总结（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除演练总结成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='演练总结统计',
        operation_description='获取演练总结统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['演练总结']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """演练总结统计"""
        queryset = self.get_queryset()
        
        # 按总体等级统计
        level_stats = queryset.values('overall_level').annotate(count=Count('id')).exclude(overall_level__isnull=True)
        
        # 平均得分
        avg_score = queryset.exclude(overall_score__isnull=True).aggregate(avg=Avg('overall_score'))['avg']
        if avg_score:
            avg_score = float(avg_score)

        statistics_data = {
            'total_count': queryset.count(),
            'level_stats': list(level_stats),
            'avg_score': avg_score,
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')


class DrillAnalysisViewSet(viewsets.ModelViewSet):
    """
    演练分析管理视图集
    """
    queryset = DrillAnalysis.objects.all()
    serializer_class = DrillAnalysisSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['stat_type', 'organization_id', 'drill_type', 'accident_type']
    search_fields = []
    ordering_fields = ['stat_date', 'created_at']
    ordering = ['-stat_date', '-created_at']

    @swagger_auto_schema(tags=['演练分析'])
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

    @swagger_auto_schema(tags=['演练分析'])
    def create(self, request, *args, **kwargs):
        """创建演练分析"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建演练分析成功')

    @swagger_auto_schema(tags=['演练分析'])
    def retrieve(self, request, *args, **kwargs):
        """获取演练分析详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['演练分析'])
    def update(self, request, *args, **kwargs):
        """更新演练分析"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新演练分析成功')

    @swagger_auto_schema(tags=['演练分析'])
    def destroy(self, request, *args, **kwargs):
        """删除演练分析"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除演练分析成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='演练分析统计',
        operation_description='获取演练分析统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['演练分析']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """演练分析统计"""
        queryset = self.get_queryset()
        
        # 按统计类型统计
        stat_type_stats = queryset.values('stat_type').annotate(count=Count('id'))
        
        # 按演练类型统计
        drill_type_stats = queryset.values('drill_type').annotate(count=Count('id')).exclude(drill_type__isnull=True)
        
        # 按事故类型统计
        accident_type_stats = queryset.values('accident_type').annotate(count=Count('id')).exclude(accident_type__isnull=True)
        
        # 总演练次数和完成次数
        total_drill_count = queryset.aggregate(total=Count('drill_count'))['total'] or 0
        total_completed = queryset.aggregate(total=Count('completed_count'))['total'] or 0
        
        # 平均得分
        avg_score = queryset.exclude(avg_score__isnull=True).aggregate(avg=Avg('avg_score'))['avg']
        if avg_score:
            avg_score = float(avg_score)

        statistics_data = {
            'total_count': queryset.count(),
            'stat_type_stats': list(stat_type_stats),
            'drill_type_stats': list(drill_type_stats),
            'accident_type_stats': list(accident_type_stats),
            'total_drill_count': total_drill_count,
            'total_completed': total_completed,
            'avg_score': avg_score,
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')

