/**
 * 风险监测预警模块类型定义
 */

/**
 * 监测类型
 */
export type MonitorType = 1 | 2 | 3 // 1-实时监测，2-全域监测，3-重点监测

/**
 * 行业类型
 */
export type IndustryType = 1 | 2 | 3 | 4 // 1-森林火灾，2-防汛，3-交通运输，4-危险化学品

/**
 * 风险监测点
 */
export interface RiskMonitor {
  id: number
  monitor_code: string
  monitor_name: string
  monitor_type: MonitorType
  monitor_type_display: string
  industry_type: IndustryType
  industry_type_display: string
  data_source_id: number | null
  location: string | null
  longitude: number | null
  latitude: number | null
  street: string | null
  address: string | null
  monitor_value: number | null
  monitor_unit: string | null
  threshold_min: number | null
  threshold_max: number | null
  online_status: 0 | 1
  online_status_display: string
  last_data_time: string | null
  status: 0 | 1
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 风险监测点列表查询参数
 */
export interface RiskMonitorListParams {
  page?: number
  page_size?: number
  monitor_type?: MonitorType
  industry_type?: IndustryType
  data_source_id?: number
  online_status?: 0 | 1
  status?: 0 | 1
  street?: string
  search?: string
  ordering?: string
}

/**
 * 风险监测点创建/更新参数
 */
export interface RiskMonitorFormData {
  monitor_code: string
  monitor_name: string
  monitor_type: MonitorType
  industry_type: IndustryType
  data_source_id?: number | null
  longitude?: number | null
  latitude?: number | null
  street?: string | null
  address?: string | null
  monitor_value?: number | null
  monitor_unit?: string | null
  threshold_min?: number | null
  threshold_max?: number | null
  online_status?: 0 | 1
  status?: 0 | 1
  description?: string | null
  remark?: string | null
}

/**
 * 预警级别
 */
export interface WarningLevel {
  id: number
  level_code: string
  level_name: string
  level_color: 'red' | 'orange' | 'yellow' | 'blue'
  level_color_display: string
  severity: number
  response_org: string | null
  response_time: number | null
  description: string | null
  status: 0 | 1
  sort_order: number
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 预警规则
 */
export interface WarningRule {
  id: number
  rule_code: string
  rule_name: string
  rule_type: 1 | 2 // 1-预警生成规则，2-预警处置规则
  rule_type_display: string
  industry_type: IndustryType
  industry_type_display: string
  warning_level: number | null
  warning_level_detail?: WarningLevel | null
  condition_config: string
  condition_config_dict?: any
  action_config: string | null
  action_config_dict?: any
  response_time: number | null
  handle_time: number | null
  feedback_time: number | null
  status: 0 | 1
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 报警记录
 */
export interface AlarmRecord {
  id: number
  alarm_code: string
  monitor: number
  monitor_id: number
  monitor_detail?: RiskMonitor
  industry_type: IndustryType
  industry_type_display: string
  alarm_type: string
  alarm_value: number | null
  threshold_value: number | null
  longitude: number | null
  latitude: number | null
  street: string | null
  address: string | null
  alarm_time: string
  alarm_duration: number | null
  alarm_status: 0 | 1 | 2 | 3 // 0-未处理，1-处理中，2-已处理，3-已忽略
  alarm_status_display?: string
  handle_user_id: number | null
  handle_time: string | null
  handle_result: string | null
  feedback_time: string | null
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 风险预警
 */
export interface RiskWarning {
  id: number
  warning_code: string
  warning_level_id: number
  warning_level_detail?: WarningLevel
  warning_rule_id: number | null
  industry_type: IndustryType
  industry_type_display: string
  warning_type: string
  warning_analysis_type: 1 | 2 | 3 | null // 1-突出预警，2-同比预警，3-环比预警
  warning_title: string
  warning_content: string
  longitude: number | null
  latitude: number | null
  street: string | null
  address: string | null
  warning_time: string
  warning_source: 1 | 2 // 1-自动生成，2-手动创建
  warning_status: 0 | 1 | 2 | 3 | 4 // 0-未发布，1-已发布，2-处理中，3-已处置，4-已关闭
  warning_status_display?: string
  response_org_id: number | null
  response_user_id: number | null
  response_time: string | null
  handle_time: string | null
  handle_result: string | null
  feedback_time: string | null
  publish_time: string | null
  related_alarm_ids: string | null
  related_plan_id: number | null
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 风险隐患
 */
export interface RiskHiddenDanger {
  id: number
  danger_code: string
  danger_name: string
  monitor_id: number
  monitor_detail?: RiskMonitor
  organization_id: number
  organization_name?: string
  industry_type: 4 // 固定为4-危险化学品
  industry_type_display: string
  longitude: number | null
  latitude: number | null
  street: string | null
  address: string | null
  danger_level: 1 | 2 | 3 // 1-重大，2-较大，3-一般
  danger_level_display?: string
  danger_category: string | null
  danger_description: string
  discover_time: string
  discover_user_id: number | null
  discover_user_name?: string
  status: 0 | 1 | 2 | 3 // 0-待整改，1-整改中，2-已完成，3-已关闭
  status_display?: string
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 风险隐患列表查询参数
 */
export interface RiskHiddenDangerListParams {
  page?: number
  page_size?: number
  monitor_id?: number
  organization_id?: number
  danger_level?: 1 | 2 | 3
  danger_category?: string
  status?: 0 | 1 | 2 | 3
  street?: string
  start_time?: string
  end_time?: string
  search?: string
  ordering?: string
}

/**
 * 风险隐患创建/更新参数
 */
export interface RiskHiddenDangerFormData {
  danger_code: string
  danger_name: string
  monitor_id: number
  organization_id: number
  longitude?: number | null
  latitude?: number | null
  street?: string | null
  address?: string | null
  danger_level: 1 | 2 | 3
  danger_category?: string | null
  danger_description: string
  discover_time: string
  discover_user_id?: number | null
  status?: 0 | 1 | 2 | 3
  remark?: string | null
}

/**
 * 隐患整改
 */
export interface RiskRectification {
  id: number
  rectification_code: string
  danger_id: number
  danger_detail?: RiskHiddenDanger
  rectification_plan: string
  rectification_measures: string
  responsible_user_id: number
  responsible_user_name?: string
  responsible_org_id: number
  responsible_org_name?: string
  plan_start_time: string
  plan_end_time: string
  actual_start_time: string | null
  actual_end_time: string | null
  rectification_status: 0 | 1 | 2 | 3 // 0-待开始，1-进行中，2-已完成，3-已延期
  rectification_status_display?: string
  rectification_result: string | null
  verification_status: 0 | 1 | 2 // 0-待验收，1-验收通过，2-验收不通过
  verification_status_display?: string
  verification_time: string | null
  verification_user_id: number | null
  verification_user_name?: string
  verification_opinion: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 隐患整改列表查询参数
 */
export interface RiskRectificationListParams {
  page?: number
  page_size?: number
  danger_id?: number
  responsible_user_id?: number
  responsible_org_id?: number
  rectification_status?: 0 | 1 | 2 | 3
  verification_status?: 0 | 1 | 2
  start_time?: string
  end_time?: string
  search?: string
  ordering?: string
}

/**
 * 隐患整改创建/更新参数
 */
export interface RiskRectificationFormData {
  rectification_code: string
  danger_id: number
  rectification_plan: string
  rectification_measures: string
  responsible_user_id: number
  responsible_org_id: number
  plan_start_time: string
  plan_end_time: string
  actual_start_time?: string | null
  actual_end_time?: string | null
  rectification_status?: 0 | 1 | 2 | 3
  rectification_result?: string | null
  verification_status?: 0 | 1 | 2
  verification_time?: string | null
  verification_user_id?: number | null
  verification_opinion?: string | null
  remark?: string | null
}

/**
 * 报警统计
 */
export interface AlarmStatistics {
  id: number
  stat_date: string
  stat_type: 1 | 2 | 3 | 4 // 1-日报，2-周报，3-月报，4-年报
  stat_type_display?: string
  industry_type: number | null
  industry_type_display?: string
  street: string | null
  alarm_count: number
  unhandled_count: number
  handling_count: number
  handled_count: number
  ignored_count: number
  avg_handle_time: number | null
  stat_data: string | null
  created_at: string
  updated_at: string
}

/**
 * 报警统计分析查询参数
 */
export interface AlarmStatisticsParams {
  stat_type?: 1 | 2 | 3 | 4
  industry_type?: number
  street?: string
  start_date?: string
  end_date?: string
}

/**
 * 预警统计分析查询参数
 */
export interface WarningAnalysisParams {
  analysis_type: 1 | 2 | 3 // 1-突出预警，2-同比预警，3-环比预警
  industry_type?: number
  warning_type?: string
  street?: string
  start_time?: string
  end_time?: string
  compare_time?: string // 对比时间段（同比、环比）
}

