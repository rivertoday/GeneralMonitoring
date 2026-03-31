#!/usr/bin/env python
"""
数据验证和优化脚本
用于验证fixtures数据的完整性、合理性和逻辑性
"""
import os
import sys
import django
from datetime import datetime
from decimal import Decimal
from django.db import models

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import Organization, User
from apps.plan.models import EmergencyPlan, PlanStructure, PlanFlow, PlanTask, PlanExecution
from apps.drill.models import DrillEvent, DrillEvaluation, DrillSummary, DrillAnalysis
from apps.safety.models import SafetyResource, SafetyTarget, Shelter, HazardSource, VideoMonitor
from apps.risk.models import RiskMonitor, RiskWarning, RiskHiddenDanger, AlarmRecord
from apps.call.models import CallPerson, CallGroup, CallTarget, PolicyFile, PolicyDistribution, CallRecord
from apps.brief.models import BriefTemplate, BriefStrategy, BriefData, BriefPush
from apps.system.models import MessageTemplate

# 马鞍山市地理范围（大致）
MAANSHAN_LONGITUDE_MIN = Decimal('118.300000')
MAANSHAN_LONGITUDE_MAX = Decimal('118.700000')
MAANSHAN_LATITUDE_MIN = Decimal('31.500000')
MAANSHAN_LATITUDE_MAX = Decimal('31.900000')

class DataValidator:
    """数据验证器"""
    
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.info = []
        
    def log_error(self, message):
        """记录错误"""
        self.errors.append(message)
        print(f"❌ 错误: {message}")
        
    def log_warning(self, message):
        """记录警告"""
        self.warnings.append(message)
        print(f"⚠️  警告: {message}")
        
    def log_info(self, message):
        """记录信息"""
        self.info.append(message)
        print(f"ℹ️  信息: {message}")
        
    def validate_foreign_keys(self):
        """任务1: 验证数据关联关系完整性"""
        print("\n" + "="*60)
        print("任务1: 验证数据关联关系完整性")
        print("="*60)
        
        # 验证组织关联
        self.log_info("验证组织关联...")
        org_ids = set(Organization.objects.values_list('pk', flat=True))
        
        # 验证用户关联的组织
        invalid_users = User.objects.exclude(organization_id__in=org_ids).exclude(organization_id__isnull=True)
        if invalid_users.exists():
            for user in invalid_users:
                self.log_error(f"用户 {user.username} (ID: {user.pk}) 关联的组织ID {user.organization_id} 不存在")
        else:
            self.log_info("✓ 所有用户关联的组织ID有效")
            
        # 验证预案关联
        self.log_info("验证预案关联...")
        plan_ids = set(EmergencyPlan.objects.values_list('pk', flat=True))
        
        # 验证演练事件关联的预案
        invalid_drill_events = DrillEvent.objects.exclude(
            related_plan_id__in=plan_ids
        ).exclude(related_plan_id__isnull=True)
        if invalid_drill_events.exists():
            for event in invalid_drill_events:
                self.log_error(f"演练事件 {event.event_name} (ID: {event.pk}) 关联的预案ID {event.related_plan_id} 不存在")
        else:
            self.log_info("✓ 所有演练事件关联的预案ID有效")
            
        # 验证演练事件关联的组织
        invalid_drill_orgs = DrillEvent.objects.exclude(organization_id__in=org_ids)
        if invalid_drill_orgs.exists():
            for event in invalid_drill_orgs:
                self.log_error(f"演练事件 {event.event_name} (ID: {event.pk}) 关联的组织ID {event.organization_id} 不存在")
        else:
            self.log_info("✓ 所有演练事件关联的组织ID有效")
            
        # 验证演练评价关联的演练事件
        drill_event_ids = set(DrillEvent.objects.values_list('pk', flat=True))
        invalid_evaluations = DrillEvaluation.objects.exclude(event_id__in=drill_event_ids)
        if invalid_evaluations.exists():
            for eval in invalid_evaluations:
                self.log_error(f"演练评价 (ID: {eval.pk}) 关联的演练事件ID {eval.event_id} 不存在")
        else:
            self.log_info("✓ 所有演练评价关联的演练事件ID有效")
            
        # 验证演练总结关联的演练事件
        invalid_summaries = DrillSummary.objects.exclude(event_id__in=drill_event_ids)
        if invalid_summaries.exists():
            for summary in invalid_summaries:
                self.log_error(f"演练总结 (ID: {summary.pk}) 关联的演练事件ID {summary.event_id} 不存在")
        else:
            self.log_info("✓ 所有演练总结关联的演练事件ID有效")
            
        # 验证预案结构关联的预案
        invalid_structures = PlanStructure.objects.exclude(plan_id__in=plan_ids)
        if invalid_structures.exists():
            for struct in invalid_structures:
                self.log_error(f"预案结构 (ID: {struct.pk}) 关联的预案ID {struct.plan_id} 不存在")
        else:
            self.log_info("✓ 所有预案结构关联的预案ID有效")
            
        # 验证预案流程关联的预案
        invalid_flows = PlanFlow.objects.exclude(plan_id__in=plan_ids)
        if invalid_flows.exists():
            for flow in invalid_flows:
                self.log_error(f"预案流程 {flow.flow_name} (ID: {flow.pk}) 关联的预案ID {flow.plan_id} 不存在")
        else:
            self.log_info("✓ 所有预案流程关联的预案ID有效")
            
        # 验证预案任务关联的预案
        invalid_tasks = PlanTask.objects.exclude(plan_id__in=plan_ids)
        if invalid_tasks.exists():
            for task in invalid_tasks:
                self.log_error(f"预案任务 {task.task_name} (ID: {task.pk}) 关联的预案ID {task.plan_id} 不存在")
        else:
            self.log_info("✓ 所有预案任务关联的预案ID有效")
            
        # 验证预案执行关联的预案
        invalid_executions = PlanExecution.objects.exclude(plan_id__in=plan_ids)
        if invalid_executions.exists():
            for exec in invalid_executions:
                self.log_error(f"预案执行 {exec.execution_code} (ID: {exec.pk}) 关联的预案ID {exec.plan_id} 不存在")
        else:
            self.log_info("✓ 所有预案执行关联的预案ID有效")
            
        # 验证安全资源关联的组织
        invalid_resources = SafetyResource.objects.exclude(
            organization_id__in=org_ids
        ).exclude(organization_id__isnull=True)
        if invalid_resources.exists():
            for resource in invalid_resources:
                self.log_error(f"安全资源 {resource.resource_name} (ID: {resource.pk}) 关联的组织ID {resource.organization_id} 不存在")
        else:
            self.log_info("✓ 所有安全资源关联的组织ID有效")
            
        # 验证危险源关联的组织和预案
        invalid_hazards = HazardSource.objects.exclude(organization_id__in=org_ids)
        if invalid_hazards.exists():
            for hazard in invalid_hazards:
                self.log_error(f"危险源 {hazard.source_name} (ID: {hazard.pk}) 关联的组织ID {hazard.organization_id} 不存在")
        else:
            self.log_info("✓ 所有危险源关联的组织ID有效")
            
        invalid_hazard_plans = HazardSource.objects.exclude(
            emergency_plan_id__in=plan_ids
        ).exclude(emergency_plan_id__isnull=True)
        if invalid_hazard_plans.exists():
            for hazard in invalid_hazard_plans:
                self.log_error(f"危险源 {hazard.source_name} (ID: {hazard.pk}) 关联的预案ID {hazard.emergency_plan_id} 不存在")
        else:
            self.log_info("✓ 所有危险源关联的预案ID有效")
            
        print(f"\n任务1完成: 发现 {len(self.errors)} 个错误, {len(self.warnings)} 个警告")
        
    def validate_geographic_data(self):
        """任务2: 验证地理数据分布合理性"""
        print("\n" + "="*60)
        print("任务2: 验证地理数据分布合理性")
        print("="*60)
        
        # 验证演练事件坐标
        self.log_info("验证演练事件坐标...")
        invalid_events = DrillEvent.objects.filter(
            longitude__lt=MAANSHAN_LONGITUDE_MIN
        ) | DrillEvent.objects.filter(
            longitude__gt=MAANSHAN_LONGITUDE_MAX
        ) | DrillEvent.objects.filter(
            latitude__lt=MAANSHAN_LATITUDE_MIN
        ) | DrillEvent.objects.filter(
            latitude__gt=MAANSHAN_LATITUDE_MAX
        )
        if invalid_events.exists():
            for event in invalid_events:
                self.log_warning(
                    f"演练事件 {event.event_name} (ID: {event.pk}) 坐标 ({event.longitude}, {event.latitude}) "
                    f"不在马鞍山市范围内"
                )
        else:
            self.log_info("✓ 所有演练事件坐标在马鞍山市范围内")
            
        # 验证安全资源坐标
        self.log_info("验证安全资源坐标...")
        invalid_resources = SafetyResource.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            longitude__lt=MAANSHAN_LONGITUDE_MIN
        ) | SafetyResource.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            longitude__gt=MAANSHAN_LONGITUDE_MAX
        ) | SafetyResource.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            latitude__lt=MAANSHAN_LATITUDE_MIN
        ) | SafetyResource.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            latitude__gt=MAANSHAN_LATITUDE_MAX
        )
        if invalid_resources.exists():
            for resource in invalid_resources:
                self.log_warning(
                    f"安全资源 {resource.resource_name} (ID: {resource.pk}) 坐标 "
                    f"({resource.longitude}, {resource.latitude}) 不在马鞍山市范围内"
                )
        else:
            self.log_info("✓ 所有安全资源坐标在马鞍山市范围内")
            
        # 验证防护目标坐标
        self.log_info("验证防护目标坐标...")
        invalid_targets = SafetyTarget.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            longitude__lt=MAANSHAN_LONGITUDE_MIN
        ) | SafetyTarget.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            longitude__gt=MAANSHAN_LONGITUDE_MAX
        ) | SafetyTarget.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            latitude__lt=MAANSHAN_LATITUDE_MIN
        ) | SafetyTarget.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            latitude__gt=MAANSHAN_LATITUDE_MAX
        )
        if invalid_targets.exists():
            for target in invalid_targets:
                self.log_warning(
                    f"防护目标 {target.target_name} (ID: {target.pk}) 坐标 "
                    f"({target.longitude}, {target.latitude}) 不在马鞍山市范围内"
                )
        else:
            self.log_info("✓ 所有防护目标坐标在马鞍山市范围内")
            
        # 验证避难场所坐标
        self.log_info("验证避难场所坐标...")
        invalid_shelters = Shelter.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            longitude__lt=MAANSHAN_LONGITUDE_MIN
        ) | Shelter.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            longitude__gt=MAANSHAN_LONGITUDE_MAX
        ) | Shelter.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            latitude__lt=MAANSHAN_LATITUDE_MIN
        ) | Shelter.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            latitude__gt=MAANSHAN_LATITUDE_MAX
        )
        if invalid_shelters.exists():
            for shelter in invalid_shelters:
                self.log_warning(
                    f"避难场所 {shelter.shelter_name} (ID: {shelter.pk}) 坐标 "
                    f"({shelter.longitude}, {shelter.latitude}) 不在马鞍山市范围内"
                )
        else:
            self.log_info("✓ 所有避难场所坐标在马鞍山市范围内")
            
        # 验证危险源坐标
        self.log_info("验证危险源坐标...")
        invalid_hazards = HazardSource.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            longitude__lt=MAANSHAN_LONGITUDE_MIN
        ) | HazardSource.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            longitude__gt=MAANSHAN_LONGITUDE_MAX
        ) | HazardSource.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            latitude__lt=MAANSHAN_LATITUDE_MIN
        ) | HazardSource.objects.filter(
            longitude__isnull=False, latitude__isnull=False
        ).filter(
            latitude__gt=MAANSHAN_LATITUDE_MAX
        )
        if invalid_hazards.exists():
            for hazard in invalid_hazards:
                self.log_warning(
                    f"危险源 {hazard.source_name} (ID: {hazard.pk}) 坐标 "
                    f"({hazard.longitude}, {hazard.latitude}) 不在马鞍山市范围内"
                )
        else:
            self.log_info("✓ 所有危险源坐标在马鞍山市范围内")
            
        print(f"\n任务2完成: 发现 {len(self.errors)} 个错误, {len(self.warnings)} 个警告")
        
    def validate_time_logic(self):
        """任务3: 验证时间数据逻辑性"""
        print("\n" + "="*60)
        print("任务3: 验证时间数据逻辑性")
        print("="*60)
        
        # 验证BaseModel的时间逻辑 (created_at <= updated_at)
        self.log_info("验证创建时间和更新时间逻辑...")
        invalid_base_models = []
        for model_class in [DrillEvent, DrillEvaluation, DrillSummary, EmergencyPlan, 
                           PlanStructure, PlanFlow, PlanTask, PlanExecution,
                           SafetyResource, SafetyTarget, Shelter, HazardSource, VideoMonitor]:
            invalid = model_class.objects.filter(created_at__gt=models.F('updated_at'))
            if invalid.exists():
                for obj in invalid:
                    invalid_base_models.append(f"{model_class.__name__} (ID: {obj.pk})")
        if invalid_base_models:
            for item in invalid_base_models:
                self.log_error(f"{item}: created_at > updated_at")
        else:
            self.log_info("✓ 所有BaseModel的创建时间和更新时间逻辑正确")
            
        # 验证预案时间逻辑
        self.log_info("验证预案时间逻辑...")
        invalid_plans = EmergencyPlan.objects.filter(
            approve_time__isnull=False,
            publish_time__isnull=False
        ).filter(approve_time__gt=models.F('publish_time'))
        if invalid_plans.exists():
            for plan in invalid_plans:
                self.log_warning(
                    f"预案 {plan.plan_name} (ID: {plan.pk}): 审批时间晚于发布时间"
                )
        else:
            self.log_info("✓ 所有预案的审批时间和发布时间逻辑正确")
            
        invalid_plans2 = EmergencyPlan.objects.filter(
            effective_time__isnull=False,
            expire_time__isnull=False
        ).filter(effective_time__gt=models.F('expire_time'))
        if invalid_plans2.exists():
            for plan in invalid_plans2:
                self.log_error(
                    f"预案 {plan.plan_name} (ID: {plan.pk}): 生效时间晚于失效时间"
                )
        else:
            self.log_info("✓ 所有预案的生效时间和失效时间逻辑正确")
            
        # 验证预案执行时间逻辑
        self.log_info("验证预案执行时间逻辑...")
        invalid_executions = PlanExecution.objects.filter(
            start_time__isnull=False,
            end_time__isnull=False
        ).filter(start_time__gt=models.F('end_time'))
        if invalid_executions.exists():
            for exec in invalid_executions:
                self.log_error(
                    f"预案执行 {exec.execution_code} (ID: {exec.pk}): 开始时间晚于结束时间"
                )
        else:
            self.log_info("✓ 所有预案执行的开始时间和结束时间逻辑正确")
            
        # 验证演练事件时间逻辑
        self.log_info("验证演练事件时间逻辑...")
        invalid_drill_events = DrillEvent.objects.filter(
            created_at__gt=models.F('event_time')
        )
        if invalid_drill_events.exists():
            for event in invalid_drill_events:
                self.log_warning(
                    f"演练事件 {event.event_name} (ID: {event.pk}): 创建时间晚于事件时间"
                )
        else:
            self.log_info("✓ 所有演练事件的时间逻辑正确")
            
        # 验证演练评价时间逻辑
        self.log_info("验证演练评价时间逻辑...")
        drill_events = DrillEvent.objects.all()
        for event in drill_events:
            evaluations = DrillEvaluation.objects.filter(event_id=event.pk)
            for eval in evaluations:
                if eval.evaluation_time < event.event_time:
                    self.log_warning(
                        f"演练评价 (ID: {eval.pk}): 评价时间早于演练事件时间"
                    )
        self.log_info("✓ 演练评价时间逻辑验证完成")
            
        print(f"\n任务3完成: 发现 {len(self.errors)} 个错误, {len(self.warnings)} 个警告")
        
    def validate_data_quality(self):
        """任务4: 优化数据质量和真实性"""
        print("\n" + "="*60)
        print("任务4: 优化数据质量和真实性")
        print("="*60)
        
        # 验证编码唯一性
        self.log_info("验证编码唯一性...")
        # 这个在数据库层面已经通过unique约束保证，这里只做统计
        self.log_info(f"✓ 编码唯一性由数据库约束保证")
        
        # 验证必填字段
        self.log_info("验证必填字段...")
        # 演练事件必填字段
        invalid_events = DrillEvent.objects.filter(
            event_code__isnull=True
        ) | DrillEvent.objects.filter(
            event_name__isnull=True
        ) | DrillEvent.objects.filter(
            event_time__isnull=True
        )
        if invalid_events.exists():
            for event in invalid_events:
                self.log_error(f"演练事件 (ID: {event.pk}): 必填字段缺失")
        else:
            self.log_info("✓ 所有演练事件的必填字段完整")
            
        # 验证数据格式
        self.log_info("验证数据格式...")
        # 验证手机号格式（简单验证）
        import re
        phone_pattern = re.compile(r'^1[3-9]\d{9}$|^0\d{2,3}-?\d{7,8}$')
        
        for model_class, phone_field in [
            (SafetyResource, 'contact_phone'),
            (SafetyTarget, 'contact_phone'),
            (Shelter, 'contact_phone'),
            (HazardSource, 'contact_phone'),
            (VideoMonitor, None),  # VideoMonitor没有contact_phone
        ]:
            if phone_field:
                invalid_phones = []
                for obj in model_class.objects.exclude(**{f'{phone_field}__isnull': True}):
                    phone = getattr(obj, phone_field)
                    if phone and not phone_pattern.match(phone.replace('-', '').replace(' ', '')):
                        invalid_phones.append(f"{model_class.__name__} {obj.pk}: {phone}")
                if invalid_phones:
                    for item in invalid_phones[:5]:  # 只显示前5个
                        self.log_warning(f"手机号格式可能不正确: {item}")
                else:
                    self.log_info(f"✓ {model_class.__name__} 的手机号格式验证通过")
        
        # 验证坐标精度
        self.log_info("验证坐标精度...")
        # 检查坐标是否精确到小数点后6位
        invalid_coords = []
        for event in DrillEvent.objects.exclude(longitude__isnull=True):
            lon_str = str(event.longitude)
            lat_str = str(event.latitude)
            if '.' in lon_str:
                decimal_places = len(lon_str.split('.')[1])
                if decimal_places < 6:
                    invalid_coords.append(f"演练事件 {event.pk}: 经度精度不足 ({decimal_places}位)")
        if invalid_coords:
            for item in invalid_coords[:5]:
                self.log_warning(item)
        else:
            self.log_info("✓ 坐标精度验证通过")
            
        # 验证状态分布
        self.log_info("验证状态分布...")
        # 检查演练状态分布
        status_counts = DrillEvent.objects.values('drill_status').annotate(
            count=models.Count('pk')
        )
        self.log_info(f"演练状态分布: {dict(status_counts)}")
        
        # 检查预案状态分布
        plan_status_counts = EmergencyPlan.objects.values('plan_status').annotate(
            count=models.Count('pk')
        )
        self.log_info(f"预案状态分布: {dict(plan_status_counts)}")
        
        print(f"\n任务4完成: 发现 {len(self.errors)} 个错误, {len(self.warnings)} 个警告")
        
    def validate_business_flow(self):
        """任务5: 测试业务流程完整性"""
        print("\n" + "="*60)
        print("任务5: 测试业务流程完整性")
        print("="*60)
        
        # 测试演练业务流程
        self.log_info("测试演练业务流程...")
        completed_events = DrillEvent.objects.filter(drill_status=2)  # 已完成的演练
        for event in completed_events[:3]:  # 只测试前3个
            # 检查是否有评价
            evaluations = DrillEvaluation.objects.filter(event_id=event.pk)
            if not evaluations.exists():
                self.log_warning(f"已完成的演练事件 {event.event_name} (ID: {event.pk}) 没有评价记录")
            else:
                self.log_info(f"✓ 演练事件 {event.event_name} 有 {evaluations.count()} 条评价记录")
                
            # 检查是否有总结
            summaries = DrillSummary.objects.filter(event_id=event.pk)
            if not summaries.exists():
                self.log_warning(f"已完成的演练事件 {event.event_name} (ID: {event.pk}) 没有总结记录")
            else:
                self.log_info(f"✓ 演练事件 {event.event_name} 有总结记录")
                
        # 测试预案业务流程
        self.log_info("测试预案业务流程...")
        published_plans = EmergencyPlan.objects.filter(plan_status=1)  # 已发布的预案
        for plan in published_plans[:3]:  # 只测试前3个
            # 检查是否有结构
            structures = PlanStructure.objects.filter(plan_id=plan.pk)
            if not structures.exists():
                self.log_warning(f"已发布的预案 {plan.plan_name} (ID: {plan.pk}) 没有结构数据")
            else:
                self.log_info(f"✓ 预案 {plan.plan_name} 有 {structures.count()} 个结构节点")
                
            # 检查是否有流程
            flows = PlanFlow.objects.filter(plan_id=plan.pk)
            if not flows.exists():
                self.log_warning(f"已发布的预案 {plan.plan_name} (ID: {plan.pk}) 没有流程数据")
            else:
                self.log_info(f"✓ 预案 {plan.plan_name} 有 {flows.count()} 个流程")
                
            # 检查是否有任务
            tasks = PlanTask.objects.filter(plan_id=plan.pk)
            if not tasks.exists():
                self.log_warning(f"已发布的预案 {plan.plan_name} (ID: {plan.pk}) 没有任务数据")
            else:
                self.log_info(f"✓ 预案 {plan.plan_name} 有 {tasks.count()} 个任务")
                
        # 测试安全资源业务流程
        self.log_info("测试安全资源业务流程...")
        resources = SafetyResource.objects.all()[:5]
        for resource in resources:
            if resource.longitude and resource.latitude:
                self.log_info(f"✓ 安全资源 {resource.resource_name} 有完整的地理信息")
            else:
                self.log_warning(f"安全资源 {resource.resource_name} (ID: {resource.pk}) 缺少地理信息")
                
        print(f"\n任务5完成: 发现 {len(self.errors)} 个错误, {len(self.warnings)} 个警告")
        
    def generate_report(self):
        """生成验证报告"""
        print("\n" + "="*60)
        print("验证报告汇总")
        print("="*60)
        print(f"总错误数: {len(self.errors)}")
        print(f"总警告数: {len(self.warnings)}")
        print(f"总信息数: {len(self.info)}")
        
        if self.errors:
            print("\n错误列表:")
            for i, error in enumerate(self.errors[:10], 1):  # 只显示前10个
                print(f"  {i}. {error}")
            if len(self.errors) > 10:
                print(f"  ... 还有 {len(self.errors) - 10} 个错误未显示")
                
        if self.warnings:
            print("\n警告列表:")
            for i, warning in enumerate(self.warnings[:10], 1):  # 只显示前10个
                print(f"  {i}. {warning}")
            if len(self.warnings) > 10:
                print(f"  ... 还有 {len(self.warnings) - 10} 个警告未显示")
                
        return {
            'errors': len(self.errors),
            'warnings': len(self.warnings),
            'info': len(self.info)
        }

def main():
    """主函数"""
    print("="*60)
    print("数据验证和优化脚本")
    print("="*60)
    
    validator = DataValidator()
    
    # 依次执行5项任务
    validator.validate_foreign_keys()
    validator.validate_geographic_data()
    validator.validate_time_logic()
    validator.validate_data_quality()
    validator.validate_business_flow()
    
    # 生成报告
    report = validator.generate_report()
    
    print("\n" + "="*60)
    if report['errors'] == 0 and report['warnings'] == 0:
        print("✅ 数据验证通过！")
    elif report['errors'] == 0:
        print("⚠️  数据验证完成，有警告但无错误")
    else:
        print("❌ 数据验证发现错误，请检查并修复")
    print("="*60)
    
    return report

if __name__ == '__main__':
    main()

