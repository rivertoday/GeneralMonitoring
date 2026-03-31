<template>
  <ScreenLayout title="监测预警一张图" :show-home-button="true">
    <div class="monitor-warn-content">
      <!-- 实时监测数据面板 -->
      <MonitorDataPanel :warning-statistics="warningStatistics" />
      
      <!-- 报警记录/预警事件列表（Tab切换） -->
      <div class="list-panel">
        <div class="panel-tabs">
          <button
            class="tab-btn"
            :class="{ active: listTab === 'alarm' }"
            @click="listTab = 'alarm'"
          >
            报警记录
          </button>
          <button
            class="tab-btn"
            :class="{ active: listTab === 'warning' }"
            @click="listTab = 'warning'"
          >
            预警事件
          </button>
        </div>
        <div class="panel-content">
          <!-- 报警记录列表 -->
          <AlarmRecordList
            v-show="listTab === 'alarm'"
            :records="alarmRecordList"
            @record-click="handleRecordClick"
          />
          <!-- 预警事件列表 -->
          <WarningEventList
            v-show="listTab === 'warning'"
            :events="warningEventList"
            @event-click="handleEventClick"
          />
        </div>
      </div>
      
      <!-- 地图容器 -->
      <div class="map-wrapper">
        <!-- Cesium地图 -->
        <CesiumMap
          ref="cesiumMapRef"
          :center="mapCenter"
          :zoom="mapZoom"
          :map-style="mapStyle"
          :scene-mode="'2D'"
          @ready="onCesiumMapReady"
          @click="handleMapClick"
          @mousemove="handleMapMouseMove"
        />
        
        <!-- 鼠标悬停提示 -->
        <div
          v-if="hoverTip.visible"
          class="hover-tip"
          :style="{ left: hoverTip.x + 'px', top: hoverTip.y + 'px' }"
        >
          {{ hoverTip.text }}
        </div>
        
        <!-- 图层控制和地图样式面板 -->
        <div class="layer-control-panel">
          <div class="panel-tabs">
            <button
              class="panel-tab-btn"
              :class="{ active: controlTab === 'layer' }"
              @click="controlTab = 'layer'"
            >
              图层控制
            </button>
            <button
              class="panel-tab-btn"
              :class="{ active: controlTab === 'style' }"
              @click="controlTab = 'style'"
            >
              地图样式
            </button>
          </div>
          <div class="panel-content">
            <!-- 图层控制 -->
            <div v-show="controlTab === 'layer'" class="layer-control-content">
              <label class="layer-control-item">
                <input
                  type="checkbox"
                  v-model="layerSettings.showAlarms"
                  @change="updateMarkers"
                />
                <span class="layer-control-label">
                  <span class="layer-icon">🔴</span>
                  报警记录 ({{ alarmMarkers.length }})
                </span>
              </label>
              <label class="layer-control-item">
                <input
                  type="checkbox"
                  v-model="layerSettings.showWarnings"
                  @change="updateMarkers"
                />
                <span class="layer-control-label">
                  <span class="layer-icon">⚠️</span>
                  预警事件 ({{ warningMarkers.length }})
                </span>
              </label>
              <label class="layer-control-item">
                <input
                  type="checkbox"
                  v-model="layerSettings.showVideos"
                  @change="updateMarkers"
                />
                <span class="layer-control-label">
                  <span class="layer-icon">📹</span>
                  视频监控 ({{ videoMarkers.length }})
                </span>
              </label>
            </div>
            <!-- 地图样式 -->
            <div v-show="controlTab === 'style'" class="map-style-content">
              <label class="style-control-item">
                <input
                  type="radio"
                  name="mapStyle"
                  value="normal"
                  v-model="mapStyle"
                />
                <span class="style-control-label">
                  <span class="style-icon">🗺️</span>
                  标准地图
                </span>
              </label>
              <label class="style-control-item">
                <input
                  type="radio"
                  name="mapStyle"
                  value="satellite"
                  v-model="mapStyle"
                />
                <span class="style-control-label">
                  <span class="style-icon">🛰️</span>
                  卫星地图
                </span>
              </label>
              <label class="style-control-item">
                <input
                  type="radio"
                  name="mapStyle"
                  value="terrain"
                  v-model="mapStyle"
                />
                <span class="style-control-label">
                  <span class="style-icon">⛰️</span>
                  地形地图
                </span>
              </label>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 报警记录详情对话框 -->
    <AlarmRecordDetailDialog
      v-model:visible="alarmDialogVisible"
      :record-data="selectedRecord"
    />
    
    <!-- 预警事件详情对话框 -->
    <WarningEventDetailDialog
      v-model:visible="warningDialogVisible"
      :event-data="selectedEvent"
    />
    
    <!-- 视频监控详情对话框 -->
    <VideoMonitorDetailDialog
      v-model:visible="videoDialogVisible"
      :monitor-data="selectedMonitor"
    />
    <!-- 调试信息 -->
    <div v-if="false" style="position: fixed; top: 10px; left: 10px; background: rgba(0,0,0,0.8); color: white; padding: 10px; z-index: 9999; font-size: 12px;">
      <div>视频对话框状态: {{ videoDialogVisible }}</div>
      <div>选中监控: {{ selectedMonitor?.monitor_name ?? 'null' }}</div>
      <div>视频标记点数量: {{ videoMarkers.length }}</div>
      <div>所有标记点数量: {{ markers.length }}</div>
    </div>
  </ScreenLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import ScreenLayout from '@/components/layout/ScreenLayout.vue'
import CesiumMap from '@/components/map/CesiumMap.vue'
import MonitorDataPanel from '@/components/widgets/MonitorDataPanel.vue'
import AlarmRecordList from '@/components/widgets/AlarmRecordList.vue'
import WarningEventList from '@/components/widgets/WarningEventList.vue'
import AlarmRecordDetailDialog from '@/components/map/AlarmRecordDetailDialog.vue'
import WarningEventDetailDialog from '@/components/map/WarningEventDetailDialog.vue'
import VideoMonitorDetailDialog from '@/components/map/VideoMonitorDetailDialog.vue'
import { useRefreshStrategy } from '@/composables/useRefreshStrategy'
import { useAlarmMarkers } from '@/composables/useAlarmMarkers'
import { useWarningMarkers } from '@/composables/useWarningMarkers'
import { useVideoMonitors } from '@/composables/useVideoMonitors'
import type { Point, MapMarker } from '@/types/map'
import type { AlarmRecord } from '@/api/modules/risk'
import type { WarningEvent } from '@/api/modules/safety'
import type { VideoMonitor } from '@/api/modules/safety'
import {
  addMarkers,
  clearAllEntities,
  removeEntity,
} from '@/utils/cesium-entity'

const cesiumMapRef = ref<InstanceType<typeof CesiumMap> | null>(null)
const viewer = ref<any>(null)
const isMapReady = ref(false)

// Tab切换：alarm（报警记录）或 warning（预警事件）
const listTab = ref<'alarm' | 'warning'>('alarm')

// 控制面板Tab切换：layer（图层控制）或 style（地图样式）
const controlTab = ref<'layer' | 'style'>('layer')

// 使用报警记录标记点管理
const {
  alarmRecordList,
  markers: alarmMarkers,
  loadAlarmRecords,
} = useAlarmMarkers()

// 使用预警事件标记点管理
const {
  warningEventList,
  markers: warningMarkers,
  warningStatistics,
  loadWarningEvents,
} = useWarningMarkers()

// 使用视频监控标记点管理
const {
  markers: videoMarkers,
  loadAllMonitors,
  loadNearbyMonitors,
} = useVideoMonitors()

// 地图中心点（马鞍山市中心）
const mapCenter = ref<Point>({ lng: 118.521577, lat: 31.742368 })
const mapZoom = ref(12)
const mapStyle = ref<'normal' | 'satellite' | 'terrain'>('normal')

// 图层设置
const layerSettings = reactive({
  showMarkers: true,
  showLabels: true,
  showAlarms: true, // 显示报警记录
  showWarnings: true, // 显示预警事件
  showVideos: true, // 显示视频监控
})

// Entity 集合（用于管理标记点）
const markerEntities = ref<Map<string | number, any>>(new Map())

// 合并所有标记点（报警记录 + 预警事件 + 视频监控）
const markers = computed<MapMarker[]>(() => {
  if (!layerSettings.showMarkers) {
    return []
  }
  const result: MapMarker[] = []
  
  // 根据图层设置决定是否包含各类标记点
  if (layerSettings.showAlarms) {
    result.push(...alarmMarkers.value)
  }
  if (layerSettings.showWarnings) {
    result.push(...warningMarkers.value)
  }
  if (layerSettings.showVideos) {
    result.push(...videoMarkers.value)
  }
  
  return result
})

// 鼠标悬停提示
const hoverTip = reactive({
  visible: false,
  x: 0,
  y: 0,
  text: '',
})

// 对话框显示状态和数据
const alarmDialogVisible = ref(false)
const selectedRecord = ref<AlarmRecord | null>(null)

const warningDialogVisible = ref(false)
const selectedEvent = ref<WarningEvent | null>(null)

const videoDialogVisible = ref(false)
const selectedMonitor = ref<VideoMonitor | null>(null)

// Cesium地图就绪回调
const onCesiumMapReady = (cesiumViewer: any) => {
  viewer.value = cesiumViewer
  isMapReady.value = true
  console.log('Cesium 地图初始化完成', cesiumViewer)
  
  // 等待下一帧后渲染标记点
  nextTick(() => {
    updateMarkers()
  })
}

// 更新标记点
const updateMarkers = () => {
  if (!viewer.value || !isMapReady.value) return

  // 清除现有标记点
  markerEntities.value.forEach((entity, id) => {
    removeEntity(viewer.value, id)
  })
  markerEntities.value.clear()

  if (!layerSettings.showMarkers) {
    return
  }

  // 添加新标记点
  const entities = addMarkers(viewer.value, markers.value)
  entities.forEach((entity) => {
    if (entity.id) {
      markerEntities.value.set(entity.id, entity)
    }
  })

  console.log(`已添加 ${entities.length} 个标记点（报警: ${alarmMarkers.value.length}, 预警: ${warningMarkers.value.length}, 视频: ${videoMarkers.value.length}）`)
}

// 地图点击事件
const handleMapClick = (event: any) => {
  if (!viewer.value) return

  console.log('地图点击事件:', event)
  
  // CesiumMap组件传递了pickedObject和pickedEntity
  // 优先使用pickedEntity（直接是Entity对象），如果没有则使用pickedObject.id
  let entity = event.pickedEntity
  
  if (!entity && event.pickedObject) {
    // 如果pickedObject有id属性，使用它
    if (event.pickedObject.id) {
      entity = event.pickedObject.id
    } else if (event.pickedObject.primitive && event.pickedObject.primitive.id) {
      entity = event.pickedObject.primitive.id
    }
  }
  
  if (entity) {
    console.log('点击到的Entity:', {
      id: entity.id,
      hasPosition: !!entity.position,
      hasBillboard: !!entity.billboard,
      hasPoint: !!entity.point,
      hasLabel: !!entity.label,
      properties: entity.properties,
    })

    // 检查是否是标记点（Billboard、Point、Label 或 Position）
    if (entity.billboard || entity.point || entity.label || entity.position) {
      // 尝试通过 Entity ID 匹配
      let marker = markers.value.find((m) => {
        const markerId = String(m.id)
        const entityId = String(entity.id)
        return markerId === entityId
      })
      
      // 如果通过 ID 找不到，尝试通过 properties 中的 markerId 匹配
      if (!marker && entity.properties) {
        const markerId = entity.properties.markerId
        if (markerId !== undefined) {
          marker = markers.value.find((m) => {
            const mId = String(m.id)
            const pId = String(markerId)
            return mId === pId
          })
        }
      }
      
      if (marker) {
        console.log('找到匹配的标记点:', marker)
        handleMarkerClick(marker, event)
        return
      } else {
        console.warn('未找到匹配的标记点', {
          entityId: entity.id,
          entityProperties: entity.properties,
          allMarkerIds: markers.value.map(m => m.id),
        })
      }
    }
  } else {
    console.log('未点击到Entity')
  }

  // 如果没有点击到Entity，隐藏悬停提示
  hoverTip.visible = false
}

// 地图鼠标移动事件（用于悬停提示）
const handleMapMouseMove = (event: any) => {
  if (!viewer.value) return

  // 优先使用pickedEntity，如果没有则使用pickedObject.id
  let entity = event.pickedEntity
  
  if (!entity && event.pickedObject) {
    if (event.pickedObject.id) {
      entity = event.pickedObject.id
    } else if (event.pickedObject.primitive && event.pickedObject.primitive.id) {
      entity = event.pickedObject.primitive.id
    }
  }
  
  if (entity) {
    // 检查是否是标记点
    if (entity.billboard || entity.point || entity.label || entity.position) {
      // 尝试通过 Entity ID 匹配
      let marker = markers.value.find((m) => {
        const markerId = String(m.id)
        const entityId = String(entity.id)
        return markerId === entityId
      })
      
      // 如果通过 ID 找不到，尝试通过 properties 中的 markerId 匹配
      if (!marker && entity.properties) {
        const markerId = entity.properties.markerId
        if (markerId !== undefined) {
          marker = markers.value.find((m) => {
            const mId = String(m.id)
            const pId = String(markerId)
            return mId === pId
          })
        }
      }
      
      if (marker) {
        let tipText = marker.label || '未知标记点'
        
        if (marker.data?.type === 'alarm') {
          tipText = `${marker.label || '报警记录'} - ${marker.data.alarm_status_display || ''}`
        } else if (marker.data?.type === 'warning') {
          tipText = `${marker.label || '预警事件'} - ${marker.data.warning_level_display || marker.data.warning_status_display || ''}`
        } else if (marker.data?.type === 'video') {
          tipText = `${marker.label || '视频监控'} - ${marker.data.online_status_display || ''}`
        }

        hoverTip.visible = true
        hoverTip.text = tipText
        // 获取鼠标位置
        if (event.event) {
          hoverTip.x = event.event.clientX + 10
          hoverTip.y = event.event.clientY - 10
        }
        return
      }
    }
  }

  // 如果没有悬停到Entity，隐藏悬停提示
  hoverTip.visible = false
}

// 处理标记点点击事件
const handleMarkerClick = (marker: MapMarker, event: any) => {
  console.log('点击了标记点:', marker)
  console.log('标记点数据类型:', marker.data?.type)
  
  if (marker.data) {
    if (marker.data.type === 'alarm') {
      // 报警记录
      console.log('打开报警记录详情对话框')
      selectedRecord.value = marker.data as AlarmRecord
      alarmDialogVisible.value = true
      
      // 如果报警记录有坐标，定位到该位置
      if (marker.data.longitude && marker.data.latitude && cesiumMapRef.value) {
        cesiumMapRef.value.setCenter({
          lng: Number(marker.data.longitude),
          lat: Number(marker.data.latitude),
        })
        cesiumMapRef.value.setZoom(15)
      }
    } else if (marker.data.type === 'warning') {
      // 预警事件
      console.log('打开预警事件详情对话框')
      selectedEvent.value = marker.data as WarningEvent
      warningDialogVisible.value = true
      
      // 加载附近的视频监控设施
      if (marker.data.longitude && marker.data.latitude) {
        loadNearbyMonitors(
          Number(marker.data.longitude),
          Number(marker.data.latitude),
          5000 // 5公里范围
        )
      }
    } else if (marker.data.type === 'video') {
      // 视频监控
      console.log('打开视频监控详情对话框', marker.data)
      selectedMonitor.value = marker.data as VideoMonitor
      videoDialogVisible.value = true
      console.log('视频对话框状态:', videoDialogVisible.value, '监控数据:', selectedMonitor.value)
    } else {
      console.warn('未知的标记点类型:', marker.data.type)
    }
  } else {
    console.warn('标记点没有data属性:', marker)
  }
}

// 处理报警记录列表点击事件
const handleRecordClick = (record: AlarmRecord) => {
  selectedRecord.value = record
  alarmDialogVisible.value = true
  
  // 如果报警记录有坐标，定位到该位置
  if (record.longitude && record.latitude && cesiumMapRef.value) {
    cesiumMapRef.value.setCenter({
      lng: Number(record.longitude),
      lat: Number(record.latitude),
    })
    cesiumMapRef.value.setZoom(15)
  }
}

// 处理预警事件列表点击事件
const handleEventClick = (event: WarningEvent) => {
  selectedEvent.value = event
  warningDialogVisible.value = true
  
  // 如果事件有坐标，定位到该位置
  if (event.longitude && event.latitude && cesiumMapRef.value) {
    cesiumMapRef.value.setCenter({
      lng: Number(event.longitude),
      lat: Number(event.latitude),
    })
    cesiumMapRef.value.setZoom(15)
    
    // 加载附近的视频监控设施
    loadNearbyMonitors(
      Number(event.longitude),
      Number(event.latitude),
      5000 // 5公里范围
    )
  }
}

// 使用刷新策略（实时数据，30秒刷新一次）
const { startRefresh: startDataRefresh, stopRefresh: stopDataRefresh } = useRefreshStrategy(
  async () => {
    await Promise.all([
      loadAlarmRecords(),
      loadWarningEvents(),
      loadAllMonitors(),
    ])
  },
  {
    interval: 30000, // 30秒 = 30000毫秒（监测数据和预警事件需要实时更新）
    immediate: true,
    retry: {
      maxRetries: 3,
      retryDelay: 1000,
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

onMounted(() => {
  // 启动定时刷新（会在immediate=true时立即执行一次）
  startDataRefresh()
})

onUnmounted(() => {
  stopDataRefresh()
  
  // 清理所有Entity
  if (viewer.value) {
    clearAllEntities(viewer.value)
    markerEntities.value.clear()
  }
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;

.monitor-warn-content {
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

.list-panel {
  position: absolute;
  top: 2vh;
  right: 2vw;
  width: 18.7vw;
  min-width: 267px;
  max-width: 333px;
  z-index: 1000;
  background: rgba(0, 20, 40, 0.85);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  max-height: 85vh;
  display: flex;
  flex-direction: column;
}

.panel-tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid rgba(64, 158, 255, 0.2);
  padding: 0 16px;
}

.tab-btn {
  flex: 1;
  padding: 12px 16px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: #e0e0e0;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;

  &:hover {
    color: #409eff;
    background: rgba(64, 158, 255, 0.1);
  }

  &.active {
    color: #409eff;
    border-bottom-color: #409eff;
    font-weight: 600;
  }
}

.panel-content {
  flex: 1;
  overflow: hidden;
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

.layer-control-panel {
  position: absolute;
  bottom: 2vh;
  right: 2vw;
  width: 200px;
  background: rgba(0, 20, 40, 0.85);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: 8px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  max-height: 300px;
}

.layer-control-panel .panel-tabs {
  display: flex;
  gap: 0;
  border-bottom: 1px solid rgba(64, 158, 255, 0.2);
  padding: 0 8px;
  margin-bottom: 8px;
}

.layer-control-panel .panel-tab-btn {
  flex: 1;
  padding: 8px 12px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: #e0e0e0;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  text-align: center;

  &:hover {
    color: #409eff;
    background: rgba(64, 158, 255, 0.1);
  }

  &.active {
    color: #409eff;
    border-bottom-color: #409eff;
    font-weight: 600;
  }
}

.layer-control-panel .panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 0 4px;
}

.layer-control-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.map-style-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.layer-control-item,
.style-control-item {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 6px;
  border-radius: 4px;
  transition: background 0.3s;

  &:hover {
    background: rgba(64, 158, 255, 0.1);
  }

  input[type="checkbox"],
  input[type="radio"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
    accent-color: #409eff;
  }
}

.layer-control-label,
.style-control-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #e0e0e0;
  user-select: none;
}

.layer-icon,
.style-icon {
  font-size: 16px;
}
</style>
