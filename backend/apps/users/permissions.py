"""
用户权限管理模块 - 权限类
"""
from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    检查用户是否为管理员
    可以通过角色判断，或者通过is_staff字段判断
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # 检查用户是否有管理员角色（可以根据实际需求调整角色编码）
        return request.user.roles.filter(role_code='admin', status=1, deleted_at__isnull=True).exists()


class HasPermission(permissions.BasePermission):
    """
    检查用户是否拥有指定权限
    使用方式：在ViewSet中设置 permission_classes = [HasPermission]
    并在ViewSet中定义 permission_required 属性
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        # 获取需要的权限编码
        permission_required = getattr(view, 'permission_required', None)
        if not permission_required:
            return True  # 如果没有指定权限要求，默认允许

        # 检查用户是否拥有该权限
        return request.user.has_permission(permission_required)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    对象级权限：只有对象的所有者可以编辑
    使用方式：在ViewSet中设置 permission_classes = [IsOwnerOrReadOnly]
    需要模型有user字段或created_by字段
    """
    def has_object_permission(self, request, view, obj):
        # 读取权限允许所有请求
        if request.method in permissions.SAFE_METHODS:
            return True

        # 写入权限只给对象的所有者
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        return False

