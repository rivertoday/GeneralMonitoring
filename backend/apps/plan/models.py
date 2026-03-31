"""
预案模块 - 数据模型
"""
from django.db import models
from apps.common.models import BaseModel


class EmergencyPlan(BaseModel):
    """
    应急预案表
    """
    PLAN_TYPE_CHOICES = (
        (1, '综合应急预案'),
        (2, '专项应急预案'),
        (3, '现场处置方案'),
    )
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )
    PLAN_STATUS_CHOICES = (
        (0, '草稿'),
        (1, '已发布'),
        (2, '已修订'),
        (3, '已废止'),
    )

    plan_code = models.CharField('预案编码', max_length=50, unique=True, db_index=True)
    plan_name = models.CharField('预案名称', max_length=200)
    plan_type = models.SmallIntegerField('预案类型', choices=PLAN_TYPE_CHOICES, default=1, db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, blank=True, null=True,
                                            db_index=True)
    organization_id = models.BigIntegerField('所属部门ID', blank=True, null=True, db_index=True)
    version = models.CharField('预案版本号', max_length=20, default='1.0')
    plan_file_path = models.CharField('预案文件路径', max_length=500, blank=True, null=True, help_text='原始文档')
    plan_file_name = models.CharField('预案文件名称', max_length=200, blank=True, null=True)
    plan_summary = models.TextField('预案摘要', blank=True, null=True)
    plan_status = models.SmallIntegerField('预案状态', choices=PLAN_STATUS_CHOICES, default=0, db_index=True)
    publish_time = models.DateTimeField('发布时间', blank=True, null=True, db_index=True)
    effective_time = models.DateTimeField('生效时间', blank=True, null=True)
    expire_time = models.DateTimeField('失效时间', blank=True, null=True)
    revision_reason = models.TextField('修订原因', blank=True, null=True)
    create_user_id = models.BigIntegerField('创建人ID', db_index=True)
    approve_user_id = models.BigIntegerField('审批人ID', blank=True, null=True, db_index=True)
    approve_time = models.DateTimeField('审批时间', blank=True, null=True)
    description = models.CharField('预案描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'emergency_plans'
        verbose_name = '应急预案'
        verbose_name_plural = '应急预案'
        indexes = [
            models.Index(fields=['plan_type']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['organization_id']),
            models.Index(fields=['plan_status']),
            models.Index(fields=['publish_time']),
            models.Index(fields=['create_user_id']),
            models.Index(fields=['approve_user_id']),
        ]

    def __str__(self):
        return self.plan_name


class PlanStructure(BaseModel):
    """
    预案结构表
    """
    NODE_TYPE_CHOICES = (
        (1, '章节'),
        (2, '条款'),
        (3, '子条款'),
    )

    plan_id = models.BigIntegerField('预案ID', db_index=True)
    node_code = models.CharField('节点编码', max_length=50)
    node_name = models.CharField('节点名称', max_length=200)
    parent_id = models.BigIntegerField('父节点ID', default=0, db_index=True, help_text='0表示顶级节点')
    node_type = models.SmallIntegerField('节点类型', choices=NODE_TYPE_CHOICES, default=1, db_index=True)
    node_level = models.IntegerField('节点层级', default=1)
    node_content = models.TextField('节点内容（文本）', blank=True, null=True)
    node_index = models.IntegerField('节点索引', default=0, help_text='用于排序')
    is_key_info = models.SmallIntegerField('是否重点信息', default=0, db_index=True, help_text='0-否，1-是')
    description = models.CharField('节点描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'plan_structures'
        verbose_name = '预案结构'
        verbose_name_plural = '预案结构'
        unique_together = [['plan_id', 'node_code']]
        indexes = [
            models.Index(fields=['plan_id']),
            models.Index(fields=['parent_id']),
            models.Index(fields=['node_type']),
            models.Index(fields=['is_key_info']),
        ]

    def __str__(self):
        return f'Plan {self.plan_id} - {self.node_name}'


class PlanFlow(BaseModel):
    """
    预案流程表
    """
    FLOW_TYPE_CHOICES = (
        (1, '主流程'),
        (2, '子流程'),
        (3, '任务节点'),
    )

    plan_id = models.BigIntegerField('预案ID', db_index=True)
    flow_code = models.CharField('流程编码', max_length=50, unique=True, db_index=True)
    flow_name = models.CharField('流程名称', max_length=200)
    parent_id = models.BigIntegerField('父流程ID', default=0, db_index=True, help_text='0表示顶级流程')
    flow_type = models.SmallIntegerField('流程类型', choices=FLOW_TYPE_CHOICES, default=1, db_index=True)
    flow_level = models.IntegerField('流程层级', default=1)
    flow_config = models.TextField('流程配置', blank=True, null=True, help_text='JSON格式，包含流程节点、连线等信息')
    next_flow_ids = models.TextField('下一流程ID列表', blank=True, null=True, help_text='JSON数组')
    condition_config = models.TextField('条件配置', blank=True, null=True, help_text='JSON格式，定义流程执行条件')
    sort_order = models.IntegerField('排序顺序', default=0)
    description = models.CharField('流程描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'plan_flows'
        verbose_name = '预案流程'
        verbose_name_plural = '预案流程'
        indexes = [
            models.Index(fields=['plan_id']),
            models.Index(fields=['parent_id']),
            models.Index(fields=['flow_type']),
        ]

    def __str__(self):
        return self.flow_name


class PlanTask(BaseModel):
    """
    预案任务表
    """
    TASK_TYPE_CHOICES = (
        (1, '信息收集'),
        (2, '决策指挥'),
        (3, '资源调配'),
        (4, '现场处置'),
        (5, '其他'),
    )
    PRIORITY_CHOICES = (
        (1, '高'),
        (2, '中'),
        (3, '低'),
    )

    plan_id = models.BigIntegerField('预案ID', db_index=True)
    flow_id = models.BigIntegerField('关联流程ID', blank=True, null=True, db_index=True)
    task_code = models.CharField('任务编码', max_length=50, unique=True, db_index=True)
    task_name = models.CharField('任务名称', max_length=200)
    task_type = models.SmallIntegerField('任务类型', choices=TASK_TYPE_CHOICES, default=1, db_index=True)
    organization_id = models.BigIntegerField('负责组织ID', blank=True, null=True, db_index=True)
    assign_user_id = models.BigIntegerField('指定执行人ID', blank=True, null=True, db_index=True)
    assign_role_id = models.BigIntegerField('指定角色ID', blank=True, null=True, db_index=True)
    task_description = models.TextField('任务描述', blank=True, null=True)
    task_requirement = models.TextField('任务要求', blank=True, null=True)
    estimated_time = models.IntegerField('预计完成时间（分钟）', blank=True, null=True)
    priority = models.SmallIntegerField('优先级', choices=PRIORITY_CHOICES, default=3, db_index=True)
    sort_order = models.IntegerField('排序顺序', default=0)
    description = models.CharField('任务描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'plan_tasks'
        verbose_name = '预案任务'
        verbose_name_plural = '预案任务'
        indexes = [
            models.Index(fields=['plan_id']),
            models.Index(fields=['flow_id']),
            models.Index(fields=['task_type']),
            models.Index(fields=['organization_id']),
            models.Index(fields=['assign_user_id']),
            models.Index(fields=['assign_role_id']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        return self.task_name


class PlanExecution(BaseModel):
    """
    预案执行记录表
    """
    EXECUTION_TYPE_CHOICES = (
        (1, '演练执行'),
        (2, '实战执行'),
    )
    EXECUTION_STATUS_CHOICES = (
        (0, '未开始'),
        (1, '执行中'),
        (2, '已完成'),
        (3, '已终止'),
    )

    execution_code = models.CharField('执行编码', max_length=50, unique=True, db_index=True)
    plan_id = models.BigIntegerField('预案ID', db_index=True)
    warning_id = models.BigIntegerField('关联预警ID', blank=True, null=True, db_index=True)
    execution_type = models.SmallIntegerField('执行类型', choices=EXECUTION_TYPE_CHOICES, default=1, db_index=True)
    execution_status = models.SmallIntegerField('执行状态', choices=EXECUTION_STATUS_CHOICES, default=0, db_index=True)
    start_time = models.DateTimeField('开始时间', blank=True, null=True, db_index=True)
    end_time = models.DateTimeField('结束时间', blank=True, null=True, db_index=True)
    duration = models.IntegerField('执行时长（分钟）', blank=True, null=True)
    command_user_id = models.BigIntegerField('指挥人ID', db_index=True)
    current_flow_id = models.BigIntegerField('当前流程ID', blank=True, null=True, db_index=True)
    execution_result = models.TextField('执行结果', blank=True, null=True)
    execution_summary = models.TextField('执行总结', blank=True, null=True)
    description = models.CharField('执行描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'plan_executions'
        verbose_name = '预案执行记录'
        verbose_name_plural = '预案执行记录'
        indexes = [
            models.Index(fields=['plan_id']),
            models.Index(fields=['warning_id']),
            models.Index(fields=['execution_type']),
            models.Index(fields=['execution_status']),
            models.Index(fields=['start_time']),
            models.Index(fields=['end_time']),
            models.Index(fields=['command_user_id']),
            models.Index(fields=['current_flow_id']),
        ]

    def __str__(self):
        return f'{self.execution_code} - Plan {self.plan_id}'


class PlanTaskExecution(BaseModel):
    """
    预案任务执行记录表
    """
    TASK_STATUS_CHOICES = (
        (0, '待执行'),
        (1, '执行中'),
        (2, '已完成'),
        (3, '已取消'),
    )

    execution_id = models.BigIntegerField('预案执行记录ID', db_index=True)
    task_id = models.BigIntegerField('任务ID', db_index=True)
    assign_user_id = models.BigIntegerField('执行人ID', blank=True, null=True, db_index=True)
    task_status = models.SmallIntegerField('任务状态', choices=TASK_STATUS_CHOICES, default=0, db_index=True)
    assign_time = models.DateTimeField('分配时间', blank=True, null=True, db_index=True)
    accept_time = models.DateTimeField('接受时间', blank=True, null=True)
    start_time = models.DateTimeField('开始时间', blank=True, null=True, db_index=True)
    end_time = models.DateTimeField('结束时间', blank=True, null=True, db_index=True)
    duration = models.IntegerField('执行时长（分钟）', blank=True, null=True)
    task_result = models.TextField('任务结果', blank=True, null=True)
    feedback_content = models.TextField('反馈内容', blank=True, null=True)
    feedback_time = models.DateTimeField('反馈时间', blank=True, null=True)
    description = models.CharField('执行描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'plan_task_executions'
        verbose_name = '预案任务执行记录'
        verbose_name_plural = '预案任务执行记录'
        indexes = [
            models.Index(fields=['execution_id']),
            models.Index(fields=['task_id']),
            models.Index(fields=['assign_user_id']),
            models.Index(fields=['task_status']),
            models.Index(fields=['assign_time']),
            models.Index(fields=['start_time']),
            models.Index(fields=['end_time']),
        ]

    def __str__(self):
        return f'Execution {self.execution_id} - Task {self.task_id}'

