/**
 * 简报模块API
 */
import { get, post, put, del, getList } from '../request'
import type { PaginatedResponse } from '../types'
import type {
  BriefTemplate,
  BriefTemplateListParams,
  BriefTemplateFormData,
  BriefStrategy,
  BriefStrategyListParams,
  BriefStrategyFormData,
  BriefData,
  BriefDataListParams,
  BriefDataGenerateParams,
  BriefPush,
  BriefPushListParams,
  BriefPushCreateParams,
  BriefPushReadParams,
} from '@/types/modules/brief'

/**
 * 简报模板API
 */
export const briefTemplateApi = {
  // 获取简报模板列表
  getList: (params?: BriefTemplateListParams) => {
    return getList<BriefTemplate>('/brief/templates/', params)
  },

  // 获取简报模板详情
  getDetail: (id: number) => {
    return get<BriefTemplate>(`/brief/templates/${id}/`)
  },

  // 创建简报模板
  create: (data: BriefTemplateFormData) => {
    return post<BriefTemplate>('/brief/templates/', data)
  },

  // 更新简报模板
  update: (id: number, data: Partial<BriefTemplateFormData>) => {
    return put<BriefTemplate>(`/brief/templates/${id}/`, data)
  },

  // 删除简报模板
  delete: (id: number) => {
    return del(`/brief/templates/${id}/`)
  },
}

/**
 * 简报策略API
 */
export const briefStrategyApi = {
  // 获取简报策略列表
  getList: (params?: BriefStrategyListParams) => {
    return getList<BriefStrategy>('/brief/strategies/', params)
  },

  // 获取简报策略详情
  getDetail: (id: number) => {
    return get<BriefStrategy>(`/brief/strategies/${id}/`)
  },

  // 创建简报策略
  create: (data: BriefStrategyFormData) => {
    return post<BriefStrategy>('/brief/strategies/', data)
  },

  // 更新简报策略
  update: (id: number, data: Partial<BriefStrategyFormData>) => {
    return put<BriefStrategy>(`/brief/strategies/${id}/`, data)
  },

  // 删除简报策略
  delete: (id: number) => {
    return del(`/brief/strategies/${id}/`)
  },
}

/**
 * 简报数据API
 */
export const briefDataApi = {
  // 获取简报数据列表
  getList: (params?: BriefDataListParams) => {
    return getList<BriefData>('/brief/data/', params)
  },

  // 获取简报数据详情
  getDetail: (id: number) => {
    return get<BriefData>(`/brief/data/${id}/`)
  },

  // 生成简报数据
  generate: (data: BriefDataGenerateParams) => {
    return post<BriefData>('/brief/data/generate/', data)
  },

  // 删除简报数据
  delete: (id: number) => {
    return del(`/brief/data/${id}/`)
  },
}

/**
 * 简报推送API
 */
export const briefPushApi = {
  // 获取简报推送记录列表
  getList: (params?: BriefPushListParams) => {
    return getList<BriefPush>('/brief/pushes/', params)
  },

  // 获取简报推送记录详情
  getDetail: (id: number) => {
    return get<BriefPush>(`/brief/pushes/${id}/`)
  },

  // 推送简报
  push: (data: BriefPushCreateParams) => {
    return post<BriefPush[]>('/brief/pushes/push/', data)
  },

  // 标记已读
  markRead: (data: BriefPushReadParams) => {
    return post<BriefPush>('/brief/pushes/mark_read/', data)
  },

  // 删除推送记录
  delete: (id: number) => {
    return del(`/brief/pushes/${id}/`)
  },
}

