/**
 * 安全态势API模块
 */
import { get, getList } from '../request'
import type { ListParams, PaginatedResponse } from '../types'

/**
 * 安全资源统计
 */
export interface ResourceStatistics {
  total_count: number
  type_stats: Array<{ resource_type: number; count: number }>
  sub_type_stats: Array<{ sub_type: string; count: number }>
  status_stats: Array<{ status: number; count: number }>
  team_count: number
  team_capacity: number
  expert_count: number
  equipment_count: number
  equipment_quantity: number
}

/**
 * 防护目标统计
 */
export interface TargetStatistics {
  total_count: number
  type_stats: Array<{ target_type: number; count: number }>
  risk_stats: Array<{ risk_level: number; count: number }>
  total_population: number
}

/**
 * 避难场所统计
 */
export interface ShelterStatistics {
  total_count: number
  type_stats: Array<{ shelter_type: number; count: number }>
  total_capacity: number
}

/**
 * 安全资源
 */
export interface SafetyResource {
  id: number
  resource_code: string
  resource_name: string
  resource_type: number
  resource_type_display: string
  sub_type?: string
  longitude?: number
  latitude?: number
  street?: string
  address?: string
  organization_id?: number
  organization_name?: string
  contact_person?: string
  contact_phone?: string
  capacity?: number
  equipment_info?: string
  equipment_info_dict?: any
  expert_field?: string
  expert_level?: string
  quantity?: number
  unit?: string
  status: number
  description?: string
  remark?: string
  created_at: string
  updated_at: string
}

/**
 * 防护目标
 */
export interface SafetyTarget {
  id: number
  target_code: string
  target_name: string
  target_type: number
  target_type_display: string
  longitude?: number
  latitude?: number
  street?: string
  address?: string
  population?: number
  area?: number
  risk_level?: number
  risk_level_display?: string
  contact_person?: string
  contact_phone?: string
  description?: string
  status: number
  remark?: string
  created_at: string
  updated_at: string
}

/**
 * 避难场所
 */
export interface Shelter {
  id: number
  shelter_code: string
  shelter_name: string
  shelter_type: number
  shelter_type_display: string
  longitude?: number
  latitude?: number
  street?: string
  address?: string
  capacity?: number
  area?: number
  facilities?: string
  facilities_dict?: any
  contact_person?: string
  contact_phone?: string
  description?: string
  status: number
  remark?: string
  created_at: string
  updated_at: string
}

/**
 * 获取安全资源统计
 */
export function getResourceStatistics(): Promise<ResourceStatistics> {
  return get<ResourceStatistics>('/safety/resources/statistics/')
}

/**
 * 获取防护目标统计
 */
export function getTargetStatistics(): Promise<TargetStatistics> {
  return get<TargetStatistics>('/safety/targets/statistics/')
}

/**
 * 获取避难场所统计
 */
export function getShelterStatistics(): Promise<ShelterStatistics> {
  return get<ShelterStatistics>('/safety/shelters/statistics/')
}

/**
 * 获取安全资源列表
 */
export function getResourceList(params?: ListParams): Promise<PaginatedResponse<SafetyResource>> {
  return getList<SafetyResource>('/safety/resources/', params)
}

/**
 * 获取防护目标列表
 */
export function getTargetList(params?: ListParams): Promise<PaginatedResponse<SafetyTarget>> {
  return getList<SafetyTarget>('/safety/targets/', params)
}

/**
 * 获取避难场所列表
 */
export function getShelterList(params?: ListParams): Promise<PaginatedResponse<Shelter>> {
  return getList<Shelter>('/safety/shelters/', params)
}

/**
 * 区域态势
 */
export interface RegionStatus {
  id: number
  stat_date: string
  street: string
  alarm_count: number
  warning_count: number
  risk_count: number
  risk_level_1_count: number // 红色I级风险数量
  risk_level_2_count: number // 橙色Ⅱ级风险数量
  risk_level_3_count: number // 黄色Ⅲ级风险数量
  risk_level_4_count: number // 蓝色Ⅳ级风险数量
  risk_color: 'red' | 'orange' | 'yellow' | 'blue' | null // 风险颜色
  status_data?: string
  status_data_dict?: any
  created_at: string
  updated_at: string
}

/**
 * 获取四色图数据
 */
export function getColorMapData(): Promise<RegionStatus[]> {
  return get<RegionStatus[]>('/safety/region-status/color_map/')
}

/**
 * 行业态势
 */
export interface IndustryStatus {
  id: number
  stat_date: string
  industry_type: number // 1-森林火灾，2-防汛，3-交通运输，4-危险化学品
  industry_type_display: string
  alarm_count: number
  warning_count: number
  risk_count: number
  risk_level_1_count: number // 红色I级风险数量
  risk_level_2_count: number // 橙色Ⅱ级风险数量
  risk_level_3_count: number // 黄色Ⅲ级风险数量
  risk_level_4_count: number // 蓝色Ⅳ级风险数量
  status_data?: string
  status_data_dict?: any
  created_at: string
  updated_at: string
}

/**
 * 获取行业态势列表
 */
export function getIndustryStatusList(params?: ListParams): Promise<PaginatedResponse<IndustryStatus>> {
  return getList<IndustryStatus>('/safety/industry-status/', params)
}

/**
 * 获取最新行业态势数据（用于大屏展示）
 */
export function getLatestIndustryStatus(): Promise<IndustryStatus[]> {
  return getList<IndustryStatus>('/safety/industry-status/', {
    ordering: '-stat_date',
    page_size: 100, // 获取足够多的数据
  }).then((response) => {
    // 提取结果数组
    return response.results || []
  })
}

/**
 * 监测数据
 */
export interface MonitorData {
  id: number
  monitor_id: number
  monitor_name?: string
  industry_type: number
  industry_type_display: string
  data_time: string
  monitor_value?: number
  monitor_unit?: string
  online_status: number // 0-离线，1-在线
  online_status_display?: string
  data_source?: string
  created_at: string
}

/**
 * 监测数据统计（后端返回）
 */
export interface MonitorDataStatisticsResponse {
  total_count: number
  online_count: number
  offline_count: number
  industry_stats: Array<{ industry_type: number; count: number }>
  online_stats?: Array<{ online_status: number; count: number }>
}

/**
 * 监测数据统计（前端使用）
 */
export interface MonitorDataStatistics {
  total_count: number
  online_count: number
  offline_count: number
  industry_stats: Array<{ industry_type: number; count: number }>
  online_rate: number // 在线率（百分比）
}

/**
 * 获取监测数据统计
 */
export function getMonitorDataStatistics(params?: { start_time?: string; end_time?: string }): Promise<MonitorDataStatistics> {
  return get<MonitorDataStatisticsResponse>('/safety/monitor-data/statistics/', params).then((data) => {
    // 计算在线率
    const onlineRate = data.total_count > 0 
      ? Math.round((data.online_count / data.total_count) * 100 * 100) / 100 
      : 0
    
    return {
      ...data,
      online_rate: onlineRate,
    }
  })
}

/**
 * 获取监测数据列表
 */
export function getMonitorDataList(params?: ListParams): Promise<PaginatedResponse<MonitorData>> {
  return getList<MonitorData>('/safety/monitor-data/', params)
}

/**
 * 预警事件
 */
export interface WarningEvent {
  id: number
  warning_id: number
  warning_code: string
  warning_level_id: number
  industry_type: number
  industry_type_display: string
  warning_type: string
  warning_title: string
  longitude?: number
  latitude?: number
  street?: string
  address?: string
  warning_time: string
  warning_status: number // 0-未发布，1-已发布，2-处理中，3-已处置，4-已关闭
  warning_status_display: string
  nearby_monitor_count: number
  nearby_risk_count: number
  nearby_resource_count: number
  description?: string
  warning_detail?: any
  warning_level_detail?: any
  created_at: string
  updated_at: string
}

/**
 * 获取预警事件列表
 */
export function getWarningEventList(params?: ListParams): Promise<PaginatedResponse<WarningEvent>> {
  return getList<WarningEvent>('/safety/warning-events/', params)
}

/**
 * 获取最新预警事件（用于大屏展示）
 */
export function getLatestWarningEvents(params?: { limit?: number }): Promise<WarningEvent[]> {
  return getList<WarningEvent>('/safety/warning-events/', {
    ordering: '-warning_time',
    page_size: params?.limit || 100,
  }).then((response) => {
    return response.results || []
  })
}

/**
 * 视频监控设施
 */
export interface VideoMonitor {
  id: number
  monitor_code: string
  monitor_name: string
  monitor_type: number // 1-固定监控，2-移动监控，3-无人机监控
  monitor_type_display: string
  industry_type: number
  industry_type_display: string
  longitude?: number
  latitude?: number
  street?: string
  address?: string
  video_url?: string
  rtsp_url?: string
  coverage_radius?: number
  camera_angle?: number
  online_status: number // 0-离线，1-在线
  online_status_display: string
  organization_id?: number
  organization_name?: string
  description?: string
  status: number // 0-禁用，1-启用
  remark?: string
  created_at: string
  updated_at: string
}

/**
 * 获取视频监控设施列表
 */
export function getVideoMonitorList(params?: ListParams): Promise<PaginatedResponse<VideoMonitor>> {
  return getList<VideoMonitor>('/safety/video-monitors/', params)
}

/**
 * 获取附近的视频监控设施
 */
export function getNearbyVideoMonitors(params: {
  longitude: number
  latitude: number
  radius?: number // 半径（米），默认5000米
}): Promise<VideoMonitor[]> {
  return get<VideoMonitor[]>('/safety/video-monitors/nearby/', {
    longitude: params.longitude,
    latitude: params.latitude,
    radius: params.radius || 5000,
  })
}

/**
 * 视频监控设施统计（后端返回）
 */
export interface VideoMonitorStatisticsResponse {
  total_count: number
  online_count: number
  offline_count: number
  type_stats: Array<{ monitor_type: number; count: number }>
  industry_stats: Array<{ industry_type: number; count: number }>
  online_stats?: Array<{ online_status: number; count: number }>
}

/**
 * 视频监控设施统计（前端使用）
 */
export interface VideoMonitorStatistics {
  total_count: number
  online_count: number
  offline_count: number
  online_rate: number // 在线率（百分比）
  type_stats: Array<{ monitor_type: number; count: number }>
  industry_stats: Array<{ industry_type: number; count: number }>
}

/**
 * 获取视频监控设施统计
 */
export function getVideoMonitorStatistics(): Promise<VideoMonitorStatistics> {
  return get<VideoMonitorStatisticsResponse>('/safety/video-monitors/statistics/').then((data) => {
    // 计算在线率
    const onlineRate = data.total_count > 0 
      ? Math.round((data.online_count / data.total_count) * 100 * 100) / 100 
      : 0
    
    return {
      total_count: data.total_count,
      online_count: data.online_count,
      offline_count: data.offline_count,
      online_rate: onlineRate,
      type_stats: data.type_stats || [],
      industry_stats: data.industry_stats || [],
    }
  })
}

