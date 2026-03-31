"""
安全态势展示模块 - 视图
"""
import uuid
from django.db.models import Count, Q, Sum
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
from .models import (
    SafetyResource, SafetyTarget, Shelter, IndustryStatus,
    RegionStatus, MonitorData, WarningEvent, HazardSource, VideoMonitor
)
from .serializers import (
    SafetyResourceSerializer, SafetyTargetSerializer, ShelterSerializer,
    IndustryStatusSerializer, RegionStatusSerializer, MonitorDataSerializer,
    WarningEventSerializer, HazardSourceSerializer, VideoMonitorSerializer
)


class SafetyResourceViewSet(viewsets.ModelViewSet):
    """
    安全资源管理视图集
    """
    queryset = SafetyResource.objects.filter(deleted_at__isnull=True)
    serializer_class = SafetyResourceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['resource_type', 'sub_type', 'organization_id', 'status']
    search_fields = ['resource_code', 'resource_name', 'description']
    ordering_fields = ['created_at', 'resource_type']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['安全资源'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
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

    @swagger_auto_schema(tags=['安全资源'])
    def create(self, request, *args, **kwargs):
        """创建安全资源"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成资源编码
        if not serializer.validated_data.get('resource_code'):
            serializer.validated_data['resource_code'] = f'RES_{uuid.uuid4().hex[:16].upper()}'
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建安全资源成功')

    @swagger_auto_schema(tags=['安全资源'])
    def retrieve(self, request, *args, **kwargs):
        """获取安全资源详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['安全资源'])
    def update(self, request, *args, **kwargs):
        """更新安全资源"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新安全资源成功')

    @swagger_auto_schema(tags=['安全资源'])
    def destroy(self, request, *args, **kwargs):
        """删除安全资源（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除安全资源成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='资源统计',
        operation_description='获取安全资源统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['安全资源']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """资源统计"""
        queryset = self.get_queryset()
        
        # 按资源类型统计
        type_stats = queryset.values('resource_type').annotate(count=Count('id'))
        
        # 按子类型统计
        sub_type_stats = queryset.values('sub_type').annotate(count=Count('id'))
        
        # 按状态统计
        status_stats = queryset.values('status').annotate(count=Count('id'))
        
        # 救援队伍统计
        team_count = queryset.filter(resource_type=1).count()
        team_capacity = queryset.filter(resource_type=1).aggregate(total=Sum('capacity'))['total'] or 0
        
        # 应急专家统计
        expert_count = queryset.filter(resource_type=2).count()
        
        # 物资装备统计
        equipment_count = queryset.filter(resource_type=3).count()
        equipment_quantity = queryset.filter(resource_type=3).aggregate(total=Sum('quantity'))['total'] or 0

        statistics_data = {
            'total_count': queryset.count(),
            'type_stats': list(type_stats),
            'sub_type_stats': list(sub_type_stats),
            'status_stats': list(status_stats),
            'team_count': team_count,
            'team_capacity': team_capacity,
            'expert_count': expert_count,
            'equipment_count': equipment_count,
            'equipment_quantity': equipment_quantity,
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')


class SafetyTargetViewSet(viewsets.ModelViewSet):
    """
    防护目标管理视图集
    """
    queryset = SafetyTarget.objects.filter(deleted_at__isnull=True)
    serializer_class = SafetyTargetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['target_type', 'risk_level', 'status']
    search_fields = ['target_code', 'target_name', 'description']
    ordering_fields = ['created_at', 'target_type']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['防护目标'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
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

    @swagger_auto_schema(tags=['防护目标'])
    def create(self, request, *args, **kwargs):
        """创建防护目标"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成目标编码
        if not serializer.validated_data.get('target_code'):
            serializer.validated_data['target_code'] = f'TARGET_{uuid.uuid4().hex[:16].upper()}'
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建防护目标成功')

    @swagger_auto_schema(tags=['防护目标'])
    def retrieve(self, request, *args, **kwargs):
        """获取防护目标详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['防护目标'])
    def update(self, request, *args, **kwargs):
        """更新防护目标"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新防护目标成功')

    @swagger_auto_schema(tags=['防护目标'])
    def destroy(self, request, *args, **kwargs):
        """删除防护目标（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除防护目标成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='防护目标统计',
        operation_description='获取防护目标统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['防护目标']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """防护目标统计"""
        queryset = self.get_queryset()
        
        # 按目标类型统计
        type_stats = queryset.values('target_type').annotate(count=Count('id'))
        
        # 按风险等级统计
        risk_stats = queryset.values('risk_level').annotate(count=Count('id'))
        
        # 总人口数
        total_population = queryset.aggregate(total=Sum('population'))['total'] or 0

        statistics_data = {
            'total_count': queryset.count(),
            'type_stats': list(type_stats),
            'risk_stats': list(risk_stats),
            'total_population': total_population,
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')


class ShelterViewSet(viewsets.ModelViewSet):
    """
    避难场所管理视图集
    """
    queryset = Shelter.objects.filter(deleted_at__isnull=True)
    serializer_class = ShelterSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['shelter_type', 'status']
    search_fields = ['shelter_code', 'shelter_name', 'description']
    ordering_fields = ['created_at', 'shelter_type']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['避难场所'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
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

    @swagger_auto_schema(tags=['避难场所'])
    def create(self, request, *args, **kwargs):
        """创建避难场所"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成场所编码
        if not serializer.validated_data.get('shelter_code'):
            serializer.validated_data['shelter_code'] = f'SHELTER_{uuid.uuid4().hex[:16].upper()}'
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建避难场所成功')

    @swagger_auto_schema(tags=['避难场所'])
    def retrieve(self, request, *args, **kwargs):
        """获取避难场所详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['避难场所'])
    def update(self, request, *args, **kwargs):
        """更新避难场所"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新避难场所成功')

    @swagger_auto_schema(tags=['避难场所'])
    def destroy(self, request, *args, **kwargs):
        """删除避难场所（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除避难场所成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='避难场所统计',
        operation_description='获取避难场所统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['避难场所']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """避难场所统计"""
        queryset = self.get_queryset()
        
        # 按场所类型统计
        type_stats = queryset.values('shelter_type').annotate(count=Count('id'))
        
        # 总容纳能力
        total_capacity = queryset.aggregate(total=Sum('capacity'))['total'] or 0

        statistics_data = {
            'total_count': queryset.count(),
            'type_stats': list(type_stats),
            'total_capacity': total_capacity,
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')


class IndustryStatusViewSet(viewsets.ModelViewSet):
    """
    行业态势管理视图集
    """
    queryset = IndustryStatus.objects.all()
    serializer_class = IndustryStatusSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['industry_type']
    search_fields = []
    ordering_fields = ['stat_date', 'created_at']
    ordering = ['-stat_date', '-created_at']

    @swagger_auto_schema(tags=['行业态势'])
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

    @swagger_auto_schema(tags=['行业态势'])
    def create(self, request, *args, **kwargs):
        """创建行业态势"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建行业态势成功')

    @swagger_auto_schema(tags=['行业态势'])
    def retrieve(self, request, *args, **kwargs):
        """获取行业态势详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['行业态势'])
    def update(self, request, *args, **kwargs):
        """更新行业态势"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新行业态势成功')

    @swagger_auto_schema(tags=['行业态势'])
    def destroy(self, request, *args, **kwargs):
        """删除行业态势"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除行业态势成功')


class RegionStatusViewSet(viewsets.ModelViewSet):
    """
    区域态势管理视图集
    """
    queryset = RegionStatus.objects.all()
    serializer_class = RegionStatusSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['street', 'risk_color']
    search_fields = ['street']
    ordering_fields = ['stat_date', 'created_at']
    ordering = ['-stat_date', '-created_at']

    @swagger_auto_schema(tags=['区域态势'])
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

    @swagger_auto_schema(tags=['区域态势'])
    def create(self, request, *args, **kwargs):
        """创建区域态势"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建区域态势成功')

    @swagger_auto_schema(tags=['区域态势'])
    def retrieve(self, request, *args, **kwargs):
        """获取区域态势详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['区域态势'])
    def update(self, request, *args, **kwargs):
        """更新区域态势"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新区域态势成功')

    @swagger_auto_schema(tags=['区域态势'])
    def destroy(self, request, *args, **kwargs):
        """删除区域态势"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除区域态势成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='四色图数据',
        operation_description='获取四色图渲染数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['区域态势']
    )
    @action(detail=False, methods=['get'])
    def color_map(self, request):
        """四色图数据"""
        # 获取最新日期的区域态势数据
        latest_date = RegionStatus.objects.order_by('-stat_date').first()
        if not latest_date:
            return SuccessResponse(data=[], message='暂无数据')
        
        queryset = RegionStatus.objects.filter(stat_date=latest_date.stat_date)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data, message='获取四色图数据成功')


class MonitorDataViewSet(viewsets.ModelViewSet):
    """
    监测数据管理视图集
    """
    queryset = MonitorData.objects.all()
    serializer_class = MonitorDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['monitor_id', 'industry_type', 'online_status']
    search_fields = []
    ordering_fields = ['data_time', 'created_at']
    ordering = ['-data_time', '-created_at']

    @swagger_auto_schema(tags=['监测数据'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(data_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(data_time__lte=end_time)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['监测数据'])
    def create(self, request, *args, **kwargs):
        """创建监测数据"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建监测数据成功')

    @swagger_auto_schema(tags=['监测数据'])
    def retrieve(self, request, *args, **kwargs):
        """获取监测数据详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['监测数据'])
    def update(self, request, *args, **kwargs):
        """更新监测数据"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新监测数据成功')

    @swagger_auto_schema(tags=['监测数据'])
    def destroy(self, request, *args, **kwargs):
        """删除监测数据"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除监测数据成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='监测数据统计',
        operation_description='获取监测数据统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['监测数据']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """监测数据统计"""
        queryset = self.get_queryset()
        
        # 时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(data_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(data_time__lte=end_time)
        
        # 按行业类型统计
        industry_stats = queryset.values('industry_type').annotate(count=Count('id'))
        
        # 按在线状态统计
        online_stats = queryset.values('online_status').annotate(count=Count('id'))
        
        # 在线监测点数量
        online_count = queryset.filter(online_status=1).count()
        offline_count = queryset.filter(online_status=0).count()

        statistics_data = {
            'total_count': queryset.count(),
            'industry_stats': list(industry_stats),
            'online_stats': list(online_stats),
            'online_count': online_count,
            'offline_count': offline_count,
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')


class WarningEventViewSet(viewsets.ModelViewSet):
    """
    预警事件管理视图集
    """
    queryset = WarningEvent.objects.filter(deleted_at__isnull=True)
    serializer_class = WarningEventSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['warning_id', 'warning_level_id', 'industry_type', 'warning_type', 'warning_status']
    search_fields = ['warning_code', 'warning_title', 'description']
    ordering_fields = ['warning_time', 'created_at']
    ordering = ['-warning_time', '-created_at']

    @swagger_auto_schema(tags=['预警事件'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        # 如果 WarningEvent 表为空，先尝试从 RiskWarning 同步数据
        if not WarningEvent.objects.filter(deleted_at__isnull=True).exists():
            self._sync_from_risk_warnings()
        
        queryset = self.filter_queryset(self.get_queryset())
        # 支持时间范围过滤
        start_time = request.query_params.get('start_time', None)
        end_time = request.query_params.get('end_time', None)
        if start_time:
            queryset = queryset.filter(warning_time__gte=start_time)
        if end_time:
            queryset = queryset.filter(warning_time__lte=end_time)
        
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
    
    def _sync_from_risk_warnings(self):
        """从 RiskWarning 同步数据到 WarningEvent"""
        try:
            from apps.risk.models import RiskWarning
            
            # 获取所有未删除的 RiskWarning
            risk_warnings = RiskWarning.objects.filter(deleted_at__isnull=True)
            
            synced_count = 0
            for risk_warning in risk_warnings:
                # 检查是否已经存在对应的 WarningEvent
                existing_event = WarningEvent.objects.filter(
                    warning_id=risk_warning.id,
                    deleted_at__isnull=True
                ).first()
                
                if existing_event:
                    # 如果已存在，更新数据
                    existing_event.warning_code = risk_warning.warning_code
                    existing_event.warning_level_id = risk_warning.warning_level.id if risk_warning.warning_level else None
                    existing_event.industry_type = risk_warning.industry_type
                    existing_event.warning_type = risk_warning.warning_type
                    existing_event.warning_title = risk_warning.warning_title
                    existing_event.longitude = risk_warning.longitude
                    existing_event.latitude = risk_warning.latitude
                    existing_event.street = risk_warning.street
                    existing_event.address = risk_warning.address
                    existing_event.warning_time = risk_warning.warning_time
                    existing_event.warning_status = risk_warning.warning_status
                    existing_event.description = risk_warning.warning_content[:255] if risk_warning.warning_content else None
                    existing_event.save()
                else:
                    # 如果不存在，创建新的 WarningEvent
                    WarningEvent.objects.create(
                        warning_id=risk_warning.id,
                        warning_code=risk_warning.warning_code,
                        warning_level_id=risk_warning.warning_level.id if risk_warning.warning_level else None,
                        industry_type=risk_warning.industry_type,
                        warning_type=risk_warning.warning_type,
                        warning_title=risk_warning.warning_title,
                        longitude=risk_warning.longitude,
                        latitude=risk_warning.latitude,
                        street=risk_warning.street,
                        address=risk_warning.address,
                        warning_time=risk_warning.warning_time,
                        warning_status=risk_warning.warning_status,
                        description=risk_warning.warning_content[:255] if risk_warning.warning_content else None,
                    )
                    synced_count += 1
            
            if synced_count > 0:
                print(f'已从 RiskWarning 同步 {synced_count} 条数据到 WarningEvent')
        except Exception as e:
            print(f'同步 RiskWarning 数据到 WarningEvent 时出错: {e}')

    @swagger_auto_schema(tags=['预警事件'])
    def create(self, request, *args, **kwargs):
        """创建预警事件"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成预警事件编码
        if not serializer.validated_data.get('warning_code'):
            serializer.validated_data['warning_code'] = f'WARN_EVENT_{uuid.uuid4().hex[:16].upper()}'
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建预警事件成功')

    @swagger_auto_schema(tags=['预警事件'])
    def retrieve(self, request, *args, **kwargs):
        """获取预警事件详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['预警事件'])
    def update(self, request, *args, **kwargs):
        """更新预警事件"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新预警事件成功')

    @swagger_auto_schema(tags=['预警事件'])
    def destroy(self, request, *args, **kwargs):
        """删除预警事件（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除预警事件成功')


class HazardSourceViewSet(viewsets.ModelViewSet):
    """
    危险源管理视图集
    """
    queryset = HazardSource.objects.filter(deleted_at__isnull=True)
    serializer_class = HazardSourceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['source_type', 'industry_type', 'organization_id', 'risk_level', 'status']
    search_fields = ['source_code', 'source_name', 'description']
    ordering_fields = ['created_at', 'source_type']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['危险源'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
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

    @swagger_auto_schema(tags=['危险源'])
    def create(self, request, *args, **kwargs):
        """创建危险源"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成危险源编码
        if not serializer.validated_data.get('source_code'):
            serializer.validated_data['source_code'] = f'HAZARD_{uuid.uuid4().hex[:16].upper()}'
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建危险源成功')

    @swagger_auto_schema(tags=['危险源'])
    def retrieve(self, request, *args, **kwargs):
        """获取危险源详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['危险源'])
    def update(self, request, *args, **kwargs):
        """更新危险源"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新危险源成功')

    @swagger_auto_schema(tags=['危险源'])
    def destroy(self, request, *args, **kwargs):
        """删除危险源（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除危险源成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='危险源统计',
        operation_description='获取危险源统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['危险源']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """危险源统计"""
        queryset = self.get_queryset()
        
        # 按危险源类型统计
        type_stats = queryset.values('source_type').annotate(count=Count('id'))
        
        # 按行业类型统计
        industry_stats = queryset.values('industry_type').annotate(count=Count('id'))
        
        # 按风险等级统计
        risk_stats = queryset.values('risk_level').annotate(count=Count('id'))

        statistics_data = {
            'total_count': queryset.count(),
            'type_stats': list(type_stats),
            'industry_stats': list(industry_stats),
            'risk_stats': list(risk_stats),
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')


class VideoMonitorViewSet(viewsets.ModelViewSet):
    """
    视频监控设施管理视图集
    """
    queryset = VideoMonitor.objects.filter(deleted_at__isnull=True)
    serializer_class = VideoMonitorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['monitor_type', 'industry_type', 'online_status', 'organization_id', 'status']
    search_fields = ['monitor_code', 'monitor_name', 'description']
    ordering_fields = ['created_at', 'monitor_type']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['视频监控设施'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
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

    @swagger_auto_schema(tags=['视频监控设施'])
    def create(self, request, *args, **kwargs):
        """创建视频监控设施"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成监控设施编码
        if not serializer.validated_data.get('monitor_code'):
            serializer.validated_data['monitor_code'] = f'VIDEO_{uuid.uuid4().hex[:16].upper()}'
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建视频监控设施成功')

    @swagger_auto_schema(tags=['视频监控设施'])
    def retrieve(self, request, *args, **kwargs):
        """获取视频监控设施详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['视频监控设施'])
    def update(self, request, *args, **kwargs):
        """更新视频监控设施"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新视频监控设施成功')

    @swagger_auto_schema(tags=['视频监控设施'])
    def destroy(self, request, *args, **kwargs):
        """删除视频监控设施（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除视频监控设施成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='附近监控设施',
        operation_description='根据指定位置查询附近一定范围内的视频监控设施',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['视频监控设施']
    )
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """附近监控设施"""
        longitude = request.query_params.get('longitude', None)
        latitude = request.query_params.get('latitude', None)
        radius = request.query_params.get('radius', 1000)  # 默认1000米
        
        if not longitude or not latitude:
            return ErrorResponse(message='请指定longitude和latitude参数', code=400)
        
        try:
            longitude = float(longitude)
            latitude = float(latitude)
            radius = float(radius)
        except ValueError:
            return ErrorResponse(message='参数格式错误', code=400)
        
        # 简单的矩形范围查询（实际应该使用空间查询）
        # 1度经度约等于111km，1度纬度约等于111km
        lng_offset = radius / 111000
        lat_offset = radius / 111000
        
        queryset = VideoMonitor.objects.filter(
            deleted_at__isnull=True,
            longitude__gte=longitude - lng_offset,
            longitude__lte=longitude + lng_offset,
            latitude__gte=latitude - lat_offset,
            latitude__lte=latitude + lat_offset,
        )
        
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data, message='获取附近监控设施成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='视频监控统计',
        operation_description='获取视频监控设施统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['视频监控设施']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """视频监控统计"""
        queryset = self.get_queryset()
        
        # 按监控类型统计
        type_stats = queryset.values('monitor_type').annotate(count=Count('id'))
        
        # 按行业类型统计
        industry_stats = queryset.values('industry_type').annotate(count=Count('id'))
        
        # 按在线状态统计
        online_stats = queryset.values('online_status').annotate(count=Count('id'))
        
        # 在线数量
        online_count = queryset.filter(online_status=1).count()
        offline_count = queryset.filter(online_status=0).count()

        statistics_data = {
            'total_count': queryset.count(),
            'type_stats': list(type_stats),
            'industry_stats': list(industry_stats),
            'online_stats': list(online_stats),
            'online_count': online_count,
            'offline_count': offline_count,
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')

