/**
 * 安全态势模块类型定义
 */

/**
 * 资源类型
 */
export type ResourceType = 1 | 2 | 3 // 1-救援队伍，2-应急专家，3-物资装备

/**
 * 防护目标类型
 */
export type TargetType = 1 | 2 | 3 | 4 | 5 // 1-学校，2-居民区，3-医院，4-商场，5-其他人员密集场所

/**
 * 避难场所类型
 */
export type ShelterType = 1 | 2 | 3 | 4 | 5 // 1-公园，2-广场，3-体育场，4-学校，5-其他

/**
 * 危险源类型
 */
export type HazardSourceType = 1 | 2 // 1-重大危险源，2-一般危险源

/**
 * 风险等级
 */
export type RiskLevel = 1 | 2 | 3 // 1-高，2-中，3-低

/**
 * 行业类型
 */
export type IndustryType = 1 | 2 | 3 | 4 // 1-森林火灾，2-防汛，3-交通运输，4-危险化学品

/**
 * 安全资源
 */
export interface SafetyResource {
  id: number
  resource_code: string
  resource_name: string
  resource_type: ResourceType
  resource_type_display: string
  sub_type: string | null
  sub_type_display: string | null
  longitude: number | null
  latitude: number | null
  street: string | null
  address: string | null
  organization_id: number | null
  organization_name: string | null
  contact_person: string | null
  contact_phone: string | null
  capacity: number | null
  equipment_info: string | null
  equipment_info_obj?: any
  expert_field: string | null
  expert_level: string | null
  quantity: number | null
  unit: string | null
  status: 0 | 1
  status_display: string
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 安全资源列表查询参数
 */
export interface SafetyResourceListParams {
  page?: number
  page_size?: number
  resource_type?: ResourceType
  sub_type?: string
  street?: string
  organization_id?: number
  status?: 0 | 1
  search?: string
}

/**
 * 安全资源表单数据
 */
export interface SafetyResourceFormData {
  resource_code?: string
  resource_name: string
  resource_type: ResourceType
  sub_type?: string | null
  longitude?: number | null
  latitude?: number | null
  street?: string | null
  address?: string | null
  organization_id?: number | null
  contact_person?: string | null
  contact_phone?: string | null
  capacity?: number | null
  equipment_info?: string | null
  expert_field?: string | null
  expert_level?: string | null
  quantity?: number | null
  unit?: string | null
  status?: 0 | 1
  description?: string | null
  remark?: string | null
}

/**
 * 防护目标
 */
export interface SafetyTarget {
  id: number
  target_code: string
  target_name: string
  target_type: TargetType
  target_type_display: string
  longitude: number | null
  latitude: number | null
  street: string | null
  address: string | null
  population: number | null
  area: number | null
  risk_level: RiskLevel | null
  risk_level_display: string | null
  contact_person: string | null
  contact_phone: string | null
  description: string | null
  status: 0 | 1
  status_display: string
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 防护目标列表查询参数
 */
export interface SafetyTargetListParams {
  page?: number
  page_size?: number
  target_type?: TargetType
  street?: string
  risk_level?: RiskLevel
  status?: 0 | 1
  search?: string
}

/**
 * 防护目标表单数据
 */
export interface SafetyTargetFormData {
  target_code?: string
  target_name: string
  target_type: TargetType
  longitude?: number | null
  latitude?: number | null
  street?: string | null
  address?: string | null
  population?: number | null
  area?: number | null
  risk_level?: RiskLevel | null
  contact_person?: string | null
  contact_phone?: string | null
  description?: string | null
  status?: 0 | 1
  remark?: string | null
}

/**
 * 避难场所
 */
export interface Shelter {
  id: number
  shelter_code: string
  shelter_name: string
  shelter_type: ShelterType
  shelter_type_display: string
  longitude: number | null
  latitude: number | null
  street: string | null
  address: string | null
  capacity: number
  area: number | null
  facilities: string | null
  facilities_obj?: any
  contact_person: string | null
  contact_phone: string | null
  description: string | null
  status: 0 | 1
  status_display: string
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 避难场所列表查询参数
 */
export interface ShelterListParams {
  page?: number
  page_size?: number
  shelter_type?: ShelterType
  street?: string
  status?: 0 | 1
  search?: string
}

/**
 * 避难场所表单数据
 */
export interface ShelterFormData {
  shelter_code?: string
  shelter_name: string
  shelter_type: ShelterType
  longitude?: number | null
  latitude?: number | null
  street?: string | null
  address?: string | null
  capacity: number
  area?: number | null
  facilities?: string | null
  contact_person?: string | null
  contact_phone?: string | null
  description?: string | null
  status?: 0 | 1
  remark?: string | null
}

/**
 * 危险源
 */
export interface HazardSource {
  id: number
  source_code: string
  source_name: string
  source_type: HazardSourceType
  source_type_display: string
  industry_type: IndustryType
  industry_type_display: string
  organization_id: number
  organization_name: string | null
  longitude: number | null
  latitude: number | null
  street: string | null
  address: string | null
  risk_level: RiskLevel | null
  risk_level_display: string | null
  hazard_category: string | null
  hazard_description: string | null
  control_measures: string | null
  emergency_plan: string | null
  contact_person: string | null
  contact_phone: string | null
  description: string | null
  status: 0 | 1
  status_display: string
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 危险源列表查询参数
 */
export interface HazardSourceListParams {
  page?: number
  page_size?: number
  source_type?: HazardSourceType
  industry_type?: IndustryType
  street?: string
  risk_level?: RiskLevel
  organization_id?: number
  status?: 0 | 1
  search?: string
}

/**
 * 危险源表单数据
 */
export interface HazardSourceFormData {
  source_code?: string
  source_name: string
  source_type: HazardSourceType
  industry_type: IndustryType
  organization_id: number
  longitude?: number | null
  latitude?: number | null
  street?: string | null
  address?: string | null
  risk_level?: RiskLevel | null
  hazard_category?: string | null
  hazard_description?: string | null
  control_measures?: string | null
  emergency_plan?: string | null
  contact_person?: string | null
  contact_phone?: string | null
  description?: string | null
  status?: 0 | 1
  remark?: string | null
}

/**
 * 视频监控设施
 */
export interface VideoMonitor {
  id: number
  monitor_code: string
  monitor_name: string
  longitude: number | null
  latitude: number | null
  street: string | null
  address: string | null
  monitor_type: string | null
  monitor_type_display: string | null
  video_url: string | null
  rtsp_url: string | null
  status: 0 | 1
  status_display: string
  description: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

/**
 * 视频监控列表查询参数
 */
export interface VideoMonitorListParams {
  page?: number
  page_size?: number
  monitor_type?: string
  street?: string
  status?: 0 | 1
  search?: string
}

/**
 * 视频监控表单数据
 */
export interface VideoMonitorFormData {
  monitor_code?: string
  monitor_name: string
  longitude?: number | null
  latitude?: number | null
  street?: string | null
  address?: string | null
  monitor_type?: string | null
  video_url?: string | null
  rtsp_url?: string | null
  status?: 0 | 1
  description?: string | null
  remark?: string | null
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

