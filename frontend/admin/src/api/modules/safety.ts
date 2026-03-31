/**
 * 安全态势模块API
 */
import { get, post, put, patch, del, getList } from '../request'
import type { PaginatedResponse } from '../types'
import type {
  SafetyResource,
  SafetyResourceListParams,
  SafetyResourceFormData,
  SafetyTarget,
  SafetyTargetListParams,
  SafetyTargetFormData,
  Shelter,
  ShelterListParams,
  ShelterFormData,
  HazardSource,
  HazardSourceListParams,
  HazardSourceFormData,
  VideoMonitor,
  VideoMonitorListParams,
  VideoMonitorFormData,
} from '@/types/modules/safety'

/**
 * 安全资源API
 */
export const safetyResourceApi = {
  // 获取资源列表
  getList: (params?: SafetyResourceListParams) => {
    return getList<SafetyResource>('/safety/resources/', params)
  },

  // 获取资源详情
  getDetail: (id: number) => {
    return get<SafetyResource>(`/safety/resources/${id}/`)
  },

  // 创建资源
  create: (data: SafetyResourceFormData) => {
    return post<SafetyResource>('/safety/resources/', data)
  },

  // 更新资源
  update: (id: number, data: Partial<SafetyResourceFormData>) => {
    return put<SafetyResource>(`/safety/resources/${id}/`, data)
  },

  // 部分更新资源
  partialUpdate: (id: number, data: Partial<SafetyResourceFormData>) => {
    return patch<SafetyResource>(`/safety/resources/${id}/`, data)
  },

  // 删除资源
  delete: (id: number) => {
    return del(`/safety/resources/${id}/`)
  },

  // 获取资源统计
  getStatistics: (params?: { resource_type?: number; street?: string }) => {
    return get('/safety/resources/statistics/', params)
  },
}

/**
 * 防护目标API
 */
export const safetyTargetApi = {
  // 获取目标列表
  getList: (params?: SafetyTargetListParams) => {
    return getList<SafetyTarget>('/safety/targets/', params)
  },

  // 获取目标详情
  getDetail: (id: number) => {
    return get<SafetyTarget>(`/safety/targets/${id}/`)
  },

  // 创建目标
  create: (data: SafetyTargetFormData) => {
    return post<SafetyTarget>('/safety/targets/', data)
  },

  // 更新目标
  update: (id: number, data: Partial<SafetyTargetFormData>) => {
    return put<SafetyTarget>(`/safety/targets/${id}/`, data)
  },

  // 部分更新目标
  partialUpdate: (id: number, data: Partial<SafetyTargetFormData>) => {
    return patch<SafetyTarget>(`/safety/targets/${id}/`, data)
  },

  // 删除目标
  delete: (id: number) => {
    return del(`/safety/targets/${id}/`)
  },

  // 获取目标统计
  getStatistics: (params?: { target_type?: number; street?: string }) => {
    return get('/safety/targets/statistics/', params)
  },
}

/**
 * 避难场所API
 */
export const shelterApi = {
  // 获取场所列表
  getList: (params?: ShelterListParams) => {
    return getList<Shelter>('/safety/shelters/', params)
  },

  // 获取场所详情
  getDetail: (id: number) => {
    return get<Shelter>(`/safety/shelters/${id}/`)
  },

  // 创建场所
  create: (data: ShelterFormData) => {
    return post<Shelter>('/safety/shelters/', data)
  },

  // 更新场所
  update: (id: number, data: Partial<ShelterFormData>) => {
    return put<Shelter>(`/safety/shelters/${id}/`, data)
  },

  // 部分更新场所
  partialUpdate: (id: number, data: Partial<ShelterFormData>) => {
    return patch<Shelter>(`/safety/shelters/${id}/`, data)
  },

  // 删除场所
  delete: (id: number) => {
    return del(`/safety/shelters/${id}/`)
  },

  // 获取场所统计
  getStatistics: (params?: { shelter_type?: number; street?: string }) => {
    return get('/safety/shelters/statistics/', params)
  },
}

/**
 * 危险源API
 */
export const hazardSourceApi = {
  // 获取危险源列表
  getList: (params?: HazardSourceListParams) => {
    return getList<HazardSource>('/safety/hazard-sources/', params)
  },

  // 获取危险源详情
  getDetail: (id: number) => {
    return get<HazardSource>(`/safety/hazard-sources/${id}/`)
  },

  // 创建危险源
  create: (data: HazardSourceFormData) => {
    return post<HazardSource>('/safety/hazard-sources/', data)
  },

  // 更新危险源
  update: (id: number, data: Partial<HazardSourceFormData>) => {
    return put<HazardSource>(`/safety/hazard-sources/${id}/`, data)
  },

  // 部分更新危险源
  partialUpdate: (id: number, data: Partial<HazardSourceFormData>) => {
    return patch<HazardSource>(`/safety/hazard-sources/${id}/`, data)
  },

  // 删除危险源
  delete: (id: number) => {
    return del(`/safety/hazard-sources/${id}/`)
  },

  // 获取危险源统计
  getStatistics: (params?: { source_type?: number; industry_type?: number; street?: string }) => {
    return get('/safety/hazard-sources/statistics/', params)
  },
}

/**
 * 视频监控API
 */
export const videoMonitorApi = {
  // 获取监控列表
  getList: (params?: VideoMonitorListParams) => {
    return getList<VideoMonitor>('/safety/video-monitors/', params)
  },

  // 获取监控详情
  getDetail: (id: number) => {
    return get<VideoMonitor>(`/safety/video-monitors/${id}/`)
  },

  // 创建监控
  create: (data: VideoMonitorFormData) => {
    return post<VideoMonitor>('/safety/video-monitors/', data)
  },

  // 更新监控
  update: (id: number, data: Partial<VideoMonitorFormData>) => {
    return put<VideoMonitor>(`/safety/video-monitors/${id}/`, data)
  },

  // 部分更新监控
  partialUpdate: (id: number, data: Partial<VideoMonitorFormData>) => {
    return patch<VideoMonitor>(`/safety/video-monitors/${id}/`, data)
  },

  // 删除监控
  delete: (id: number) => {
    return del(`/safety/video-monitors/${id}/`)
  },

  // 获取附近监控设施
  getNearbyMonitors: (params: { longitude: number; latitude: number; radius?: number }) => {
    return get<VideoMonitor[]>('/safety/video-monitors/nearby/', params)
  },

  // 获取监控统计
  getStatistics: (params?: { monitor_type?: number; street?: string }) => {
    return get('/safety/video-monitors/statistics/', params)
  },
}

