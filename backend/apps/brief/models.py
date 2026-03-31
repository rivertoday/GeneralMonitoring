"""
简报模块 - 数据模型
"""
from django.db import models
from apps.common.models import BaseModel


class BriefTemplate(BaseModel):
    """
    简报模板表
    """
    TEMPLATE_TYPE_CHOICES = (
        (1, '常态化运行报告'),
        (2, '非常态化突发预警简报'),
    )
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )

    template_code = models.CharField('模板编码', max_length=50, unique=True, db_index=True)
    template_name = models.CharField('模板名称', max_length=100)
    template_type = models.SmallIntegerField('模板类型', choices=TEMPLATE_TYPE_CHOICES, default=1, db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, blank=True, null=True,
                                            db_index=True, help_text='NULL表示全部')
    time_dimension = models.CharField('时间维度', max_length=20, blank=True, null=True, db_index=True,
                                      help_text='day-日，week-周，month-月，year-年（常态化模板）')
    region_dimension = models.CharField('区域维度配置', max_length=50, blank=True, null=True, help_text='JSON格式')
    industry_dimension = models.CharField('行业维度配置', max_length=50, blank=True, null=True, help_text='JSON格式')
    template_content = models.TextField('模板内容', help_text='支持变量占位符')
    variables = models.TextField('变量说明', blank=True, null=True, help_text='JSON格式')
    data_config = models.TextField('数据配置', blank=True, null=True, help_text='JSON格式，定义需要统计的数据项')
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    description = models.CharField('模板描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'brief_templates'
        verbose_name = '简报模板'
        verbose_name_plural = '简报模板'
        indexes = [
            models.Index(fields=['template_type']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['time_dimension']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.template_name


class BriefStrategy(BaseModel):
    """
    简报策略表
    """
    STRATEGY_TYPE_CHOICES = (
        (1, '常态化策略'),
        (2, '非常态化策略'),
    )
    TRIGGER_TYPE_CHOICES = (
        (1, '定时触发'),
        (2, '事件触发'),
    )
    PUSH_TARGET_TYPE_CHOICES = (
        (1, '指定用户'),
        (2, '指定角色'),
        (3, '指定组织'),
    )

    strategy_code = models.CharField('策略编码', max_length=50, unique=True, db_index=True)
    strategy_name = models.CharField('策略名称', max_length=100)
    template_id = models.BigIntegerField('模板ID', db_index=True)
    strategy_type = models.SmallIntegerField('策略类型', choices=STRATEGY_TYPE_CHOICES, default=1, db_index=True)
    report_type = models.CharField('报告类型', max_length=20, blank=True, null=True, db_index=True,
                                   help_text='daily-日报，weekly-周报，monthly-月报，yearly-年报（常态化策略）')
    trigger_type = models.SmallIntegerField('触发类型', choices=TRIGGER_TYPE_CHOICES, default=1, db_index=True,
                                           help_text='非常态化策略')
    trigger_config = models.TextField('触发配置', blank=True, null=True, help_text='JSON格式，包含触发时间、触发条件等')
    warning_type_filter = models.CharField('预警类型过滤', max_length=100, blank=True, null=True,
                                          help_text='非常态化策略，JSON数组')
    warning_level_filter = models.CharField('预警级别过滤', max_length=50, blank=True, null=True,
                                           help_text='非常态化策略，JSON数组')
    industry_filter = models.CharField('行业过滤', max_length=50, blank=True, null=True, help_text='JSON数组')
    region_filter = models.CharField('区域过滤', max_length=255, blank=True, null=True, help_text='JSON数组')
    push_target_type = models.SmallIntegerField('推送目标类型', choices=PUSH_TARGET_TYPE_CHOICES, default=1,
                                                db_index=True)
    push_target_ids = models.TextField('推送目标ID列表', blank=True, null=True, help_text='JSON数组')
    push_channel = models.CharField('推送渠道', max_length=50, blank=True, null=True,
                                   help_text='JSON数组：system-系统消息，sms-短信，email-邮件')
    message_template_id = models.BigIntegerField('消息模板ID', blank=True, null=True, db_index=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    last_execute_at = models.DateTimeField('最后执行时间', blank=True, null=True, db_index=True)
    next_execute_at = models.DateTimeField('下次执行时间', blank=True, null=True, db_index=True)
    description = models.CharField('策略描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'brief_strategies'
        verbose_name = '简报策略'
        verbose_name_plural = '简报策略'
        indexes = [
            models.Index(fields=['template_id']),
            models.Index(fields=['strategy_type']),
            models.Index(fields=['report_type']),
            models.Index(fields=['trigger_type']),
            models.Index(fields=['push_target_type']),
            models.Index(fields=['message_template_id']),
            models.Index(fields=['status']),
            models.Index(fields=['last_execute_at']),
            models.Index(fields=['next_execute_at']),
        ]

    def __str__(self):
        return self.strategy_name


class BriefData(BaseModel):
    """
    简报数据表
    """
    BRIEF_TYPE_CHOICES = (
        (1, '常态化运行报告'),
        (2, '非常态化突发预警简报'),
    )
    STATUS_CHOICES = (
        (0, '未推送'),
        (1, '已推送'),
        (2, '已查看'),
    )

    brief_code = models.CharField('简报编码', max_length=50, unique=True, db_index=True)
    template_id = models.BigIntegerField('模板ID', db_index=True)
    strategy_id = models.BigIntegerField('策略ID', blank=True, null=True, db_index=True)
    brief_type = models.SmallIntegerField('简报类型', choices=BRIEF_TYPE_CHOICES, default=1, db_index=True)
    report_type = models.CharField('报告类型', max_length=20, blank=True, null=True, db_index=True,
                                   help_text='daily-日报，weekly-周报，monthly-月报，yearly-年报')
    report_date = models.DateField('报告日期', db_index=True)
    report_period_start = models.DateTimeField('报告周期开始时间', blank=True, null=True, db_index=True)
    report_period_end = models.DateTimeField('报告周期结束时间', blank=True, null=True, db_index=True)
    brief_title = models.CharField('简报标题', max_length=200)
    brief_content = models.TextField('简报内容')
    data_summary = models.TextField('数据摘要', blank=True, null=True, help_text='JSON格式')
    alarm_count = models.IntegerField('报警次数', default=0)
    warning_count = models.IntegerField('预警次数', default=0)
    risk_count = models.IntegerField('风险隐患数量', default=0)
    industry_data = models.TextField('行业维度数据', blank=True, null=True, help_text='JSON格式')
    region_data = models.TextField('区域维度数据', blank=True, null=True, help_text='JSON格式')
    time_data = models.TextField('时间维度数据', blank=True, null=True, help_text='JSON格式')
    attachment_url = models.CharField('附件URL', max_length=500, blank=True, null=True, help_text='如PDF文件')
    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=0, db_index=True)
    generate_user_id = models.BigIntegerField('生成人ID', blank=True, null=True, db_index=True)
    generate_time = models.DateTimeField('生成时间', auto_now_add=True, db_index=True)
    description = models.CharField('简报描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'brief_data'
        verbose_name = '简报数据'
        verbose_name_plural = '简报数据'
        indexes = [
            models.Index(fields=['template_id']),
            models.Index(fields=['strategy_id']),
            models.Index(fields=['brief_type']),
            models.Index(fields=['report_type']),
            models.Index(fields=['report_date']),
            models.Index(fields=['report_period_start']),
            models.Index(fields=['report_period_end']),
            models.Index(fields=['status']),
            models.Index(fields=['generate_user_id']),
            models.Index(fields=['generate_time']),
        ]

    def __str__(self):
        return f'{self.brief_code} - {self.brief_title}'


class BriefPush(models.Model):
    """
    简报推送记录表
    """
    PUSH_TARGET_TYPE_CHOICES = (
        (1, '用户'),
        (2, '角色'),
        (3, '组织'),
    )
    PUSH_CHANNEL_CHOICES = (
        ('system', '系统消息'),
        ('sms', '短信'),
        ('email', '邮件'),
    )
    PUSH_STATUS_CHOICES = (
        (0, '待推送'),
        (1, '推送中'),
        (2, '推送成功'),
        (3, '推送失败'),
    )
    READ_STATUS_CHOICES = (
        (0, '未读'),
        (1, '已读'),
    )

    brief_id = models.BigIntegerField('简报ID', db_index=True)
    push_target_type = models.SmallIntegerField('推送目标类型', choices=PUSH_TARGET_TYPE_CHOICES, default=1,
                                                db_index=True)
    target_id = models.BigIntegerField('目标ID', db_index=True, help_text='用户ID、角色ID或组织ID')
    push_channel = models.CharField('推送渠道', max_length=20, db_index=True,
                                    help_text='system-系统消息，sms-短信，email-邮件')
    push_status = models.SmallIntegerField('推送状态', choices=PUSH_STATUS_CHOICES, default=0, db_index=True)
    push_time = models.DateTimeField('推送时间', blank=True, null=True, db_index=True)
    read_status = models.SmallIntegerField('阅读状态', choices=READ_STATUS_CHOICES, default=0, db_index=True)
    read_time = models.DateTimeField('阅读时间', blank=True, null=True)
    error_message = models.CharField('错误信息', max_length=500, blank=True, null=True, help_text='推送失败时')
    message_id = models.CharField('消息ID', max_length=100, blank=True, null=True, db_index=True,
                                  help_text='系统消息或短信平台返回的ID')
    remark = models.TextField('备注信息', blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'brief_pushes'
        verbose_name = '简报推送记录'
        verbose_name_plural = '简报推送记录'
        indexes = [
            models.Index(fields=['brief_id']),
            models.Index(fields=['push_target_type']),
            models.Index(fields=['target_id']),
            models.Index(fields=['push_channel']),
            models.Index(fields=['push_status']),
            models.Index(fields=['push_time']),
            models.Index(fields=['read_status']),
            models.Index(fields=['message_id']),
        ]

    def __str__(self):
        return f'Brief {self.brief_id} - {self.get_push_channel_display()}'

