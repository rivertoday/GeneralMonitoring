"""
演练监督模块 - 数据模型
"""
from django.db import models
from apps.common.models import BaseModel


class DrillEvent(BaseModel):
    """
    演练事件表
    """
    EVENT_TYPE_CHOICES = (
        (1, '火灾'),
        (2, '爆炸'),
        (3, '泄漏'),
        (4, '坍塌'),
        (5, '其他'),
    )
    DRILL_STATUS_CHOICES = (
        (0, '未开始'),
        (1, '进行中'),
        (2, '已完成'),
        (3, '已取消'),
    )
    DATA_SOURCE_CHOICES = (
        (1, '企业安全在线服务'),
        (2, '化工园区安全智能化管控平台'),
        (3, '手动录入'),
    )

    event_code = models.CharField('事件编码', max_length=50, unique=True, db_index=True)
    event_name = models.CharField('演练事件名称', max_length=200)
    organization_id = models.BigIntegerField('事发单位ID', db_index=True)
    drill_plan_name = models.CharField('关联演练计划名称', max_length=200, blank=True, null=True)
    drill_plan_id = models.BigIntegerField('关联演练计划ID', blank=True, null=True, db_index=True)
    event_type = models.SmallIntegerField('事件类型', choices=EVENT_TYPE_CHOICES, default=1, db_index=True)
    accident_type = models.CharField('事故类型（详细分类）', max_length=50, blank=True, null=True, db_index=True)
    location = models.TextField('事件位置（WKT格式）', blank=True, null=True, help_text='POINT类型的WKT格式字符串')
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    event_time = models.DateTimeField('事发时间', db_index=True)
    injured_count = models.IntegerField('受伤人数', default=0)
    death_count = models.IntegerField('死亡人数', default=0)
    accident_summary = models.TextField('事故简介', blank=True, null=True)
    related_plan_id = models.BigIntegerField('需要启动的预案ID', blank=True, null=True, db_index=True)
    drill_status = models.SmallIntegerField('演练状态', choices=DRILL_STATUS_CHOICES, default=0, db_index=True)
    data_source = models.SmallIntegerField('数据来源', choices=DATA_SOURCE_CHOICES, blank=True, null=True, db_index=True)
    external_id = models.CharField('外部系统ID', max_length=100, blank=True, null=True, db_index=True)
    description = models.CharField('事件描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'drill_events'
        verbose_name = '演练事件'
        verbose_name_plural = '演练事件'
        indexes = [
            models.Index(fields=['organization_id']),
            models.Index(fields=['drill_plan_id']),
            models.Index(fields=['event_type']),
            models.Index(fields=['accident_type']),
            models.Index(fields=['longitude']),
            models.Index(fields=['latitude']),
            models.Index(fields=['street']),
            models.Index(fields=['event_time']),
            models.Index(fields=['related_plan_id']),
            models.Index(fields=['drill_status']),
            models.Index(fields=['data_source']),
            models.Index(fields=['external_id']),
        ]

    def __str__(self):
        return self.event_name


class DrillEvaluation(BaseModel):
    """
    演练评价表
    """
    NODE_TYPE_CHOICES = (
        (1, '信息收集'),
        (2, '决策指挥'),
        (3, '资源调配'),
        (4, '现场处置'),
        (5, '其他'),
    )
    EVALUATION_LEVEL_CHOICES = (
        (1, '优秀'),
        (2, '良好'),
        (3, '合格'),
        (4, '不合格'),
    )

    event_id = models.BigIntegerField('演练事件ID', db_index=True)
    node_name = models.CharField('演练节点名称', max_length=200)
    node_type = models.SmallIntegerField('节点类型', choices=NODE_TYPE_CHOICES, default=1, db_index=True)
    evaluation_item = models.CharField('评价项', max_length=200)
    evaluation_content = models.TextField('评价内容')
    evaluation_score = models.DecimalField('评价得分', max_digits=5, decimal_places=2, blank=True, null=True,
                                          help_text='0-100')
    evaluation_level = models.SmallIntegerField('评价等级', choices=EVALUATION_LEVEL_CHOICES, blank=True, null=True,
                                                db_index=True)
    evaluator_id = models.BigIntegerField('评价人ID', db_index=True)
    evaluation_time = models.DateTimeField('评价时间', auto_now_add=True, db_index=True)
    description = models.CharField('评价描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'drill_evaluations'
        verbose_name = '演练评价'
        verbose_name_plural = '演练评价'
        indexes = [
            models.Index(fields=['event_id']),
            models.Index(fields=['node_type']),
            models.Index(fields=['evaluation_level']),
            models.Index(fields=['evaluator_id']),
            models.Index(fields=['evaluation_time']),
        ]

    def __str__(self):
        return f'Event {self.event_id} - {self.evaluation_item}'


class DrillSummary(BaseModel):
    """
    演练总结表
    """
    STATUS_CHOICES = (
        (1, '顺畅/熟悉/可操作/明确/科学/得当'),
        (2, '一般'),
        (3, '不顺畅/不熟悉/不可操作/不明确/不科学/不得当'),
    )
    OVERALL_LEVEL_CHOICES = (
        (1, '优秀'),
        (2, '良好'),
        (3, '合格'),
        (4, '不合格'),
    )

    event_id = models.BigIntegerField('演练事件ID', unique=True, db_index=True)
    summary_title = models.CharField('总结标题', max_length=200)
    communication_status = models.SmallIntegerField('内部沟通和传递是否顺畅', choices=STATUS_CHOICES, blank=True,
                                                    null=True, db_index=True)
    communication_comment = models.TextField('内部沟通评价说明', blank=True, null=True)
    plan_familiarity = models.SmallIntegerField('各级人员对预案的熟悉程度', choices=STATUS_CHOICES, blank=True,
                                               null=True, db_index=True)
    plan_familiarity_comment = models.TextField('预案熟悉程度评价说明', blank=True, null=True)
    plan_operability = models.SmallIntegerField('预案的可操作性', choices=STATUS_CHOICES, blank=True, null=True,
                                               db_index=True)
    plan_operability_comment = models.TextField('预案可操作性评价说明', blank=True, null=True)
    duty_clarity = models.SmallIntegerField('各级部门的职责定位是否明确', choices=STATUS_CHOICES, blank=True,
                                           null=True, db_index=True)
    duty_clarity_comment = models.TextField('职责定位评价说明', blank=True, null=True)
    command_science = models.SmallIntegerField('应急指挥是否科学', choices=STATUS_CHOICES, blank=True, null=True,
                                              db_index=True)
    command_science_comment = models.TextField('应急指挥评价说明', blank=True, null=True)
    disposal_appropriateness = models.SmallIntegerField('应急处置是否得当', choices=STATUS_CHOICES, blank=True,
                                                       null=True, db_index=True)
    disposal_appropriateness_comment = models.TextField('应急处置评价说明', blank=True, null=True)
    problems_analysis = models.TextField('存在的问题分析', blank=True, null=True)
    improvement_suggestions = models.TextField('改进建议', blank=True, null=True)
    overall_score = models.DecimalField('总体得分', max_digits=5, decimal_places=2, blank=True, null=True,
                                       help_text='0-100')
    overall_level = models.SmallIntegerField('总体等级', choices=OVERALL_LEVEL_CHOICES, blank=True, null=True,
                                            db_index=True)
    enterprise_summary = models.TextField('企业演练总结报告内容', blank=True, null=True)
    supervisor_opinion = models.TextField('监管单位意见', blank=True, null=True)
    summary_user_id = models.BigIntegerField('总结人ID', db_index=True)
    summary_time = models.DateTimeField('总结时间', auto_now_add=True, db_index=True)
    description = models.CharField('总结描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'drill_summaries'
        verbose_name = '演练总结'
        verbose_name_plural = '演练总结'
        indexes = [
            models.Index(fields=['event_id']),
            models.Index(fields=['communication_status']),
            models.Index(fields=['plan_familiarity']),
            models.Index(fields=['plan_operability']),
            models.Index(fields=['duty_clarity']),
            models.Index(fields=['command_science']),
            models.Index(fields=['disposal_appropriateness']),
            models.Index(fields=['overall_level']),
            models.Index(fields=['summary_user_id']),
            models.Index(fields=['summary_time']),
        ]

    def __str__(self):
        return f'{self.summary_title} - Event {self.event_id}'


class DrillAnalysis(models.Model):
    """
    演练分析表
    """
    STAT_TYPE_CHOICES = (
        (1, '日报'),
        (2, '周报'),
        (3, '月报'),
        (4, '年报'),
    )
    DRILL_TYPE_CHOICES = (
        (1, '桌面演练'),
        (2, '功能演练'),
        (3, '全面演练'),
    )

    stat_date = models.DateField('统计日期', db_index=True)
    stat_type = models.SmallIntegerField('统计类型', choices=STAT_TYPE_CHOICES, default=1, db_index=True)
    organization_id = models.BigIntegerField('演练单位ID', blank=True, null=True, db_index=True,
                                            help_text='NULL表示全部')
    drill_type = models.SmallIntegerField('演练类型', choices=DRILL_TYPE_CHOICES, blank=True, null=True,
                                         db_index=True, help_text='NULL表示全部')
    accident_type = models.CharField('事故类型', max_length=50, blank=True, null=True, db_index=True,
                                    help_text='NULL表示全部')
    drill_count = models.IntegerField('演练次数', default=0)
    completed_count = models.IntegerField('已完成次数', default=0)
    excellent_count = models.IntegerField('优秀次数', default=0)
    good_count = models.IntegerField('良好次数', default=0)
    qualified_count = models.IntegerField('合格次数', default=0)
    unqualified_count = models.IntegerField('不合格次数', default=0)
    avg_score = models.DecimalField('平均得分', max_digits=5, decimal_places=2, blank=True, null=True)
    analysis_data = models.TextField('详细分析数据', blank=True, null=True, help_text='JSON格式')
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'drill_analyses'
        verbose_name = '演练分析'
        verbose_name_plural = '演练分析'
        unique_together = [['stat_date', 'stat_type', 'organization_id', 'drill_type', 'accident_type']]
        indexes = [
            models.Index(fields=['stat_date']),
            models.Index(fields=['stat_type']),
            models.Index(fields=['organization_id']),
            models.Index(fields=['drill_type']),
            models.Index(fields=['accident_type']),
        ]

    def __str__(self):
        return f'{self.stat_date} - {self.get_stat_type_display()}'

