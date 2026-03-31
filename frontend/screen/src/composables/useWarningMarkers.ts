/**
 * 预警事件标记点管理 Composable
 * 用于管理预警事件数据并转换为地图标记点
 */
import { ref, computed } from 'vue'
import { getLatestWarningEvents, type WarningEvent } from '@/api/modules/safety'
import type { MapMarker } from '@/types/map'

// 预警级别颜色映射（根据warning_level_id，这里使用简化的映射）
// 实际应该根据预警级别详情来确定颜色
export const WARNING_LEVEL_COLORS: Record<number, string> = {
  1: '#ff4d4f', // 红色I级
  2: '#ffa940', // 橙色Ⅱ级
  3: '#ffd666', // 黄色Ⅲ级
  4: '#1890ff', // 蓝色Ⅳ级
}

// 预警状态图标映射
const WARNING_STATUS_ICONS: Record<number, string> = {
  0: '⏸️', // 未发布
  1: '📢', // 已发布
  2: '⚙️', // 处理中
  3: '✅', // 已处置
  4: '🔒', // 已关闭
}

// 预警事件数据
const warningEventList = ref<WarningEvent[]>([])

/**
 * 将预警事件转换为地图标记点
 */
const convertToMarkers = (events: WarningEvent[]): MapMarker[] => {
  return events
    .filter((event) => {
      // 验证坐标是否存在且有效
      if (!event.longitude || !event.latitude) {
        console.warn(`预警事件 ${event.warning_title} (ID: ${event.id}) 缺少坐标信息，跳过标记`)
        return false
      }

      const lng = Number(event.longitude)
      const lat = Number(event.latitude)

      // 验证坐标范围（马鞍山市范围：经度 118.3-118.7，纬度 31.5-31.9）
      if (isNaN(lng) || isNaN(lat) || lng < 118 || lng > 119 || lat < 31 || lat > 32) {
        console.warn(`预警事件 ${event.warning_title} (ID: ${event.id}) 坐标无效 (${lng}, ${lat})，跳过标记`)
        return false
      }

      return true
    })
    .map((event) => {
      const lng = Number(event.longitude!)
      const lat = Number(event.latitude!)
      
      // 根据预警级别确定颜色（默认使用橙色）
      const color = WARNING_LEVEL_COLORS[event.warning_level_id] || '#ffa940'
      
      // 根据预警状态确定图标
      const statusIcon = WARNING_STATUS_ICONS[event.warning_status] || '⚠️'

      return {
        id: `warning-${event.id}`,
        position: {
          lng: lng,
          lat: lat,
        },
        label: event.warning_title,
        icon: statusIcon, // 使用状态图标（emoji）
        data: {
          type: 'warning',
          color: color, // 添加颜色信息，用于标记点显示
          warning_level_display: getWarningLevelDisplay(event.warning_level_id), // 预警级别显示文本
          ...event,
        },
      }
    })
}

/**
 * 获取预警级别显示文本
 */
function getWarningLevelDisplay(levelId: number): string {
  const labels: Record<number, string> = {
    1: '红色I级',
    2: '橙色Ⅱ级',
    3: '黄色Ⅲ级',
    4: '蓝色Ⅳ级',
  }
  return labels[levelId] || '未知级别'
}

/**
 * 计算属性：转换为地图标记点
 */
const markers = computed<MapMarker[]>(() => {
  const result = convertToMarkers(warningEventList.value)
  
  // 输出统计信息（仅在标记点数量变化时输出，避免频繁日志）
  if (result.length > 0 || warningEventList.value.length > 0) {
    const skippedCount = warningEventList.value.length - result.length
    if (skippedCount > 0) {
      console.log(`预警事件标记点: 成功创建 ${result.length} 个标记点, 跳过 ${skippedCount} 个无效数据（缺少坐标或坐标无效）`)
    } else if (result.length > 0) {
      console.log(`预警事件标记点: 成功创建 ${result.length} 个标记点`)
    }
  }
  
  return result
})

/**
 * 加载预警事件数据
 */
const loadWarningEvents = async () => {
  try {
    console.log('开始加载预警事件数据...')
    const data = await getLatestWarningEvents({ limit: 200 })
    
    // 验证数据有效性
    if (!data || !Array.isArray(data)) {
      console.warn('预警事件数据格式错误，返回空数组')
      warningEventList.value = []
      return
    }
    
    warningEventList.value = data
    
    // 统计信息
    const totalCount = data.length
    const validCoordCount = data.filter(e => e.longitude && e.latitude).length
    const levelStats: Record<number, number> = {}
    const statusStats: Record<number, number> = {}
    
    data.forEach(event => {
      levelStats[event.warning_level_id] = (levelStats[event.warning_level_id] || 0) + 1
      statusStats[event.warning_status] = (statusStats[event.warning_status] || 0) + 1
    })
    
    const levelStr = Object.entries(levelStats)
      .map(([level, count]) => {
        const levelNames: Record<string, string> = { '1': 'I级', '2': 'Ⅱ级', '3': 'Ⅲ级', '4': 'Ⅳ级' }
        return `${levelNames[level] || '未知'}: ${count}`
      })
      .join(', ')
    
    console.log(`预警事件数据加载成功: 总计 ${totalCount} 个事件, 有效坐标 ${validCoordCount} 个`)
    if (levelStr) {
      console.log(`预警级别分布: ${levelStr}`)
    }
    
    if (validCoordCount < totalCount) {
      console.warn(`其中 ${totalCount - validCoordCount} 个事件缺少坐标信息，将不会显示在地图上`)
    }
  } catch (error) {
    console.error('加载预警事件数据失败:', error)
    // API失败时，清空数据，不显示模拟数据
    warningEventList.value = []
    
    // 可以在这里添加错误提示，例如使用 ElMessage
    if (window.console && console.error) {
      console.error('预警事件数据加载失败，请检查后端API是否正常', error)
    }
  }
}

/**
 * 获取预警事件统计信息
 */
const warningStatistics = computed(() => {
  const stats = {
    total: warningEventList.value.length,
    byLevel: {
      1: 0, // 红色I级
      2: 0, // 橙色Ⅱ级
      3: 0, // 黄色Ⅲ级
      4: 0, // 蓝色Ⅳ级
    },
    byStatus: {
      0: 0, // 未发布
      1: 0, // 已发布
      2: 0, // 处理中
      3: 0, // 已处置
      4: 0, // 已关闭
    },
  }

  warningEventList.value.forEach((event) => {
    stats.byLevel[event.warning_level_id as keyof typeof stats.byLevel]++
    stats.byStatus[event.warning_status as keyof typeof stats.byStatus]++
  })

  return stats
})

export function useWarningMarkers() {
  return {
    warningEventList,
    markers,
    warningStatistics,
    loadWarningEvents,
  }
}

