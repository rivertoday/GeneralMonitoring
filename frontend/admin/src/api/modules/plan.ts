/**
 * 预案模块API
 */
import { get, post, put, patch, del, getList } from '../request'
import type { PaginatedResponse } from '../types'
import type {
  EmergencyPlan,
  EmergencyPlanListParams,
  EmergencyPlanFormData,
  PlanStructure,
  PlanStructureListParams,
  PlanStructureFormData,
  PlanFlow,
  PlanFlowListParams,
  PlanFlowFormData,
  PlanTask,
  PlanTaskListParams,
  PlanTaskFormData,
  PlanExecution,
  PlanExecutionListParams,
  PlanExecutionFormData,
  PlanStatistics,
  PlanStatisticsParams,
} from '@/types/modules/plan'

/**
 * 应急预案API
 */
export const emergencyPlanApi = {
  // 获取预案列表
  getList: (params?: EmergencyPlanListParams) => {
    return getList<EmergencyPlan>('/plan/plans/', params)
  },

  // 获取预案详情
  getDetail: (id: number) => {
    return get<EmergencyPlan>(`/plan/plans/${id}/`)
  },

  // 创建预案
  create: (data: EmergencyPlanFormData) => {
    return post<EmergencyPlan>('/plan/plans/', data)
  },

  // 更新预案
  update: (id: number, data: Partial<EmergencyPlanFormData>) => {
    return put<EmergencyPlan>(`/plan/plans/${id}/`, data)
  },

  // 部分更新预案
  partialUpdate: (id: number, data: Partial<EmergencyPlanFormData>) => {
    return patch<EmergencyPlan>(`/plan/plans/${id}/`, data)
  },

  // 删除预案
  delete: (id: number) => {
    return del(`/plan/plans/${id}/`)
  },

  // 发布预案
  publish: (id: number) => {
    return post<EmergencyPlan>(`/plan/plans/${id}/publish/`)
  },

  // 审批预案
  approve: (id: number, approved: boolean, comment?: string) => {
    return post<EmergencyPlan>(`/plan/plans/${id}/approve/`, {
      approved,
      comment,
    })
  },

  // 修订预案
  revise: (id: number, data: { revision_reason: string; version?: string }) => {
    return post<EmergencyPlan>(`/plan/plans/${id}/revise/`, data)
  },

  // 废止预案
  abolish: (id: number, reason?: string) => {
    return post<EmergencyPlan>(`/plan/plans/${id}/abolish/`, { reason })
  },

  // 获取预案统计
  getStatistics: (params?: PlanStatisticsParams) => {
    return get<PlanStatistics>('/plan/plans/statistics/', params)
  },
}

/**
 * 预案结构API
 */
export const planStructureApi = {
  // 获取结构列表（树形）
  getTree: (planId: number, params?: Omit<PlanStructureListParams, 'plan_id'>) => {
    return get<PlanStructure[]>(`/plan/plans/${planId}/structures/tree/`, params)
  },

  // 获取结构列表（扁平）
  getList: (planId: number, params?: Omit<PlanStructureListParams, 'plan_id'>) => {
    return get<PlanStructure[]>(`/plan/plans/${planId}/structures/`, params)
  },

  // 获取结构详情
  getDetail: (planId: number, id: number) => {
    return get<PlanStructure>(`/plan/plans/${planId}/structures/${id}/`)
  },

  // 创建结构
  create: (planId: number, data: PlanStructureFormData) => {
    return post<PlanStructure>(`/plan/plans/${planId}/structures/`, data)
  },

  // 更新结构
  update: (planId: number, id: number, data: Partial<PlanStructureFormData>) => {
    return put<PlanStructure>(`/plan/plans/${planId}/structures/${id}/`, data)
  },

  // 部分更新结构
  partialUpdate: (planId: number, id: number, data: Partial<PlanStructureFormData>) => {
    return patch<PlanStructure>(`/plan/plans/${planId}/structures/${id}/`, data)
  },

  // 删除结构
  delete: (planId: number, id: number) => {
    return del(`/plan/plans/${planId}/structures/${id}/`)
  },
}

/**
 * 预案流程API
 */
export const planFlowApi = {
  // 获取流程列表（树形）
  getTree: (planId: number, params?: Omit<PlanFlowListParams, 'plan_id'>) => {
    return get<PlanFlow[]>(`/plan/plans/${planId}/flows/tree/`, params)
  },

  // 获取流程列表（扁平）
  getList: (planId: number, params?: Omit<PlanFlowListParams, 'plan_id'>) => {
    return get<PlanFlow[]>(`/plan/plans/${planId}/flows/`, params)
  },

  // 获取流程详情
  getDetail: (planId: number, id: number) => {
    return get<PlanFlow>(`/plan/plans/${planId}/flows/${id}/`)
  },

  // 创建流程
  create: (planId: number, data: PlanFlowFormData) => {
    return post<PlanFlow>(`/plan/plans/${planId}/flows/`, data)
  },

  // 更新流程
  update: (planId: number, id: number, data: Partial<PlanFlowFormData>) => {
    return put<PlanFlow>(`/plan/plans/${planId}/flows/${id}/`, data)
  },

  // 部分更新流程
  partialUpdate: (planId: number, id: number, data: Partial<PlanFlowFormData>) => {
    return patch<PlanFlow>(`/plan/plans/${planId}/flows/${id}/`, data)
  },

  // 删除流程
  delete: (planId: number, id: number) => {
    return del(`/plan/plans/${planId}/flows/${id}/`)
  },
}

/**
 * 预案任务API
 */
export const planTaskApi = {
  // 获取任务列表
  getList: (params?: PlanTaskListParams) => {
    return getList<PlanTask>('/plan/tasks/', params)
  },

  // 获取任务详情
  getDetail: (id: number) => {
    return get<PlanTask>(`/plan/tasks/${id}/`)
  },

  // 创建任务
  create: (data: PlanTaskFormData) => {
    return post<PlanTask>('/plan/tasks/', data)
  },

  // 更新任务
  update: (id: number, data: Partial<PlanTaskFormData>) => {
    return put<PlanTask>(`/plan/tasks/${id}/`, data)
  },

  // 部分更新任务
  partialUpdate: (id: number, data: Partial<PlanTaskFormData>) => {
    return patch<PlanTask>(`/plan/tasks/${id}/`, data)
  },

  // 删除任务
  delete: (id: number) => {
    return del(`/plan/tasks/${id}/`)
  },
}

/**
 * 预案执行记录API
 */
export const planExecutionApi = {
  // 获取执行记录列表
  getList: (params?: PlanExecutionListParams) => {
    return getList<PlanExecution>('/plan/executions/', params)
  },

  // 获取执行记录详情
  getDetail: (id: number) => {
    return get<PlanExecution>(`/plan/executions/${id}/`)
  },

  // 创建执行记录
  create: (data: PlanExecutionFormData) => {
    return post<PlanExecution>('/plan/executions/', data)
  },

  // 更新执行记录
  update: (id: number, data: Partial<PlanExecutionFormData>) => {
    return put<PlanExecution>(`/plan/executions/${id}/`, data)
  },

  // 部分更新执行记录
  partialUpdate: (id: number, data: Partial<PlanExecutionFormData>) => {
    return patch<PlanExecution>(`/plan/executions/${id}/`, data)
  },

  // 删除执行记录
  delete: (id: number) => {
    return del(`/plan/executions/${id}/`)
  },

  // 启动执行
  start: (id: number) => {
    return post<PlanExecution>(`/plan/executions/${id}/start/`)
  },

  // 更新执行状态
  updateStatus: (id: number, status: number, data?: { current_flow_id?: number; execution_result?: string }) => {
    return post<PlanExecution>(`/plan/executions/${id}/update_status/`, {
      execution_status: status,
      ...data,
    })
  },

  // 完成执行
  complete: (id: number, data?: { execution_summary?: string; execution_result?: string }) => {
    return post<PlanExecution>(`/plan/executions/${id}/complete/`, data)
  },
}

