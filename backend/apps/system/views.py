"""
系统管理模块 - 视图
"""
import uuid
from django.db.models import Count
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
from .models import DataSource, MessageTemplate
from .serializers import DataSourceSerializer, MessageTemplateSerializer


class DataSourceViewSet(viewsets.ModelViewSet):
    """
    数据源管理视图集
    """
    queryset = DataSource.objects.filter(deleted_at__isnull=True)
    serializer_class = DataSourceSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['source_type', 'industry_type', 'status']
    search_fields = ['source_code', 'source_name', 'description']
    ordering_fields = ['created_at', 'source_type']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['数据源'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['数据源'])
    def create(self, request, *args, **kwargs):
        """创建数据源"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成数据源编码
        if not serializer.validated_data.get('source_code'):
            serializer.validated_data['source_code'] = f'DS_{uuid.uuid4().hex[:16].upper()}'
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建数据源成功')

    @swagger_auto_schema(tags=['数据源'])
    def retrieve(self, request, *args, **kwargs):
        """获取数据源详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['数据源'])
    def update(self, request, *args, **kwargs):
        """更新数据源"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新数据源成功')

    @swagger_auto_schema(tags=['数据源'])
    def destroy(self, request, *args, **kwargs):
        """删除数据源（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除数据源成功')

    @swagger_auto_schema(
        method='post',
        operation_summary='同步数据源',
        operation_description='手动触发数据源同步',
        responses={
            200: openapi.Response('同步成功'),
            400: '参数错误',
            404: '数据源不存在',
        },
        tags=['数据源']
    )
    @action(detail=True, methods=['post'])
    def sync(self, request, pk=None):
        """同步数据源"""
        instance = self.get_object()
        # 更新最后同步时间
        instance.last_sync_at = timezone.now()
        instance.save()
        
        # TODO: 这里可以添加实际的数据同步逻辑
        # 例如：调用API、连接数据库、读取文件等
        
        result_serializer = self.get_serializer(instance)
        return SuccessResponse(data=result_serializer.data, message='数据源同步成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='数据源统计',
        operation_description='获取数据源统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['数据源']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """数据源统计"""
        queryset = self.get_queryset()
        
        # 按数据源类型统计
        type_stats = queryset.values('source_type').annotate(count=Count('id'))
        
        # 按行业类型统计
        industry_stats = queryset.values('industry_type').annotate(count=Count('id'))
        
        # 按状态统计
        status_stats = queryset.values('status').annotate(count=Count('id'))

        statistics_data = {
            'total_count': queryset.count(),
            'type_stats': list(type_stats),
            'industry_stats': list(industry_stats),
            'status_stats': list(status_stats),
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')


class MessageTemplateViewSet(viewsets.ModelViewSet):
    """
    消息模板管理视图集
    """
    queryset = MessageTemplate.objects.filter(deleted_at__isnull=True)
    serializer_class = MessageTemplateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['template_type', 'message_type', 'status']
    search_fields = ['template_code', 'template_name', 'content', 'description']
    ordering_fields = ['created_at', 'template_type']
    ordering = ['-created_at']

    @swagger_auto_schema(tags=['消息模板'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['消息模板'])
    def create(self, request, *args, **kwargs):
        """创建消息模板"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 生成模板编码
        if not serializer.validated_data.get('template_code'):
            serializer.validated_data['template_code'] = f'TEMPLATE_{uuid.uuid4().hex[:16].upper()}'
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建消息模板成功')

    @swagger_auto_schema(tags=['消息模板'])
    def retrieve(self, request, *args, **kwargs):
        """获取消息模板详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['消息模板'])
    def update(self, request, *args, **kwargs):
        """更新消息模板"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新消息模板成功')

    @swagger_auto_schema(tags=['消息模板'])
    def destroy(self, request, *args, **kwargs):
        """删除消息模板（软删除）"""
        instance = self.get_object()
        instance.delete()
        return SuccessResponse(message='删除消息模板成功')

    @swagger_auto_schema(
        method='get',
        operation_summary='消息模板统计',
        operation_description='获取消息模板统计数据',
        responses={
            200: openapi.Response('获取成功'),
        },
        tags=['消息模板']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """消息模板统计"""
        queryset = self.get_queryset()
        
        # 按模板类型统计
        type_stats = queryset.values('template_type').annotate(count=Count('id'))
        
        # 按消息类型统计
        message_type_stats = queryset.values('message_type').annotate(count=Count('id'))
        
        # 按状态统计
        status_stats = queryset.values('status').annotate(count=Count('id'))

        statistics_data = {
            'total_count': queryset.count(),
            'type_stats': list(type_stats),
            'message_type_stats': list(message_type_stats),
            'status_stats': list(status_stats),
        }

        return SuccessResponse(data=statistics_data, message='获取统计成功')

