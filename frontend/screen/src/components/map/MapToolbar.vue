<template>
  <div class="map-toolbar">
    <!-- 图层控制 -->
    <div class="toolbar-section">
      <div class="section-title">图层控制</div>
      <div class="layer-controls">
        <label class="layer-item">
          <input
            v-model="layerSettings.showMarkers"
            type="checkbox"
            @change="handleLayerChange('markers')"
          />
          <span>资源标记</span>
        </label>
        <!-- 资源分类列表 -->
        <div v-if="layerSettings.showMarkers" class="resource-categories">
          <label class="layer-item sub-item">
            <input
              v-model="resourceCategories.showTeams"
              type="checkbox"
              data-category="teams"
              @change="handleResourceCategoryChange('teams')"
            />
            <span>🚑 救援队伍 ({{ resourceStats.team_count || 0 }})</span>
          </label>
          <label class="layer-item sub-item">
            <input
              v-model="resourceCategories.showExperts"
              type="checkbox"
              data-category="experts"
              @change="handleResourceCategoryChange('experts')"
            />
            <span>👨‍🔬 应急专家 ({{ resourceStats.expert_count || 0 }})</span>
          </label>
          <label class="layer-item sub-item">
            <input
              v-model="resourceCategories.showEquipment"
              type="checkbox"
              data-category="equipment"
              @change="handleResourceCategoryChange('equipment')"
            />
            <span>📦 物资装备 ({{ resourceStats.equipment_count || 0 }})</span>
          </label>
          <label class="layer-item sub-item">
            <input
              v-model="resourceCategories.showTargets"
              type="checkbox"
              data-category="targets"
              @change="handleResourceCategoryChange('targets')"
            />
            <span>🏛️ 防护目标 ({{ resourceStats.target_count || 0 }})</span>
          </label>
          <label class="layer-item sub-item">
            <input
              v-model="resourceCategories.showShelters"
              type="checkbox"
              data-category="shelters"
              @change="handleResourceCategoryChange('shelters')"
            />
            <span>🏕️ 避难场所 ({{ resourceStats.shelter_count || 0 }})</span>
          </label>
        </div>
        <label class="layer-item">
          <input
            v-model="layerSettings.showPolygons"
            type="checkbox"
            @change="handleLayerChange('polygons')"
          />
          <span>区域边界</span>
        </label>
        <label class="layer-item">
          <input
            v-model="layerSettings.showLabels"
            type="checkbox"
            @change="handleLayerChange('labels')"
          />
          <span>标注信息</span>
        </label>
      </div>
    </div>

    <!-- 场景模式 -->
    <div class="toolbar-section">
      <div class="section-title">场景模式</div>
      <div class="scene-mode-controls">
        <button
          v-for="mode in sceneModes"
          :key="mode.value"
          class="mode-btn"
          :class="{ active: currentSceneMode === mode.value }"
          @click="handleSceneModeChange(mode.value as '2D' | '3D' | 'COLUMBUS_VIEW')"
          :title="mode.label"
        >
          <span class="mode-icon">{{ mode.icon }}</span>
          <span class="mode-text">{{ mode.label }}</span>
        </button>
      </div>
    </div>

    <!-- 视图控制 -->
    <div class="toolbar-section">
      <div class="section-title">视图控制</div>
      <div class="view-controls">
        <button class="tool-btn" @click="handleResetView" title="重置视图">
          <span class="icon">📍</span>
          <span class="text">重置视图</span>
        </button>
        <button class="tool-btn" @click="handleFitBounds" title="适应范围">
          <span class="icon">🔍</span>
          <span class="text">适应范围</span>
        </button>
        <button class="tool-btn" @click="handleFullscreen" :title="isFullscreen ? '退出全屏' : '全屏显示'">
          <span class="icon">{{ isFullscreen ? '⛶' : '⛶' }}</span>
          <span class="text">{{ isFullscreen ? '退出全屏' : '全屏' }}</span>
        </button>
      </div>
    </div>

    <!-- 地图样式 -->
    <div class="toolbar-section">
      <div class="section-title">地图样式</div>
      <div class="map-style-controls">
        <button
          v-for="style in mapStyles"
          :key="style.value"
          class="style-btn"
          :class="{ active: currentMapStyle === style.value }"
          @click="handleMapStyleChange(style.value)"
          :title="style.label"
        >
          {{ style.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import type { Point } from '@/types/map'

interface Props {
  /** 默认中心点 */
  defaultCenter?: Point
  /** 默认缩放级别 */
  defaultZoom?: number
  /** 是否显示标记点 */
  showMarkers?: boolean
  /** 是否显示多边形 */
  showPolygons?: boolean
  /** 资源统计数据 */
  resourceStats?: {
    team_count?: number
    expert_count?: number
    equipment_count?: number
    target_count?: number
    shelter_count?: number
  }
}

interface Emits {
  (e: 'layer-change', data: { type: string; visible: boolean }): void
  (e: 'resource-category-change', data: { category: string; visible: boolean }): void
  (e: 'reset-view'): void
  (e: 'fit-bounds'): void
  (e: 'map-style-change', style: string): void
  (e: 'scene-mode-change', mode: '2D' | '3D' | 'COLUMBUS_VIEW'): void
}

const props = withDefaults(defineProps<Props>(), {
  defaultCenter: () => ({ lng: 118.521577, lat: 31.742368 }),
  defaultZoom: 12,
  showMarkers: true,
  showPolygons: true,
  resourceStats: () => ({
    team_count: 0,
    expert_count: 0,
    equipment_count: 0,
    target_count: 0,
    shelter_count: 0,
  }),
})

const emit = defineEmits<Emits>()

// 图层设置
const layerSettings = reactive({
  showMarkers: props.showMarkers,
  showPolygons: props.showPolygons,
  showLabels: true,
})

// 资源分类设置
const resourceCategories = reactive({
  showTeams: true,
  showExperts: true,
  showEquipment: true,
  showTargets: true,
  showShelters: true,
})

// 场景模式
const sceneModes = [
  { value: '2D', label: '2D', icon: '🗺️' },
  { value: '3D', label: '3D', icon: '🌍' },
  { value: 'COLUMBUS_VIEW', label: '哥伦布', icon: '🌐' },
]
const currentSceneMode = ref<'2D' | '3D' | 'COLUMBUS_VIEW'>('2D')

// 地图样式
const mapStyles = [
  { value: 'normal', label: '标准' },
  { value: 'satellite', label: '卫星' },
  { value: 'terrain', label: '地形' },
]
const currentMapStyle = ref('normal')

// 全屏状态
const isFullscreen = ref(false)

// 处理图层变化
const handleLayerChange = (type: string) => {
  let visible = false
  switch (type) {
    case 'markers':
      visible = layerSettings.showMarkers
      break
    case 'polygons':
      visible = layerSettings.showPolygons
      break
    case 'labels':
      visible = layerSettings.showLabels
      break
  }
  emit('layer-change', { type, visible })
}

// 处理资源分类变化
const handleResourceCategoryChange = (category: string) => {
  let visible = false
  switch (category) {
    case 'teams':
      visible = resourceCategories.showTeams
      break
    case 'experts':
      visible = resourceCategories.showExperts
      break
    case 'equipment':
      visible = resourceCategories.showEquipment
      break
    case 'targets':
      visible = resourceCategories.showTargets
      break
    case 'shelters':
      visible = resourceCategories.showShelters
      break
  }
  emit('resource-category-change', { category, visible })
  
  // 视觉反馈：添加短暂的高亮效果
  const checkbox = document.querySelector(`input[type="checkbox"][data-category="${category}"]`)
  if (checkbox) {
    checkbox.parentElement?.classList.add('category-changed')
    setTimeout(() => {
      checkbox.parentElement?.classList.remove('category-changed')
    }, 300)
  }
}

// 处理重置视图
const handleResetView = () => {
  emit('reset-view')
}

// 处理适应范围
const handleFitBounds = () => {
  emit('fit-bounds')
}

// 处理场景模式切换
const handleSceneModeChange = (mode: '2D' | '3D' | 'COLUMBUS_VIEW') => {
  currentSceneMode.value = mode
  emit('scene-mode-change', mode)
}

// 处理地图样式切换
const handleMapStyleChange = (style: string) => {
  currentMapStyle.value = style
  emit('map-style-change', style)
}

// 处理全屏
const handleFullscreen = () => {
  if (!document.fullscreenElement) {
    // 进入全屏
    const element = document.documentElement
    if (element.requestFullscreen) {
      element.requestFullscreen()
    }
  } else {
    // 退出全屏
    if (document.exitFullscreen) {
      document.exitFullscreen()
    }
  }
}

// 监听全屏状态变化
const handleFullscreenChange = () => {
  isFullscreen.value = !!document.fullscreenElement
}

onMounted(() => {
  document.addEventListener('fullscreenchange', handleFullscreenChange)
})

onUnmounted(() => {
  document.removeEventListener('fullscreenchange', handleFullscreenChange)
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;

.map-toolbar {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 200px;
  background: rgba(0, 20, 40, 0.85);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: 8px;
  padding: 16px;
  z-index: 1500;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.toolbar-section {
  margin-bottom: 16px;

  &:last-child {
    margin-bottom: 0;
  }
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #409eff;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(64, 158, 255, 0.2);
}

.layer-controls {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.layer-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #e0e0e0;
  cursor: pointer;
  user-select: none;

  &:hover {
    color: #409eff;
  }

  input[type="checkbox"] {
    width: 16px;
    height: 16px;
    cursor: pointer;
    accent-color: #409eff;
  }

  span {
    flex: 1;
  }
}

.resource-categories {
  margin-left: 24px;
  margin-top: 8px;
  margin-bottom: 8px;
  padding-left: 12px;
  border-left: 2px solid rgba(64, 158, 255, 0.3);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.sub-item {
  font-size: 12px;
  opacity: 0.9;
  
  &.category-changed {
    animation: highlight 0.3s ease;
  }
}

@keyframes highlight {
  0% {
    background: transparent;
  }
  50% {
    background: rgba(64, 158, 255, 0.2);
  }
  100% {
    background: transparent;
  }
}

.view-controls {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tool-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  padding: 8px 12px;
  background: rgba(64, 158, 255, 0.1);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: 4px;
  color: #e0e0e0;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    background: rgba(64, 158, 255, 0.2);
    border-color: rgba(64, 158, 255, 0.5);
    color: #409eff;
  }

  &:active {
    transform: scale(0.98);
  }

  .icon {
    font-size: 16px;
    line-height: 1;
  }

  .text {
    flex: 1;
    text-align: left;
  }
}

.scene-mode-controls {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.mode-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
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

  &.active {
    background: rgba(64, 158, 255, 0.2);
    border-color: #409eff;
    color: #409eff;
    font-weight: 600;
  }

  .mode-icon {
    font-size: 16px;
    line-height: 1;
  }

  .mode-text {
    flex: 1;
    text-align: left;
  }
}

.map-style-controls {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.style-btn {
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

  &.active {
    background: rgba(64, 158, 255, 0.2);
    border-color: #409eff;
    color: #409eff;
    font-weight: 600;
  }
}
</style>

