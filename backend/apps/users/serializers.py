"""
用户权限管理模块 - 序列化器
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from .models import User, Role, Permission, Organization, UserRole, RolePermission


class OrganizationSerializer(serializers.ModelSerializer):
    """组织序列化器"""
    parent_name = serializers.SerializerMethodField()
    org_type_display = serializers.CharField(source='get_org_type_display', read_only=True)

    def get_parent_name(self, obj):
        """获取父组织名称"""
        if obj.parent_id and obj.parent_id > 0:
            try:
                parent = Organization.objects.get(id=obj.parent_id, deleted_at__isnull=True)
                return parent.org_name
            except Organization.DoesNotExist:
                return None
        return None

    class Meta:
        model = Organization
        fields = [
            'id', 'org_code', 'org_name', 'parent_id', 'parent_name',
            'org_type', 'org_type_display', 'level', 'leader', 'phone',
            'address', 'description', 'status', 'sort_order', 'remark',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrganizationTreeSerializer(serializers.ModelSerializer):
    """组织树形结构序列化器"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            'id', 'org_code', 'org_name', 'parent_id', 'org_type',
            'level', 'leader', 'phone', 'address', 'description',
            'status', 'sort_order', 'children'
        ]

    def get_children(self, obj):
        """获取子组织"""
        children = Organization.objects.filter(parent_id=obj.id, deleted_at__isnull=True)
        return OrganizationTreeSerializer(children, many=True).data


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    permission_type_display = serializers.CharField(source='get_permission_type_display', read_only=True)
    parent_name = serializers.SerializerMethodField()

    def get_parent_name(self, obj):
        """获取父权限名称"""
        if obj.parent_id and obj.parent_id > 0:
            try:
                parent = Permission.objects.get(id=obj.parent_id, deleted_at__isnull=True)
                return parent.permission_name
            except Permission.DoesNotExist:
                return None
        return None

    class Meta:
        model = Permission
        fields = [
            'id', 'permission_code', 'permission_name', 'permission_type',
            'permission_type_display', 'parent_id', 'parent_name', 'path',
            'component', 'icon', 'api_path', 'http_method', 'description',
            'status', 'sort_order', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PermissionTreeSerializer(serializers.ModelSerializer):
    """权限树形结构序列化器"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = [
            'id', 'permission_code', 'permission_name', 'permission_type',
            'parent_id', 'path', 'component', 'icon', 'api_path',
            'http_method', 'description', 'status', 'sort_order', 'children'
        ]

    def get_children(self, obj):
        """获取子权限"""
        children = Permission.objects.filter(parent_id=obj.id, deleted_at__isnull=True)
        return PermissionTreeSerializer(children, many=True).data


class RoleSerializer(serializers.ModelSerializer):
    """角色序列化器"""
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text='权限ID列表'
    )

    class Meta:
        model = Role
        fields = [
            'id', 'role_code', 'role_name', 'description', 'status',
            'sort_order', 'remark', 'permissions', 'permission_ids',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """创建角色并关联权限"""
        permission_ids = validated_data.pop('permission_ids', [])
        role = Role.objects.create(**validated_data)
        if permission_ids:
            RolePermission.objects.bulk_create([
                RolePermission(role=role, permission_id=pid)
                for pid in permission_ids
            ])
        return role

    def update(self, instance, validated_data):
        """更新角色并更新权限关联"""
        permission_ids = validated_data.pop('permission_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if permission_ids is not None:
            # 删除旧关联
            RolePermission.objects.filter(role=instance).delete()
            # 创建新关联
            if permission_ids:
                RolePermission.objects.bulk_create([
                    RolePermission(role=instance, permission_id=pid)
                    for pid in permission_ids
                ])

        return instance


class UserListSerializer(serializers.ModelSerializer):
    """用户列表序列化器（简化版）"""
    organization_name = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'real_name', 'email', 'phone', 'avatar',
            'gender', 'gender_display', 'status', 'organization',
            'organization_name', 'roles', 'last_login_at', 'last_login_ip',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login_at', 'last_login_ip']

    def get_organization_name(self, obj):
        """获取所属组织名称"""
        if obj.organization:
            return obj.organization.org_name
        return None

    def get_roles(self, obj):
        """获取用户角色列表"""
        return [{'id': role.id, 'role_name': role.role_name} for role in obj.roles.filter(deleted_at__isnull=True)]


class UserDetailSerializer(serializers.ModelSerializer):
    """用户详情序列化器"""
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    roles = RoleSerializer(many=True, read_only=True)
    role_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False,
        help_text='角色ID列表'
    )
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'real_name', 'email', 'phone',
            'avatar', 'gender', 'gender_display', 'status', 'organization',
            'organization_id', 'roles', 'role_ids', 'permissions',
            'last_login_at', 'last_login_ip', 'remark', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login_at', 'last_login_ip']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def get_permissions(self, obj):
        """获取用户的所有权限"""
        permissions = obj.get_permissions()
        return PermissionSerializer(permissions, many=True).data

    def validate_password(self, value):
        """验证密码强度"""
        if value:
            validate_password(value)
        return value

    def create(self, validated_data):
        """创建用户并关联角色"""
        role_ids = validated_data.pop('role_ids', [])
        password = validated_data.pop('password', None)
        organization_id = validated_data.pop('organization_id', None)

        if password:
            validated_data['password'] = make_password(password)
        else:
            raise serializers.ValidationError({'password': '密码不能为空'})

        if organization_id:
            try:
                organization = Organization.objects.get(id=organization_id, deleted_at__isnull=True)
                validated_data['organization'] = organization
            except Organization.DoesNotExist:
                raise serializers.ValidationError({'organization_id': '组织不存在'})

        user = User.objects.create(**validated_data)

        if role_ids:
            UserRole.objects.bulk_create([
                UserRole(user=user, role_id=rid)
                for rid in role_ids
            ])

        return user

    def update(self, instance, validated_data):
        """更新用户并更新角色关联"""
        role_ids = validated_data.pop('role_ids', None)
        password = validated_data.pop('password', None)
        organization_id = validated_data.pop('organization_id', None)

        if password:
            instance.set_password(password)

        if organization_id is not None:
            if organization_id:
                try:
                    organization = Organization.objects.get(id=organization_id, deleted_at__isnull=True)
                    instance.organization = organization
                except Organization.DoesNotExist:
                    raise serializers.ValidationError({'organization_id': '组织不存在'})
            else:
                instance.organization = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if role_ids is not None:
            # 删除旧关联
            UserRole.objects.filter(user=instance).delete()
            # 创建新关联
            if role_ids:
                UserRole.objects.bulk_create([
                    UserRole(user=instance, role_id=rid)
                    for rid in role_ids
                ])

        return instance


class UserPasswordSerializer(serializers.Serializer):
    """用户密码修改序列化器"""
    old_password = serializers.CharField(required=True, write_only=True, help_text='旧密码')
    new_password = serializers.CharField(required=True, write_only=True, help_text='新密码')
    confirm_password = serializers.CharField(required=True, write_only=True, help_text='确认密码')

    def validate_new_password(self, value):
        """验证新密码强度"""
        validate_password(value)
        return value

    def validate(self, attrs):
        """验证两次密码输入是否一致"""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': '两次密码输入不一致'})
        return attrs


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    username = serializers.CharField(required=True, help_text='用户名')
    password = serializers.CharField(required=True, write_only=True, help_text='密码')

