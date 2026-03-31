/**
 * 演练模块API
 */
import { get, post, put, patch, del, getList } from '../request'
import type {
  DrillEvent,
  DrillEventListParams,
  DrillEventFormData,
  DrillEvaluation,
  DrillEvaluationListParams,
  DrillEvaluationFormData,
  DrillSummary,
  DrillSummaryListParams,
  DrillSummaryFormData,
  DrillAnalysis,
  DrillAnalysisParams,
} from '@/types/modules/drill'

/**
 * 演练事件API
 */
export const drillEventApi = {
  // 获取演练事件列表
  getList: (params?: DrillEventListParams) => {
    return getList<DrillEvent>('/drill/events/', params)
  },

  // 获取演练事件详情
  getDetail: (id: number) => {
    return get<DrillEvent>(`/drill/events/${id}/`)
  },

  // 创建演练事件
  create: (data: DrillEventFormData) => {
    return post<DrillEvent>('/drill/events/', data)
  },

  // 更新演练事件
  update: (id: number, data: Partial<DrillEventFormData>) => {
    return put<DrillEvent>(`/drill/events/${id}/`, data)
  },

  // 部分更新演练事件
  partialUpdate: (id: number, data: Partial<DrillEventFormData>) => {
    return patch<DrillEvent>(`/drill/events/${id}/`, data)
  },

  // 删除演练事件
  delete: (id: number) => {
    return del(`/drill/events/${id}/`)
  },

  // 获取演练事件统计
  getStatistics: (params?: { start_time?: string; end_time?: string }) => {
    return get('/drill/events/statistics/', params)
  },
}

/**
 * 演练评价API
 */
export const drillEvaluationApi = {
  // 获取演练评价列表
  getList: (params?: DrillEvaluationListParams) => {
    return getList<DrillEvaluation>('/drill/evaluations/', params)
  },

  // 获取演练评价详情
  getDetail: (id: number) => {
    return get<DrillEvaluation>(`/drill/evaluations/${id}/`)
  },

  // 创建演练评价
  create: (data: DrillEvaluationFormData) => {
    return post<DrillEvaluation>('/drill/evaluations/', data)
  },

  // 更新演练评价
  update: (id: number, data: Partial<DrillEvaluationFormData>) => {
    return put<DrillEvaluation>(`/drill/evaluations/${id}/`, data)
  },

  // 部分更新演练评价
  partialUpdate: (id: number, data: Partial<DrillEvaluationFormData>) => {
    return patch<DrillEvaluation>(`/drill/evaluations/${id}/`, data)
  },

  // 删除演练评价
  delete: (id: number) => {
    return del(`/drill/evaluations/${id}/`)
  },
}

/**
 * 演练总结API
 */
export const drillSummaryApi = {
  // 获取演练总结列表
  getList: (params?: DrillSummaryListParams) => {
    return getList<DrillSummary>('/drill/summaries/', params)
  },

  // 获取演练总结详情
  getDetail: (id: number) => {
    return get<DrillSummary>(`/drill/summaries/${id}/`)
  },

  // 根据事件ID获取演练总结
  getByEventId: (eventId: number) => {
    return get<DrillSummary>(`/drill/summaries/by_event/${eventId}/`)
  },

  // 创建演练总结
  create: (data: DrillSummaryFormData) => {
    return post<DrillSummary>('/drill/summaries/', data)
  },

  // 更新演练总结
  update: (id: number, data: Partial<DrillSummaryFormData>) => {
    return put<DrillSummary>(`/drill/summaries/${id}/`, data)
  },

  // 部分更新演练总结
  partialUpdate: (id: number, data: Partial<DrillSummaryFormData>) => {
    return patch<DrillSummary>(`/drill/summaries/${id}/`, data)
  },

  // 删除演练总结
  delete: (id: number) => {
    return del(`/drill/summaries/${id}/`)
  },
}

/**
 * 演练分析API
 */
export const drillAnalysisApi = {
  // 获取演练分析数据
  getAnalysis: (params?: DrillAnalysisParams) => {
    return get<DrillAnalysis[]>('/drill/analyses/', params)
  },

  // 获取演练统计
  getStatistics: (params?: DrillAnalysisParams) => {
    return get<any>('/drill/analyses/statistics/', params)
  },
}

