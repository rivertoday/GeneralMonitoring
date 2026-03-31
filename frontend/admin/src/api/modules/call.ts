/**
 * 叫应模块API
 */
import { get, post, put, patch, del, getList, uploadFile } from '../request'
import type { PaginatedResponse } from '../types'
import type {
  CallTarget,
  CallTargetListParams,
  CallTargetFormData,
  CallPerson,
  CallPersonListParams,
  CallPersonFormData,
  CallGroup,
  CallGroupListParams,
  CallGroupFormData,
  PolicyFile,
  PolicyFileListParams,
  PolicyFileFormData,
  PolicyFilePublishData,
  PolicyDistribution,
  PolicyDistributionListParams,
  PolicyDistributionFormData,
  PolicyDistributionFeedbackData,
  PolicyDistributionSuperviseData,
  CallRecord,
  CallRecordListParams,
  CallRecordFormData,
  CallRecordResponseData,
  EmergencyCallData,
  EmergencyCallResponse,
} from '@/types/modules/call'

/**
 * 叫应对象API
 */
export const callTargetApi = {
  // 获取叫应对象列表
  getList: (params?: CallTargetListParams) => {
    return getList<CallTarget>('/call/targets/', params)
  },

  // 获取叫应对象详情
  getDetail: (id: number) => {
    return get<CallTarget>(`/call/targets/${id}/`)
  },

  // 创建叫应对象
  create: (data: CallTargetFormData) => {
    return post<CallTarget>('/call/targets/', data)
  },

  // 更新叫应对象
  update: (id: number, data: Partial<CallTargetFormData>) => {
    return put<CallTarget>(`/call/targets/${id}/`, data)
  },

  // 部分更新叫应对象
  partialUpdate: (id: number, data: Partial<CallTargetFormData>) => {
    return patch<CallTarget>(`/call/targets/${id}/`, data)
  },

  // 删除叫应对象
  delete: (id: number) => {
    return del(`/call/targets/${id}/`)
  },
}

/**
 * 叫应人员API
 */
export const callPersonApi = {
  // 获取叫应人员列表
  getList: (params?: CallPersonListParams) => {
    return getList<CallPerson>('/call/persons/', params)
  },

  // 获取叫应人员详情
  getDetail: (id: number) => {
    return get<CallPerson>(`/call/persons/${id}/`)
  },

  // 创建叫应人员
  create: (data: CallPersonFormData) => {
    return post<CallPerson>('/call/persons/', data)
  },

  // 更新叫应人员
  update: (id: number, data: Partial<CallPersonFormData>) => {
    return put<CallPerson>(`/call/persons/${id}/`, data)
  },

  // 部分更新叫应人员
  partialUpdate: (id: number, data: Partial<CallPersonFormData>) => {
    return patch<CallPerson>(`/call/persons/${id}/`, data)
  },

  // 删除叫应人员
  delete: (id: number) => {
    return del(`/call/persons/${id}/`)
  },
}

/**
 * 叫应分组API
 */
export const callGroupApi = {
  // 获取叫应分组列表
  getList: (params?: CallGroupListParams) => {
    return getList<CallGroup>('/call/groups/', params)
  },

  // 获取叫应分组详情
  getDetail: (id: number) => {
    return get<CallGroup>(`/call/groups/${id}/`)
  },

  // 创建叫应分组
  create: (data: CallGroupFormData) => {
    return post<CallGroup>('/call/groups/', data)
  },

  // 更新叫应分组
  update: (id: number, data: Partial<CallGroupFormData>) => {
    return put<CallGroup>(`/call/groups/${id}/`, data)
  },

  // 部分更新叫应分组
  partialUpdate: (id: number, data: Partial<CallGroupFormData>) => {
    return patch<CallGroup>(`/call/groups/${id}/`, data)
  },

  // 删除叫应分组
  delete: (id: number) => {
    return del(`/call/groups/${id}/`)
  },
}

/**
 * 政策文件API
 */
export const policyFileApi = {
  // 获取政策文件列表
  getList: (params?: PolicyFileListParams) => {
    return getList<PolicyFile>('/call/policy-files/', params)
  },

  // 获取政策文件详情
  getDetail: (id: number) => {
    return get<PolicyFile>(`/call/policy-files/${id}/`)
  },

  // 创建政策文件
  create: (data: PolicyFileFormData) => {
    return post<PolicyFile>('/call/policy-files/', data)
  },

  // 更新政策文件
  update: (id: number, data: Partial<PolicyFileFormData>) => {
    return put<PolicyFile>(`/call/policy-files/${id}/`, data)
  },

  // 部分更新政策文件
  partialUpdate: (id: number, data: Partial<PolicyFileFormData>) => {
    return patch<PolicyFile>(`/call/policy-files/${id}/`, data)
  },

  // 删除政策文件
  delete: (id: number) => {
    return del(`/call/policy-files/${id}/`)
  },

  // 发布政策文件
  publish: (id: number, data?: PolicyFilePublishData) => {
    return post<PolicyFile>(`/call/policy-files/${id}/publish/`, data || {})
  },

  // 上传文件（需要先上传文件获取file_path等信息，然后再创建政策文件）
  upload: (file: File, onUploadProgress?: (progressEvent: any) => void) => {
    // 这里假设后端有文件上传接口，如果没有，可能需要调整
    // 实际的文件上传接口路径需要根据后端实际情况调整
    return uploadFile<{ file_path: string; file_name: string; file_size: number; file_type: string; file_ext: string }>(
      '/call/policy-files/upload/',
      file,
      onUploadProgress
    )
  },
}

/**
 * 政策文件下发API
 */
export const policyDistributionApi = {
  // 获取政策文件下发列表
  getList: (params?: PolicyDistributionListParams) => {
    return getList<PolicyDistribution>('/call/policy-distributions/', params)
  },

  // 获取政策文件下发详情
  getDetail: (id: number) => {
    return get<PolicyDistribution>(`/call/policy-distributions/${id}/`)
  },

  // 创建政策文件下发
  create: (data: PolicyDistributionFormData) => {
    return post<PolicyDistribution>('/call/policy-distributions/', data)
  },

  // 更新政策文件下发
  update: (id: number, data: Partial<PolicyDistributionFormData>) => {
    return put<PolicyDistribution>(`/call/policy-distributions/${id}/`, data)
  },

  // 部分更新政策文件下发
  partialUpdate: (id: number, data: Partial<PolicyDistributionFormData>) => {
    return patch<PolicyDistribution>(`/call/policy-distributions/${id}/`, data)
  },

  // 删除政策文件下发
  delete: (id: number) => {
    return del(`/call/policy-distributions/${id}/`)
  },

  // 反馈政策文件下发
  feedback: (id: number, data: PolicyDistributionFeedbackData) => {
    return post<PolicyDistribution>(`/call/policy-distributions/${id}/feedback/`, data)
  },

  // 督办政策文件下发
  supervise: (id: number, data: PolicyDistributionSuperviseData) => {
    return post<PolicyDistribution>(`/call/policy-distributions/${id}/supervise/`, data)
  },
}

/**
 * 叫应记录API
 */
export const callRecordApi = {
  // 获取叫应记录列表
  getList: (params?: CallRecordListParams) => {
    return getList<CallRecord>('/call/records/', params)
  },

  // 获取叫应记录详情
  getDetail: (id: number) => {
    return get<CallRecord>(`/call/records/${id}/`)
  },

  // 创建叫应记录
  create: (data: CallRecordFormData) => {
    return post<CallRecord>('/call/records/', data)
  },

  // 更新叫应记录
  update: (id: number, data: Partial<CallRecordFormData>) => {
    return put<CallRecord>(`/call/records/${id}/`, data)
  },

  // 部分更新叫应记录
  partialUpdate: (id: number, data: Partial<CallRecordFormData>) => {
    return patch<CallRecord>(`/call/records/${id}/`, data)
  },

  // 删除叫应记录
  delete: (id: number) => {
    return del(`/call/records/${id}/`)
  },

  // 响应叫应记录
  response: (id: number, data: CallRecordResponseData) => {
    return post<CallRecord>(`/call/records/${id}/response/`, data)
  },

  // 重试叫应记录
  retry: (id: number) => {
    return post<CallRecord>(`/call/records/${id}/retry/`, {})
  },

  // 获取叫应记录统计
  getStatistics: (params?: { start_time?: string; end_time?: string }) => {
    return get('/call/records/statistics/', params)
  },
}

/**
 * 一键叫应API
 */
export const emergencyCallApi = {
  // 一键叫应
  call: (data: EmergencyCallData) => {
    return post<EmergencyCallResponse>('/call/emergency/call/', data)
  },
}

