"""
Swagger/OpenAPI 自定义配置
用于统一设置中文标签
"""
from drf_yasg.inspectors import SwaggerAutoSchema


class ChineseTagsAutoSchema(SwaggerAutoSchema):
    """
    自定义Swagger Schema生成器，统一使用中文标签
    """
    # 定义ViewSet类名到中文标签的映射
    TAG_MAPPING = {
        # 用户权限管理模块
        'OrganizationViewSet': '组织管理',
        'PermissionViewSet': '权限管理',
        'RoleViewSet': '角色管理',
        'UserViewSet': '用户管理',
        
        # 风险监测预警模块
        'WarningLevelViewSet': '预警级别',
        'WarningRuleViewSet': '预警规则',
        'RiskMonitorViewSet': '风险监测点',
        'AlarmRecordViewSet': '报警记录',
        'RiskWarningViewSet': '风险预警',
        'AlarmStatisticsViewSet': '报警统计',
        'RiskHiddenDangerViewSet': '隐患排查',
        'RiskRectificationViewSet': '隐患整改',
        
        # 简报模块
        'BriefTemplateViewSet': '简报模板',
        'BriefStrategyViewSet': '简报策略',
        'BriefDataViewSet': '简报数据',
        'BriefPushViewSet': '简报推送',
        
        # 叫应模块
        'CallGroupViewSet': '叫应分组',
        'CallTargetViewSet': '叫应对象',
        'CallPersonViewSet': '叫应人员',
        'PolicyFileViewSet': '政策文件',
        'PolicyDistributionViewSet': '政策文件下发',
        'CallRecordViewSet': '叫应记录',
        'EmergencyCallViewSet': '一键叫应',
        
        # 预案模块
        'EmergencyPlanViewSet': '应急预案',
        'PlanStructureViewSet': '预案结构',
        'PlanFlowViewSet': '预案流程',
        'PlanTaskViewSet': '预案任务',
        'PlanExecutionViewSet': '预案执行记录',
        'PlanTaskExecutionViewSet': '预案任务执行记录',
        
        # 安全态势展示模块
        'SafetyResourceViewSet': '安全资源',
        'SafetyTargetViewSet': '防护目标',
        'ShelterViewSet': '避难场所',
        'IndustryStatusViewSet': '行业态势',
        'RegionStatusViewSet': '区域态势',
        'MonitorDataViewSet': '监测数据',
        'WarningEventViewSet': '预警事件',
        'HazardSourceViewSet': '危险源',
        'VideoMonitorViewSet': '视频监控设施',
        
        # 演练监督模块
        'DrillEventViewSet': '演练事件',
        'DrillEvaluationViewSet': '演练评价',
        'DrillSummaryViewSet': '演练总结',
        'DrillAnalysisViewSet': '演练分析',
        
        # 系统管理模块
        'DataSourceViewSet': '数据源',
        'MessageTemplateViewSet': '消息模板',
    }

    def get_tags(self, operation_keys=None):
        """
        获取标签，根据ViewSet类名或operation_keys映射到中文标签
        """
        # 尝试从ViewSet类获取标签
        view_class = None
        if hasattr(self.view, 'cls'):
            view_class = self.view.cls
        elif hasattr(self.view, '__class__'):
            view_class = self.view.__class__
        
        if view_class:
            view_class_name = view_class.__name__
            if view_class_name in self.TAG_MAPPING:
                return [self.TAG_MAPPING[view_class_name]]
        
        # 尝试从operation_keys获取（用于函数视图或无法识别类名的情况）
        if operation_keys:
            # operation_keys格式: ['api', 'v1', 'risk', 'warning-levels', 'list']
            # 提取模块名（通常是第三个元素）
            if len(operation_keys) >= 3:
                module_key = operation_keys[2]
                # 将模块名转换为中文
                module_mapping = {
                    'auth': '认证',
                    'risk': '风险监测预警',
                    'brief': '简报',
                    'call': '叫应',
                    'plan': '预案',
                    'safety': '安全态势',
                    'drill': '演练',
                    'system': '系统管理',
                }
                if module_key in module_mapping:
                    return [module_mapping[module_key]]
        
        # 默认返回父类方法
        tags = super().get_tags(operation_keys)
        # 如果父类返回的标签是英文，尝试转换
        if tags and len(tags) > 0:
            tag = tags[0]
            # 如果标签是英文模块名，转换为中文
            module_mapping = {
                'auth': '认证',
                'risk': '风险监测预警',
                'brief': '简报',
                'call': '叫应',
                'plan': '预案',
                'safety': '安全态势',
                'drill': '演练',
                'system': '系统管理',
            }
            if tag in module_mapping:
                return [module_mapping[tag]]
        
        return tags

