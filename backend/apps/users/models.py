"""
用户权限管理模块 - 数据模型
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from apps.common.models import BaseModel


class UserManager(BaseUserManager):
    """
    自定义用户管理器
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        """创建普通用户"""
        if not username:
            raise ValueError('用户名必须设置')
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """创建超级用户"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置 is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置 is_superuser=True')

        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        """通过用户名获取用户（用于认证），排除已软删除的用户"""
        return self.get(username=username, deleted_at__isnull=True)


class Organization(BaseModel):
    """
    组织表
    """
    ORG_TYPE_CHOICES = (
        (1, '政府部门'),
        (2, '企业单位'),
        (3, '事业单位'),
    )

    org_code = models.CharField('组织编码', max_length=50, unique=True, db_index=True)
    org_name = models.CharField('组织名称', max_length=100)
    parent_id = models.BigIntegerField('父组织ID', default=0, db_index=True, help_text='0表示顶级组织')
    org_type = models.SmallIntegerField('组织类型', choices=ORG_TYPE_CHOICES, default=1, db_index=True)
    level = models.IntegerField('组织层级', default=1)
    leader = models.CharField('负责人', max_length=50, blank=True, null=True)
    phone = models.CharField('联系电话', max_length=20, blank=True, null=True)
    address = models.CharField('地址', max_length=255, blank=True, null=True)
    description = models.CharField('组织描述', max_length=255, blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    sort_order = models.IntegerField('排序顺序', default=0)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'organizations'
        verbose_name = '组织'
        verbose_name_plural = '组织'
        indexes = [
            models.Index(fields=['parent_id']),
            models.Index(fields=['org_type']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.org_name


class Role(BaseModel):
    """
    角色表
    """
    role_code = models.CharField('角色编码', max_length=50, unique=True, db_index=True)
    role_name = models.CharField('角色名称', max_length=50)
    description = models.CharField('角色描述', max_length=255, blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    sort_order = models.IntegerField('排序顺序', default=0)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'roles'
        verbose_name = '角色'
        verbose_name_plural = '角色'
        indexes = [
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.role_name


class Permission(BaseModel):
    """
    权限表
    """
    PERMISSION_TYPE_CHOICES = (
        (1, '菜单'),
        (2, '按钮'),
        (3, '接口'),
    )

    permission_code = models.CharField('权限编码', max_length=100, unique=True, db_index=True)
    permission_name = models.CharField('权限名称', max_length=100)
    permission_type = models.SmallIntegerField('权限类型', choices=PERMISSION_TYPE_CHOICES, default=1, db_index=True)
    parent_id = models.BigIntegerField('父权限ID', default=0, db_index=True, help_text='0表示顶级权限')
    path = models.CharField('路由路径', max_length=255, blank=True, null=True, help_text='菜单类型使用')
    component = models.CharField('组件路径', max_length=255, blank=True, null=True, help_text='菜单类型使用')
    icon = models.CharField('图标', max_length=100, blank=True, null=True, help_text='菜单类型使用')
    api_path = models.CharField('API路径', max_length=255, blank=True, null=True, help_text='接口类型使用')
    http_method = models.CharField('HTTP方法', max_length=10, blank=True, null=True, help_text='GET, POST, PUT, DELETE等')
    description = models.CharField('权限描述', max_length=255, blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    sort_order = models.IntegerField('排序顺序', default=0)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'permissions'
        verbose_name = '权限'
        verbose_name_plural = '权限'
        indexes = [
            models.Index(fields=['permission_type']),
            models.Index(fields=['parent_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.permission_name


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    用户表
    继承AbstractBaseUser和PermissionsMixin以获得Django认证系统的完整支持
    """
    GENDER_CHOICES = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )

    username = models.CharField('用户名', max_length=50, unique=True, db_index=True)
    real_name = models.CharField('真实姓名', max_length=50, blank=True, null=True)
    email = models.CharField('邮箱地址', max_length=100, blank=True, null=True, db_index=True)
    phone = models.CharField('手机号码', max_length=20, blank=True, null=True, db_index=True)
    avatar = models.CharField('头像URL', max_length=255, blank=True, null=True)
    gender = models.SmallIntegerField('性别', choices=GENDER_CHOICES, default=0)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    last_login_at = models.DateTimeField('最后登录时间', blank=True, null=True, help_text='自定义最后登录时间字段')
    last_login_ip = models.CharField('最后登录IP', max_length=50, blank=True, null=True)
    is_staff = models.BooleanField('是否为员工', default=False, help_text='是否可以访问管理后台')
    is_superuser = models.BooleanField('是否为超级用户', default=False)
    date_joined = models.DateTimeField('注册时间', default=timezone.now, help_text='AbstractBaseUser要求的字段')
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        db_index=True,
        verbose_name='所属组织'
    )
    roles = models.ManyToManyField(Role, through='UserRole', related_name='users', verbose_name='角色')
    remark = models.TextField('备注信息', blank=True, null=True)

    # 指定用户名作为唯一标识符
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # createsuperuser命令需要的字段
    
    # 使用自定义管理器
    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = '用户'
        verbose_name_plural = '用户'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
            models.Index(fields=['organization']),
        ]

    def __str__(self):
        return self.username

    @property
    def is_active(self):
        """判断用户是否激活（基于status字段）"""
        return self.status == 1 and self.deleted_at is None

    def update_last_login(self, ip_address=None):
        """更新最后登录时间和IP"""
        self.last_login = timezone.now()  # AbstractBaseUser的last_login字段
        self.last_login_at = timezone.now()  # 自定义字段
        if ip_address:
            self.last_login_ip = ip_address
        update_fields = ['last_login', 'last_login_at']
        if ip_address:
            update_fields.append('last_login_ip')
        self.save(update_fields=update_fields)

    def get_permissions(self):
        """获取用户的所有权限"""
        permissions = Permission.objects.filter(
            role_permissions__role__user_roles__user=self,
            role_permissions__role__user_roles__user__status=1,
            role_permissions__role__status=1,
            status=1,
            deleted_at__isnull=True
        ).distinct()
        return permissions

    def has_permission(self, permission_code):
        """检查用户是否拥有指定权限"""
        return self.get_permissions().filter(permission_code=permission_code).exists()


class UserRole(models.Model):
    """
    用户角色关联表
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles', db_index=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_roles', db_index=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'user_roles'
        verbose_name = '用户角色关联'
        verbose_name_plural = '用户角色关联'
        unique_together = [['user', 'role']]
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.role.role_name}'


class RolePermission(models.Model):
    """
    角色权限关联表
    """
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions', db_index=True)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='role_permissions', db_index=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'role_permissions'
        verbose_name = '角色权限关联'
        verbose_name_plural = '角色权限关联'
        unique_together = [['role', 'permission']]
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['permission']),
        ]

    def __str__(self):
        return f'{self.role.role_name} - {self.permission.permission_name}'

