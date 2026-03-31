/**
 * 简报模块类型定义
 */

/**
 * 行业类型
 */
export type IndustryType = 1 | 2 | 3 | 4 // 1-森林火灾，2-防汛，3-交通运输，4-危险化学品

/**
 * 简报模板
 */
export interface BriefTemplate {
  id: number
  template_code: string
  template_name: string
  template_type: 1 | 2 // 1-常态化运行报告，2-非常态化突发预警简报
  template_type_display?: string
  industry_type: IndustryType | null
  industry_type_display?: string
  time_dimension: string | null // day, week, month, year
  time_dimension_display?: string
  region_dimension: string | null // JSON格式
  region_dimension_dict?: any
  industry_dimension: string | null // JSON格式
  industry_dimension_dict?: any
  template_content: string
  variables: string | null // JSON格式，变量说明
  variables_dict?: any
  data_config: string | null // JSON格式，数据配置
  data_config_dict?: any
  status: 0 | 1
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 简报模板列表查询参数
 */
export interface BriefTemplateListParams {
  page?: number
  page_size?: number
  template_type?: 1 | 2
  industry_type?: IndustryType
  time_dimension?: string
  status?: 0 | 1
  search?: string
  ordering?: string
}

/**
 * 简报模板创建/更新参数
 */
export interface BriefTemplateFormData {
  template_code: string
  template_name: string
  template_type: 1 | 2
  industry_type?: IndustryType | null
  time_dimension?: string | null
  region_dimension?: string | null
  industry_dimension?: string | null
  template_content: string
  variables?: string | null
  data_config?: string | null
  status?: 0 | 1
  description?: string | null
  remark?: string | null
}

/**
 * 简报策略
 */
export interface BriefStrategy {
  id: number
  strategy_code: string
  strategy_name: string
  template_id: number
  template_detail?: BriefTemplate
  strategy_type: 1 | 2 // 1-常态化策略，2-非常态化策略
  strategy_type_display?: string
  report_type: string | null // daily, weekly, monthly, yearly
  report_type_display?: string
  trigger_type: 1 | 2 // 1-定时触发，2-事件触发
  trigger_type_display?: string
  trigger_config: string | null // JSON格式
  trigger_config_dict?: any
  warning_type_filter: string | null // JSON数组
  warning_type_filter_list?: string[]
  warning_level_filter: string | null // JSON数组
  warning_level_filter_list?: string[]
  industry_filter: string | null // JSON数组
  industry_filter_list?: number[]
  region_filter: string | null // JSON数组
  region_filter_list?: string[]
  push_target_type: 1 | 2 | 3 // 1-指定用户，2-指定角色，3-指定组织
  push_target_type_display?: string
  push_target_ids: string | null // JSON数组
  push_target_ids_list?: number[]
  push_channel: string | null // JSON数组
  push_channel_list?: string[]
  message_template_id: number | null
  status: 0 | 1
  last_execute_at: string | null
  next_execute_at: string | null
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 简报策略列表查询参数
 */
export interface BriefStrategyListParams {
  page?: number
  page_size?: number
  strategy_type?: 1 | 2
  report_type?: string
  trigger_type?: 1 | 2
  status?: 0 | 1
  search?: string
  ordering?: string
}

/**
 * 简报策略创建/更新参数
 */
export interface BriefStrategyFormData {
  strategy_code: string
  strategy_name: string
  template_id: number
  strategy_type: 1 | 2
  report_type?: string | null
  trigger_type?: 1 | 2
  trigger_config?: string | null
  warning_type_filter?: string | null
  warning_level_filter?: string | null
  industry_filter?: string | null
  region_filter?: string | null
  push_target_type: 1 | 2 | 3
  push_target_ids?: string | null
  push_channel?: string | null
  message_template_id?: number | null
  status?: 0 | 1
  description?: string | null
  remark?: string | null
}

/**
 * 简报数据
 */
export interface BriefData {
  id: number
  brief_code: string
  template_id: number
  template_detail?: BriefTemplate
  strategy_id: number | null
  strategy_detail?: BriefStrategy
  brief_type: 1 | 2 // 1-常态化运行报告，2-非常态化突发预警简报
  brief_type_display?: string
  report_type: string | null
  report_type_display?: string
  report_date: string
  report_period_start: string | null
  report_period_end: string | null
  brief_title: string
  brief_content: string
  data_summary: string | null // JSON格式
  data_summary_dict?: any
  alarm_count: number
  warning_count: number
  risk_count: number
  industry_data: string | null // JSON格式
  industry_data_dict?: any
  region_data: string | null // JSON格式
  region_data_dict?: any
  time_data: string | null // JSON格式
  time_data_dict?: any
  attachment_url: string | null
  status: 0 | 1 | 2 // 0-未推送，1-已推送，2-已查看
  status_display?: string
  generate_user_id: number | null
  generate_time: string
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 简报数据列表查询参数
 */
export interface BriefDataListParams {
  page?: number
  page_size?: number
  brief_type?: 1 | 2
  report_type?: string
  status?: 0 | 1 | 2
  template_id?: number
  strategy_id?: number
  start_date?: string
  end_date?: string
  search?: string
  ordering?: string
}

/**
 * 简报数据生成参数
 */
export interface BriefDataGenerateParams {
  template_id: number
  strategy_id?: number | null
  report_date?: string
  report_period_start?: string
  report_period_end?: string
}

/**
 * 简报推送记录
 */
export interface BriefPush {
  id: number
  brief_id: number
  brief_detail?: BriefData
  push_target_type: 1 | 2 | 3 // 1-用户，2-角色，3-组织
  push_target_type_display?: string
  target_id: number
  push_channel: string // system, sms, email
  push_channel_display?: string
  push_status: 0 | 1 | 2 | 3 // 0-待推送，1-推送中，2-推送成功，3-推送失败
  push_status_display?: string
  push_time: string | null
  read_status: 0 | 1 // 0-未读，1-已读
  read_status_display?: string
  read_time: string | null
  error_message: string | null
  message_id: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 简报推送记录列表查询参数
 */
export interface BriefPushListParams {
  page?: number
  page_size?: number
  brief_id?: number
  push_target_type?: 1 | 2 | 3
  push_channel?: string
  push_status?: 0 | 1 | 2 | 3
  read_status?: 0 | 1
  start_time?: string
  end_time?: string
  search?: string
  ordering?: string
}

/**
 * 简报推送创建参数
 */
export interface BriefPushCreateParams {
  brief_id: number
  push_target_type: 1 | 2 | 3
  target_ids: number[]
  push_channel: string[]
}

/**
 * 简报推送标记已读参数
 */
export interface BriefPushReadParams {
  push_id: number
}

