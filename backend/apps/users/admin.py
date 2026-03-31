"""
用户权限管理模块 - Django Admin配置
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role, Permission, Organization, UserRole, RolePermission


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """组织管理"""
    list_display = ['id', 'org_code', 'org_name', 'parent_id', 'org_type', 'level', 'status', 'created_at']
    list_filter = ['org_type', 'status', 'created_at']
    search_fields = ['org_code', 'org_name', 'leader', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('org_code', 'org_name', 'parent_id', 'org_type', 'level')
        }),
        ('详细信息', {
            'fields': ('leader', 'phone', 'address', 'description', 'status', 'sort_order', 'remark')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'deleted_at')
        }),
    )


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    """权限管理"""
    list_display = ['id', 'permission_code', 'permission_name', 'permission_type', 'parent_id', 'status', 'sort_order']
    list_filter = ['permission_type', 'status', 'created_at']
    search_fields = ['permission_code', 'permission_name', 'api_path']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('permission_code', 'permission_name', 'permission_type', 'parent_id', 'status', 'sort_order')
        }),
        ('菜单配置（菜单类型）', {
            'fields': ('path', 'component', 'icon'),
            'classes': ('collapse',)
        }),
        ('接口配置（接口类型）', {
            'fields': ('api_path', 'http_method'),
            'classes': ('collapse',)
        }),
        ('其他信息', {
            'fields': ('description', 'remark', 'created_at', 'updated_at', 'deleted_at')
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    """角色管理"""
    list_display = ['id', 'role_code', 'role_name', 'status', 'sort_order', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['role_code', 'role_name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = []  # 可以添加权限的多选字段
    fieldsets = (
        ('基本信息', {
            'fields': ('role_code', 'role_name', 'description', 'status', 'sort_order', 'remark')
        }),
        ('时间信息', {
            'fields': ('created_at', 'updated_at', 'deleted_at')
        }),
    )


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    """用户角色关联管理"""
    list_display = ['id', 'user', 'role', 'created_at']
    list_filter = ['created_at', 'role']
    search_fields = ['user__username', 'role__role_name']


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """角色权限关联管理"""
    list_display = ['id', 'role', 'permission', 'created_at']
    list_filter = ['created_at', 'role', 'permission']
    search_fields = ['role__role_name', 'permission__permission_name']


class UserRoleInline(admin.TabularInline):
    """用户角色关联内联管理"""
    model = UserRole
    extra = 1
    verbose_name = '角色'
    verbose_name_plural = '用户角色'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """用户管理"""
    list_display = ['id', 'username', 'real_name', 'email', 'phone', 'organization', 'status', 'is_staff', 'last_login']
    list_filter = ['status', 'gender', 'organization', 'is_staff', 'is_superuser', 'created_at', 'last_login']
    search_fields = ['username', 'real_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'last_login_at', 'last_login_ip', 'date_joined']
    inlines = [UserRoleInline]  # 使用inline管理用户角色关联
    
    fieldsets = (
        ('认证信息', {
            'fields': ('username', 'password')
        }),
        ('基本信息', {
            'fields': ('real_name', 'email', 'phone', 'avatar', 'gender')
        }),
        ('组织信息', {
            'fields': ('organization',)
        }),
        ('权限信息', {
            'fields': ('status', 'is_staff', 'is_superuser', 'user_permissions', 'groups')
        }),
        ('登录信息', {
            'fields': ('last_login', 'last_login_at', 'last_login_ip', 'date_joined')
        }),
        ('其他信息', {
            'fields': ('remark', 'created_at', 'updated_at', 'deleted_at')
        }),
    )
    
    add_fieldsets = (
        ('创建用户', {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'real_name', 'email', 'phone', 'organization', 'status', 'is_staff', 'is_superuser'),
        }),
    )
    
    filter_horizontal = ['user_permissions', 'groups']  # 移除roles，因为使用inline管理
    ordering = ['-created_at']

