<template>
  <ScreenLayout title="安全运行一张图" :show-home-button="true">
    <div class="safety-run-content">
      <!-- 统计面板 -->
      <StatisticsPanel @stats-updated="handleStatsUpdated" @card-click="handleStatCardClick" />
      
      <!-- 地图容器 -->
      <div class="map-wrapper">
        <!-- Cesium地图 -->
        <CesiumMap
          ref="cesiumMapRef"
          :center="mapCenter"
          :zoom="mapZoom"
          :map-style="mapStyle"
          :scene-mode="sceneMode"
          @ready="onCesiumMapReady"
          @click="handleMapClick"
          @mousemove="handleMapMouseMove"
        />
        
        <!-- 地图工具栏 -->
        <MapToolbar
          :default-center="cihuStationPosition"
          :default-zoom="12"
          :show-markers="layerSettings.showMarkers"
          :show-polygons="layerSettings.showPolygons"
          :resource-stats="resourceStats"
          @layer-change="handleLayerChange"
          @resource-category-change="handleResourceCategoryChange"
          @reset-view="handleResetView"
          @fit-bounds="handleFitBounds"
          @map-style-change="handleMapStyleChange"
          @scene-mode-change="handleSceneModeChange"
        />
        
        <!-- 鼠标悬停提示 -->
        <div
          v-if="hoverTip.visible"
          class="hover-tip"
          :style="{ left: hoverTip.x + 'px', top: hoverTip.y + 'px' }"
        >
          {{ hoverTip.text }}
        </div>
      </div>
    </div>
    
    <!-- 安全资源详情对话框 -->
    <ResourceDetailDialog
      v-model:visible="resourceDialogVisible"
      :resource-data="resourceData"
      @call="handleCall"
    />
    
    <!-- 防护目标/避难场所详情对话框 -->
    <TargetShelterDetailDialog
      v-model:visible="targetShelterDialogVisible"
      :data="targetShelterData"
    />
    
    <!-- 视频监控详情对话框 -->
    <VideoMonitorDetailDialog
      v-model:visible="videoDialogVisible"
      :monitor-data="videoData"
    />
    
    <!-- 呼叫对话框 -->
    <CallDialog
      v-model:visible="callDialogVisible"
      :phone="callPhone"
    />
    
    <!-- 重点管控区域详情对话框 -->
    <TargetDetailDialog
      v-model:visible="areaDialogVisible"
      :target-data="areaData"
    />
  </ScreenLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import ScreenLayout from '@/components/layout/ScreenLayout.vue'
import CesiumMap from '@/components/map/CesiumMap.vue'
import MapToolbar from '@/components/map/MapToolbar.vue'
import TargetDetailDialog from '@/components/map/TargetDetailDialog.vue'
import ResourceDetailDialog from '@/components/map/ResourceDetailDialog.vue'
import TargetShelterDetailDialog from '@/components/map/TargetShelterDetailDialog.vue'
import VideoMonitorDetailDialog from '@/components/map/VideoMonitorDetailDialog.vue'
import CallDialog from '@/components/map/CallDialog.vue'
import StatisticsPanel from '@/components/widgets/StatisticsPanel.vue'
import { useResourceMarkers } from '@/composables/useResourceMarkers'
import { useRefreshStrategy } from '@/composables/useRefreshStrategy'
import type { Point, MapMarker, MapPolygon } from '@/types/map'
import { createCirclePoints } from '@/utils/geometry'
import {
  addMarkers,
  addPolygons,
  clearAllEntities,
  findEntityById,
  removeEntity,
} from '@/utils/cesium-entity'

const cesiumMapRef = ref<InstanceType<typeof CesiumMap> | null>(null)
const viewer = ref<any>(null)
const isMapReady = ref(false)

// 使用资源标记点管理
const {
  markers: resourceMarkers,
  loadAll: loadAllResources,
  showTeams,
  showExperts,
  showEquipment,
  showTargets,
  showShelters,
} = useResourceMarkers()

// 慈湖站（火车站）的位置坐标
const cihuStationPosition: Point = { lng: 118.521577, lat: 31.742368 }
const mapCenter = ref<Point>({ ...cihuStationPosition })
const mapZoom = ref(12)
const mapStyle = ref<'normal' | 'satellite' | 'terrain'>('normal')
const sceneMode = ref<'2D' | '3D' | 'COLUMBUS_VIEW'>('2D')

// 图层设置
const layerSettings = reactive({
  showMarkers: true,
  showPolygons: true,
  showLabels: true,
})

// Entity 集合（用于管理标记点和多边形）
const markerEntities = ref<Map<string | number, any>>(new Map())
const polygonEntities = ref<Map<string | number, any>>(new Map())

// 创建5公里半径的圆形区域
const protectionCirclePath = createCirclePoints(cihuStationPosition, 5000, 64) // 5公里 = 5000米

// 合并所有标记点（包括资源标记点和固定标记点）
const markers = computed<MapMarker[]>(() => {
  const fixedMarkers: MapMarker[] = [
    {
      id: 'cihu-station',
      position: cihuStationPosition,
      label: '慈湖站',
      icon: '🚂', // 使用 emoji 图标，会自动转换为 SVG
      data: {
        name: '慈湖站',
        type: 'railway_station',
        color: '#FFD700', // 金色
        station: true,
      },
    },
  ]
  
  if (!layerSettings.showMarkers) {
    return []
  }
  
  return [...fixedMarkers, ...resourceMarkers.value]
})

// 多边形数据（5公里防护圆形区域）
const polygons = ref<MapPolygon[]>([
  {
    id: 'protection-circle',
    path: protectionCirclePath,
    strokeColor: 'rgba(255, 69, 0, 1)', // 更鲜明的橙红色边框
    strokeWeight: 4, // 稍粗的边框
    fillColor: 'rgba(255, 69, 0, 0.25)', // 半透明填充
    fillOpacity: 0.25,
    data: {
      name: '重点防护地区（5公里）',
      type: 'protection_area',
      radius: 5,
    },
  },
])

// 鼠标悬停提示
const hoverTip = reactive({
  visible: false,
  x: 0,
  y: 0,
  text: '',
})

// 对话框显示状态和数据
const resourceDialogVisible = ref(false)
const targetShelterDialogVisible = ref(false)
const videoDialogVisible = ref(false)
const callDialogVisible = ref(false)
const areaDialogVisible = ref(false)
const resourceData = ref<any>(null)
const targetShelterData = ref<any>(null)
const videoData = ref<any>(null)
const callPhone = ref('')
const areaData = ref<any>(null)

// 重点管控区域数据
const controlAreaInfo = {
  name: '重点管控区域',
  type: '重点管控区域',
  level: '一级重点管控',
  location: '慈湖高新区',
  address: '以慈湖站为中心，半径5公里范围内',
  radius: 5,
  contactPerson: '区域负责人：张明',
  contactPhone: '0555-1234567',
  protectionMeasures:
    '1. 建立24小时视频监控系统，覆盖全区域重点部位\n2. 设置三级管控体系：外围警戒、区域防护、重点部位守卫\n3. 配备专业管控人员30名，实行三班倒工作制\n4. 安装智能监测系统，实时监测区域内安全态势\n5. 建立应急响应机制，与当地公安、消防、医疗等部门建立联动\n6. 定期开展安全演练和应急演练，提高应急处置能力\n7. 建立区域风险评估机制，定期更新风险等级\n8. 配备应急物资储备，确保应急处置能力',
  emergencyContact: '应急指挥中心：0555-7654321\n值班负责人：李华 13800138000\n技术支持：王强 13900139000\n区域协调：赵强 13900139001',
  remark: '该区域为马鞍山市重点管控区域，涵盖重要交通枢纽、人员密集场所、危险源等重点目标。区域内日均人流量约20000人次，节假日高峰期可达50000人次。需重点关注公共安全、消防安全、反恐防暴、危险源监控等工作。区域内包含3个重大危险源、15个防护目标、6个避难场所，需建立完善的应急响应体系。',
}

// Cesium地图就绪回调
const onCesiumMapReady = (cesiumViewer: any) => {
  console.log('SafetyRun: 地图就绪回调', {
    viewer: !!cesiumViewer,
    markersCount: markers.value.length,
  })
  viewer.value = cesiumViewer
  isMapReady.value = true
  
  // 等待下一帧后渲染标记点和多边形
  nextTick(() => {
    console.log('SafetyRun: 地图就绪，开始更新标记点和多边形', {
      markersCount: markers.value.length,
      showMarkers: layerSettings.showMarkers,
      viewer: !!viewer.value,
    })
    updateMarkers()
    updatePolygons()
  })
}

// 更新标记点
const updateMarkers = () => {
  if (!viewer.value || !isMapReady.value) {
    console.warn('updateMarkers: 地图未就绪', { viewer: !!viewer.value, isMapReady: isMapReady.value })
    return
  }

  console.log('updateMarkers: 开始更新标记点', {
    markersCount: markers.value.length,
    showMarkers: layerSettings.showMarkers,
    showTeams,
    showExperts,
    showEquipment,
    showTargets,
    showShelters,
  })

  // 清除现有标记点
  markerEntities.value.forEach((entity, id) => {
    removeEntity(viewer.value, id)
  })
  markerEntities.value.clear()

  if (!layerSettings.showMarkers) {
    console.log('updateMarkers: 标记点图层已隐藏，跳过添加')
    return
  }

  // 检查是否有标记点数据
  if (!markers.value || markers.value.length === 0) {
    console.warn('updateMarkers: 没有标记点数据', { markers: markers.value })
    return
  }

  // 添加新标记点
  console.log('updateMarkers: 准备添加标记点', markers.value.map(m => ({ id: m.id, label: m.label, position: m.position })))
  const entities = addMarkers(viewer.value, markers.value)
  console.log('updateMarkers: addMarkers返回的entities', entities.map(e => ({ id: e.id, hasBillboard: !!e.billboard })))
  
  entities.forEach((entity) => {
    if (entity.id) {
      markerEntities.value.set(entity.id, entity)
      console.log('updateMarkers: 已添加Entity到Map', entity.id, entity)
    } else {
      console.warn('updateMarkers: Entity没有ID', entity)
    }
  })

  console.log(`updateMarkers: 已添加 ${entities.length} 个标记点，当前Map中有 ${markerEntities.value.size} 个Entity`)
  
  // 验证Entity是否真的在地图上
  const allEntities = viewer.value.entities.values
  console.log('updateMarkers: 地图上实际Entity数量', allEntities.length, allEntities.map((e: any) => ({ id: e.id, hasBillboard: !!e.billboard })))
}

// 更新多边形
const updatePolygons = () => {
  if (!viewer.value || !isMapReady.value) return

  // 清除现有多边形
  polygonEntities.value.forEach((entity, id) => {
    removeEntity(viewer.value, id)
  })
  polygonEntities.value.clear()

  if (!layerSettings.showPolygons) {
    return
  }

  // 添加新多边形
  const entities = addPolygons(viewer.value, polygons.value)
  entities.forEach((entity) => {
    if (entity.id) {
      polygonEntities.value.set(entity.id, entity)
    }
  })

  console.log(`已添加 ${entities.length} 个多边形`)
}

// 地图点击事件
const handleMapClick = (event: any) => {
  if (!viewer.value) return

  console.log('地图点击事件:', event)

  // CesiumMap组件已经传递了pickedObject和pickedEntity
  // 优先使用pickedEntity，如果没有则使用pickedObject.id
  let entity = null
  
  if (event.pickedEntity) {
    // 直接使用pickedEntity（这是Entity对象本身）
    entity = event.pickedEntity
    console.log('使用pickedEntity:', entity.id)
  } else if (event.pickedObject) {
    // 从pickedObject中提取Entity
    if (event.pickedObject.id) {
      entity = event.pickedObject.id
      console.log('从pickedObject.id获取Entity:', entity.id)
    } else if (event.pickedObject.primitive && event.pickedObject.primitive.id) {
      entity = event.pickedObject.primitive.id
      console.log('从pickedObject.primitive.id获取Entity:', entity.id)
    } else {
      entity = event.pickedObject
      console.log('使用pickedObject本身作为Entity:', entity.id)
    }
  }
  
  if (entity && entity.id !== undefined && entity.id !== null) {
    console.log('找到Entity，ID:', entity.id, '类型:', typeof entity.id)
    
    // 查找对应的标记点
    const marker = markers.value.find((m) => {
      // 支持多种id匹配方式
      if (m.id === entity.id) return true
      if (String(m.id) === String(entity.id)) return true
      if (typeof m.id === 'number' && typeof entity.id === 'string' && m.id === parseInt(entity.id)) return true
      if (typeof m.id === 'string' && typeof entity.id === 'number' && parseInt(m.id) === entity.id) return true
      return false
    })
    
    if (marker) {
      console.log('找到匹配的标记点:', marker.id, marker.label || marker.data?.name)
      handleMarkerClick(marker, event)
      return
    }
    
    // 查找对应的多边形
    const polygon = polygons.value.find((p) => {
      if (p.id === entity.id) return true
      if (String(p.id) === String(entity.id)) return true
      if (typeof p.id === 'number' && typeof entity.id === 'string' && p.id === parseInt(entity.id)) return true
      if (typeof p.id === 'string' && typeof entity.id === 'number' && parseInt(p.id) === entity.id) return true
      return false
    })
    
    if (polygon) {
      console.log('找到匹配的多边形:', polygon.id)
      handlePolygonClick(polygon, event)
      return
    }
    
    console.warn('找到Entity但未找到对应的标记点或多边形，ID:', entity.id)
  } else {
    console.log('未找到Entity，点击的是空白区域')
  }

  // 如果点击的是空白区域，关闭所有对话框
  resourceDialogVisible.value = false
  targetShelterDialogVisible.value = false
  videoDialogVisible.value = false
  areaDialogVisible.value = false
  
  // 如果没有点击到Entity，隐藏悬停提示
  hoverTip.visible = false
}

// 地图鼠标移动事件（用于悬停提示）
const handleMapMouseMove = (event: any) => {
  if (!viewer.value) return

  const pickedObject = event.pickedObject
  
  if (pickedObject) {
    const entity = pickedObject.id || pickedObject
    
    if (entity) {
      // 优先检查Billboard（图标），然后检查其他类型
      let tipText = ''
      
      if (entity.billboard) {
        // 标记点图标
        const marker = markers.value.find((m) => m.id === entity.id || entity.id === m.id)
        if (marker) {
          tipText = marker.label || marker.data?.name || marker.data?.resource_name || marker.data?.target_name || marker.data?.shelter_name || '未知标记点'
        }
      } else if (entity.position || entity.point) {
        // 标记点（Point类型）
        const marker = markers.value.find((m) => m.id === entity.id || entity.id === m.id)
        if (marker) {
          tipText = marker.label || marker.data?.name || marker.data?.resource_name || marker.data?.target_name || marker.data?.shelter_name || '未知标记点'
        }
      } else if (entity.id) {
        // 通过id查找标记点
        const marker = markers.value.find((m) => {
          return m.id === entity.id || 
                 String(m.id) === String(entity.id) ||
                 (typeof m.id === 'string' && typeof entity.id === 'string' && m.id === entity.id)
        })
        if (marker) {
          tipText = marker.label || marker.data?.name || marker.data?.resource_name || marker.data?.target_name || marker.data?.shelter_name || '未知标记点'
        }
      } else if (entity.polygon) {
        // 多边形
        const polygon = polygons.value.find((p) => p.id === entity.id || entity.id === p.id)
        if (polygon) {
          tipText = polygon.data?.name || '未知区域'
        }
      }

      if (tipText) {
        hoverTip.visible = true
        hoverTip.text = tipText
        // 获取鼠标位置，添加偏移避免遮挡
        if (event.event) {
          const offset = 15 // 偏移量
          hoverTip.x = event.event.clientX + offset
          hoverTip.y = event.event.clientY - offset
          
          // 确保提示框不会超出屏幕边界
          const tipWidth = 200 // 估算提示框宽度
          const tipHeight = 40 // 估算提示框高度
          const windowWidth = window.innerWidth
          const windowHeight = window.innerHeight
          
          if (hoverTip.x + tipWidth > windowWidth) {
            hoverTip.x = event.event.clientX - tipWidth - offset
          }
          if (hoverTip.y - tipHeight < 0) {
            hoverTip.y = event.event.clientY + tipHeight + offset
          }
        }
        return
      }
    }
  }

  // 如果没有悬停到Entity，隐藏悬停提示
  hoverTip.visible = false
}

// 资源统计数据（用于MapToolbar）
const resourceStats = ref({
  team_count: 0,
  expert_count: 0,
  equipment_count: 0,
  target_count: 0,
  shelter_count: 0,
})

// 处理统计数据更新（来自StatisticsPanel组件）
const handleStatsUpdated = (stats: {
  resource: any
  target: any
  shelter: any
}) => {
  // 更新resourceStats供MapToolbar使用
  resourceStats.value = {
    team_count: stats.resource.team_count || 0,
    expert_count: stats.resource.expert_count || 0,
    equipment_count: stats.resource.equipment_count || 0,
    target_count: stats.target.total_count || 0,
    shelter_count: stats.shelter.total_count || 0,
  }
}

// 处理统计卡片点击事件（用于聚焦到对应的资源类型）
const handleStatCardClick = (category: string) => {
  console.log('统计卡片点击:', category)
  
  // 根据分类筛选并聚焦到对应的标记点
  let filteredMarkers: MapMarker[] = []
  
  switch (category) {
    case 'teams':
      filteredMarkers = markers.value.filter((m) => 
        m.data?.type === 'resource' && 
        (m.data?.resource_type === 1 || m.data?.sub_type?.includes('救援队伍'))
      )
      break
    case 'experts':
      filteredMarkers = markers.value.filter((m) => 
        m.data?.type === 'resource' && 
        (m.data?.resource_type === 2 || m.data?.sub_type?.includes('专家'))
      )
      break
    case 'equipment':
      filteredMarkers = markers.value.filter((m) => 
        m.data?.type === 'resource' && 
        (m.data?.resource_type === 3 || m.data?.sub_type?.includes('装备'))
      )
      break
    case 'targets':
      filteredMarkers = markers.value.filter((m) => m.data?.type === 'target')
      break
    case 'shelters':
      filteredMarkers = markers.value.filter((m) => m.data?.type === 'shelter')
      break
  }
  
  // 如果有匹配的标记点，适应范围显示
  if (filteredMarkers.length > 0 && viewer.value) {
    const Cesium = window.Cesium
    if (Cesium) {
      // 获取所有匹配标记点的坐标
      const validMarkers = filteredMarkers.filter((m) => 
        m.position && 
        typeof m.position.lng === 'number' && 
        typeof m.position.lat === 'number'
      )
      
      if (validMarkers.length > 0) {
        const positions = validMarkers.map((m) => m.position!)
        const lngs = positions.map((p) => p.lng)
        const lats = positions.map((p) => p.lat)
        
        const minLng = Math.min(...lngs)
        const maxLng = Math.max(...lngs)
        const minLat = Math.min(...lats)
        const maxLat = Math.max(...lats)
        
        const centerLng = (minLng + maxLng) / 2
        const centerLat = (minLat + maxLat) / 2
        const lngSpan = maxLng - minLng
        const latSpan = maxLat - minLat
        const maxSpan = Math.max(lngSpan, latSpan)
        
        const earthRadius = 6378137
        const spanInMeters = maxSpan * Math.PI / 180 * earthRadius
        const height = Math.max(5000, Math.min(spanInMeters * 1.5, 100000))
        
        viewer.value.camera.flyTo({
          destination: Cesium.Cartesian3.fromDegrees(centerLng, centerLat, height),
          duration: 1.5,
        })
      }
    }
  }
}

// 处理标记点点击事件
const handleMarkerClick = (marker: MapMarker, event: any) => {
  console.log('点击了标记点:', marker)
  
  // 如果标记点有坐标，可以平滑飞行到该位置
  if (marker.position && viewer.value) {
    const Cesium = window.Cesium
    if (Cesium) {
      const currentHeight = viewer.value.camera.positionCartographic.height
      // 根据当前高度决定目标高度，如果当前高度较高，则适当降低；如果较低，则保持或略微提高
      const targetHeight = currentHeight > 50000 ? 20000 : Math.min(currentHeight * 1.2, 30000)
      
      viewer.value.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(
          marker.position.lng,
          marker.position.lat,
          targetHeight
        ),
        duration: 1.0,
      })
    }
  }
  
  const markerType = marker.data?.type
  
  if (markerType === 'resource') {
    // 安全资源：显示详情对话框（带呼叫按钮）
    resourceData.value = marker.data
    resourceDialogVisible.value = true
  } else if (markerType === 'target' || markerType === 'shelter') {
    // 防护目标或避难场所：显示详情对话框
    targetShelterData.value = marker.data
    targetShelterDialogVisible.value = true
  } else if (markerType === 'video') {
    // 视频监控：显示视频播放窗口（左侧视频，右侧详情）
    videoData.value = marker.data
    videoDialogVisible.value = true
  } else if (marker.id === 'cihu-station') {
    // 慈湖站：显示区域信息
    areaData.value = controlAreaInfo
    areaDialogVisible.value = true
  }
}

// 处理呼叫
const handleCall = (phone: string) => {
  callPhone.value = phone
  callDialogVisible.value = true
}

// 处理资源分类变化
const handleResourceCategoryChange = (data: { category: string; visible: boolean }) => {
  switch (data.category) {
    case 'teams':
      showTeams.value = data.visible
      break
    case 'experts':
      showExperts.value = data.visible
      break
    case 'equipment':
      showEquipment.value = data.visible
      break
    case 'targets':
      showTargets.value = data.visible
      break
    case 'shelters':
      showShelters.value = data.visible
      break
  }
  // 标记点会自动更新（因为使用了computed）
}

// 处理多边形点击事件
const handlePolygonClick = (polygon: MapPolygon, event: any) => {
  console.log('点击了多边形:', polygon)
  
  // 如果是重点管控区域，显示详情对话框
  if (polygon.id === 'protection-circle') {
    // 飞行到多边形中心
    if (polygon.path && polygon.path.length > 0 && viewer.value) {
      const Cesium = window.Cesium
      if (Cesium) {
        // 计算多边形的中心点（简单平均）
        const centerLng = polygon.path.reduce((sum, p) => sum + p.lng, 0) / polygon.path.length
        const centerLat = polygon.path.reduce((sum, p) => sum + p.lat, 0) / polygon.path.length
        
        // 计算多边形的范围以确定合适的高度
        const lngs = polygon.path.map((p) => p.lng)
        const lats = polygon.path.map((p) => p.lat)
        const lngSpan = Math.max(...lngs) - Math.min(...lngs)
        const latSpan = Math.max(...lats) - Math.min(...lats)
        const maxSpan = Math.max(lngSpan, latSpan)
        
        // 根据范围计算高度
        const earthRadius = 6378137
        const spanInMeters = maxSpan * Math.PI / 180 * earthRadius
        const height = Math.max(5000, Math.min(spanInMeters * 1.5, 100000))
        
        viewer.value.camera.flyTo({
          destination: Cesium.Cartesian3.fromDegrees(centerLng, centerLat, height),
          duration: 1.0,
        })
      }
    }
    
    areaData.value = controlAreaInfo
    areaDialogVisible.value = true
  }
}

// 处理图层变化
const handleLayerChange = (data: { type: string; visible: boolean }) => {
  switch (data.type) {
    case 'markers':
      layerSettings.showMarkers = data.visible
      updateMarkers()
      break
    case 'polygons':
      layerSettings.showPolygons = data.visible
      updatePolygons()
      break
    case 'labels':
      layerSettings.showLabels = data.visible
      // 更新所有Entity的标签显示状态
      if (viewer.value) {
        const allEntities = viewer.value.entities.values
        allEntities.forEach((entity: any) => {
          if (entity.label) {
            entity.label.show = data.visible
          }
        })
      }
      break
  }
}

// 处理重置视图
const handleResetView = () => {
  mapCenter.value = { ...cihuStationPosition }
  mapZoom.value = 12
  
  if (viewer.value) {
    const Cesium = window.Cesium
    if (Cesium) {
      const height = 20000 // 12级缩放对应的高度约为20000米
      viewer.value.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(
          cihuStationPosition.lng,
          cihuStationPosition.lat,
          height
        ),
        orientation: {
          heading: Cesium.Math.toRadians(0),
          pitch: Cesium.Math.toRadians(-90), // 垂直向下
          roll: 0.0,
        },
        duration: 1.0,
      })
    }
  } else if (cesiumMapRef.value) {
    cesiumMapRef.value.setCenter(cihuStationPosition)
    cesiumMapRef.value.setZoom(12)
  }
}

// 处理适应范围
const handleFitBounds = () => {
  if (!viewer.value || !cesiumMapRef.value || markers.value.length === 0) {
    console.warn('无法适应范围：地图未就绪或没有标记点')
    return
  }

  const Cesium = window.Cesium
  if (!Cesium) {
    console.error('Cesium未加载')
    return
  }

  try {
    // 获取所有标记点的坐标范围（过滤掉无效坐标）
    const validMarkers = markers.value.filter((m) => 
      m.position && 
      typeof m.position.lng === 'number' && 
      typeof m.position.lat === 'number' &&
      !isNaN(m.position.lng) && 
      !isNaN(m.position.lat)
    )

    if (validMarkers.length === 0) {
      console.warn('没有有效的标记点坐标')
      return
    }

    const positions = validMarkers.map((m) => m.position)
    const lngs = positions.map((p) => p.lng)
    const lats = positions.map((p) => p.lat)

    const minLng = Math.min(...lngs)
    const maxLng = Math.max(...lngs)
    const minLat = Math.min(...lats)
    const maxLat = Math.max(...lats)

    // 计算中心点和范围
    const centerLng = (minLng + maxLng) / 2
    const centerLat = (minLat + maxLat) / 2

    // 计算合适的相机高度
    const latSpan = maxLat - minLat
    const lngSpan = maxLng - minLng
    const maxSpan = Math.max(latSpan, lngSpan)

    // 根据范围计算合适的高度（使用更合理的算法）
    // 考虑地球曲率，使用更准确的估算
    const earthRadius = 6378137 // 地球半径（米）
    const spanInMeters = maxSpan * Math.PI / 180 * earthRadius
    
    // 根据跨度计算合适的高度，添加一些边距
    let height = spanInMeters * 1.5 // 高度约为跨度的1.5倍，确保所有标记点都在视野内
    
    // 限制高度范围，避免过高或过低
    height = Math.max(1000, Math.min(height, 50000000)) // 1000米 - 50000公里

    console.log('适应范围:', {
      markerCount: validMarkers.length,
      bounds: { minLng, maxLng, minLat, maxLat },
      center: { lng: centerLng, lat: centerLat },
      span: maxSpan,
      height,
    })

    // 使用flyTo平滑过渡到目标位置
    viewer.value.camera.flyTo({
      destination: Cesium.Cartesian3.fromDegrees(centerLng, centerLat, height),
      orientation: {
        heading: Cesium.Math.toRadians(0),
        pitch: Cesium.Math.toRadians(-90), // 垂直向下
        roll: 0.0,
      },
      duration: 1.5, // 动画时长1.5秒
    })
  } catch (error) {
    console.error('适应范围失败:', error)
  }
}

// 处理场景模式切换
const handleSceneModeChange = (mode: '2D' | '3D' | 'COLUMBUS_VIEW') => {
  sceneMode.value = mode
  console.log('切换场景模式:', mode)
  
  if (cesiumMapRef.value) {
    // 调用CesiumMap组件的方法切换场景模式
    const setSceneMode = cesiumMapRef.value.setSceneMode
    if (setSceneMode) {
      setSceneMode(mode)
    }
  }
}

// 处理地图样式切换
const handleMapStyleChange = (style: string) => {
  mapStyle.value = style as 'normal' | 'satellite' | 'terrain'
  
  if (cesiumMapRef.value) {
    cesiumMapRef.value.setMapStyle(mapStyle.value)
  }
}

// 使用刷新策略（基础数据，5分钟刷新一次）
const { startRefresh: startResourceRefresh, stopRefresh: stopResourceRefresh } = useRefreshStrategy(
  async () => {
    console.log('SafetyRun: 定时刷新资源数据')
    await loadAllResources()
    if (isMapReady.value) {
      updateMarkers()
    }
  },
  {
    interval: 300000, // 5分钟 = 300000毫秒（基础数据变化较慢）
    immediate: true,
    retry: {
      maxRetries: 3,
      retryDelay: 2000,
      exponentialBackoff: true,
    },
    enableVisibilityCheck: true,
  }
)

// 监听标记点变化
watch(
  () => markers.value,
  () => {
    if (isMapReady.value) {
      updateMarkers()
    }
  },
  { deep: true }
)

// 监听多边形变化
watch(
  () => polygons.value,
  () => {
    if (isMapReady.value) {
      updatePolygons()
    }
  },
  { deep: true }
)

// 加载资源数据
onMounted(async () => {
  console.log('SafetyRun: onMounted, 开始加载资源数据')
  try {
    await loadAllResources()
    console.log('SafetyRun: 资源数据加载完成', {
      markersCount: markers.value.length,
      isMapReady: isMapReady.value,
    })
    // 如果地图已经就绪，立即更新标记点
    if (isMapReady.value) {
      console.log('SafetyRun: 地图已就绪，立即更新标记点')
      updateMarkers()
    } else {
      console.log('SafetyRun: 地图未就绪，等待地图就绪后自动更新')
    }
  } catch (error) {
    console.error('SafetyRun: 加载资源数据失败', error)
  }
  
  // StatisticsPanel组件会自动加载统计数据，并通过事件传递给父组件
  
  // 启动定时刷新
  startResourceRefresh()
})

onUnmounted(() => {
  stopResourceRefresh()
  
  // 清理所有Entity
  if (viewer.value) {
    clearAllEntities(viewer.value)
    markerEntities.value.clear()
    polygonEntities.value.clear()
  }
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;

.safety-run-content {
  width: 100%;
  height: 100%;
  padding: 0;
  position: relative;
  overflow: hidden;
}

.map-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.hover-tip {
  position: absolute;
  padding: 8px 16px;
  background: rgba(0, 102, 255, 0.9);
  color: #fff;
  border-radius: 4px;
  font-size: 14px;
  pointer-events: none;
  z-index: 2000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  white-space: nowrap;
  border: 1px solid rgba(255, 255, 255, 0.3);

  &::before {
    content: '';
    position: absolute;
    left: -6px;
    top: 50%;
    transform: translateY(-50%);
    border: 6px solid transparent;
    border-right-color: rgba(0, 102, 255, 0.9);
  }
}
</style>
