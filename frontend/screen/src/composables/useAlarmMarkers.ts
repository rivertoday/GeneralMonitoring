/**
 * 报警记录标记点管理 Composable
 * 用于管理报警记录数据并转换为地图标记点
 */
import { ref, computed } from 'vue'
import { getLatestAlarmRecords, type AlarmRecord } from '@/api/modules/risk'
import type { MapMarker } from '@/types/map'

// 报警状态颜色映射
export const ALARM_STATUS_COLORS: Record<number, string> = {
  0: '#ff4d4f', // 未处理 - 红色
  1: '#ffa940', // 处理中 - 橙色
  2: '#52c41a', // 已处理 - 绿色
  3: '#999999', // 已忽略 - 灰色
}

// 报警状态图标映射
const ALARM_STATUS_ICONS: Record<number, string> = {
  0: '🔴', // 未处理
  1: '🟠', // 处理中
  2: '🟢', // 已处理
  3: '⚪', // 已忽略
}

// 报警记录数据
const alarmRecordList = ref<AlarmRecord[]>([])

/**
 * 将报警记录转换为地图标记点
 */
const convertToMarkers = (records: AlarmRecord[]): MapMarker[] => {
  return records
    .filter((record) => {
      // 验证坐标是否存在且有效
      if (!record.longitude || !record.latitude) {
        console.warn(`报警记录 ${record.alarm_code} (ID: ${record.id}) 缺少坐标信息，跳过标记`)
        return false
      }

      const lng = Number(record.longitude)
      const lat = Number(record.latitude)

      // 验证坐标范围（马鞍山市范围：经度 118.3-118.7，纬度 31.5-31.9）
      if (isNaN(lng) || isNaN(lat) || lng < 118 || lng > 119 || lat < 31 || lat > 32) {
        console.warn(`报警记录 ${record.alarm_code} (ID: ${record.id}) 坐标无效 (${lng}, ${lat})，跳过标记`)
        return false
      }

      return true
    })
    .map((record) => {
      const lng = Number(record.longitude!)
      const lat = Number(record.latitude!)
      
      // 根据报警状态确定颜色
      const color = ALARM_STATUS_COLORS[record.alarm_status] || '#ff4d4f'
      
      // 根据报警状态确定图标
      const statusIcon = ALARM_STATUS_ICONS[record.alarm_status] || '🔴'

      // 构建标签文本
      let labelText = record.alarm_type || '报警'
      if (record.monitor_detail?.monitor_name) {
        labelText = `${record.monitor_detail.monitor_name} - ${record.alarm_type}`
      }

      return {
        id: `alarm-${record.id}`,
        position: {
          lng: lng,
          lat: lat,
        },
        label: labelText,
        icon: statusIcon, // 使用状态图标（emoji）
        data: {
          type: 'alarm',
          color: color, // 添加颜色信息，用于标记点显示
          ...record,
        },
      }
    })
}

/**
 * 计算属性：转换为地图标记点
 */
const markers = computed<MapMarker[]>(() => {
  const result = convertToMarkers(alarmRecordList.value)
  
  // 输出统计信息（仅在标记点数量变化时输出，避免频繁日志）
  if (result.length > 0 || alarmRecordList.value.length > 0) {
    const skippedCount = alarmRecordList.value.length - result.length
    if (skippedCount > 0) {
      console.log(`报警记录标记点: 成功创建 ${result.length} 个标记点, 跳过 ${skippedCount} 个无效数据（缺少坐标或坐标无效）`)
    } else if (result.length > 0) {
      console.log(`报警记录标记点: 成功创建 ${result.length} 个标记点`)
    }
  }
  
  return result
})

/**
 * 加载报警记录数据
 */
const loadAlarmRecords = async () => {
  try {
    console.log('开始加载报警记录数据...')
    const data = await getLatestAlarmRecords({ limit: 200 })
    
    // 验证数据有效性
    if (!data || !Array.isArray(data)) {
      console.warn('报警记录数据格式错误，返回空数组')
      alarmRecordList.value = []
      return
    }
    
    alarmRecordList.value = data
    
    // 统计信息
    const totalCount = data.length
    const validCoordCount = data.filter(r => r.longitude && r.latitude).length
    const statusStats: Record<number, number> = {}
    
    data.forEach(record => {
      statusStats[record.alarm_status] = (statusStats[record.alarm_status] || 0) + 1
    })
    
    const statusStr = Object.entries(statusStats)
      .map(([status, count]) => {
        const statusNames: Record<string, string> = { '0': '未处理', '1': '处理中', '2': '已处理', '3': '已忽略' }
        return `${statusNames[status] || '未知'}: ${count}`
      })
      .join(', ')
    
    console.log(`报警记录数据加载成功: 总计 ${totalCount} 条记录, 有效坐标 ${validCoordCount} 条`)
    if (statusStr) {
      console.log(`报警状态分布: ${statusStr}`)
    }
    
    if (validCoordCount < totalCount) {
      console.warn(`其中 ${totalCount - validCoordCount} 条记录缺少坐标信息，将不会显示在地图上`)
    }
  } catch (error) {
    console.error('加载报警记录数据失败:', error)
    // API失败时，清空数据，不显示模拟数据
    alarmRecordList.value = []
    
    // 可以在这里添加错误提示，例如使用 ElMessage
    if (window.console && console.error) {
      console.error('报警记录数据加载失败，请检查后端API是否正常', error)
    }
  }
}

/**
 * 获取报警记录统计信息
 */
const alarmStatistics = computed(() => {
  const stats = {
    total: alarmRecordList.value.length,
    byStatus: {
      0: 0, // 未处理
      1: 0, // 处理中
      2: 0, // 已处理
      3: 0, // 已忽略
    },
    unhandledCount: 0, // 未处理数量（用于统计面板）
    handlingCount: 0, // 处理中数量
    handledCount: 0, // 已处理数量
  }

  alarmRecordList.value.forEach((record) => {
    stats.byStatus[record.alarm_status as keyof typeof stats.byStatus]++
    if (record.alarm_status === 0) {
      stats.unhandledCount++
    } else if (record.alarm_status === 1) {
      stats.handlingCount++
    } else if (record.alarm_status === 2) {
      stats.handledCount++
    }
  })

  return stats
})

export function useAlarmMarkers() {
  return {
    alarmRecordList,
    markers,
    alarmStatistics,
    loadAlarmRecords,
  }
}

