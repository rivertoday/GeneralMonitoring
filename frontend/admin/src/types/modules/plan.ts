/**
 * 预案模块类型定义
 */

/**
 * 预案类型
 */
export type PlanType = 1 | 2 | 3 // 1-综合应急预案，2-专项应急预案，3-现场处置方案

/**
 * 行业类型
 */
export type IndustryType = 1 | 2 | 3 | 4 // 1-森林火灾，2-防汛，3-交通运输，4-危险化学品

/**
 * 预案状态
 */
export type PlanStatus = 0 | 1 | 2 | 3 // 0-草稿，1-已发布，2-已修订，3-已废止

/**
 * 节点类型
 */
export type NodeType = 1 | 2 | 3 // 1-章节，2-条款，3-子条款

/**
 * 流程类型
 */
export type FlowType = 1 | 2 | 3 // 1-主流程，2-子流程，3-任务节点

/**
 * 任务类型
 */
export type TaskType = 1 | 2 | 3 | 4 | 5 // 1-信息收集，2-决策指挥，3-资源调配，4-现场处置，5-其他

/**
 * 优先级
 */
export type Priority = 1 | 2 | 3 // 1-高，2-中，3-低

/**
 * 执行类型
 */
export type ExecutionType = 1 | 2 // 1-演练执行，2-实战执行

/**
 * 执行状态
 */
export type ExecutionStatus = 0 | 1 | 2 | 3 // 0-未开始，1-执行中，2-已完成，3-已终止

/**
 * 应急预案
 */
export interface EmergencyPlan {
  id: number
  plan_code: string
  plan_name: string
  plan_type: PlanType
  plan_type_display: string
  industry_type: IndustryType | null
  industry_type_display: string | null
  organization_id: number | null
  organization_name: string | null
  version: string
  plan_file_path: string | null
  plan_file_name: string | null
  plan_summary: string | null
  plan_status: PlanStatus
  plan_status_display: string
  publish_time: string | null
  effective_time: string | null
  expire_time: string | null
  revision_reason: string | null
  create_user_id: number
  create_user_name: string | null
  approve_user_id: number | null
  approve_user_name: string | null
  approve_time: string | null
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 应急预案列表查询参数
 */
export interface EmergencyPlanListParams {
  page?: number
  page_size?: number
  plan_type?: PlanType
  industry_type?: IndustryType
  organization_id?: number
  plan_status?: PlanStatus
  search?: string
  start_time?: string
  end_time?: string
}

/**
 * 应急预案表单数据
 */
export interface EmergencyPlanFormData {
  plan_code?: string
  plan_name: string
  plan_type: PlanType
  industry_type?: IndustryType | null
  organization_id?: number | null
  version?: string
  plan_file_path?: string | null
  plan_file_name?: string | null
  plan_summary?: string | null
  effective_time?: string | null
  expire_time?: string | null
  description?: string | null
  remark?: string | null
}

/**
 * 预案结构
 */
export interface PlanStructure {
  id: number
  plan_id: number
  plan_name: string | null
  node_code: string
  node_name: string
  parent_id: number
  parent_name: string | null
  node_type: NodeType
  node_type_display: string
  node_level: number
  node_content: string | null
  node_index: number
  is_key_info: 0 | 1
  is_key_info_display: string
  description: string | null
  remark: string | null
  children?: PlanStructure[]
  created_at: string
  updated_at: string
}

/**
 * 预案结构列表查询参数
 */
export interface PlanStructureListParams {
  plan_id: number
  parent_id?: number
  node_type?: NodeType
  is_key_info?: 0 | 1
  search?: string
}

/**
 * 预案结构表单数据
 */
export interface PlanStructureFormData {
  plan_id: number
  node_code?: string
  node_name: string
  parent_id?: number
  node_type: NodeType
  node_content?: string | null
  node_index?: number
  is_key_info?: 0 | 1
  description?: string | null
  remark?: string | null
}

/**
 * 预案流程
 */
export interface PlanFlow {
  id: number
  plan_id: number
  plan_name: string | null
  flow_code: string
  flow_name: string
  parent_id: number
  parent_name: string | null
  flow_type: FlowType
  flow_type_display: string
  flow_level: number
  flow_config: string | null // JSON格式
  flow_config_obj?: any // 解析后的对象
  next_flow_ids: string | null // JSON数组
  next_flow_ids_arr?: number[] // 解析后的数组
  condition_config: string | null // JSON格式
  condition_config_obj?: any // 解析后的对象
  sort_order: number
  description: string | null
  remark: string | null
  children?: PlanFlow[]
  created_at: string
  updated_at: string
}

/**
 * 预案流程列表查询参数
 */
export interface PlanFlowListParams {
  plan_id: number
  parent_id?: number
  flow_type?: FlowType
  search?: string
}

/**
 * 预案流程表单数据
 */
export interface PlanFlowFormData {
  plan_id: number
  flow_code?: string
  flow_name: string
  parent_id?: number
  flow_type: FlowType
  flow_config?: string | null
  next_flow_ids?: string | null
  condition_config?: string | null
  sort_order?: number
  description?: string | null
  remark?: string | null
}

/**
 * 预案任务
 */
export interface PlanTask {
  id: number
  plan_id: number
  plan_name: string | null
  flow_id: number | null
  flow_name: string | null
  task_code: string
  task_name: string
  task_type: TaskType
  task_type_display: string
  organization_id: number | null
  organization_name: string | null
  assign_user_id: number | null
  assign_user_name: string | null
  assign_role_id: number | null
  assign_role_name: string | null
  task_description: string | null
  task_requirement: string | null
  estimated_time: number | null
  priority: Priority
  priority_display: string
  sort_order: number
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 预案任务列表查询参数
 */
export interface PlanTaskListParams {
  page?: number
  page_size?: number
  plan_id?: number
  flow_id?: number
  task_type?: TaskType
  organization_id?: number
  assign_user_id?: number
  assign_role_id?: number
  priority?: Priority
  search?: string
}

/**
 * 预案任务表单数据
 */
export interface PlanTaskFormData {
  plan_id: number
  flow_id?: number | null
  task_code?: string
  task_name: string
  task_type: TaskType
  organization_id?: number | null
  assign_user_id?: number | null
  assign_role_id?: number | null
  task_description?: string | null
  task_requirement?: string | null
  estimated_time?: number | null
  priority?: Priority
  sort_order?: number
  description?: string | null
  remark?: string | null
}

/**
 * 预案执行记录
 */
export interface PlanExecution {
  id: number
  execution_code: string
  plan_id: number
  plan_name: string | null
  warning_id: number | null
  warning_title: string | null
  execution_type: ExecutionType
  execution_type_display: string
  execution_status: ExecutionStatus
  execution_status_display: string
  start_time: string | null
  end_time: string | null
  duration: number | null
  command_user_id: number
  command_user_name: string | null
  current_flow_id: number | null
  current_flow_name: string | null
  execution_result: string | null
  execution_summary: string | null
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 预案执行记录列表查询参数
 */
export interface PlanExecutionListParams {
  page?: number
  page_size?: number
  plan_id?: number
  warning_id?: number
  execution_type?: ExecutionType
  execution_status?: ExecutionStatus
  command_user_id?: number
  start_time?: string
  end_time?: string
  ordering?: string
  search?: string
}

/**
 * 预案执行记录表单数据
 */
export interface PlanExecutionFormData {
  plan_id: number
  warning_id?: number | null
  execution_type: ExecutionType
  command_user_id: number
  description?: string | null
  remark?: string | null
}

/**
 * 预案统计
 */
export interface PlanStatistics {
  total_count: number
  by_type: {
    plan_type: PlanType
    plan_type_display: string
    count: number
  }[]
  by_industry: {
    industry_type: IndustryType
    industry_type_display: string
    count: number
  }[]
  by_status: {
    plan_status: PlanStatus
    plan_status_display: string
    count: number
  }[]
  by_month: {
    month: string
    count: number
  }[]
}

/**
 * 预案统计查询参数
 */
export interface PlanStatisticsParams {
  organization_id?: number
  start_time?: string
  end_time?: string
}

/**
 * 分页响应
 */
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

