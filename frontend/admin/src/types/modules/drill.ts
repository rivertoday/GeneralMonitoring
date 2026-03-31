/**
 * 演练模块类型定义
 */

/**
 * 事件类型
 */
export type EventType = 1 | 2 | 3 | 4 | 5 // 1-火灾，2-爆炸，3-泄漏，4-坍塌，5-其他

/**
 * 演练状态
 */
export type DrillStatus = 0 | 1 | 2 | 3 // 0-未开始，1-进行中，2-已完成，3-已取消

/**
 * 数据来源
 */
export type DataSource = 1 | 2 | 3 // 1-企业安全在线服务，2-化工园区安全智能化管控平台，3-手动录入

/**
 * 节点类型
 */
export type NodeType = 1 | 2 | 3 | 4 | 5 // 1-信息收集，2-决策指挥，3-资源调配，4-现场处置，5-其他

/**
 * 评价等级
 */
export type EvaluationLevel = 1 | 2 | 3 | 4 // 1-优秀，2-良好，3-合格，4-不合格

/**
 * 状态选项
 */
export type StatusChoice = 1 | 2 | 3 // 1-顺畅/熟悉/可操作/明确/科学/得当，2-一般，3-不顺畅/不熟悉/不可操作/不明确/不科学/不得当

/**
 * 演练事件
 */
export interface DrillEvent {
  id: number
  event_code: string
  event_name: string
  organization_id: number
  organization_name?: string | null
  drill_plan_name?: string | null
  drill_plan_id?: number | null
  event_type: EventType
  event_type_display?: string
  accident_type?: string | null
  location?: string | null
  longitude?: string | null
  latitude?: string | null
  street?: string | null
  address?: string | null
  event_time: string
  injured_count: number
  death_count: number
  accident_summary?: string | null
  related_plan_id?: number | null
  related_plan_name?: string | null
  drill_status: DrillStatus
  drill_status_display?: string
  data_source?: DataSource | null
  data_source_display?: string | null
  external_id?: string | null
  description?: string | null
  remark?: string | null
  created_at: string
  updated_at: string
}

/**
 * 演练事件列表查询参数
 */
export interface DrillEventListParams {
  page?: number
  page_size?: number
  organization_id?: number
  event_type?: EventType
  drill_status?: DrillStatus
  data_source?: DataSource
  search?: string
  start_time?: string
  end_time?: string
  ordering?: string
}

/**
 * 演练事件表单数据
 */
export interface DrillEventFormData {
  event_code?: string
  event_name: string
  organization_id: number
  drill_plan_name?: string | null
  drill_plan_id?: number | null
  event_type: EventType
  accident_type?: string | null
  longitude?: string | null
  latitude?: string | null
  street?: string | null
  address?: string | null
  event_time: string
  injured_count?: number
  death_count?: number
  accident_summary?: string | null
  related_plan_id?: number | null
  drill_status?: DrillStatus
  data_source?: DataSource | null
  external_id?: string | null
  description?: string | null
  remark?: string | null
}

/**
 * 演练评价
 */
export interface DrillEvaluation {
  id: number
  event_id: number
  event_name?: string
  node_name: string
  node_type: NodeType
  node_type_display?: string
  evaluation_item: string
  evaluation_content: string
  evaluation_score?: string | null
  evaluation_level?: EvaluationLevel | null
  evaluation_level_display?: string | null
  evaluator_id: number
  evaluator_name?: string | null
  evaluation_time: string
  description?: string | null
  remark?: string | null
  created_at: string
  updated_at: string
}

/**
 * 演练评价列表查询参数
 */
export interface DrillEvaluationListParams {
  page?: number
  page_size?: number
  event_id?: number
  node_type?: NodeType
  evaluation_level?: EvaluationLevel
  search?: string
  start_time?: string
  end_time?: string
}

/**
 * 演练评价表单数据
 */
export interface DrillEvaluationFormData {
  event_id: number
  node_name: string
  node_type: NodeType
  evaluation_item: string
  evaluation_content: string
  evaluation_score?: string | null
  evaluation_level?: EvaluationLevel | null
  description?: string | null
  remark?: string | null
}

/**
 * 演练总结
 */
export interface DrillSummary {
  id: number
  event_id: number
  event_name?: string
  summary_title: string
  communication_status?: StatusChoice | null
  communication_comment?: string | null
  plan_familiarity?: StatusChoice | null
  plan_familiarity_comment?: string | null
  plan_operability?: StatusChoice | null
  plan_operability_comment?: string | null
  duty_clarity?: StatusChoice | null
  duty_clarity_comment?: string | null
  command_science?: StatusChoice | null
  command_science_comment?: string | null
  disposal_appropriateness?: StatusChoice | null
  disposal_appropriateness_comment?: string | null
  problems_analysis?: string | null
  improvement_suggestions?: string | null
  overall_score?: string | null
  overall_level?: EvaluationLevel | null
  overall_level_display?: string | null
  enterprise_summary?: string | null
  supervisor_opinion?: string | null
  summary_user_id: number
  summary_user_name?: string | null
  summary_time: string
  description?: string | null
  remark?: string | null
  created_at: string
  updated_at: string
}

/**
 * 演练总结列表查询参数
 */
export interface DrillSummaryListParams {
  page?: number
  page_size?: number
  event_id?: number
  overall_level?: EvaluationLevel
  search?: string
  start_time?: string
  end_time?: string
}

/**
 * 演练总结表单数据
 */
export interface DrillSummaryFormData {
  event_id: number
  summary_title: string
  communication_status?: StatusChoice | null
  communication_comment?: string | null
  plan_familiarity?: StatusChoice | null
  plan_familiarity_comment?: string | null
  plan_operability?: StatusChoice | null
  plan_operability_comment?: string | null
  duty_clarity?: StatusChoice | null
  duty_clarity_comment?: string | null
  command_science?: StatusChoice | null
  command_science_comment?: string | null
  disposal_appropriateness?: StatusChoice | null
  disposal_appropriateness_comment?: string | null
  problems_analysis?: string | null
  improvement_suggestions?: string | null
  overall_score?: string | null
  overall_level?: EvaluationLevel | null
  enterprise_summary?: string | null
  supervisor_opinion?: string | null
  description?: string | null
  remark?: string | null
}

/**
 * 演练分析统计类型
 */
export type StatType = 1 | 2 | 3 | 4 // 1-日报，2-周报，3-月报，4-年报

/**
 * 演练类型
 */
export type DrillType = 1 | 2 | 3 // 1-桌面演练，2-功能演练，3-全面演练

/**
 * 演练分析
 */
export interface DrillAnalysis {
  id: number
  stat_date: string
  stat_type: StatType
  stat_type_display?: string
  organization_id?: number | null
  organization_name?: string | null
  drill_type?: DrillType | null
  drill_type_display?: string | null
  accident_type?: string | null
  drill_count: number
  completed_count: number
  excellent_count: number
  good_count: number
  qualified_count: number
  unqualified_count: number
  avg_score?: string | null
  analysis_data?: string | null
  created_at: string
  updated_at: string
}

/**
 * 演练分析查询参数
 */
export interface DrillAnalysisParams {
  stat_type?: StatType
  organization_id?: number
  drill_type?: DrillType
  accident_type?: string
  start_date?: string
  end_date?: string
}

