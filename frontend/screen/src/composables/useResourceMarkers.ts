/**
 * 资源标记点管理 Composable
 * 从后端API获取真实数据，不再使用模拟数据
 */
import { ref, computed } from 'vue'
import type { MapMarker } from '@/types/map'
import { getResourceList, getTargetList, getShelterList } from '@/api/modules/safety'
import type { SafetyResource, SafetyTarget, Shelter } from '@/api/modules/safety'

// 资源类型枚举
export const ResourceType = {
  TEAM: 1, // 救援队伍
  EXPERT: 2, // 应急专家
  EQUIPMENT: 3, // 物资装备
} as const

// 防护目标类型枚举
export const TargetType = {
  SCHOOL: 1, // 学校
  RESIDENTIAL: 2, // 居民区
  HOSPITAL: 3, // 医院
  MALL: 4, // 商场
  OTHER: 5, // 其他人员密集场所
} as const

// 避难场所类型枚举
export const ShelterType = {
  PARK: 1, // 公园
  SQUARE: 2, // 广场
  STADIUM: 3, // 体育场
  SCHOOL: 4, // 学校
  OTHER: 5, // 其他
} as const

// 资源图标映射（统一使用emoji图标）
const resourceIcons: Record<number, string> = {
  [ResourceType.TEAM]: '🚑', // 救援队伍
  [ResourceType.EXPERT]: '👨‍🔬', // 应急专家
  [ResourceType.EQUIPMENT]: '📦', // 物资装备
}

// 防护目标图标映射（统一使用emoji图标）
const targetIcons: Record<number, string> = {
  [TargetType.SCHOOL]: '🏫', // 学校
  [TargetType.RESIDENTIAL]: '🏘️', // 居民区
  [TargetType.HOSPITAL]: '🏥', // 医院
  [TargetType.MALL]: '🏬', // 商场
  [TargetType.OTHER]: '🏛️', // 其他
}

// 避难场所图标映射（统一使用emoji图标）
const shelterIcons: Record<number, string> = {
  [ShelterType.PARK]: '🌳', // 公园
  [ShelterType.SQUARE]: '🏛️', // 广场
  [ShelterType.STADIUM]: '🏟️', // 体育场
  [ShelterType.SCHOOL]: '🏫', // 学校
  [ShelterType.OTHER]: '🏕️', // 其他
}

// 资源颜色映射
const resourceColors: Record<number, string> = {
  [ResourceType.TEAM]: '#ff4d4f', // 红色 - 救援队伍
  [ResourceType.EXPERT]: '#1890ff', // 蓝色 - 应急专家
  [ResourceType.EQUIPMENT]: '#52c41a', // 绿色 - 物资装备
}

// 防护目标颜色映射
const targetColors: Record<number, string> = {
  [TargetType.SCHOOL]: '#faad14', // 橙色 - 学校
  [TargetType.RESIDENTIAL]: '#722ed1', // 紫色 - 居民区
  [TargetType.HOSPITAL]: '#eb2f96', // 粉色 - 医院
  [TargetType.MALL]: '#13c2c2', // 青色 - 商场
  [TargetType.OTHER]: '#fa8c16', // 橙红色 - 其他
}

// 避难场所颜色映射
const shelterColors: Record<number, string> = {
  [ShelterType.PARK]: '#52c41a', // 绿色 - 公园
  [ShelterType.SQUARE]: '#1890ff', // 蓝色 - 广场
  [ShelterType.STADIUM]: '#faad14', // 橙色 - 体育场
  [ShelterType.SCHOOL]: '#722ed1', // 紫色 - 学校
  [ShelterType.OTHER]: '#13c2c2', // 青色 - 其他
}

/**
 * 将安全资源转换为地图标记点
 */
function resourceToMarker(resource: SafetyResource): MapMarker | null {
  // 验证坐标是否存在且有效
  if (!resource.longitude || !resource.latitude) {
    console.warn(`安全资源 ${resource.resource_name} (ID: ${resource.id}) 缺少坐标信息，跳过标记`)
    return null
  }

  const lng = Number(resource.longitude)
  const lat = Number(resource.latitude)

  // 验证坐标范围（马鞍山市范围：经度 118.3-118.7，纬度 31.5-31.9）
  if (isNaN(lng) || isNaN(lat) || lng < 118 || lng > 119 || lat < 31 || lat > 32) {
    console.warn(`安全资源 ${resource.resource_name} (ID: ${resource.id}) 坐标无效 (${lng}, ${lat})，跳过标记`)
    return null
  }

  // 获取图标和颜色（确保每个资源都有图标）
  const icon = resourceIcons[resource.resource_type] || '📍'
  const color = resourceColors[resource.resource_type] || '#409eff'

  // 构建标签文本（包含子类型信息，如果有）
  let labelText = resource.resource_name
  if (resource.sub_type) {
    labelText = `${resource.resource_name} (${resource.sub_type})`
  }

  return {
    id: `resource-${resource.id}`,
    position: {
      lng: lng,
      lat: lat,
    },
    label: labelText,
    icon: icon, // 确保所有资源都有图标
    data: {
      type: 'resource',
      sub_type: resource.sub_type,
      color: color,
      ...resource,
    },
  }
}

/**
 * 将防护目标转换为地图标记点
 */
function targetToMarker(target: SafetyTarget): MapMarker | null {
  // 验证坐标是否存在且有效
  if (!target.longitude || !target.latitude) {
    console.warn(`防护目标 ${target.target_name} (ID: ${target.id}) 缺少坐标信息，跳过标记`)
    return null
  }

  const lng = Number(target.longitude)
  const lat = Number(target.latitude)

  // 验证坐标范围（马鞍山市范围：经度 118.3-118.7，纬度 31.5-31.9）
  if (isNaN(lng) || isNaN(lat) || lng < 118 || lng > 119 || lat < 31 || lat > 32) {
    console.warn(`防护目标 ${target.target_name} (ID: ${target.id}) 坐标无效 (${lng}, ${lat})，跳过标记`)
    return null
  }

  // 获取图标和颜色（确保每个目标都有图标）
  const icon = targetIcons[target.target_type] || '📍'
  const color = targetColors[target.target_type] || '#409eff'

  // 构建标签文本（包含风险等级信息，如果有）
  let labelText = target.target_name
  if (target.risk_level_display) {
    labelText = `${target.target_name} (${target.risk_level_display})`
  }

  return {
    id: `target-${target.id}`,
    position: {
      lng: lng,
      lat: lat,
    },
    label: labelText,
    icon: icon, // 确保所有目标都有图标
    data: {
      type: 'target',
      risk_level: target.risk_level,
      risk_level_display: target.risk_level_display,
      color: color,
      ...target,
    },
  }
}

/**
 * 将避难场所转换为地图标记点
 */
function shelterToMarker(shelter: Shelter): MapMarker | null {
  // 验证坐标是否存在且有效
  if (!shelter.longitude || !shelter.latitude) {
    console.warn(`避难场所 ${shelter.shelter_name} (ID: ${shelter.id}) 缺少坐标信息，跳过标记`)
    return null
  }

  const lng = Number(shelter.longitude)
  const lat = Number(shelter.latitude)

  // 验证坐标范围（马鞍山市范围：经度 118.3-118.7，纬度 31.5-31.9）
  if (isNaN(lng) || isNaN(lat) || lng < 118 || lng > 119 || lat < 31 || lat > 32) {
    console.warn(`避难场所 ${shelter.shelter_name} (ID: ${shelter.id}) 坐标无效 (${lng}, ${lat})，跳过标记`)
    return null
  }

  // 获取图标和颜色（确保每个场所都有图标）
  const icon = shelterIcons[shelter.shelter_type] || '📍'
  const color = shelterColors[shelter.shelter_type] || '#409eff'

  // 构建标签文本（包含容量信息，如果有）
  let labelText = shelter.shelter_name
  if (shelter.capacity) {
    labelText = `${shelter.shelter_name} (${shelter.capacity}人)`
  }

  return {
    id: `shelter-${shelter.id}`,
    position: {
      lng: lng,
      lat: lat,
    },
    label: labelText,
    icon: icon, // 确保所有场所都有图标
    data: {
      type: 'shelter',
      capacity: shelter.capacity,
      color: color,
      ...shelter,
    },
  }
}

/**
 * 资源标记点管理
 */
export function useResourceMarkers() {
  const resources = ref<SafetyResource[]>([])
  const targets = ref<SafetyTarget[]>([])
  const shelters = ref<Shelter[]>([])
  
  const showResources = ref(true)
  const showTargets = ref(true)
  const showShelters = ref(true)
  
  // 资源分类显示控制
  const showTeams = ref(true)
  const showExperts = ref(true)
  const showEquipment = ref(true)

  // 计算所有标记点
  const markers = computed<MapMarker[]>(() => {
    const result: MapMarker[] = []
    let resourceCount = 0
    let targetCount = 0
    let shelterCount = 0
    let skippedCount = 0

    if (showResources.value) {
      resources.value.forEach((resource) => {
        // 根据资源类型过滤
        if (resource.resource_type === ResourceType.TEAM && !showTeams.value) {
          return
        }
        if (resource.resource_type === ResourceType.EXPERT && !showExperts.value) {
          return
        }
        if (resource.resource_type === ResourceType.EQUIPMENT && !showEquipment.value) {
          return
        }
        
        const marker = resourceToMarker(resource)
        if (marker) {
          result.push(marker)
          resourceCount++
        } else {
          skippedCount++
        }
      })
    }

    if (showTargets.value) {
      targets.value.forEach((target) => {
        const marker = targetToMarker(target)
        if (marker) {
          result.push(marker)
          targetCount++
        } else {
          skippedCount++
        }
      })
    }

    if (showShelters.value) {
      shelters.value.forEach((shelter) => {
        const marker = shelterToMarker(shelter)
        if (marker) {
          result.push(marker)
          shelterCount++
        } else {
          skippedCount++
        }
      })
    }

    // 输出统计信息（仅在标记点数量变化时输出，避免频繁日志）
    if (result.length > 0 || skippedCount > 0) {
      console.log(`标记点统计: 安全资源 ${resourceCount} 个, 防护目标 ${targetCount} 个, 避难场所 ${shelterCount} 个, 总计 ${result.length} 个标记点`)
      if (skippedCount > 0) {
        console.warn(`已跳过 ${skippedCount} 个无效数据（缺少坐标或坐标无效）`)
      }
    }

    return result
  })

  // 加载资源数据
  const loadResources = async () => {
    try {
      const response = await getResourceList({ page_size: 1000, status: 1 })
      const apiResources = response.results || []
      resources.value = apiResources
      
      if (apiResources.length === 0) {
        console.warn('安全资源数据为空，请检查后端数据')
      } else {
        // 统计各类型资源数量
        const teamCount = apiResources.filter(r => r.resource_type === ResourceType.TEAM).length
        const expertCount = apiResources.filter(r => r.resource_type === ResourceType.EXPERT).length
        const equipmentCount = apiResources.filter(r => r.resource_type === ResourceType.EQUIPMENT).length
        const validCoordCount = apiResources.filter(r => r.longitude && r.latitude).length
        
        console.log(`成功加载 ${apiResources.length} 个安全资源: 救援队伍 ${teamCount} 个, 应急专家 ${expertCount} 个, 物资装备 ${equipmentCount} 个`)
        if (validCoordCount < apiResources.length) {
          console.warn(`其中 ${apiResources.length - validCoordCount} 个资源缺少坐标信息，将不会显示在地图上`)
        }
      }
    } catch (error) {
      console.error('加载安全资源失败:', error)
      // API失败时清空数据，不显示任何标记点
      resources.value = []
    }
  }

  // 加载防护目标数据
  const loadTargets = async () => {
    try {
      const response = await getTargetList({ page_size: 1000, status: 1 })
      const apiTargets = response.results || []
      targets.value = apiTargets
      
      if (apiTargets.length === 0) {
        console.warn('防护目标数据为空，请检查后端数据')
      } else {
        // 统计各类型目标数量
        const typeStats: Record<number, number> = {}
        apiTargets.forEach(target => {
          typeStats[target.target_type] = (typeStats[target.target_type] || 0) + 1
        })
        const validCoordCount = apiTargets.filter(t => t.longitude && t.latitude).length
        
        // 类型名称映射
        const targetTypeNames: Record<number, string> = {
          [TargetType.SCHOOL]: '学校',
          [TargetType.RESIDENTIAL]: '居民区',
          [TargetType.HOSPITAL]: '医院',
          [TargetType.MALL]: '商场',
          [TargetType.OTHER]: '其他',
        }
        
        const typeStr = Object.entries(typeStats)
          .map(([type, count]) => `${targetTypeNames[Number(type)] || '未知'}: ${count}`)
          .join(', ')
        console.log(`成功加载 ${apiTargets.length} 个防护目标 (${typeStr})`)
        if (validCoordCount < apiTargets.length) {
          console.warn(`其中 ${apiTargets.length - validCoordCount} 个目标缺少坐标信息，将不会显示在地图上`)
        }
      }
    } catch (error) {
      console.error('加载防护目标失败:', error)
      // API失败时清空数据，不显示任何标记点
      targets.value = []
    }
  }

  // 加载避难场所数据
  const loadShelters = async () => {
    try {
      const response = await getShelterList({ page_size: 1000, status: 1 })
      const apiShelters = response.results || []
      shelters.value = apiShelters
      
      if (apiShelters.length === 0) {
        console.warn('避难场所数据为空，请检查后端数据')
      } else {
        // 统计各类型场所数量和总容量
        const typeStats: Record<number, number> = {}
        let totalCapacity = 0
        apiShelters.forEach(shelter => {
          typeStats[shelter.shelter_type] = (typeStats[shelter.shelter_type] || 0) + 1
          if (shelter.capacity) {
            totalCapacity += shelter.capacity
          }
        })
        const validCoordCount = apiShelters.filter(s => s.longitude && s.latitude).length
        
        // 类型名称映射
        const shelterTypeNames: Record<number, string> = {
          [ShelterType.PARK]: '公园',
          [ShelterType.SQUARE]: '广场',
          [ShelterType.STADIUM]: '体育场',
          [ShelterType.SCHOOL]: '学校',
          [ShelterType.OTHER]: '其他',
        }
        
        const typeStr = Object.entries(typeStats)
          .map(([type, count]) => `${shelterTypeNames[Number(type)] || '未知'}: ${count}`)
          .join(', ')
        console.log(`成功加载 ${apiShelters.length} 个避难场所 (${typeStr}), 总容量: ${totalCapacity} 人`)
        if (validCoordCount < apiShelters.length) {
          console.warn(`其中 ${apiShelters.length - validCoordCount} 个场所缺少坐标信息，将不会显示在地图上`)
        }
      }
    } catch (error) {
      console.error('加载避难场所失败:', error)
      // API失败时清空数据，不显示任何标记点
      shelters.value = []
    }
  }

  // 加载所有数据
  const loadAll = async () => {
    await Promise.all([loadResources(), loadTargets(), loadShelters()])
  }

  return {
    resources,
    targets,
    shelters,
    showResources,
    showTargets,
    showShelters,
    showTeams,
    showExperts,
    showEquipment,
    markers,
    loadResources,
    loadTargets,
    loadShelters,
    loadAll,
  }
}

