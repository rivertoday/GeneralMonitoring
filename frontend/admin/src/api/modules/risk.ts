/**
 * 风险监测预警模块API
 */
import { get, post, put, patch, del, getList } from '../request'
import type { PaginatedResponse } from '../types'
import type {
  RiskMonitor,
  RiskMonitorListParams,
  RiskMonitorFormData,
  WarningLevel,
  WarningRule,
  AlarmRecord,
  RiskWarning,
  RiskHiddenDanger,
  RiskHiddenDangerListParams,
  RiskHiddenDangerFormData,
  RiskRectification,
  RiskRectificationListParams,
  RiskRectificationFormData,
  AlarmStatistics,
  AlarmStatisticsParams,
  WarningAnalysisParams,
} from '@/types/modules/risk'

/**
 * 风险监测点API
 */
export const riskMonitorApi = {
  // 获取监测点列表
  getList: (params?: RiskMonitorListParams) => {
    return getList<RiskMonitor>('/risk/monitors/', params)
  },

  // 获取监测点详情
  getDetail: (id: number) => {
    return get<RiskMonitor>(`/risk/monitors/${id}/`)
  },

  // 创建监测点
  create: (data: RiskMonitorFormData) => {
    return post<RiskMonitor>('/risk/monitors/', data)
  },

  // 更新监测点
  update: (id: number, data: Partial<RiskMonitorFormData>) => {
    return put<RiskMonitor>(`/risk/monitors/${id}/`, data)
  },

  // 部分更新监测点
  partialUpdate: (id: number, data: Partial<RiskMonitorFormData>) => {
    return patch<RiskMonitor>(`/risk/monitors/${id}/`, data)
  },

  // 删除监测点
  delete: (id: number) => {
    return del(`/risk/monitors/${id}/`)
  },

  // 更新监测点在线状态
  updateStatus: (id: number, onlineStatus: 0 | 1) => {
    return post<RiskMonitor>(`/risk/monitors/${id}/update_status/`, {
      online_status: onlineStatus,
    })
  },
}

/**
 * 预警级别API
 */
export const warningLevelApi = {
  // 获取预警级别列表
  getList: (params?: { page?: number; page_size?: number; status?: 0 | 1 }) => {
    return getList<WarningLevel>('/risk/warning-levels/', params)
  },

  // 获取预警级别详情
  getDetail: (id: number) => {
    return get<WarningLevel>(`/risk/warning-levels/${id}/`)
  },

  // 创建预警级别
  create: (data: Partial<WarningLevel>) => {
    return post<WarningLevel>('/risk/warning-levels/', data)
  },

  // 更新预警级别
  update: (id: number, data: Partial<WarningLevel>) => {
    return put<WarningLevel>(`/risk/warning-levels/${id}/`, data)
  },

  // 删除预警级别
  delete: (id: number) => {
    return del(`/risk/warning-levels/${id}/`)
  },
}

/**
 * 预警规则API
 */
export const warningRuleApi = {
  // 获取预警规则列表
  getList: (params?: {
    page?: number
    page_size?: number
    rule_type?: 1 | 2
    industry_type?: number
    warning_level?: number
    status?: 0 | 1
    search?: string
    ordering?: string
  }) => {
    return getList<WarningRule>('/risk/warning-rules/', params)
  },

  // 获取预警规则详情
  getDetail: (id: number) => {
    return get<WarningRule>(`/risk/warning-rules/${id}/`)
  },

  // 创建预警规则
  create: (data: Partial<WarningRule>) => {
    return post<WarningRule>('/risk/warning-rules/', data)
  },

  // 更新预警规则
  update: (id: number, data: Partial<WarningRule>) => {
    return put<WarningRule>(`/risk/warning-rules/${id}/`, data)
  },

  // 删除预警规则
  delete: (id: number) => {
    return del(`/risk/warning-rules/${id}/`)
  },
}

/**
 * 报警记录API
 */
export const alarmRecordApi = {
  // 获取报警记录列表
  getList: (params?: {
    page?: number
    page_size?: number
    monitor?: number
    industry_type?: number
    alarm_type?: string
    alarm_status?: 0 | 1 | 2 | 3
    street?: string
    start_time?: string
    end_time?: string
    search?: string
    ordering?: string
  }) => {
    return getList<AlarmRecord>('/risk/alarm-records/', params)
  },

  // 获取报警记录详情
  getDetail: (id: number) => {
    return get<AlarmRecord>(`/risk/alarm-records/${id}/`)
  },

  // 创建报警记录
  create: (data: Partial<AlarmRecord>) => {
    return post<AlarmRecord>('/risk/alarm-records/', data)
  },

  // 更新报警记录
  update: (id: number, data: Partial<AlarmRecord>) => {
    return put<AlarmRecord>(`/risk/alarm-records/${id}/`, data)
  },

  // 处理报警
  handle: (id: number, data: { alarm_status: 0 | 1 | 2 | 3; handle_result: string }) => {
    return post<AlarmRecord>(`/risk/alarm-records/${id}/handle/`, data)
  },

  // 删除报警记录
  delete: (id: number) => {
    return del(`/risk/alarm-records/${id}/`)
  },
}

/**
 * 风险预警API
 */
export const riskWarningApi = {
  // 获取风险预警列表
  getList: (params?: {
    page?: number
    page_size?: number
    warning_level?: number
    warning_rule?: number
    industry_type?: number
    warning_type?: string
    warning_analysis_type?: 1 | 2 | 3
    warning_source?: 1 | 2
    warning_status?: 0 | 1 | 2 | 3 | 4
    street?: string
    start_time?: string
    end_time?: string
    search?: string
    ordering?: string
  }) => {
    return getList<RiskWarning>('/risk/warnings/', params)
  },

  // 获取风险预警详情
  getDetail: (id: number) => {
    return get<RiskWarning>(`/risk/warnings/${id}/`)
  },

  // 创建风险预警
  create: (data: Partial<RiskWarning>) => {
    return post<RiskWarning>('/risk/warnings/', data)
  },

  // 更新风险预警
  update: (id: number, data: Partial<RiskWarning>) => {
    return put<RiskWarning>(`/risk/warnings/${id}/`, data)
  },

  // 发布预警
  publish: (id: number) => {
    return post<RiskWarning>(`/risk/warnings/${id}/publish/`)
  },

  // 处置预警
  handle: (id: number, data: { handle_result: string }) => {
    return post<RiskWarning>(`/risk/warnings/${id}/handle/`, data)
  },

  // 删除风险预警
  delete: (id: number) => {
    return del(`/risk/warnings/${id}/`)
  },
}

/**
 * 风险隐患API
 */
export const riskHiddenDangerApi = {
  // 获取风险隐患列表
  getList: (params?: RiskHiddenDangerListParams) => {
    return getList<RiskHiddenDanger>('/risk/hidden-dangers/', params)
  },

  // 获取风险隐患详情
  getDetail: (id: number) => {
    return get<RiskHiddenDanger>(`/risk/hidden-dangers/${id}/`)
  },

  // 创建风险隐患
  create: (data: RiskHiddenDangerFormData) => {
    return post<RiskHiddenDanger>('/risk/hidden-dangers/', data)
  },

  // 更新风险隐患
  update: (id: number, data: Partial<RiskHiddenDangerFormData>) => {
    return put<RiskHiddenDanger>(`/risk/hidden-dangers/${id}/`, data)
  },

  // 删除风险隐患
  delete: (id: number) => {
    return del(`/risk/hidden-dangers/${id}/`)
  },
}

/**
 * 隐患整改API
 */
export const riskRectificationApi = {
  // 获取隐患整改列表
  getList: (params?: RiskRectificationListParams) => {
    return getList<RiskRectification>('/risk/rectifications/', params)
  },

  // 获取隐患整改详情
  getDetail: (id: number) => {
    return get<RiskRectification>(`/risk/rectifications/${id}/`)
  },

  // 创建隐患整改
  create: (data: RiskRectificationFormData) => {
    return post<RiskRectification>('/risk/rectifications/', data)
  },

  // 更新隐患整改
  update: (id: number, data: Partial<RiskRectificationFormData>) => {
    return put<RiskRectification>(`/risk/rectifications/${id}/`, data)
  },

  // 验收整改
  verify: (id: number, data: { verification_status: 0 | 1 | 2; verification_opinion?: string }) => {
    return post<RiskRectification>(`/risk/rectifications/${id}/verify/`, data)
  },

  // 删除隐患整改
  delete: (id: number) => {
    return del(`/risk/rectifications/${id}/`)
  },
}

/**
 * 统计分析API
 */
export const riskStatisticsApi = {
  // 获取报警统计分析
  getAlarmStatistics: (params?: AlarmStatisticsParams) => {
    return getList<AlarmStatistics>('/risk/alarm-statistics/', params)
  },

  // 获取预警统计分析（同比、环比）
  getWarningAnalysis: (params: WarningAnalysisParams) => {
    return get<any>('/risk/warning-analysis/', params)
  },

  // 获取行业报警统计
  getIndustryAlarmStats: (params?: AlarmStatisticsParams) => {
    return get<any>('/risk/statistics/industry-alarm/', params)
  },

  // 获取街道报警统计
  getStreetAlarmStats: (params?: AlarmStatisticsParams) => {
    return get<any>('/risk/statistics/street-alarm/', params)
  },

  // 获取时间维度报警统计
  getTimeAlarmStats: (params?: AlarmStatisticsParams) => {
    return get<any>('/risk/statistics/time-alarm/', params)
  },
}

