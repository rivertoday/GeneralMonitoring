/**
 * 视频监控设施标记点管理 Composable
 * 用于管理视频监控设施数据并转换为地图标记点
 */
import { ref, computed } from 'vue'
import { getVideoMonitorList, getNearbyVideoMonitors, type VideoMonitor } from '@/api/modules/safety'
import type { MapMarker } from '@/types/map'

// 视频监控数据
const videoMonitorList = ref<VideoMonitor[]>([])

/**
 * 将视频监控设施转换为地图标记点
 */
const convertToMarkers = (monitors: VideoMonitor[]): MapMarker[] => {
  return monitors
    .filter((monitor) => monitor.longitude && monitor.latitude && monitor.status === 1) // 只处理有坐标且启用的监控
    .map((monitor) => {
      // 根据在线状态确定颜色
      const color = monitor.online_status === 1 ? '#52c41a' : '#ff4d4f' // 绿色-在线，红色-离线

      return {
        id: `video-${monitor.id}`,
        position: {
          lng: Number(monitor.longitude),
          lat: Number(monitor.latitude),
        },
        label: monitor.monitor_name,
        icon: '📹', // 视频监控图标（emoji）
        data: {
          type: 'video',
          color: color, // 添加颜色信息
          ...monitor,
        },
      }
    })
}

/**
 * 计算属性：转换为地图标记点
 */
const markers = computed<MapMarker[]>(() => {
  return convertToMarkers(videoMonitorList.value)
})

/**
 * 加载所有视频监控设施
 */
const loadAllMonitors = async () => {
  try {
    console.log('开始加载视频监控设施数据...')
    const response = await getVideoMonitorList({
      page_size: 1000, // 获取足够多的数据
      status: 1, // 只获取启用的监控
    })
    
    const data = response.results || []
    
    // 验证数据有效性
    if (!Array.isArray(data)) {
      console.warn('视频监控设施数据格式错误，返回空数组')
      videoMonitorList.value = []
      return
    }
    
    videoMonitorList.value = data
    
    const validCoordCount = data.filter(m => m.longitude && m.latitude).length
    const onlineCount = data.filter(m => m.online_status === 1).length
    
    console.log(`视频监控设施数据加载成功: 总计 ${data.length} 个监控, 有效坐标 ${validCoordCount} 个, 在线 ${onlineCount} 个`)
    
    if (data.length === 0) {
      console.warn('警告：视频监控设施数据为空，请检查后端API或数据')
    }
  } catch (error) {
    console.error('加载视频监控设施数据失败:', error)
    // API失败时，清空数据，不显示模拟数据
    videoMonitorList.value = []
    
    if (window.console && console.error) {
      console.error('视频监控设施数据加载失败，请检查后端API是否正常', error)
    }
  }
}

/**
 * 根据位置加载附近的视频监控设施
 */
const loadNearbyMonitors = async (longitude: number, latitude: number, radius: number = 5000) => {
  try {
    console.log(`开始加载附近视频监控设施 (${longitude}, ${latitude}, 半径: ${radius}m)...`)
    const data = await getNearbyVideoMonitors({ longitude, latitude, radius })
    
    // 验证数据有效性
    if (!Array.isArray(data)) {
      console.warn('附近视频监控设施数据格式错误，返回空数组')
      videoMonitorList.value = []
      return
    }
    
    // 合并到现有列表（避免重复）
    const existingIds = new Set(videoMonitorList.value.map(m => m.id))
    const newMonitors = data.filter(m => !existingIds.has(m.id))
    videoMonitorList.value = [...videoMonitorList.value, ...newMonitors]
    
    console.log(`附近视频监控设施加载成功: 找到 ${data.length} 个监控, 新增 ${newMonitors.length} 个`)
  } catch (error) {
    console.error('加载附近视频监控设施失败:', error)
    // API失败时，不清空现有数据，只记录错误
    if (window.console && console.error) {
      console.error('附近视频监控设施加载失败，请检查后端API是否正常', error)
    }
  }
}


/**
 * 获取视频监控统计信息
 */
const monitorStatistics = computed(() => {
  const stats = {
    total: videoMonitorList.value.length,
    online: 0,
    offline: 0,
    byType: {
      1: 0, // 固定监控
      2: 0, // 移动监控
      3: 0, // 无人机监控
    },
  }

  videoMonitorList.value.forEach((monitor) => {
    if (monitor.online_status === 1) {
      stats.online++
    } else {
      stats.offline++
    }
    stats.byType[monitor.monitor_type as keyof typeof stats.byType]++
  })

  return stats
})

export function useVideoMonitors() {
  return {
    videoMonitorList,
    markers,
    monitorStatistics,
    loadAllMonitors,
    loadNearbyMonitors,
  }
}

