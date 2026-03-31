"""
系统管理模块 - 数据模型
"""
from django.db import models
from apps.common.models import BaseModel


class DataSource(BaseModel):
    """
    数据源表
    """
    SOURCE_TYPE_CHOICES = (
        (1, 'API接口'),
        (2, '数据库'),
        (3, '文件'),
    )
    INDUSTRY_TYPE_CHOICES = (
        (1, '气象'),
        (2, '危化'),
        (3, '防汛'),
        (4, '交通运输'),
        (5, '森林火灾'),
    )

    source_code = models.CharField('数据源编码', max_length=50, unique=True, db_index=True)
    source_name = models.CharField('数据源名称', max_length=100)
    source_type = models.SmallIntegerField('数据源类型', choices=SOURCE_TYPE_CHOICES, default=1, db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, db_index=True)
    api_url = models.CharField('API接口地址', max_length=500, blank=True, null=True, help_text='API类型')
    api_method = models.CharField('HTTP方法', max_length=10, blank=True, null=True, default='GET')
    api_params = models.TextField('API请求参数', blank=True, null=True, help_text='JSON格式')
    db_host = models.CharField('数据库主机', max_length=100, blank=True, null=True, help_text='数据库类型')
    db_port = models.IntegerField('数据库端口', blank=True, null=True, help_text='数据库类型')
    db_name = models.CharField('数据库名称', max_length=100, blank=True, null=True, help_text='数据库类型')
    db_user = models.CharField('数据库用户名', max_length=100, blank=True, null=True, help_text='数据库类型')
    db_password = models.CharField('数据库密码（加密）', max_length=255, blank=True, null=True, help_text='数据库类型，加密存储')
    db_table = models.CharField('数据表名', max_length=100, blank=True, null=True, help_text='数据库类型')
    sync_interval = models.IntegerField('同步间隔（分钟）', blank=True, null=True, default=60)
    last_sync_at = models.DateTimeField('最后同步时间', blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    description = models.CharField('数据源描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'data_sources'
        verbose_name = '数据源'
        verbose_name_plural = '数据源'
        indexes = [
            models.Index(fields=['source_type']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.source_name


class MessageTemplate(BaseModel):
    """
    消息模板表
    """
    TEMPLATE_TYPE_CHOICES = (
        (1, '系统消息'),
        (2, '短信'),
        (3, '邮件'),
    )
    MESSAGE_TYPE_CHOICES = (
        (1, '预警通知'),
        (2, '报警通知'),
        (3, '简报推送'),
        (4, '叫应通知'),
        (5, '其他'),
    )

    template_code = models.CharField('模板编码', max_length=50, unique=True, db_index=True)
    template_name = models.CharField('模板名称', max_length=100)
    template_type = models.SmallIntegerField('模板类型', choices=TEMPLATE_TYPE_CHOICES, default=1, db_index=True)
    message_type = models.SmallIntegerField('消息类型', choices=MESSAGE_TYPE_CHOICES, default=1, db_index=True)
    subject = models.CharField('消息主题', max_length=200, blank=True, null=True, help_text='邮件类型')
    content = models.TextField('消息内容', help_text='支持变量占位符，如：{变量名}')
    variables = models.TextField('变量说明', blank=True, null=True, help_text='JSON格式，说明可用变量')
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    description = models.CharField('模板描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'message_templates'
        verbose_name = '消息模板'
        verbose_name_plural = '消息模板'
        indexes = [
            models.Index(fields=['template_type']),
            models.Index(fields=['message_type']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.template_name

