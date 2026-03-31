"""
风险监测预警模块 - 数据模型
"""
from django.db import models
from apps.common.models import BaseModel


class WarningLevel(BaseModel):
    """
    预警级别表
    """
    LEVEL_COLOR_CHOICES = (
        ('red', '红色'),
        ('orange', '橙色'),
        ('yellow', '黄色'),
        ('blue', '蓝色'),
    )

    level_code = models.CharField('预警级别编码', max_length=20, unique=True, db_index=True,
                                   help_text='I-红色，II-橙色，III-黄色，IV-蓝色')
    level_name = models.CharField('预警级别名称', max_length=50)
    level_color = models.CharField('预警颜色', max_length=20, choices=LEVEL_COLOR_CHOICES)
    severity = models.SmallIntegerField('严重程度', db_index=True,
                                        help_text='1-特别严重，2-严重，3-较重，4-一般')
    response_org = models.CharField('响应组织要求', max_length=255, blank=True, null=True)
    response_time = models.IntegerField('响应时间要求（分钟）', blank=True, null=True)
    description = models.CharField('级别描述', max_length=255, blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    sort_order = models.IntegerField('排序顺序', default=0)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'warning_levels'
        verbose_name = '预警级别'
        verbose_name_plural = '预警级别'
        indexes = [
            models.Index(fields=['severity']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f'{self.level_name}({self.level_code})'


class WarningRule(BaseModel):
    """
    预警规则表
    """
    RULE_TYPE_CHOICES = (
        (1, '预警生成规则'),
        (2, '预警处置规则'),
    )
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )

    rule_code = models.CharField('规则编码', max_length=50, unique=True, db_index=True)
    rule_name = models.CharField('规则名称', max_length=100)
    rule_type = models.SmallIntegerField('规则类型', choices=RULE_TYPE_CHOICES, default=1, db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, db_index=True)
    warning_level = models.ForeignKey(
        WarningLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='warning_rules',
        db_index=True,
        verbose_name='预警级别'
    )
    condition_config = models.TextField('规则条件配置', help_text='JSON格式，包含报警频率、报警时长、报警设备等条件')
    action_config = models.TextField('规则动作配置', blank=True, null=True,
                                     help_text='JSON格式，包含响应时间、处置时间、反馈时间等要求')
    response_time = models.IntegerField('响应时间要求（分钟）', blank=True, null=True, help_text='处置规则')
    handle_time = models.IntegerField('处置时间要求（分钟）', blank=True, null=True, help_text='处置规则')
    feedback_time = models.IntegerField('反馈时间要求（分钟）', blank=True, null=True, help_text='处置规则')
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    description = models.CharField('规则描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'warning_rules'
        verbose_name = '预警规则'
        verbose_name_plural = '预警规则'
        indexes = [
            models.Index(fields=['rule_type']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['warning_level']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.rule_name


class RiskMonitor(BaseModel):
    """
    风险监测数据表
    """
    MONITOR_TYPE_CHOICES = (
        (1, '实时监测'),
        (2, '全域监测'),
        (3, '重点监测'),
    )
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )

    monitor_code = models.CharField('监测点编码', max_length=50, unique=True, db_index=True)
    monitor_name = models.CharField('监测点名称', max_length=100)
    monitor_type = models.SmallIntegerField('监测类型', choices=MONITOR_TYPE_CHOICES, default=1, db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, db_index=True)
    # data_source字段将在system模块定义后添加ForeignKey
    data_source_id = models.BigIntegerField('数据源ID', blank=True, null=True, db_index=True)
    # location字段：使用GEOMETRY类型存储空间数据（MySQL空间类型）
    location = models.TextField('地理位置（WKT格式）', blank=True, null=True, help_text='POINT类型的WKT格式字符串')
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    monitor_value = models.DecimalField('监测数值', max_digits=10, decimal_places=2, blank=True, null=True)
    monitor_unit = models.CharField('监测单位', max_length=20, blank=True, null=True)
    threshold_min = models.DecimalField('阈值下限', max_digits=10, decimal_places=2, blank=True, null=True)
    threshold_max = models.DecimalField('阈值上限', max_digits=10, decimal_places=2, blank=True, null=True)
    online_status = models.SmallIntegerField('在线状态', default=1, db_index=True, help_text='0-离线，1-在线')
    last_data_time = models.DateTimeField('最后数据时间', blank=True, null=True, db_index=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    description = models.CharField('监测点描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'risk_monitors'
        verbose_name = '风险监测点'
        verbose_name_plural = '风险监测点'
        indexes = [
            models.Index(fields=['monitor_type']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['data_source_id']),
            models.Index(fields=['longitude']),
            models.Index(fields=['latitude']),
            models.Index(fields=['street']),
            models.Index(fields=['online_status']),
            models.Index(fields=['last_data_time']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.monitor_name


class AlarmRecord(BaseModel):
    """
    报警记录表
    """
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )
    ALARM_STATUS_CHOICES = (
        (0, '未处理'),
        (1, '处理中'),
        (2, '已处理'),
        (3, '已忽略'),
    )

    alarm_code = models.CharField('报警编码', max_length=50, unique=True, db_index=True)
    monitor = models.ForeignKey(
        RiskMonitor,
        on_delete=models.CASCADE,
        related_name='alarm_records',
        db_index=True,
        verbose_name='监测点'
    )
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, db_index=True)
    alarm_type = models.CharField('报警类型', max_length=50, db_index=True)
    alarm_value = models.DecimalField('报警数值', max_digits=10, decimal_places=2, blank=True, null=True)
    threshold_value = models.DecimalField('阈值数值', max_digits=10, decimal_places=2, blank=True, null=True)
    location = models.TextField('报警位置（WKT格式）', blank=True, null=True, help_text='POINT类型的WKT格式字符串')
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    alarm_time = models.DateTimeField('报警时间', db_index=True)
    alarm_duration = models.IntegerField('报警持续时间（分钟）', blank=True, null=True)
    alarm_status = models.SmallIntegerField('报警状态', choices=ALARM_STATUS_CHOICES, default=0, db_index=True)
    handle_user_id = models.BigIntegerField('处理人ID', blank=True, null=True, db_index=True)
    handle_time = models.DateTimeField('处理时间', blank=True, null=True)
    handle_result = models.TextField('处理结果', blank=True, null=True)
    feedback_time = models.DateTimeField('反馈时间', blank=True, null=True)
    description = models.CharField('报警描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'alarm_records'
        verbose_name = '报警记录'
        verbose_name_plural = '报警记录'
        indexes = [
            models.Index(fields=['monitor']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['alarm_type']),
            models.Index(fields=['longitude']),
            models.Index(fields=['latitude']),
            models.Index(fields=['street']),
            models.Index(fields=['alarm_time']),
            models.Index(fields=['alarm_status']),
            models.Index(fields=['handle_user_id']),
        ]

    def __str__(self):
        return f'{self.alarm_code} - {self.alarm_type}'


class RiskWarning(BaseModel):
    """
    风险预警表
    """
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )
    WARNING_ANALYSIS_TYPE_CHOICES = (
        (1, '突出预警'),
        (2, '同比预警'),
        (3, '环比预警'),
    )
    WARNING_SOURCE_CHOICES = (
        (1, '自动生成'),
        (2, '手动创建'),
    )
    WARNING_STATUS_CHOICES = (
        (0, '未发布'),
        (1, '已发布'),
        (2, '处理中'),
        (3, '已处置'),
        (4, '已关闭'),
    )

    warning_code = models.CharField('预警编码', max_length=50, unique=True, db_index=True)
    warning_level = models.ForeignKey(
        WarningLevel,
        on_delete=models.PROTECT,
        related_name='risk_warnings',
        db_index=True,
        verbose_name='预警级别'
    )
    warning_rule = models.ForeignKey(
        WarningRule,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='risk_warnings',
        db_index=True,
        verbose_name='预警规则'
    )
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, db_index=True)
    warning_type = models.CharField('预警类型', max_length=50, db_index=True, help_text='如：火灾预警、泄漏预警等')
    warning_analysis_type = models.SmallIntegerField('预警分析类型', choices=WARNING_ANALYSIS_TYPE_CHOICES,
                                                      blank=True, null=True, db_index=True)
    warning_title = models.CharField('预警标题', max_length=200)
    warning_content = models.TextField('预警内容')
    location = models.TextField('预警位置（WKT格式）', blank=True, null=True, help_text='POINT类型的WKT格式字符串')
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    warning_time = models.DateTimeField('预警时间', db_index=True)
    warning_source = models.SmallIntegerField('预警来源', choices=WARNING_SOURCE_CHOICES, default=1, db_index=True)
    warning_status = models.SmallIntegerField('预警状态', choices=WARNING_STATUS_CHOICES, default=0, db_index=True)
    response_org_id = models.BigIntegerField('响应组织ID', blank=True, null=True, db_index=True)
    response_user_id = models.BigIntegerField('响应人ID', blank=True, null=True, db_index=True)
    response_time = models.DateTimeField('响应时间', blank=True, null=True)
    handle_time = models.DateTimeField('处置时间', blank=True, null=True)
    handle_result = models.TextField('处置结果', blank=True, null=True)
    feedback_time = models.DateTimeField('反馈时间', blank=True, null=True)
    publish_time = models.DateTimeField('发布时间', blank=True, null=True, db_index=True)
    related_plan_id = models.BigIntegerField('关联预案ID', blank=True, null=True,
                                              help_text='关联预案主题库，用于分级响应和处理')
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'risk_warnings'
        verbose_name = '风险预警'
        verbose_name_plural = '风险预警'
        indexes = [
            models.Index(fields=['warning_level']),
            models.Index(fields=['warning_rule']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['warning_type']),
            models.Index(fields=['warning_analysis_type']),
            models.Index(fields=['longitude']),
            models.Index(fields=['latitude']),
            models.Index(fields=['street']),
            models.Index(fields=['warning_time']),
            models.Index(fields=['warning_source']),
            models.Index(fields=['warning_status']),
            models.Index(fields=['response_org_id']),
            models.Index(fields=['response_user_id']),
            models.Index(fields=['publish_time']),
        ]

    def __str__(self):
        return f'{self.warning_code} - {self.warning_title}'


class AlarmStatistics(models.Model):
    """
    报警统计表
    """
    STAT_TYPE_CHOICES = (
        (1, '日报'),
        (2, '周报'),
        (3, '月报'),
        (4, '年报'),
    )
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )

    stat_date = models.DateField('统计日期', db_index=True)
    stat_type = models.SmallIntegerField('统计类型', choices=STAT_TYPE_CHOICES, default=1, db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, blank=True, null=True,
                                             db_index=True, help_text='NULL表示全部')
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True,
                             help_text='NULL表示全部')
    alarm_count = models.IntegerField('报警总数', default=0)
    unhandled_count = models.IntegerField('未处理数量', default=0)
    handling_count = models.IntegerField('处理中数量', default=0)
    handled_count = models.IntegerField('已处理数量', default=0)
    ignored_count = models.IntegerField('已忽略数量', default=0)
    avg_handle_time = models.IntegerField('平均处理时间（分钟）', blank=True, null=True)
    stat_data = models.TextField('详细统计数据', blank=True, null=True, help_text='JSON格式')
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'alarm_statistics'
        verbose_name = '报警统计'
        verbose_name_plural = '报警统计'
        unique_together = [['stat_date', 'stat_type', 'industry_type', 'street']]
        indexes = [
            models.Index(fields=['stat_date']),
            models.Index(fields=['stat_type']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['street']),
        ]

    def __str__(self):
        return f'{self.stat_date} - {self.get_stat_type_display()}'


class RiskHiddenDanger(BaseModel):
    """
    隐患排查表
    """
    INDUSTRY_TYPE_CHOICES = (
        (4, '危险化学品'),
    )
    DANGER_LEVEL_CHOICES = (
        (1, '重大'),
        (2, '较大'),
        (3, '一般'),
    )
    STATUS_CHOICES = (
        (0, '待整改'),
        (1, '整改中'),
        (2, '已完成'),
        (3, '已关闭'),
    )

    danger_code = models.CharField('隐患编码', max_length=50, unique=True, db_index=True)
    danger_name = models.CharField('隐患名称', max_length=200)
    monitor = models.ForeignKey(
        RiskMonitor,
        on_delete=models.CASCADE,
        related_name='hidden_dangers',
        db_index=True,
        verbose_name='监测点',
        help_text='重点监测类型'
    )
    organization_id = models.BigIntegerField('企业ID', db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, default=4, db_index=True)
    location = models.TextField('隐患位置（WKT格式）', blank=True, null=True, help_text='POINT类型的WKT格式字符串')
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    danger_level = models.SmallIntegerField('隐患等级', choices=DANGER_LEVEL_CHOICES, default=1, db_index=True)
    danger_category = models.CharField('隐患类别', max_length=100, blank=True, null=True, db_index=True)
    danger_description = models.TextField('隐患描述')
    discover_time = models.DateTimeField('发现时间', db_index=True)
    discover_user_id = models.BigIntegerField('发现人ID', blank=True, null=True, db_index=True)
    status = models.SmallIntegerField('状态', choices=STATUS_CHOICES, default=0, db_index=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'risk_hidden_dangers'
        verbose_name = '隐患排查'
        verbose_name_plural = '隐患排查'
        indexes = [
            models.Index(fields=['monitor']),
            models.Index(fields=['organization_id']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['longitude']),
            models.Index(fields=['latitude']),
            models.Index(fields=['street']),
            models.Index(fields=['danger_level']),
            models.Index(fields=['danger_category']),
            models.Index(fields=['discover_time']),
            models.Index(fields=['discover_user_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f'{self.danger_code} - {self.danger_name}'


class RiskRectification(BaseModel):
    """
    隐患整改表
    """
    RECTIFICATION_STATUS_CHOICES = (
        (0, '待开始'),
        (1, '进行中'),
        (2, '已完成'),
        (3, '已延期'),
    )
    VERIFICATION_STATUS_CHOICES = (
        (0, '待验收'),
        (1, '验收通过'),
        (2, '验收不通过'),
    )

    rectification_code = models.CharField('整改编码', max_length=50, unique=True, db_index=True)
    danger = models.ForeignKey(
        RiskHiddenDanger,
        on_delete=models.CASCADE,
        related_name='rectifications',
        db_index=True,
        verbose_name='隐患'
    )
    rectification_plan = models.TextField('整改方案')
    rectification_measures = models.TextField('整改措施')
    responsible_user_id = models.BigIntegerField('责任人ID', db_index=True)
    responsible_org_id = models.BigIntegerField('责任组织ID', db_index=True)
    plan_start_time = models.DateTimeField('计划开始时间', db_index=True)
    plan_end_time = models.DateTimeField('计划完成时间', db_index=True)
    actual_start_time = models.DateTimeField('实际开始时间', blank=True, null=True)
    actual_end_time = models.DateTimeField('实际完成时间', blank=True, null=True, db_index=True)
    rectification_status = models.SmallIntegerField('整改状态', choices=RECTIFICATION_STATUS_CHOICES, default=0,
                                                    db_index=True)
    rectification_result = models.TextField('整改结果', blank=True, null=True)
    verification_status = models.SmallIntegerField('验收状态', choices=VERIFICATION_STATUS_CHOICES, default=0,
                                                   db_index=True)
    verification_time = models.DateTimeField('验收时间', blank=True, null=True)
    verification_user_id = models.BigIntegerField('验收人ID', blank=True, null=True, db_index=True)
    verification_opinion = models.TextField('验收意见', blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'risk_rectifications'
        verbose_name = '隐患整改'
        verbose_name_plural = '隐患整改'
        indexes = [
            models.Index(fields=['danger']),
            models.Index(fields=['responsible_user_id']),
            models.Index(fields=['responsible_org_id']),
            models.Index(fields=['plan_start_time']),
            models.Index(fields=['plan_end_time']),
            models.Index(fields=['actual_end_time']),
            models.Index(fields=['rectification_status']),
            models.Index(fields=['verification_status']),
            models.Index(fields=['verification_user_id']),
        ]

    def __str__(self):
        return f'{self.rectification_code} - {self.danger.danger_name}'

