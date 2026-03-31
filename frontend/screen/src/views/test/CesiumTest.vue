<template>
  <ScreenLayout title="Cesium 地图测试">
    <div class="cesium-test-content">
      <!-- 控制面板 -->
      <div class="control-panel">
        <h3>地图控制</h3>
        <div class="control-group">
          <label>地图样式：</label>
          <select v-model="mapStyle" @change="handleMapStyleChange">
            <option value="normal">标准地图</option>
            <option value="satellite">影像地图</option>
            <option value="terrain">地形地图</option>
          </select>
        </div>
        <div class="control-group">
          <label>场景模式：</label>
          <select v-model="sceneMode" @change="handleSceneModeChange">
            <option value="2D">2D</option>
            <option value="3D">3D</option>
            <option value="COLUMBUS_VIEW">哥伦布视图</option>
          </select>
        </div>
        <div class="control-group">
          <label>中心点：</label>
          <div class="coord-input">
            <input v-model.number="center.lng" type="number" step="0.000001" placeholder="经度" />
            <input v-model.number="center.lat" type="number" step="0.000001" placeholder="纬度" />
          </div>
        </div>
        <div class="control-group">
          <label>缩放级别：</label>
          <input v-model.number="zoom" type="number" min="3" max="19" step="1" />
        </div>
        <div class="control-buttons">
          <button @click="handleResetView">重置视图</button>
          <button @click="handleAddTestMarker">添加测试标记点</button>
          <button @click="handleAddTestPolygon">添加测试多边形</button>
          <button @click="handleClearEntities">清除所有要素</button>
        </div>
        <div class="info-panel">
          <h4>地图信息</h4>
          <div class="info-item">
            <span>当前中心点：</span>
            <span>{{ currentCenter.lng.toFixed(6) }}, {{ currentCenter.lat.toFixed(6) }}</span>
          </div>
          <div class="info-item">
            <span>当前缩放级别：</span>
            <span>{{ currentZoom.toFixed(2) }}</span>
          </div>
          <div class="info-item">
            <span>要素数量：</span>
            <span>{{ entityCount }}</span>
          </div>
          <div class="info-item">
            <span>地图状态：</span>
            <span :class="{ 'status-ok': isMapReady, 'status-error': !isMapReady }">
              {{ isMapReady ? '已就绪' : '未就绪' }}
            </span>
          </div>
          <div class="info-item" v-if="isMapReady">
            <span>当前图层类型：</span>
            <span class="layer-type-info">
              {{ getLayerTypeInfo() }}
            </span>
          </div>
        </div>
      </div>

      <!-- 地图容器 -->
      <div class="map-wrapper">
        <CesiumMap
          ref="cesiumMapRef"
          :center="center"
          :zoom="zoom"
          :map-style="mapStyle"
          :scene-mode="sceneMode"
          @ready="onMapReady"
          @click="handleMapClick"
          @moveend="handleMapMoveEnd"
        />
        <div v-if="!isMapReady" class="loading-overlay">
          <div class="loading-text">正在加载 Cesium 地图...</div>
        </div>
      </div>
    </div>
  </ScreenLayout>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import ScreenLayout from '@/components/layout/ScreenLayout.vue'
import CesiumMap from '@/components/map/CesiumMap.vue'
import type { Point } from '@/types/map'

const cesiumMapRef = ref<InstanceType<typeof CesiumMap> | null>(null)
const viewer = ref<any>(null)
const isMapReady = ref(false)

// 地图配置
const center = reactive<Point>({ lng: 118.521577, lat: 31.742368 }) // 慈湖站位置
const zoom = ref(12)
const mapStyle = ref<'normal' | 'satellite' | 'terrain'>('normal')
const sceneMode = ref<'2D' | '3D' | 'COLUMBUS_VIEW'>('2D')

// 当前地图状态
const currentCenter = reactive<Point>({ lng: 0, lat: 0 })
const currentZoom = ref(12)
const entityCount = ref(0)

// 地图就绪回调
const onMapReady = (cesiumViewer: any) => {
  viewer.value = cesiumViewer
  isMapReady.value = true
  console.log('Cesium 地图初始化完成', cesiumViewer)
  
  // 更新初始状态
  updateMapInfo()
  
  // 监听实体变化
  if (viewer.value) {
    viewer.value.entities.collectionChanged.addEventListener(() => {
      entityCount.value = viewer.value.entities.values.length
    })
  }
}

// 更新地图信息
const updateMapInfo = () => {
  if (cesiumMapRef.value) {
    currentCenter.lng = cesiumMapRef.value.getCenter().lng
    currentCenter.lat = cesiumMapRef.value.getCenter().lat
    currentZoom.value = cesiumMapRef.value.getZoom()
  }
}

// 地图移动结束
const handleMapMoveEnd = () => {
  updateMapInfo()
}

// 地图点击事件
const handleMapClick = (event: any) => {
  console.log('地图点击事件:', event)
  
  if (event.position && viewer.value) {
    const Cesium = window.Cesium
    if (!Cesium) return
    
    const cartographic = Cesium.Cartographic.fromCartesian(event.position)
    const lng = Cesium.Math.toDegrees(cartographic.longitude)
    const lat = Cesium.Math.toDegrees(cartographic.latitude)
    
    console.log('点击位置:', { lng, lat })
    
    // 在点击位置添加标记点
    if (viewer.value) {
      viewer.value.entities.add({
        position: event.position,
        billboard: {
          image: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTIiIGZpbGw9IiNGRjQwNDAiIHN0cm9rZT0iI0ZGRiIgc3Ryb2tlLXdpZHRoPSIyIi8+Cjwvc3ZnPg==',
          width: 24,
          height: 24,
        },
        label: {
          text: `(${lng.toFixed(6)}, ${lat.toFixed(6)})`,
          font: '12px sans-serif',
          fillColor: Cesium.Color.WHITE,
          outlineColor: Cesium.Color.BLACK,
          outlineWidth: 2,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
          verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
          pixelOffset: new Cesium.Cartesian2(0, -24),
        },
      })
      
      entityCount.value = viewer.value.entities.values.length
    }
  }
}

// 地图样式切换
const handleMapStyleChange = () => {
  if (cesiumMapRef.value) {
    cesiumMapRef.value.setMapStyle(mapStyle.value)
  }
}

// 场景模式切换
const handleSceneModeChange = () => {
  // 场景模式切换由 CesiumMap 组件内部处理
  console.log('场景模式切换为:', sceneMode.value)
  // 场景模式切换后，normal 样式会自动在 2D 模式使用矢量图层，3D 模式使用影像图层
}

// 获取当前图层类型信息
const getLayerTypeInfo = (): string => {
  if (!isMapReady.value) return '加载中...'
  
  if (mapStyle.value === 'normal') {
    if (sceneMode.value === '2D' || sceneMode.value === 'COLUMBUS_VIEW') {
      return '矢量图层 (vec_w + cva_w)'
    } else {
      return '影像图层 (img_w + ibo_w)'
    }
  } else if (mapStyle.value === 'satellite') {
    return '影像图层 (img_w + ibo_w)'
  } else if (mapStyle.value === 'terrain') {
    return '地形图层 (地形 + img_w)'
  }
  return '未知'
}

// 重置视图
const handleResetView = () => {
  center.lng = 118.521577
  center.lat = 31.742368
  zoom.value = 12
  mapStyle.value = 'normal'
  sceneMode.value = '2D'
  
  if (cesiumMapRef.value) {
    cesiumMapRef.value.setCenter(center)
    cesiumMapRef.value.setZoom(zoom.value)
    cesiumMapRef.value.setMapStyle(mapStyle.value)
  }
}

// 添加测试标记点
const handleAddTestMarker = () => {
  if (!viewer.value) return
  
  const Cesium = window.Cesium
  if (!Cesium) return
  
  const testPosition = Cesium.Cartesian3.fromDegrees(118.521577, 31.742368)
  
  viewer.value.entities.add({
    position: testPosition,
    billboard: {
      image: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIHZpZXdCb3g9IjAgMCA0OCA0OCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMjQiIGN5PSIyNCIgcj0iMjAiIGZpbGw9IiM0MDlFRkYiIHN0cm9rZT0iI0ZGRiIgc3Ryb2tlLXdpZHRoPSIzIi8+Cjx0ZXh0IHg9IjI0IiB5PSIyOCIgZm9udC1zaXplPSIxOCIgZmlsbD0iI0ZGRiIgdGV4dC1hbmNob3I9Im1pZGRsZSI+77yBPC90ZXh0Pgo8L3N2Zz4=',
      width: 32,
      height: 32,
    },
    label: {
      text: '测试标记点',
      font: '14px sans-serif',
      fillColor: Cesium.Color.WHITE,
      outlineColor: Cesium.Color.BLACK,
      outlineWidth: 2,
      style: Cesium.LabelStyle.FILL_AND_OUTLINE,
      verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
      pixelOffset: new Cesium.Cartesian2(0, -32),
    },
  })
  
  entityCount.value = viewer.value.entities.values.length
}

// 添加测试多边形
const handleAddTestPolygon = () => {
  if (!viewer.value) return
  
  const Cesium = window.Cesium
  if (!Cesium) return
  
  // 创建一个以慈湖站为中心的矩形区域
  const centerLng = 118.521577
  const centerLat = 31.742368
  const offset = 0.01 // 约1公里
  
  viewer.value.entities.add({
    polygon: {
      hierarchy: Cesium.Cartesian3.fromDegreesArray([
        centerLng - offset, centerLat - offset,
        centerLng + offset, centerLat - offset,
        centerLng + offset, centerLat + offset,
        centerLng - offset, centerLat + offset,
      ]),
      material: Cesium.Color.RED.withAlpha(0.5),
      outline: true,
      outlineColor: Cesium.Color.RED,
      height: 0,
    },
    label: {
      text: '测试多边形区域',
      font: '14px sans-serif',
      fillColor: Cesium.Color.WHITE,
      outlineColor: Cesium.Color.BLACK,
      outlineWidth: 2,
      style: Cesium.LabelStyle.FILL_AND_OUTLINE,
      position: Cesium.Cartesian3.fromDegrees(centerLng, centerLat),
    },
  })
  
  entityCount.value = viewer.value.entities.values.length
}

// 清除所有要素
const handleClearEntities = () => {
  if (viewer.value) {
    viewer.value.entities.removeAll()
    entityCount.value = 0
  }
}

onMounted(() => {
  // 定时更新地图信息
  setInterval(() => {
    if (isMapReady.value) {
      updateMapInfo()
    }
  }, 1000)
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;
@use '@/styles/mixins.scss' as *;

.cesium-test-content {
  width: 100%;
  height: 100%;
  display: flex;
  gap: 20px;
  padding: 20px;
}

.control-panel {
  @include card;
  width: 300px;
  min-width: 300px;
  padding: 20px;
  overflow-y: auto;
  
  h3 {
    @include title(3);
    margin: 0 0 20px 0;
    color: $text-primary;
  }
  
  h4 {
    @include title(4);
    margin: 20px 0 10px 0;
    color: $text-primary;
  }
}

.control-group {
  margin-bottom: 15px;
  
  label {
    display: block;
    margin-bottom: 5px;
    font-size: 13px;
    color: $text-secondary;
  }
  
  select,
  input[type='number'] {
    width: 100%;
    padding: 8px;
    border: 1px solid $border-color;
    border-radius: $radius-sm;
    background: rgba(255, 255, 255, 0.1);
    color: $text-primary;
    font-size: 13px;
    
    &:focus {
      outline: none;
      border-color: $color-primary;
    }
  }
  
  .coord-input {
    display: flex;
    gap: 10px;
    
    input {
      flex: 1;
    }
  }
}

.control-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
  
  button {
    padding: 10px;
    background: rgba(64, 158, 255, 0.2);
    border: 1px solid rgba(64, 158, 255, 0.5);
    border-radius: $radius-sm;
    color: $text-primary;
    font-size: 13px;
    cursor: pointer;
    transition: all $transition-base;
    
    &:hover {
      background: rgba(64, 158, 255, 0.4);
      border-color: $color-primary;
    }
  }
}

.info-panel {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid $border-color;
}

.info-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 12px;
  color: $text-secondary;
  
  span:last-child {
    color: $text-primary;
    font-weight: 500;
  }
}

.status-ok {
  color: #52c41a;
}

.status-error {
  color: #ff4d4f;
}

.layer-type-info {
  color: #409eff;
  font-weight: 600;
}

.map-wrapper {
  flex: 1;
  position: relative;
  border-radius: $radius-md;
  overflow: hidden;
  background: #000;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.7);
  z-index: 1000;
}

.loading-text {
  color: #fff;
  font-size: 16px;
}
</style>

