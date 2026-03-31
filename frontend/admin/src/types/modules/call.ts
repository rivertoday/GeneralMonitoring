/**
 * 叫应模块类型定义
 */

/**
 * 叫应对象类型
 */
export type CallTargetType = 1 | 2 | 3 // 1-政府部门，2-企业单位，3-事业单位

/**
 * 叫应对象
 */
export interface CallTarget {
  id: number
  target_code: string
  target_name: string
  target_type: CallTargetType
  target_type_display: string
  organization_id: number | null
  enterprise_name: string | null
  enterprise_info: string | null
  safety_person: string
  contact_phone: string
  contact_address: string | null
  description: string | null
  status: 0 | 1
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 叫应对象列表查询参数
 */
export interface CallTargetListParams {
  page?: number
  page_size?: number
  target_type?: CallTargetType
  organization_id?: number
  status?: 0 | 1
  search?: string
  ordering?: string
}

/**
 * 叫应对象创建/更新参数
 */
export interface CallTargetFormData {
  target_code: string
  target_name: string
  target_type: CallTargetType
  organization_id?: number | null
  enterprise_name?: string | null
  enterprise_info?: string | null
  safety_person: string
  contact_phone: string
  contact_address?: string | null
  description?: string | null
  status?: 0 | 1
  remark?: string | null
}

/**
 * 应急事件级别
 */
export type EventLevel = 1 | 2 | 3 | 4 // 1-红色I级，2-橙色Ⅱ级，3-黄色Ⅲ级，4-蓝色Ⅳ级

/**
 * 叫应人员
 */
export interface CallPerson {
  id: number
  person_code: string
  person_name: string
  group_id: number | null
  group_name: string | null
  rank: string | null
  mobile_phone: string
  office_phone: string | null
  contact_address: string | null
  event_level: EventLevel | null
  event_level_display: string | null
  organization_id: number | null
  description: string | null
  status: 0 | 1
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 叫应人员列表查询参数
 */
export interface CallPersonListParams {
  page?: number
  page_size?: number
  group_id?: number
  event_level?: EventLevel
  organization_id?: number
  status?: 0 | 1
  search?: string
  ordering?: string
}

/**
 * 叫应人员创建/更新参数
 */
export interface CallPersonFormData {
  person_code: string
  person_name: string
  group_id?: number | null
  rank?: string | null
  mobile_phone: string
  office_phone?: string | null
  contact_address?: string | null
  event_level?: EventLevel | null
  organization_id?: number | null
  description?: string | null
  status?: 0 | 1
  remark?: string | null
}

/**
 * 分组类型
 */
export type GroupType = 1 | 2 // 1-常态化分组，2-非常态化分组

/**
 * 叫应分组
 */
export interface CallGroup {
  id: number
  group_code: string
  group_name: string
  group_type: GroupType
  group_type_display: string
  event_level: EventLevel | null
  event_level_display: string | null
  description: string | null
  status: 0 | 1
  sort_order: number
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 叫应分组列表查询参数
 */
export interface CallGroupListParams {
  page?: number
  page_size?: number
  group_type?: GroupType
  event_level?: EventLevel
  status?: 0 | 1
  search?: string
  ordering?: string
}

/**
 * 叫应分组创建/更新参数
 */
export interface CallGroupFormData {
  group_code: string
  group_name: string
  group_type: GroupType
  event_level?: EventLevel | null
  description?: string | null
  status?: 0 | 1
  sort_order?: number
  remark?: string | null
}

/**
 * 发布状态
 */
export type PublishStatus = 0 | 1 // 0-未发布，1-已发布

/**
 * 政策文件
 */
export interface PolicyFile {
  id: number
  file_code: string
  file_name: string
  file_path: string
  file_size: number | null
  file_type: string | null
  file_ext: string | null
  policy_title: string
  policy_content: string | null
  policy_requirement: string | null
  upload_user_id: number
  upload_user_name: string | null
  upload_time: string
  publish_status: PublishStatus
  publish_status_display: string
  publish_time: string | null
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 政策文件列表查询参数
 */
export interface PolicyFileListParams {
  page?: number
  page_size?: number
  file_type?: string
  upload_user_id?: number
  publish_status?: PublishStatus
  start_time?: string
  end_time?: string
  search?: string
  ordering?: string
}

/**
 * 政策文件创建/更新参数
 */
export interface PolicyFileFormData {
  file_code: string
  file_name: string
  file_path: string
  file_size?: number | null
  file_type?: string | null
  file_ext?: string | null
  policy_title: string
  policy_content?: string | null
  policy_requirement?: string | null
  description?: string | null
  remark?: string | null
}

/**
 * 政策文件发布参数
 */
export interface PolicyFilePublishData {
  publish_time?: string | null
}

/**
 * 反馈状态
 */
export type FeedbackStatus = 0 | 1 | 2 // 0-未反馈，1-已反馈，2-超时未反馈

/**
 * 督办状态
 */
export type SuperviseStatus = 0 | 1 | 2 // 0-无需督办，1-待督办，2-已督办

/**
 * 政策文件下发
 */
export interface PolicyDistribution {
  id: number
  distribution_code: string
  policy_file_id: number
  policy_file_detail: PolicyFile | null
  target_id: number
  target_detail: CallTarget | null
  feedback_content: string | null
  feedback_deadline: string
  distribution_time: string
  distribution_user_id: number
  distribution_user_name: string | null
  feedback_status: FeedbackStatus
  feedback_status_display: string
  feedback_time: string | null
  feedback_content_actual: string | null
  supervise_status: SuperviseStatus
  supervise_status_display: string
  supervise_time: string | null
  supervise_user_id: number | null
  supervise_user_name: string | null
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 政策文件下发列表查询参数
 */
export interface PolicyDistributionListParams {
  page?: number
  page_size?: number
  policy_file_id?: number
  target_id?: number
  feedback_status?: FeedbackStatus
  supervise_status?: SuperviseStatus
  start_time?: string
  end_time?: string
  search?: string
  ordering?: string
}

/**
 * 政策文件下发创建/更新参数
 */
export interface PolicyDistributionFormData {
  distribution_code: string
  policy_file_id: number
  target_id: number
  feedback_content?: string | null
  feedback_deadline: string
  description?: string | null
  remark?: string | null
}

/**
 * 政策文件下发反馈参数
 */
export interface PolicyDistributionFeedbackData {
  feedback_content_actual: string
}

/**
 * 政策文件下发督办参数
 */
export interface PolicyDistributionSuperviseData {
  supervise_user_id: number
}

/**
 * 叫应类型
 */
export type CallType = 1 | 2 // 1-常态化叫应，2-非常态化叫应

/**
 * 叫应来源
 */
export type CallSource = 1 | 2 | 3 // 1-政策文件下发，2-一键叫应，3-预警触发

/**
 * 叫应状态
 */
export type CallStatus = 0 | 1 | 2 | 3 // 0-待发送，1-发送中，2-发送成功，3-发送失败

/**
 * 接收状态
 */
export type ReceiveStatus = 0 | 1 | 2 // 0-未接收，1-已接收，2-未响应

/**
 * 响应状态
 */
export type ResponseStatus = 0 | 1 // 0-未响应，1-已响应

/**
 * 叫应渠道
 */
export type CallChannel = 'system' | 'sms' | 'phone' // system-系统消息，sms-短信，phone-电话

/**
 * 叫应记录
 */
export interface CallRecord {
  id: number
  call_code: string
  call_type: CallType
  call_type_display: string
  call_source: CallSource
  call_source_display: string
  policy_distribution_id: number | null
  policy_distribution_detail: PolicyDistribution | null
  warning_id: number | null
  target_id: number | null
  target_detail: CallTarget | null
  person_id: number | null
  person_detail: CallPerson | null
  group_id: number | null
  group_detail: CallGroup | null
  call_channel: CallChannel
  call_content: string
  call_time: string
  call_status: CallStatus
  call_status_display: string
  receive_status: ReceiveStatus
  receive_status_display: string
  receive_time: string | null
  response_status: ResponseStatus
  response_status_display: string
  response_time: string | null
  response_content: string | null
  retry_count: number
  last_retry_time: string | null
  error_message: string | null
  external_call_id: string | null
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 叫应记录列表查询参数
 */
export interface CallRecordListParams {
  page?: number
  page_size?: number
  call_type?: CallType
  call_source?: CallSource
  call_channel?: CallChannel
  call_status?: CallStatus
  receive_status?: ReceiveStatus
  response_status?: ResponseStatus
  start_time?: string
  end_time?: string
  search?: string
  ordering?: string
}

/**
 * 叫应记录创建/更新参数
 */
export interface CallRecordFormData {
  call_code: string
  call_type: CallType
  call_source: CallSource
  policy_distribution_id?: number | null
  warning_id?: number | null
  target_id?: number | null
  person_id?: number | null
  group_id?: number | null
  call_channel: CallChannel
  call_content: string
  description?: string | null
  remark?: string | null
}

/**
 * 叫应记录响应参数
 */
export interface CallRecordResponseData {
  response_content: string
}

/**
 * 一键叫应参数
 */
export interface EmergencyCallData {
  call_type: CallType
  call_source?: CallSource
  target_ids?: number[] // 常态化叫应：叫应对象ID列表
  person_ids?: number[] // 非常态化叫应：叫应人员ID列表
  group_ids?: number[] // 非常态化叫应：叫应分组ID列表
  call_channel: CallChannel
  call_content: string
  warning_id?: number | null // 预警ID（预警触发时）
}

/**
 * 一键叫应响应
 */
export interface EmergencyCallResponse {
  created_count: number
  record_ids: number[]
}

