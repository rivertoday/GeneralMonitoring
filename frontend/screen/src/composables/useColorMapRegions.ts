/**
 * 四色风险图区域管理 Composable
 * 用于管理区域态势数据并转换为地图多边形
 */
import { ref, computed } from 'vue'
import { getColorMapData, type RegionStatus } from '@/api/modules/safety'
import type { MapPolygon } from '@/types/map'
import { createCirclePoints } from '@/utils/geometry'

// 风险颜色映射
const RISK_COLORS = {
  red: {
    stroke: 'rgba(255, 0, 0, 1)',
    fill: 'rgba(255, 0, 0, 0.4)',
    label: '红色I级',
  },
  orange: {
    stroke: 'rgba(255, 165, 0, 1)',
    fill: 'rgba(255, 165, 0, 0.4)',
    label: '橙色Ⅱ级',
  },
  yellow: {
    stroke: 'rgba(255, 255, 0, 1)',
    fill: 'rgba(255, 255, 0, 0.4)',
    label: '黄色Ⅲ级',
  },
  blue: {
    stroke: 'rgba(0, 0, 255, 1)',
    fill: 'rgba(0, 0, 255, 0.4)',
    label: '蓝色Ⅳ级',
  },
} as const

// 风险区域中心点配置（根据实际风险区域分布，不严格按照行政区域）
// 这些坐标代表实际风险区域的中心位置，用于在地图上绘制风险区域
const RISK_REGION_CENTERS: Record<string, { lng: number; lat: number; radius: number }> = {
  '马钢工业园区风险区域': { lng: 118.488765, lat: 31.740123, radius: 2500 }, // 马钢焦化厂附近
  '雨山湖周边风险区域': { lng: 118.505678, lat: 31.741234, radius: 2000 }, // 雨山湖公园附近
  '市中心商业区风险区域': { lng: 118.510000, lat: 31.750000, radius: 1800 }, // 市中心
  '东部新区风险区域': { lng: 118.540000, lat: 31.720000, radius: 2200 }, // 博望区方向
  '长江沿岸风险区域': { lng: 118.500000, lat: 31.700000, radius: 3000 }, // 长江沿岸
  '南部山区风险区域': { lng: 118.480000, lat: 31.680000, radius: 2500 }, // 南部山区
  '西部工业区风险区域': { lng: 118.460000, lat: 31.660000, radius: 2000 }, // 西部工业区
  // 默认值（如果区域名称不匹配）
  'default': { lng: 118.521577, lat: 31.742368, radius: 2000 },
}

// 区域态势数据
const regionStatusList = ref<RegionStatus[]>([])

// 图层控制：控制哪些风险等级的区域显示
const showRiskLevels = ref({
  red: true,
  orange: true,
  yellow: true,
  blue: true,
})

// 街道筛选：控制哪些街道的区域显示（空数组表示显示所有街道）
const selectedStreets = ref<string[]>([])

// 筛选模式：risk_level（风险等级）或 street（街道）
// 注意：这个值应该在使用的组件中定义，这里只提供类型定义
// 但为了composable的独立性，我们可以在convertToPolygons中根据是否有selectedStreets来决定

/**
 * 获取所有街道列表
 */
const allStreets = computed(() => {
  const streetsSet = new Set<string>()
  regionStatusList.value.forEach((region) => {
    if (region.street) {
      streetsSet.add(region.street)
    }
  })
  return Array.from(streetsSet).sort()
})

/**
 * 将区域态势数据转换为地图多边形
 * @param filterByStreet 如果为true，则按街道筛选（忽略风险等级）；如果为false，则按风险等级筛选（忽略街道）
 */
const convertToPolygons = (regions: RegionStatus[], filterByStreet: boolean = false): MapPolygon[] => {
  return regions
    .filter((region) => {
      // 只处理有风险颜色的区域
      if (!region.risk_color) return false
      
      if (filterByStreet) {
        // 街道筛选模式：按街道筛选，忽略风险等级
        // 如果selectedStreets为空数组，显示所有街道；否则只显示选中的街道
        if (selectedStreets.value.length > 0 && !selectedStreets.value.includes(region.street)) {
          return false
        }
        // 街道模式下，显示所有风险等级（只要街道匹配）
        return true
      } else {
        // 风险等级筛选模式：按风险等级筛选，忽略街道筛选
        const riskColor = region.risk_color as 'red' | 'orange' | 'yellow' | 'blue'
        return showRiskLevels.value[riskColor] === true
      }
    })
    .map((region) => {
      // 获取风险区域中心点和半径（根据区域名称匹配，不严格按照行政区域）
      const center = RISK_REGION_CENTERS[region.street] || RISK_REGION_CENTERS['default']
      
      if (!center) {
        return null
      }

      // 根据风险等级调整半径（风险越高，区域越大）
      let radius = center.radius
      if (region.risk_color === 'red') {
        radius = center.radius * 1.2
      } else if (region.risk_color === 'orange') {
        radius = center.radius * 1.1
      } else if (region.risk_color === 'yellow') {
        radius = center.radius * 1.0
      } else {
        radius = center.radius * 0.9
      }

      // 创建圆形区域路径
      const path = createCirclePoints(
        { lng: center.lng, lat: center.lat },
        radius,
        64
      )

      // 获取颜色配置
      const colorConfig = RISK_COLORS[region.risk_color as keyof typeof RISK_COLORS]

      return {
        id: `region-${region.id}`,
        path,
        strokeColor: colorConfig.stroke,
        strokeWeight: 3,
        fillColor: colorConfig.fill,
        fillOpacity: 0.4,
        data: {
          street: region.street,
          risk_color: region.risk_color,
          risk_label: colorConfig.label,
          alarm_count: region.alarm_count,
          warning_count: region.warning_count,
          risk_count: region.risk_count,
          risk_level_1_count: region.risk_level_1_count,
          risk_level_2_count: region.risk_level_2_count,
          risk_level_3_count: region.risk_level_3_count,
          risk_level_4_count: region.risk_level_4_count,
          stat_date: region.stat_date,
        },
      }
    })
    .filter((region): region is NonNullable<typeof region> => region !== null)
}

/**
 * 计算属性：转换为地图多边形（响应图层控制和街道筛选变化）
 * 注意：这个计算属性返回按风险等级筛选的多边形（默认模式）
 * 组件可以通过getPolygons方法传入filterByStreet参数来获取不同筛选模式的结果
 */
const polygons = computed<MapPolygon[]>(() => {
  // 当 showRiskLevels、selectedStreets 或 regionStatusList 变化时，重新计算多边形
  // 通过访问这些ref来建立响应式依赖
  const currentShowLevels = showRiskLevels.value
  const currentRegions = regionStatusList.value
  
  // 确保 showRiskLevels 已初始化
  if (!currentShowLevels) {
    return []
  }
  
  // 默认按风险等级筛选（保持向后兼容）
  return convertToPolygons(currentRegions, false)
})

/**
 * 获取多边形（支持自定义筛选模式）
 */
const getPolygons = (filterByStreet: boolean): MapPolygon[] => {
  if (!showRiskLevels.value) {
    return []
  }
  return convertToPolygons(regionStatusList.value, filterByStreet)
}

/**
 * 加载四色图数据
 */
const loadColorMapData = async () => {
  try {
    console.log('开始加载四色图数据...')
    const data = await getColorMapData()
    
    if (!data || !Array.isArray(data)) {
      console.warn('四色图数据格式错误，返回空数组')
      regionStatusList.value = []
      return
    }
    
    regionStatusList.value = data
    console.log('四色图数据加载成功:', {
      total: data.length,
      regions: data.map(r => ({
        id: r.id,
        street: r.street,
        risk_color: r.risk_color,
        alarm_count: r.alarm_count,
        warning_count: r.warning_count,
      })),
    })
    
    // 验证数据质量
    const validRegions = data.filter(r => r.risk_color)
    if (validRegions.length === 0) {
      console.warn('警告：没有包含风险颜色的区域数据')
    } else {
      console.log(`有效区域数量：${validRegions.length}/${data.length}`)
    }
  } catch (error) {
    console.error('加载四色图数据失败:', error)
    // API失败时，清空数据并显示错误提示
    regionStatusList.value = []
    
    // 可以在这里添加错误提示，例如使用 ElMessage
    if (window.console && console.error) {
      console.error('四色图数据加载失败，请检查后端API是否正常', error)
    }
  }
}

/**
 * 获取风险统计信息
 */
const riskStatistics = computed(() => {
  const stats = {
    red: 0,
    orange: 0,
    yellow: 0,
    blue: 0,
    total: regionStatusList.value.length,
  }

  regionStatusList.value.forEach((region) => {
    if (region.risk_color) {
      stats[region.risk_color as keyof typeof stats]++
    }
  })

  return stats
})

export function useColorMapRegions() {
  return {
    regionStatusList,
    polygons,
    riskStatistics,
    loadColorMapData,
    showRiskLevels,
    selectedStreets,
    allStreets,
    getPolygons,
  }
}

