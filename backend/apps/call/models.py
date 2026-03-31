"""
叫应模块 - 数据模型
"""
from django.db import models
from apps.common.models import BaseModel


class CallGroup(BaseModel):
    """
    叫应分组表
    """
    GROUP_TYPE_CHOICES = (
        (1, '常态化分组'),
        (2, '非常态化分组'),
    )

    group_code = models.CharField('分组编码', max_length=50, unique=True, db_index=True)
    group_name = models.CharField('分组名称', max_length=100)
    group_type = models.SmallIntegerField('分组类型', choices=GROUP_TYPE_CHOICES, default=1, db_index=True)
    event_level = models.SmallIntegerField('负责应急事件级别', blank=True, null=True, db_index=True,
                                          help_text='1-红色I级，2-橙色Ⅱ级，3-黄色Ⅲ级，4-蓝色Ⅳ级（非常态化分组）')
    description = models.CharField('分组描述', max_length=255, blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    sort_order = models.IntegerField('排序顺序', default=0)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'call_groups'
        verbose_name = '叫应分组'
        verbose_name_plural = '叫应分组'
        indexes = [
            models.Index(fields=['group_type']),
            models.Index(fields=['event_level']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.group_name


class CallTarget(BaseModel):
    """
    叫应对象表
    """
    TARGET_TYPE_CHOICES = (
        (1, '政府部门'),
        (2, '企业单位'),
        (3, '事业单位'),
    )

    target_code = models.CharField('对象编码', max_length=50, unique=True, db_index=True)
    target_name = models.CharField('对象名称', max_length=100)
    target_type = models.SmallIntegerField('对象类型', choices=TARGET_TYPE_CHOICES, default=1, db_index=True)
    organization_id = models.BigIntegerField('所属组织ID', blank=True, null=True, db_index=True)
    enterprise_name = models.CharField('企业名称', max_length=200, blank=True, null=True, help_text='企业单位')
    enterprise_info = models.TextField('企业信息', blank=True, null=True, help_text='企业单位')
    safety_person = models.CharField('安全责任人', max_length=50)
    contact_phone = models.CharField('联系电话', max_length=20, db_index=True)
    contact_address = models.CharField('联系地址', max_length=255, blank=True, null=True)
    description = models.CharField('对象描述', max_length=255, blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'call_targets'
        verbose_name = '叫应对象'
        verbose_name_plural = '叫应对象'
        indexes = [
            models.Index(fields=['target_type']),
            models.Index(fields=['organization_id']),
            models.Index(fields=['contact_phone']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.target_name


class CallPerson(BaseModel):
    """
    叫应人员表
    """
    person_code = models.CharField('人员编码', max_length=50, unique=True, db_index=True)
    person_name = models.CharField('人员姓名', max_length=50)
    group_id = models.BigIntegerField('所属分组ID', blank=True, null=True, db_index=True)
    rank = models.CharField('职级', max_length=50, blank=True, null=True, db_index=True)
    mobile_phone = models.CharField('手机号码', max_length=20, db_index=True)
    office_phone = models.CharField('办公电话', max_length=20, blank=True, null=True)
    contact_address = models.CharField('通讯地址', max_length=255, blank=True, null=True)
    event_level = models.SmallIntegerField('负责应急事件级别', blank=True, null=True, db_index=True,
                                          help_text='1-红色I级，2-橙色Ⅱ级，3-黄色Ⅲ级，4-蓝色Ⅳ级')
    organization_id = models.BigIntegerField('所属组织ID', blank=True, null=True, db_index=True)
    description = models.CharField('人员描述', max_length=255, blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'call_persons'
        verbose_name = '叫应人员'
        verbose_name_plural = '叫应人员'
        indexes = [
            models.Index(fields=['group_id']),
            models.Index(fields=['rank']),
            models.Index(fields=['mobile_phone']),
            models.Index(fields=['event_level']),
            models.Index(fields=['organization_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.person_name


class PolicyFile(BaseModel):
    """
    政策文件表
    """
    PUBLISH_STATUS_CHOICES = (
        (0, '未发布'),
        (1, '已发布'),
    )

    file_code = models.CharField('文件编码', max_length=50, unique=True, db_index=True)
    file_name = models.CharField('文件名称', max_length=200)
    file_path = models.CharField('文件存储路径', max_length=500)
    file_size = models.BigIntegerField('文件大小（字节）', blank=True, null=True)
    file_type = models.CharField('文件类型', max_length=50, blank=True, null=True, db_index=True)
    file_ext = models.CharField('文件扩展名', max_length=10, blank=True, null=True)
    policy_title = models.CharField('政策标题', max_length=200)
    policy_content = models.TextField('政策内容（文本提取）', blank=True, null=True)
    policy_requirement = models.TextField('政策要求', blank=True, null=True)
    upload_user_id = models.BigIntegerField('上传人ID', db_index=True)
    upload_time = models.DateTimeField('上传时间', auto_now_add=True, db_index=True)
    publish_status = models.SmallIntegerField('发布状态', choices=PUBLISH_STATUS_CHOICES, default=0, db_index=True)
    publish_time = models.DateTimeField('发布时间', blank=True, null=True, db_index=True)
    description = models.CharField('文件描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'policy_files'
        verbose_name = '政策文件'
        verbose_name_plural = '政策文件'
        indexes = [
            models.Index(fields=['file_type']),
            models.Index(fields=['upload_user_id']),
            models.Index(fields=['upload_time']),
            models.Index(fields=['publish_status']),
            models.Index(fields=['publish_time']),
        ]

    def __str__(self):
        return self.file_name


class PolicyDistribution(BaseModel):
    """
    政策文件下发表
    """
    FEEDBACK_STATUS_CHOICES = (
        (0, '未反馈'),
        (1, '已反馈'),
        (2, '超时未反馈'),
    )
    SUPERVISE_STATUS_CHOICES = (
        (0, '无需督办'),
        (1, '待督办'),
        (2, '已督办'),
    )

    distribution_code = models.CharField('下发编码', max_length=50, unique=True, db_index=True)
    policy_file_id = models.BigIntegerField('政策文件ID', db_index=True)
    target_id = models.BigIntegerField('叫应对象ID', db_index=True)
    feedback_content = models.TextField('反馈内容要求', blank=True, null=True)
    feedback_deadline = models.DateTimeField('反馈截止时间', db_index=True)
    distribution_time = models.DateTimeField('下发时间', auto_now_add=True, db_index=True)
    distribution_user_id = models.BigIntegerField('下发人ID', db_index=True)
    feedback_status = models.SmallIntegerField('反馈状态', choices=FEEDBACK_STATUS_CHOICES, default=0, db_index=True)
    feedback_time = models.DateTimeField('反馈时间', blank=True, null=True)
    feedback_content_actual = models.TextField('实际反馈内容', blank=True, null=True)
    supervise_status = models.SmallIntegerField('督办状态', choices=SUPERVISE_STATUS_CHOICES, default=0, db_index=True)
    supervise_time = models.DateTimeField('督办时间', blank=True, null=True)
    supervise_user_id = models.BigIntegerField('督办人ID', blank=True, null=True, db_index=True)
    description = models.CharField('下发描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'policy_distributions'
        verbose_name = '政策文件下发'
        verbose_name_plural = '政策文件下发'
        indexes = [
            models.Index(fields=['policy_file_id']),
            models.Index(fields=['target_id']),
            models.Index(fields=['feedback_deadline']),
            models.Index(fields=['distribution_time']),
            models.Index(fields=['distribution_user_id']),
            models.Index(fields=['feedback_status']),
            models.Index(fields=['supervise_status']),
            models.Index(fields=['supervise_user_id']),
        ]

    def __str__(self):
        return f'{self.distribution_code} - Policy {self.policy_file_id}'


class CallRecord(BaseModel):
    """
    叫应记录表
    """
    CALL_TYPE_CHOICES = (
        (1, '常态化叫应'),
        (2, '非常态化叫应'),
    )
    CALL_SOURCE_CHOICES = (
        (1, '政策文件下发'),
        (2, '一键叫应'),
        (3, '预警触发'),
    )
    CALL_STATUS_CHOICES = (
        (0, '待发送'),
        (1, '发送中'),
        (2, '发送成功'),
        (3, '发送失败'),
    )
    RECEIVE_STATUS_CHOICES = (
        (0, '未接收'),
        (1, '已接收'),
        (2, '未响应'),
    )
    RESPONSE_STATUS_CHOICES = (
        (0, '未响应'),
        (1, '已响应'),
    )

    call_code = models.CharField('叫应编码', max_length=50, unique=True, db_index=True)
    call_type = models.SmallIntegerField('叫应类型', choices=CALL_TYPE_CHOICES, default=1, db_index=True)
    call_source = models.SmallIntegerField('叫应来源', choices=CALL_SOURCE_CHOICES, default=1, db_index=True)
    policy_distribution_id = models.BigIntegerField('政策文件下发ID', blank=True, null=True, db_index=True,
                                                    help_text='常态化叫应')
    warning_id = models.BigIntegerField('预警ID', blank=True, null=True, db_index=True, help_text='预警触发')
    target_id = models.BigIntegerField('叫应对象ID', blank=True, null=True, db_index=True, help_text='常态化叫应')
    person_id = models.BigIntegerField('叫应人员ID', blank=True, null=True, db_index=True, help_text='非常态化叫应')
    group_id = models.BigIntegerField('叫应分组ID', blank=True, null=True, db_index=True, help_text='非常态化叫应')
    call_channel = models.CharField('叫应渠道', max_length=20, db_index=True,
                                    help_text='system-系统消息，sms-短信，phone-电话')
    call_content = models.TextField('叫应内容')
    call_time = models.DateTimeField('叫应时间', auto_now_add=True, db_index=True)
    call_status = models.SmallIntegerField('叫应状态', choices=CALL_STATUS_CHOICES, default=0, db_index=True)
    receive_status = models.SmallIntegerField('接收状态', choices=RECEIVE_STATUS_CHOICES, default=0, db_index=True)
    receive_time = models.DateTimeField('接收时间', blank=True, null=True, db_index=True)
    response_status = models.SmallIntegerField('响应状态', choices=RESPONSE_STATUS_CHOICES, default=0, db_index=True)
    response_time = models.DateTimeField('响应时间', blank=True, null=True)
    response_content = models.TextField('响应内容', blank=True, null=True)
    retry_count = models.IntegerField('重试次数', default=0)
    last_retry_time = models.DateTimeField('最后重试时间', blank=True, null=True)
    error_message = models.CharField('错误信息', max_length=500, blank=True, null=True, help_text='发送失败时')
    external_call_id = models.CharField('外部叫应ID', max_length=100, blank=True, null=True, db_index=True,
                                       help_text='智能外呼系统返回的ID')
    description = models.CharField('叫应描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'call_records'
        verbose_name = '叫应记录'
        verbose_name_plural = '叫应记录'
        indexes = [
            models.Index(fields=['call_type']),
            models.Index(fields=['call_source']),
            models.Index(fields=['policy_distribution_id']),
            models.Index(fields=['warning_id']),
            models.Index(fields=['target_id']),
            models.Index(fields=['person_id']),
            models.Index(fields=['group_id']),
            models.Index(fields=['call_channel']),
            models.Index(fields=['call_time']),
            models.Index(fields=['call_status']),
            models.Index(fields=['receive_status']),
            models.Index(fields=['receive_time']),
            models.Index(fields=['response_status']),
            models.Index(fields=['external_call_id']),
        ]

    def __str__(self):
        return f'{self.call_code} - {self.get_call_type_display()}'

