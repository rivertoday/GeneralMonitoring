/**
 * 风险监测预警API模块（大屏展示系统）
 */
import { get, getList } from '../request'
import type { ListParams, PaginatedResponse } from '../types'

/**
 * 报警记录
 */
export interface AlarmRecord {
  id: number
  alarm_code: string
  monitor: number
  monitor_id: number
  monitor_detail?: {
    id: number
    monitor_code: string
    monitor_name: string
    monitor_type: number
    monitor_type_display: string
    industry_type: number
    industry_type_display: string
    longitude?: number
    latitude?: number
    street?: string
    address?: string
    monitor_unit?: string
    online_status: number
    online_status_display: string
  }
  industry_type: number
  industry_type_display: string
  alarm_type: string
  alarm_value?: number
  threshold_value?: number
  longitude?: number
  latitude?: number
  street?: string
  address?: string
  alarm_time: string
  alarm_duration?: number
  alarm_status: number // 0-未处理，1-处理中，2-已处理，3-已忽略
  alarm_status_display: string
  handle_user_id?: number
  handle_time?: string
  handle_result?: string
  feedback_time?: string
  description?: string
  remark?: string
  created_at: string
  updated_at: string
}

/**
 * 获取报警记录列表
 */
export function getAlarmRecordList(params?: ListParams): Promise<PaginatedResponse<AlarmRecord>> {
  return getList<AlarmRecord>('/risk/alarm-records/', params)
}

/**
 * 获取最新报警记录（用于大屏展示）
 */
export function getLatestAlarmRecords(params?: { limit?: number }): Promise<AlarmRecord[]> {
  return getList<AlarmRecord>('/risk/alarm-records/', {
    ordering: '-alarm_time',
    page_size: params?.limit || 200,
  }).then((response) => {
    return response.results || []
  })
}

