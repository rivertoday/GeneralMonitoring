<template>
  <ScreenLayout title="安全态势一张图" :show-home-button="true">
    <div class="safety-status-content">
      <!-- 行业态势面板 -->
      <IndustryStatusPanel />
      
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
        
        <!-- 区域筛选和地图样式控制面板（Tab页模式） -->
        <div class="control-panel">
          <div class="panel-tabs">
            <button
              class="tab-btn"
              :class="{ active: filterMode === 'risk_level' }"
              @click="filterMode = 'risk_level'"
            >
              风险等级
            </button>
            <button
              class="tab-btn"
              :class="{ active: filterMode === 'street' }"
              @click="filterMode = 'street'"
            >
              街道筛选
            </button>
            <button
              class="tab-btn"
              :class="{ active: filterMode === 'map_style' }"
              @click="filterMode = 'map_style'"
            >
              地图样式
            </button>
          </div>
          
          <!-- 风险等级筛选面板 -->
          <div v-show="filterMode === 'risk_level'" class="panel-content">
            <div class="legend-items">
              <label class="legend-item">
                <input
                  v-model="showRiskLevels.red"
                  type="checkbox"
                  @change="handleRiskLevelChange"
                />
                <div class="legend-color red"></div>
                <span class="legend-label">红色I级</span>
              </label>
              <label class="legend-item">
                <input
                  v-model="showRiskLevels.orange"
                  type="checkbox"
                  @change="handleRiskLevelChange"
                />
                <div class="legend-color orange"></div>
                <span class="legend-label">橙色Ⅱ级</span>
              </label>
              <label class="legend-item">
                <input
                  v-model="showRiskLevels.yellow"
                  type="checkbox"
                  @change="handleRiskLevelChange"
                />
                <div class="legend-color yellow"></div>
                <span class="legend-label">黄色Ⅲ级</span>
              </label>
              <label class="legend-item">
                <input
                  v-model="showRiskLevels.blue"
                  type="checkbox"
                  @change="handleRiskLevelChange"
                />
                <div class="legend-color blue"></div>
                <span class="legend-label">蓝色Ⅳ级</span>
              </label>
            </div>
          </div>
          
          <!-- 街道筛选面板 -->
          <div v-show="filterMode === 'street'" class="panel-content">
            <div class="filter-actions">
              <button
                class="action-btn"
                @click="selectAllStreets"
              >
                全部
              </button>
              <button
                class="action-btn"
                @click="clearStreetFilter"
              >
                清除
              </button>
            </div>
            <div class="street-checkboxes">
              <label
                v-for="street in allStreets"
                :key="street"
                class="street-checkbox-item"
              >
                <input
                  type="checkbox"
                  :value="street"
                  v-model="selectedStreets"
                  @change="handleStreetFilterChange"
                />
                <span class="street-label">{{ street }}</span>
              </label>
            </div>
          </div>
          
          <!-- 地图样式选择面板 -->
          <div v-show="filterMode === 'map_style'" class="panel-content">
            <div class="style-buttons">
              <button
                class="style-btn"
                :class="{ active: mapStyle === 'normal' }"
                @click="changeMapStyle('normal')"
              >
                <span class="style-icon">🗺️</span>
                <span class="style-label">标准</span>
              </button>
              <button
                class="style-btn"
                :class="{ active: mapStyle === 'satellite' }"
                @click="changeMapStyle('satellite')"
              >
                <span class="style-icon">🛰️</span>
                <span class="style-label">卫星</span>
              </button>
              <button
                class="style-btn"
                :class="{ active: mapStyle === 'terrain' }"
                @click="changeMapStyle('terrain')"
              >
                <span class="style-icon">⛰️</span>
                <span class="style-label">地形</span>
              </button>
            </div>
          </div>
        </div>
        
        <!-- 区域态势对比图表 -->
        <div class="region-chart-wrapper">
          <RegionComparisonChart />
        </div>
        
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
    
    <!-- 区域详情对话框 -->
    <RegionDetailDialog
      v-model:visible="dialogVisible"
      :region-data="selectedRegion"
    />
  </ScreenLayout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import ScreenLayout from '@/components/layout/ScreenLayout.vue'
import CesiumMap from '@/components/map/CesiumMap.vue'
import RegionDetailDialog from '@/components/map/RegionDetailDialog.vue'
import { useRefreshStrategy } from '@/composables/useRefreshStrategy'
import IndustryStatusPanel from '@/components/widgets/IndustryStatusPanel.vue'
import RegionComparisonChart from '@/components/charts/RegionComparisonChart.vue'
import { useColorMapRegions } from '@/composables/useColorMapRegions'
import type { Point, MapPolygon } from '@/types/map'
import {
  addPolygons,
  clearAllEntities,
  removeEntity,
} from '@/utils/cesium-entity'

const cesiumMapRef = ref<InstanceType<typeof CesiumMap> | null>(null)
const viewer = ref<any>(null)
const isMapReady = ref(false)

// 使用四色风险图管理
const colorMapRegions = useColorMapRegions()
const {
  regionStatusList,
  polygons: allPolygons,
  riskStatistics,
  loadColorMapData,
  showRiskLevels,
  selectedStreets,
  allStreets,
  getPolygons,
} = colorMapRegions

// 根据筛选模式计算显示的多边形
const riskPolygons = computed(() => {
  // 根据filterMode决定筛选方式
  if (filterMode.value === 'street') {
    // 街道筛选模式
    return getPolygons(true)
  } else {
    // 风险等级筛选模式
    return getPolygons(false)
  }
})

// 确保 showRiskLevels 已初始化（添加安全检查，防止未定义错误）
if (!showRiskLevels) {
  console.error('showRiskLevels 未从 composable 中正确获取')
}

// 地图中心点（马鞍山市中心）
const mapCenter = ref<Point>({ lng: 118.521577, lat: 31.742368 })
const mapZoom = ref(11)
const mapStyle = ref<'normal' | 'satellite' | 'terrain'>('normal')

// 筛选模式：risk_level（风险等级）、street（街道）或 map_style（地图样式）
const filterMode = ref<'risk_level' | 'street' | 'map_style'>('risk_level')

// 图层设置
const layerSettings = reactive({
  showPolygons: true,
  showLabels: true,
})

// Entity 集合（用于管理多边形）
const polygonEntities = ref<Map<string | number, any>>(new Map())

// 鼠标悬停提示
const hoverTip = reactive({
  visible: false,
  x: 0,
  y: 0,
  text: '',
})

// 对话框显示状态和区域数据
const dialogVisible = ref(false)
const selectedRegion = ref<any>(null)

// Cesium地图就绪回调
const onCesiumMapReady = (cesiumViewer: any) => {
  viewer.value = cesiumViewer
  isMapReady.value = true
  console.log('Cesium 地图初始化完成', cesiumViewer)
  
  // 等待下一帧后渲染多边形
  nextTick(() => {
    updatePolygons()
  })
}

// 更新多边形图层（使用防抖和延迟更新，避免 Worker 序列化错误）
let updatePolygonsTimer: ReturnType<typeof setTimeout> | null = null
let isUpdating = false // 防止并发更新
const updatePolygons = () => {
  if (!viewer.value || !isMapReady.value || isUpdating) {
    return
  }

  // 清除之前的定时器
  if (updatePolygonsTimer) {
    clearTimeout(updatePolygonsTimer)
    updatePolygonsTimer = null
  }

  // 使用防抖，延迟执行更新，确保之前的操作完成
  updatePolygonsTimer = setTimeout(() => {
    if (isUpdating) {
      return // 如果正在更新，跳过
    }
    
    isUpdating = true // 标记正在更新
    
    try {
      // 安全地清除现有多边形
      // 先收集所有需要删除的ID，避免在遍历时修改Map
      const entityIdsToRemove: (string | number)[] = []
      polygonEntities.value.forEach((entity, id) => {
        entityIdsToRemove.push(id)
      })
      
      // 逐个删除Entity，确保完全清理
      entityIdsToRemove.forEach((id) => {
        try {
          removeEntity(viewer.value, id)
        } catch (error) {
          console.warn(`删除Entity ${id} 时出错:`, error)
        }
      })
      
      // 清空Map
      polygonEntities.value.clear()
      
      // 等待两帧，确保Entity完全清理，避免 Worker 序列化错误
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          try {
            if (!layerSettings.showPolygons || !viewer.value || !isMapReady.value) {
              isUpdating = false
              return
            }

            // 验证 riskPolygons 数据是否有效
            if (!riskPolygons.value || !Array.isArray(riskPolygons.value)) {
              console.warn('riskPolygons 数据无效')
              isUpdating = false
              return
            }

            // 添加新多边形
            const entities = addPolygons(viewer.value, riskPolygons.value)
            entities.forEach((entity) => {
              if (entity && entity.id) {
                polygonEntities.value.set(entity.id, entity)
              }
            })

            console.log(`已添加 ${entities.length} 个风险区域多边形`)
          } catch (error) {
            console.error('添加多边形时出错:', error)
            // 如果添加失败，确保状态被重置
          } finally {
            isUpdating = false
          }
        })
      })
    } catch (error) {
      console.error('更新多边形时出错:', error)
      isUpdating = false
    } finally {
      updatePolygonsTimer = null
    }
  }, 150) // 增加防抖延迟到 150ms，确保之前的操作完全完成
}

// 风险等级优先级（数字越小优先级越高）
const RISK_LEVEL_PRIORITY: Record<string, number> = {
  red: 1,    // 红色I级 - 最高优先级
  orange: 2, // 橙色Ⅱ级
  yellow: 3, // 黄色Ⅲ级
  blue: 4,   // 蓝色Ⅳ级 - 最低优先级
}

// 地图点击事件
const handleMapClick = (event: any) => {
  if (!viewer.value) return

  // 获取点击位置（CesiumMap组件传递的event对象包含event字段）
  const mouseEvent = event.event || event
  const clickPosition = mouseEvent && mouseEvent.clientX !== undefined
    ? new window.Cesium.Cartesian2(mouseEvent.clientX, mouseEvent.clientY)
    : null

  // 使用drillPick获取所有被点击的Entity（包括重叠的多边形）
  let pickedPolygons: Array<{ polygon: MapPolygon; entity: any; priority: number }> = []
  
  // 首先检查CesiumMap组件传递的pickedEntity
  if (event.pickedEntity && event.pickedEntity.polygon) {
    const entity = event.pickedEntity
    const polygon = riskPolygons.value.find((p) => {
      if (p.id === entity.id) return true
      if (String(p.id) === String(entity.id)) return true
      return false
    })
    
    if (polygon && polygon.data && polygon.data.risk_color) {
      const riskColor = polygon.data.risk_color as string
      const priority = RISK_LEVEL_PRIORITY[riskColor] || 999
      
      pickedPolygons.push({
        polygon,
        entity,
        priority,
      })
    }
  }
  
  // 如果clickPosition存在，使用drillPick获取所有被点击的Entity（包括重叠的多边形）
  if (clickPosition && viewer.value.scene) {
    const pickedObjects = viewer.value.scene.drillPick(clickPosition)
    
    if (pickedObjects && pickedObjects.length > 0) {
      // 查找所有多边形Entity
      pickedObjects.forEach((pickedObj: any) => {
        const entity = pickedObj.id || (pickedObj.primitive && pickedObj.primitive.id) || null
        
        if (entity && entity.polygon) {
          // 检查是否已经添加过
          const existing = pickedPolygons.find(p => p.polygon.id === entity.id)
          if (existing) return
          
          const polygon = riskPolygons.value.find((p) => {
            // 支持多种ID匹配方式
            if (p.id === entity.id) return true
            if (String(p.id) === String(entity.id)) return true
            return false
          })
          
          if (polygon && polygon.data && polygon.data.risk_color) {
            const riskColor = polygon.data.risk_color as string
            const priority = RISK_LEVEL_PRIORITY[riskColor] || 999
            
            pickedPolygons.push({
              polygon,
              entity,
              priority,
            })
          }
        }
      })
    }
  }
  
  // 如果drillPick没有找到，尝试使用pick（单点检测）
  if (pickedPolygons.length === 0 && clickPosition) {
    const picked = viewer.value.scene.pick(clickPosition)
    if (picked) {
      const entity = picked.id || (picked.primitive && picked.primitive.id) || null
      
      if (entity && entity.polygon) {
        const polygon = riskPolygons.value.find((p) => {
          if (p.id === entity.id) return true
          if (String(p.id) === String(entity.id)) return true
          return false
        })
        
        if (polygon && polygon.data && polygon.data.risk_color) {
          const riskColor = polygon.data.risk_color as string
          const priority = RISK_LEVEL_PRIORITY[riskColor] || 999
          
          pickedPolygons.push({
            polygon,
            entity,
            priority,
          })
        }
      }
    }
  }
  
  // 如果仍然没有找到，尝试通过坐标查找（用于检测点击在多边形内部的情况）
  if (pickedPolygons.length === 0 && clickPosition && viewer.value) {
    try {
      const cartesian = viewer.value.camera.pickEllipsoid(clickPosition, viewer.value.scene.globe.ellipsoid)
      
      if (cartesian) {
        const cartographic = window.Cesium.Cartographic.fromCartesian(cartesian)
        const clickLng = window.Cesium.Math.toDegrees(cartographic.longitude)
        const clickLat = window.Cesium.Math.toDegrees(cartographic.latitude)
        
        // 检查点击位置是否在任何多边形内部
        riskPolygons.value.forEach((polygon) => {
          if (polygon.path && polygon.path.length >= 3 && polygon.data && polygon.data.risk_color) {
            // 简单的点在多边形内判断（使用射线法）
            if (isPointInPolygon({ lng: clickLng, lat: clickLat }, polygon.path)) {
              const riskColor = polygon.data.risk_color as string
              const priority = RISK_LEVEL_PRIORITY[riskColor] || 999
              
              pickedPolygons.push({
                polygon,
                entity: null,
                priority,
              })
            }
          }
        })
      }
    } catch (error) {
      console.warn('通过坐标查找多边形时出错:', error)
    }
  }
  
  // 如果有找到多边形，选择优先级最高的（风险等级最高的）
  if (pickedPolygons.length > 0) {
    // 按优先级排序（数字越小优先级越高）
    pickedPolygons.sort((a, b) => a.priority - b.priority)
    
    // 选择优先级最高的多边形
    const selectedPolygon = pickedPolygons[0]?.polygon
    if (selectedPolygon) {
      handlePolygonClick(selectedPolygon, event)
    }
    return
  }

  // 如果没有点击到Entity，隐藏悬停提示
  hoverTip.visible = false
}

// 判断点是否在多边形内部（射线法）
function isPointInPolygon(point: Point, polygon: Point[]): boolean {
  if (!polygon || polygon.length < 3) return false
  
  let inside = false
  const x = point.lng
  const y = point.lat
  
  for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
    const pi = polygon[i]
    const pj = polygon[j]
    if (!pi || !pj) continue
    const xi = pi.lng
    const yi = pi.lat
    const xj = pj.lng
    const yj = pj.lat
    
    const intersect = ((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
    if (intersect) {
      inside = !inside
    }
  }
  
  return inside
}

// 地图鼠标移动事件（用于悬停提示）
const handleMapMouseMove = (event: any) => {
  if (!viewer.value) return

  // 从事件中获取pickedEntity（CesiumMap组件已处理）
  const pickedEntity = event.pickedEntity
  const mouseEvent = event.event || event
  
  // 检查是否有pickedEntity且是多边形Entity
  if (pickedEntity && pickedEntity.polygon) {
    // 尝试从entity.id获取对应的polygon
    let polygon = null
    
    // 方法1：直接ID匹配
    polygon = riskPolygons.value.find((p) => {
      // 支持多种ID匹配方式
      if (p.id === pickedEntity.id) return true
      if (String(p.id) === String(pickedEntity.id)) return true
      // 如果entity.id是字符串格式 "region-1"，尝试提取数字部分
      if (typeof pickedEntity.id === 'string' && typeof p.id === 'string') {
        if (p.id === pickedEntity.id) return true
        // 提取entity.id中的数字部分
        const entityIdMatch = pickedEntity.id.match(/region-(\d+)/)
        const polygonIdMatch = String(p.id).match(/region-(\d+)/)
        if (entityIdMatch && polygonIdMatch && entityIdMatch[1] === polygonIdMatch[1]) {
          return true
        }
      }
      return false
    })
    
    if (polygon && polygon.data) {
      const tipText = `${polygon.data.street} - ${polygon.data.risk_label}`
      hoverTip.visible = true
      hoverTip.text = tipText
      // 获取鼠标位置
      if (mouseEvent && mouseEvent.clientX !== undefined) {
        hoverTip.x = mouseEvent.clientX + 10
        hoverTip.y = mouseEvent.clientY - 10
      }
      return
    }
  }
  
  // 如果pickedEntity不存在或不是多边形，尝试从polygonEntities中查找
  if (pickedEntity) {
    // 遍历polygonEntities查找匹配的Entity
    for (const [entityId, entity] of polygonEntities.value.entries()) {
      if (entity === pickedEntity || entity.id === pickedEntity.id || String(entity.id) === String(pickedEntity.id)) {
        // 找到对应的多边形
        const polygon = riskPolygons.value.find((p) => {
          if (String(p.id) === String(entityId)) return true
          if (p.id === entityId) return true
          return false
        })
        
        if (polygon && polygon.data) {
          const tipText = `${polygon.data.street} - ${polygon.data.risk_label}`
          hoverTip.visible = true
          hoverTip.text = tipText
          if (mouseEvent && mouseEvent.clientX !== undefined) {
            hoverTip.x = mouseEvent.clientX + 10
            hoverTip.y = mouseEvent.clientY - 10
          }
          return
        }
      }
    }
  }

  // 如果没有悬停到Entity，隐藏悬停提示
  hoverTip.visible = false
}

// 处理多边形点击事件
const handlePolygonClick = (polygon: MapPolygon, event: any) => {
  console.log('点击了风险区域:', polygon)
  
  if (polygon.data) {
    selectedRegion.value = polygon.data
    dialogVisible.value = true
  }
}

// 处理风险等级图层控制变化
const handleRiskLevelChange = () => {
  console.log('风险等级图层控制变化:', showRiskLevels)
  // 切换到风险等级模式时，清除街道筛选
  if (filterMode.value === 'risk_level') {
    selectedStreets.value = []
  }
  // 多边形会自动更新（因为polygons是computed属性，会响应showRiskLevels的变化）
  // 需要手动触发地图更新
  if (isMapReady.value) {
    updatePolygons()
  }
}

// 处理街道筛选变化
const handleStreetFilterChange = () => {
  console.log('街道筛选变化:', selectedStreets.value)
  // 切换到街道模式时，显示所有风险等级（但筛选逻辑会基于街道）
  // 注意：这里不重置风险等级，因为筛选逻辑会在convertToPolygons中根据filterMode决定
  // 多边形会自动更新（因为polygons是computed属性，会响应selectedStreets的变化）
  // 需要手动触发地图更新
  if (isMapReady.value) {
    updatePolygons()
  }
}

// 选择所有街道
const selectAllStreets = () => {
  selectedStreets.value = []
  handleStreetFilterChange()
}

// 清除街道筛选
const clearStreetFilter = () => {
  selectedStreets.value = []
  handleStreetFilterChange()
}

// 监听筛选模式变化
watch(filterMode, (newMode, oldMode) => {
  console.log('筛选模式切换:', oldMode, '->', newMode)
  // 切换模式时，根据新模式更新筛选
  if (newMode === 'risk_level') {
    // 切换到风险等级模式，清除街道筛选
    selectedStreets.value = []
  } else if (newMode === 'street') {
    // 切换到街道模式，如果街道筛选为空，可以选择所有街道
    if (selectedStreets.value.length === 0) {
      // 默认显示所有街道
      // selectedStreets.value = [...allStreets.value] // 或者保持为空数组表示全部
    }
  }
  // 更新地图显示
  if (isMapReady.value) {
    updatePolygons()
  }
})

// 切换地图样式
const changeMapStyle = (style: 'normal' | 'satellite' | 'terrain') => {
  mapStyle.value = style
  console.log('地图样式切换为:', style)
  // CesiumMap组件已监听mapStyle prop的变化，会自动更新
}

// 使用刷新策略（实时数据，1分钟刷新一次）
const { startRefresh: startDataRefresh, stopRefresh: stopDataRefresh } = useRefreshStrategy(
  async () => {
    await loadColorMapData()
  },
  {
    interval: 60000, // 1分钟 = 60000毫秒（态势数据需要实时更新）
    immediate: true,
    retry: {
      maxRetries: 3,
      retryDelay: 1000,
      exponentialBackoff: true,
    },
    enableVisibilityCheck: true,
  }
)

// 监听多边形变化
watch(
  () => riskPolygons.value,
  () => {
    if (isMapReady.value) {
      updatePolygons()
    }
  },
  { deep: true }
)

// 加载四色图数据
onMounted(() => {
  // 启动定时刷新（会在immediate=true时立即执行一次）
  startDataRefresh()
})

onUnmounted(() => {
  // 停止定时刷新
  stopDataRefresh()
  
  // 清除更新多边形的防抖定时器
  if (updatePolygonsTimer) {
    clearTimeout(updatePolygonsTimer)
    updatePolygonsTimer = null
  }
  
  // 清理所有Entity（添加安全检查，避免viewer已销毁时出错）
  try {
    if (viewer.value && viewer.value.entities) {
      clearAllEntities(viewer.value)
      polygonEntities.value.clear()
    }
  } catch (error) {
    // viewer可能已经被销毁，忽略错误
    console.warn('清理Entity时出错（viewer可能已销毁）:', error)
  }
  
  // 清空引用
  viewer.value = null
  isMapReady.value = false
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;

.safety-status-content {
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

.control-panel {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(0, 20, 40, 0.85);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: 8px;
  padding: 16px;
  z-index: 1500;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  min-width: 220px;
  max-width: 280px;
}

.panel-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
  border-bottom: 1px solid rgba(64, 158, 255, 0.2);
  padding-bottom: 8px;
}

.tab-btn {
  flex: 1;
  padding: 6px 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: #e0e0e0;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
  text-align: center;

  &:hover {
    background: rgba(64, 158, 255, 0.1);
    border-color: rgba(64, 158, 255, 0.3);
    color: #409eff;
  }

  &.active {
    background: rgba(64, 158, 255, 0.2);
    border-color: #409eff;
    color: #409eff;
    font-weight: 600;
  }
}

.panel-content {
  min-height: 80px;
  max-height: 350px;
  overflow-y: auto;
}

.region-chart-wrapper {
  position: absolute;
  bottom: 20px;
  right: 20px;
  width: 500px;
  z-index: 1500;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  color: #e0e0e0;
  cursor: pointer;
  padding: 4px 0;
  user-select: none;
  
  &:hover {
    background: rgba(64, 158, 255, 0.1);
    border-radius: 4px;
    padding-left: 4px;
    padding-right: 4px;
  }
  
  input[type="checkbox"] {
    cursor: pointer;
    margin-right: 4px;
    width: 16px;
    height: 16px;
    flex-shrink: 0;
  }
}

.legend-color {
  width: 24px;
  height: 24px;
  border-radius: 4px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  flex-shrink: 0;

  &.red {
    background: rgba(255, 0, 0, 0.4);
    border-color: rgba(255, 0, 0, 1);
  }

  &.orange {
    background: rgba(255, 165, 0, 0.4);
    border-color: rgba(255, 165, 0, 1);
  }

  &.yellow {
    background: rgba(255, 255, 0, 0.4);
    border-color: rgba(255, 255, 0, 1);
  }

  &.blue {
    background: rgba(0, 0, 255, 0.4);
    border-color: rgba(0, 0, 255, 1);
  }
}

.legend-label {
  flex: 1;
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

.filter-actions {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.action-btn {
  flex: 1;
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: #e0e0e0;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    background: rgba(64, 158, 255, 0.1);
    border-color: rgba(64, 158, 255, 0.3);
    color: #409eff;
  }
}

.street-checkboxes {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 250px;
  overflow-y: auto;
}

.street-checkbox-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #e0e0e0;
  cursor: pointer;
  padding: 4px 0;
  user-select: none;

  &:hover {
    background: rgba(64, 158, 255, 0.1);
    border-radius: 4px;
    padding-left: 4px;
    padding-right: 4px;
  }

  input[type="checkbox"] {
    cursor: pointer;
    margin-right: 4px;
    width: 16px;
    height: 16px;
    flex-shrink: 0;
  }

  .street-label {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.style-buttons {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.style-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: #e0e0e0;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    background: rgba(64, 158, 255, 0.1);
    border-color: rgba(64, 158, 255, 0.3);
    color: #409eff;
  }

  &.active {
    background: rgba(64, 158, 255, 0.2);
    border-color: #409eff;
    color: #409eff;
    font-weight: 600;
  }

  .style-icon {
    font-size: 18px;
    flex-shrink: 0;
  }

  .style-label {
    flex: 1;
  }
}
</style>
