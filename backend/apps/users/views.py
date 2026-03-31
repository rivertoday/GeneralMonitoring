"""
用户权限管理模块 - 视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.db.models import Q
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.common.response import SuccessResponse, ErrorResponse
from apps.common.pagination import StandardResultsSetPagination
from .models import User, Role, Permission, Organization
from .serializers import (
    UserListSerializer, UserDetailSerializer, UserPasswordSerializer, UserLoginSerializer,
    RoleSerializer, PermissionSerializer, PermissionTreeSerializer,
    OrganizationSerializer, OrganizationTreeSerializer
)
from .permissions import IsAdminUser, HasPermission


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    组织管理视图集
    """
    queryset = Organization.objects.filter(deleted_at__isnull=True)
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """根据action返回不同的序列化器"""
        if self.action == 'tree':
            return OrganizationTreeSerializer
        return OrganizationSerializer

    @swagger_auto_schema(tags=['组织管理'])
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取组织树形结构"""
        organizations = self.queryset.filter(parent_id=0).order_by('sort_order')
        serializer = self.get_serializer(organizations, many=True)
        return SuccessResponse(data=serializer.data, message='获取组织树成功')

    @swagger_auto_schema(tags=['组织管理'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['组织管理'])
    def create(self, request, *args, **kwargs):
        """创建组织"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建组织成功')

    @swagger_auto_schema(tags=['组织管理'])
    def retrieve(self, request, *args, **kwargs):
        """获取组织详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['组织管理'])
    def update(self, request, *args, **kwargs):
        """更新组织"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新组织成功')

    @swagger_auto_schema(tags=['组织管理'])
    def destroy(self, request, *args, **kwargs):
        """删除组织（软删除）"""
        instance = self.get_object()
        instance.delete()  # 软删除
        return SuccessResponse(message='删除组织成功')


class PermissionViewSet(viewsets.ModelViewSet):
    """
    权限管理视图集
    """
    queryset = Permission.objects.filter(deleted_at__isnull=True)
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """根据action返回不同的序列化器"""
        if self.action == 'tree':
            return PermissionTreeSerializer
        return PermissionSerializer

    @swagger_auto_schema(tags=['权限管理'])
    @action(detail=False, methods=['get'])
    def tree(self, request):
        """获取权限树形结构"""
        permissions = self.queryset.filter(parent_id=0).order_by('sort_order')
        serializer = self.get_serializer(permissions, many=True)
        return SuccessResponse(data=serializer.data, message='获取权限树成功')

    @swagger_auto_schema(tags=['权限管理'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['权限管理'])
    def create(self, request, *args, **kwargs):
        """创建权限"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建权限成功')

    @swagger_auto_schema(tags=['权限管理'])
    def retrieve(self, request, *args, **kwargs):
        """获取权限详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['权限管理'])
    def update(self, request, *args, **kwargs):
        """更新权限"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新权限成功')

    @swagger_auto_schema(tags=['权限管理'])
    def destroy(self, request, *args, **kwargs):
        """删除权限（软删除）"""
        instance = self.get_object()
        instance.delete()  # 软删除
        return SuccessResponse(message='删除权限成功')


class RoleViewSet(viewsets.ModelViewSet):
    """
    角色管理视图集
    """
    queryset = Role.objects.filter(deleted_at__isnull=True)
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = StandardResultsSetPagination

    @swagger_auto_schema(tags=['角色管理'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['角色管理'])
    def create(self, request, *args, **kwargs):
        """创建角色"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建角色成功')

    @swagger_auto_schema(tags=['角色管理'])
    def retrieve(self, request, *args, **kwargs):
        """获取角色详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['角色管理'])
    def update(self, request, *args, **kwargs):
        """更新角色"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新角色成功')

    @swagger_auto_schema(tags=['角色管理'])
    def destroy(self, request, *args, **kwargs):
        """删除角色（软删除）"""
        instance = self.get_object()
        instance.delete()  # 软删除
        return SuccessResponse(message='删除角色成功')


class UserViewSet(viewsets.ModelViewSet):
    """
    用户管理视图集
    """
    queryset = User.objects.filter(deleted_at__isnull=True)
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """根据action返回不同的序列化器"""
        if self.action == 'list':
            return UserListSerializer
        return UserDetailSerializer

    def get_queryset(self):
        """过滤查询集"""
        queryset = super().get_queryset()
        # 可以根据权限过滤数据
        username = self.request.query_params.get('username', None)
        status = self.request.query_params.get('status', None)
        organization_id = self.request.query_params.get('organization_id', None)

        if username:
            queryset = queryset.filter(username__icontains=username)
        if status is not None:
            queryset = queryset.filter(status=status)
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)

        return queryset

    @swagger_auto_schema(tags=['用户管理'])
    def list(self, request, *args, **kwargs):
        """列表查询"""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['用户管理'])
    def create(self, request, *args, **kwargs):
        """创建用户"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='创建用户成功')

    @swagger_auto_schema(tags=['用户管理'])
    def retrieve(self, request, *args, **kwargs):
        """获取用户详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(tags=['用户管理'])
    def update(self, request, *args, **kwargs):
        """更新用户"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新用户成功')

    @swagger_auto_schema(tags=['用户管理'])
    def destroy(self, request, *args, **kwargs):
        """删除用户（软删除）"""
        instance = self.get_object()
        instance.delete()  # 软删除
        return SuccessResponse(message='删除用户成功')

    @swagger_auto_schema(tags=['用户管理'])
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """修改密码"""
        user = self.get_object()
        serializer = UserPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 验证旧密码
        if not user.check_password(serializer.validated_data['old_password']):
            return ErrorResponse(message='旧密码错误', code=400)

        # 设置新密码
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return SuccessResponse(message='密码修改成功')

    @swagger_auto_schema(tags=['用户管理'])
    @action(detail=False, methods=['get'])
    def me(self, request):
        """获取当前用户信息"""
        serializer = UserDetailSerializer(request.user)
        return SuccessResponse(data=serializer.data)

    @swagger_auto_schema(method='put', tags=['用户管理'])
    @swagger_auto_schema(method='patch', tags=['用户管理'])
    @action(detail=False, methods=['put', 'patch'])
    def update_me(self, request):
        """更新当前用户信息"""
        serializer = UserDetailSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return SuccessResponse(data=serializer.data, message='更新成功')

