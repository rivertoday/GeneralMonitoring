"""
安全态势展示模块 - 数据模型
"""
from django.db import models
from apps.common.models import BaseModel


class SafetyResource(BaseModel):
    """
    安全资源表
    """
    RESOURCE_TYPE_CHOICES = (
        (1, '救援队伍'),
        (2, '应急专家'),
        (3, '物资装备'),
    )

    resource_code = models.CharField('资源编码', max_length=50, unique=True, db_index=True)
    resource_name = models.CharField('资源名称', max_length=200)
    resource_type = models.SmallIntegerField('资源类型', choices=RESOURCE_TYPE_CHOICES, default=1, db_index=True)
    sub_type = models.CharField('子类型', max_length=50, blank=True, null=True, db_index=True,
                               help_text='救援队伍、专家、物资的子分类')
    location = models.TextField('地理位置（WKT格式）', blank=True, null=True, help_text='POINT类型的WKT格式字符串')
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    organization_id = models.BigIntegerField('所属组织ID', blank=True, null=True, db_index=True)
    contact_person = models.CharField('联系人', max_length=50, blank=True, null=True)
    contact_phone = models.CharField('联系电话', max_length=20, blank=True, null=True, db_index=True)
    capacity = models.IntegerField('容量/人数', blank=True, null=True, help_text='救援队伍、避难场所等')
    equipment_info = models.TextField('装备信息', blank=True, null=True, help_text='JSON格式，物资装备类型')
    expert_field = models.CharField('专家领域', max_length=200, blank=True, null=True, help_text='应急专家类型')
    expert_level = models.CharField('专家级别', max_length=50, blank=True, null=True, db_index=True, help_text='应急专家类型')
    quantity = models.IntegerField('数量', default=0, help_text='物资装备类型')
    unit = models.CharField('单位', max_length=20, blank=True, null=True, help_text='物资装备类型')
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    description = models.CharField('资源描述', max_length=255, blank=True, null=True)
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'safety_resources'
        verbose_name = '安全资源'
        verbose_name_plural = '安全资源'
        indexes = [
            models.Index(fields=['resource_type']),
            models.Index(fields=['sub_type']),
            models.Index(fields=['longitude']),
            models.Index(fields=['latitude']),
            models.Index(fields=['street']),
            models.Index(fields=['organization_id']),
            models.Index(fields=['contact_phone']),
            models.Index(fields=['expert_level']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.resource_name


class SafetyTarget(BaseModel):
    """
    防护目标表
    """
    TARGET_TYPE_CHOICES = (
        (1, '学校'),
        (2, '居民区'),
        (3, '医院'),
        (4, '商场'),
        (5, '其他人员密集场所'),
    )
    RISK_LEVEL_CHOICES = (
        (1, '高'),
        (2, '中'),
        (3, '低'),
    )

    target_code = models.CharField('目标编码', max_length=50, unique=True, db_index=True)
    target_name = models.CharField('目标名称', max_length=200)
    target_type = models.SmallIntegerField('目标类型', choices=TARGET_TYPE_CHOICES, default=1, db_index=True)
    location = models.TextField('地理位置（WKT格式）', blank=True, null=True, help_text='POINT类型的WKT格式字符串')
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    population = models.IntegerField('人口数量', blank=True, null=True)
    area = models.DecimalField('占地面积（平方米）', max_digits=10, decimal_places=2, blank=True, null=True)
    risk_level = models.SmallIntegerField('风险等级', choices=RISK_LEVEL_CHOICES, blank=True, null=True, db_index=True)
    contact_person = models.CharField('联系人', max_length=50, blank=True, null=True)
    contact_phone = models.CharField('联系电话', max_length=20, blank=True, null=True, db_index=True)
    description = models.CharField('目标描述', max_length=255, blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'safety_targets'
        verbose_name = '防护目标'
        verbose_name_plural = '防护目标'
        indexes = [
            models.Index(fields=['target_type']),
            models.Index(fields=['longitude']),
            models.Index(fields=['latitude']),
            models.Index(fields=['street']),
            models.Index(fields=['risk_level']),
            models.Index(fields=['contact_phone']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.target_name


class Shelter(BaseModel):
    """
    避难场所表
    """
    SHELTER_TYPE_CHOICES = (
        (1, '公园'),
        (2, '广场'),
        (3, '体育场'),
        (4, '学校'),
        (5, '其他'),
    )

    shelter_code = models.CharField('场所编码', max_length=50, unique=True, db_index=True)
    shelter_name = models.CharField('场所名称', max_length=200)
    shelter_type = models.SmallIntegerField('场所类型', choices=SHELTER_TYPE_CHOICES, default=1, db_index=True)
    location = models.TextField('地理位置（WKT格式）', blank=True, null=True, help_text='POINT类型的WKT格式字符串')
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    capacity = models.IntegerField('容纳能力（人数）', default=0)
    area = models.DecimalField('占地面积（平方米）', max_digits=10, decimal_places=2, blank=True, null=True)
    facilities = models.TextField('设施信息', blank=True, null=True, help_text='JSON格式')
    contact_person = models.CharField('联系人', max_length=50, blank=True, null=True)
    contact_phone = models.CharField('联系电话', max_length=20, blank=True, null=True, db_index=True)
    description = models.CharField('场所描述', max_length=255, blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'shelters'
        verbose_name = '避难场所'
        verbose_name_plural = '避难场所'
        indexes = [
            models.Index(fields=['shelter_type']),
            models.Index(fields=['longitude']),
            models.Index(fields=['latitude']),
            models.Index(fields=['street']),
            models.Index(fields=['contact_phone']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.shelter_name


class IndustryStatus(models.Model):
    """
    行业态势表
    """
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )

    stat_date = models.DateField('统计日期', db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, db_index=True)
    alarm_count = models.IntegerField('报警数量', default=0)
    warning_count = models.IntegerField('预警数量', default=0)
    risk_count = models.IntegerField('风险隐患数量', default=0)
    risk_level_1_count = models.IntegerField('红色I级风险数量', default=0)
    risk_level_2_count = models.IntegerField('橙色Ⅱ级风险数量', default=0)
    risk_level_3_count = models.IntegerField('黄色Ⅲ级风险数量', default=0)
    risk_level_4_count = models.IntegerField('蓝色Ⅳ级风险数量', default=0)
    status_data = models.TextField('详细态势数据', blank=True, null=True, help_text='JSON格式')
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'industry_status'
        verbose_name = '行业态势'
        verbose_name_plural = '行业态势'
        unique_together = [['stat_date', 'industry_type']]
        indexes = [
            models.Index(fields=['stat_date']),
            models.Index(fields=['industry_type']),
        ]

    def __str__(self):
        return f'{self.stat_date} - {self.get_industry_type_display()}'


class RegionStatus(models.Model):
    """
    区域态势表
    """
    stat_date = models.DateField('统计日期', db_index=True)
    street = models.CharField('所属街道', max_length=100, db_index=True)
    alarm_count = models.IntegerField('报警数量', default=0)
    warning_count = models.IntegerField('预警数量', default=0)
    risk_count = models.IntegerField('风险隐患数量', default=0)
    risk_level_1_count = models.IntegerField('红色I级风险数量', default=0)
    risk_level_2_count = models.IntegerField('橙色Ⅱ级风险数量', default=0)
    risk_level_3_count = models.IntegerField('黄色Ⅲ级风险数量', default=0)
    risk_level_4_count = models.IntegerField('蓝色Ⅳ级风险数量', default=0)
    risk_color = models.CharField('风险颜色', max_length=20, blank=True, null=True, db_index=True,
                                  help_text='red-红色，orange-橙色，yellow-黄色，blue-蓝色（用于四色图渲染）')
    status_data = models.TextField('详细态势数据', blank=True, null=True, help_text='JSON格式')
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'region_status'
        verbose_name = '区域态势'
        verbose_name_plural = '区域态势'
        unique_together = [['stat_date', 'street']]
        indexes = [
            models.Index(fields=['stat_date']),
            models.Index(fields=['street']),
            models.Index(fields=['risk_color']),
        ]

    def __str__(self):
        return f'{self.stat_date} - {self.street}'


class MonitorData(models.Model):
    """
    监测数据表（用于大屏展示）
    """
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )

    monitor_id = models.BigIntegerField('监测点ID', db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, db_index=True)
    data_time = models.DateTimeField('数据时间', db_index=True)
    monitor_value = models.DecimalField('监测数值', max_digits=10, decimal_places=2, blank=True, null=True)
    monitor_unit = models.CharField('监测单位', max_length=20, blank=True, null=True)
    online_status = models.SmallIntegerField('在线状态', default=1, db_index=True, help_text='0-离线，1-在线')
    data_source = models.CharField('数据来源', max_length=50, blank=True, null=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'monitor_data'
        verbose_name = '监测数据'
        verbose_name_plural = '监测数据'
        indexes = [
            models.Index(fields=['monitor_id']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['data_time']),
            models.Index(fields=['online_status']),
        ]

    def __str__(self):
        return f'Monitor {self.monitor_id} - {self.data_time}'


class WarningEvent(BaseModel):
    """
    预警事件表（用于大屏展示）
    """
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )
    WARNING_STATUS_CHOICES = (
        (0, '未发布'),
        (1, '已发布'),
        (2, '处理中'),
        (3, '已处置'),
        (4, '已关闭'),
    )

    warning_id = models.BigIntegerField('预警ID', db_index=True)
    warning_code = models.CharField('预警事件编码', max_length=50, unique=True, db_index=True)
    warning_level_id = models.BigIntegerField('预警级别ID', db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, db_index=True)
    warning_type = models.CharField('预警类型', max_length=50, db_index=True)
    warning_title = models.CharField('预警标题', max_length=200)
    location = models.TextField('预警位置（WKT格式）', blank=True, null=True, help_text='POINT类型的WKT格式字符串')
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    warning_time = models.DateTimeField('预警时间', db_index=True)
    warning_status = models.SmallIntegerField('预警状态', choices=WARNING_STATUS_CHOICES, default=0, db_index=True)
    nearby_monitor_count = models.IntegerField('附近监测点数量', default=0)
    nearby_risk_count = models.IntegerField('附近危险源数量', default=0)
    nearby_resource_count = models.IntegerField('附近应急资源数量', default=0)
    description = models.CharField('预警描述', max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'warning_events'
        verbose_name = '预警事件'
        verbose_name_plural = '预警事件'
        indexes = [
            models.Index(fields=['warning_id']),
            models.Index(fields=['warning_level_id']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['warning_type']),
            models.Index(fields=['longitude']),
            models.Index(fields=['latitude']),
            models.Index(fields=['street']),
            models.Index(fields=['warning_time']),
            models.Index(fields=['warning_status']),
        ]

    def __str__(self):
        return f'{self.warning_code} - {self.warning_title}'


class HazardSource(BaseModel):
    """
    危险源表
    """
    SOURCE_TYPE_CHOICES = (
        (1, '重大危险源'),
        (2, '一般危险源'),
    )
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )
    RISK_LEVEL_CHOICES = (
        (1, '高'),
        (2, '中'),
        (3, '低'),
    )

    source_code = models.CharField('危险源编码', max_length=50, unique=True, db_index=True)
    source_name = models.CharField('危险源名称', max_length=200)
    source_type = models.SmallIntegerField('危险源类型', choices=SOURCE_TYPE_CHOICES, default=1, db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, db_index=True)
    organization_id = models.BigIntegerField('所属企业ID', db_index=True)
    location = models.TextField('危险源位置（WKT格式）', blank=True, null=True, help_text='POINT类型的WKT格式字符串')
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    risk_level = models.SmallIntegerField('风险等级', choices=RISK_LEVEL_CHOICES, default=1, db_index=True)
    material_type = models.CharField('危险物质类型', max_length=100, blank=True, null=True)
    material_quantity = models.DecimalField('危险物质数量', max_digits=10, decimal_places=2, blank=True, null=True)
    material_unit = models.CharField('数量单位', max_length=20, blank=True, null=True)
    safety_measures = models.TextField('安全措施', blank=True, null=True)
    emergency_plan_id = models.BigIntegerField('关联应急预案ID', blank=True, null=True, db_index=True)
    contact_person = models.CharField('联系人', max_length=50, blank=True, null=True)
    contact_phone = models.CharField('联系电话', max_length=20, blank=True, null=True, db_index=True)
    description = models.CharField('危险源描述', max_length=255, blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'hazard_sources'
        verbose_name = '危险源'
        verbose_name_plural = '危险源'
        indexes = [
            models.Index(fields=['source_type']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['organization_id']),
            models.Index(fields=['longitude']),
            models.Index(fields=['latitude']),
            models.Index(fields=['street']),
            models.Index(fields=['risk_level']),
            models.Index(fields=['emergency_plan_id']),
            models.Index(fields=['contact_phone']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.source_name


class VideoMonitor(BaseModel):
    """
    视频监控设施表
    """
    MONITOR_TYPE_CHOICES = (
        (1, '固定监控'),
        (2, '移动监控'),
        (3, '无人机监控'),
    )
    INDUSTRY_TYPE_CHOICES = (
        (1, '森林火灾'),
        (2, '防汛'),
        (3, '交通运输'),
        (4, '危险化学品'),
    )

    monitor_code = models.CharField('监控设施编码', max_length=50, unique=True, db_index=True)
    monitor_name = models.CharField('监控设施名称', max_length=200)
    monitor_type = models.SmallIntegerField('监控类型', choices=MONITOR_TYPE_CHOICES, default=1, db_index=True)
    industry_type = models.SmallIntegerField('行业类型', choices=INDUSTRY_TYPE_CHOICES, db_index=True)
    location = models.TextField('监控位置（WKT格式）', blank=True, null=True, help_text='POINT类型的WKT格式字符串')
    longitude = models.DecimalField('经度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    latitude = models.DecimalField('纬度', max_digits=10, decimal_places=7, blank=True, null=True, db_index=True)
    street = models.CharField('所属街道', max_length=100, blank=True, null=True, db_index=True)
    address = models.CharField('详细地址', max_length=255, blank=True, null=True)
    video_url = models.CharField('视频流地址', max_length=500, blank=True, null=True)
    rtsp_url = models.CharField('RTSP流地址', max_length=500, blank=True, null=True)
    coverage_radius = models.DecimalField('覆盖半径（米）', max_digits=10, decimal_places=2, blank=True, null=True)
    camera_angle = models.DecimalField('摄像头角度（度）', max_digits=5, decimal_places=2, blank=True, null=True)
    online_status = models.SmallIntegerField('在线状态', default=1, db_index=True, help_text='0-离线，1-在线')
    organization_id = models.BigIntegerField('所属组织ID', blank=True, null=True, db_index=True)
    description = models.CharField('监控设施描述', max_length=255, blank=True, null=True)
    status = models.SmallIntegerField('状态', default=1, db_index=True, help_text='0-禁用，1-启用')
    remark = models.TextField('备注信息', blank=True, null=True)

    class Meta:
        db_table = 'video_monitors'
        verbose_name = '视频监控设施'
        verbose_name_plural = '视频监控设施'
        indexes = [
            models.Index(fields=['monitor_type']),
            models.Index(fields=['industry_type']),
            models.Index(fields=['longitude']),
            models.Index(fields=['latitude']),
            models.Index(fields=['street']),
            models.Index(fields=['online_status']),
            models.Index(fields=['organization_id']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return self.monitor_name

