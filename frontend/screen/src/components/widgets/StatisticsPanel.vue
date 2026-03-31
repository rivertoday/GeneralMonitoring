<template>
  <div class="statistics-panel">
    <div class="panel-header">
      <h3 class="panel-title">统计面板</h3>
      <div class="panel-refresh" @click="handleRefresh" :class="{ refreshing: isRefreshing }" title="刷新数据">
        <span class="refresh-icon">🔄</span>
      </div>
    </div>
    <div class="panel-content">
      <!-- 加载状态 -->
      <div v-if="isLoading && !hasData" class="loading-state">
        <div class="loading-spinner"></div>
        <div class="loading-text">加载中...</div>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="error-state">
        <div class="error-icon">⚠️</div>
        <div class="error-text">{{ error }}</div>
        <button class="retry-button" @click="handleRefresh">重试</button>
      </div>

      <!-- 数据展示 -->
      <template v-else>
        <!-- 救援队伍统计 -->
        <div class="stat-card" @click="handleCardClick('teams')">
          <div class="stat-icon">🚑</div>
          <div class="stat-info">
            <div class="stat-label">救援队伍</div>
            <div class="stat-value">{{ resourceStats.team_count || 0 }}</div>
            <div class="stat-desc">总人数: {{ formatNumber(resourceStats.team_capacity || 0) }}人</div>
          </div>
          <div class="stat-trend" v-if="resourceStats.team_count > 0">
            <span class="trend-up">↑</span>
          </div>
        </div>

        <!-- 应急专家统计 -->
        <div class="stat-card" @click="handleCardClick('experts')">
          <div class="stat-icon">👨‍🔬</div>
          <div class="stat-info">
            <div class="stat-label">应急专家</div>
            <div class="stat-value">{{ resourceStats.expert_count || 0 }}</div>
            <div class="stat-desc">专家总数</div>
          </div>
          <div class="stat-trend" v-if="resourceStats.expert_count > 0">
            <span class="trend-up">↑</span>
          </div>
        </div>

        <!-- 物资装备统计 -->
        <div class="stat-card" @click="handleCardClick('equipment')">
          <div class="stat-icon">📦</div>
          <div class="stat-info">
            <div class="stat-label">物资装备</div>
            <div class="stat-value">{{ resourceStats.equipment_count || 0 }}</div>
            <div class="stat-desc">总数量: {{ formatNumber(resourceStats.equipment_quantity || 0) }}</div>
          </div>
          <div class="stat-trend" v-if="resourceStats.equipment_count > 0">
            <span class="trend-up">↑</span>
          </div>
        </div>

        <!-- 防护目标统计 -->
        <div class="stat-card" @click="handleCardClick('targets')">
          <div class="stat-icon">🏛️</div>
          <div class="stat-info">
            <div class="stat-label">防护目标</div>
            <div class="stat-value">{{ targetStats.total_count || 0 }}</div>
            <div class="stat-desc">总人口: {{ formatNumber(targetStats.total_population || 0) }}人</div>
          </div>
          <div class="stat-trend" v-if="targetStats.total_count > 0">
            <span class="trend-up">↑</span>
          </div>
        </div>

        <!-- 避难场所统计 -->
        <div class="stat-card" @click="handleCardClick('shelters')">
          <div class="stat-icon">🏕️</div>
          <div class="stat-info">
            <div class="stat-label">避难场所</div>
            <div class="stat-value">{{ shelterStats.total_count || 0 }}</div>
            <div class="stat-desc">总容量: {{ formatNumber(shelterStats.total_capacity || 0) }}人</div>
          </div>
          <div class="stat-trend" v-if="shelterStats.total_count > 0">
            <span class="trend-up">↑</span>
          </div>
        </div>
      </template>
    </div>
    
    <!-- 最后更新时间 -->
    <div class="panel-footer" v-if="hasData">
      <div class="update-time">更新于: {{ lastUpdateTime }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { getResourceStatistics, getTargetStatistics, getShelterStatistics } from '@/api/modules/safety'
import type { ResourceStatistics, TargetStatistics, ShelterStatistics } from '@/api/modules/safety'
import { useRefreshStrategy } from '@/composables/useRefreshStrategy'

// 定义事件，用于与父组件通信（可选）
const emit = defineEmits<{
  (e: 'card-click', category: string): void
  (e: 'stats-updated', stats: {
    resource: ResourceStatistics
    target: TargetStatistics
    shelter: ShelterStatistics
  }): void
}>()

const resourceStats = ref<ResourceStatistics>({
  total_count: 0,
  type_stats: [],
  sub_type_stats: [],
  status_stats: [],
  team_count: 0,
  team_capacity: 0,
  expert_count: 0,
  equipment_count: 0,
  equipment_quantity: 0,
})

const targetStats = ref<TargetStatistics>({
  total_count: 0,
  type_stats: [],
  risk_stats: [],
  total_population: 0,
})

const shelterStats = ref<ShelterStatistics>({
  total_count: 0,
  type_stats: [],
  total_capacity: 0,
})

const isLoading = ref(false)
const isRefreshing = ref(false)
const error = ref<string | null>(null)
const lastUpdateTime = ref<string>('')

// 判断是否有数据
const hasData = computed(() => {
  return (
    resourceStats.value.total_count > 0 ||
    targetStats.value.total_count > 0 ||
    shelterStats.value.total_count > 0
  )
})

// 格式化数字（添加千分位）
const formatNumber = (num: number): string => {
  if (num === 0) return '0'
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

// 格式化更新时间
const formatUpdateTime = (): string => {
  const now = new Date()
  const hours = String(now.getHours()).padStart(2, '0')
  const minutes = String(now.getMinutes()).padStart(2, '0')
  const seconds = String(now.getSeconds()).padStart(2, '0')
  return `${hours}:${minutes}:${seconds}`
}

// 加载统计数据
const loadStatistics = async (isManual = false) => {
  if (isManual) {
    isRefreshing.value = true
  } else {
    isLoading.value = true
  }
  error.value = null

  try {
    const [resourceData, targetData, shelterData] = await Promise.all([
      getResourceStatistics(),
      getTargetStatistics(),
      getShelterStatistics(),
    ])

    // 更新统计数据
    resourceStats.value = resourceData
    targetStats.value = targetData
    shelterStats.value = shelterData

    // 更新最后更新时间
    lastUpdateTime.value = formatUpdateTime()

    // 通知父组件统计数据已更新
    emit('stats-updated', {
      resource: resourceData,
      target: targetData,
      shelter: shelterData,
    })

    console.log('统计数据加载成功:', {
      resource: resourceData,
      target: targetData,
      shelter: shelterData,
    })
  } catch (err: any) {
    const errorMessage = err?.message || '加载统计数据失败'
    error.value = errorMessage
    console.error('加载统计数据失败:', err)
  } finally {
    isLoading.value = false
    isRefreshing.value = false
  }
}

// 使用刷新策略（基础数据，1分钟刷新一次）
const { startRefresh: startDataRefresh, stopRefresh: stopDataRefresh, lastUpdateTime: refreshLastUpdateTime } = useRefreshStrategy(
  async () => {
    await loadStatistics()
  },
  {
    interval: 60000, // 1分钟 = 60000毫秒（基础数据变化较慢）
    immediate: true,
    retry: {
      maxRetries: 3,
      retryDelay: 2000,
      exponentialBackoff: true,
    },
    enableVisibilityCheck: true,
  }
)

// 监听刷新策略的更新时间，同步到本地
watch(refreshLastUpdateTime, (newTime) => {
  if (newTime) {
    lastUpdateTime.value = formatUpdateTime()
  }
}, { immediate: true })

// 手动刷新
const handleRefresh = async () => {
  isRefreshing.value = true
  try {
    await loadStatistics(true)
  } finally {
    isRefreshing.value = false
  }
}

// 卡片点击事件
const handleCardClick = (category: string) => {
  emit('card-click', category)
  console.log('点击了统计卡片:', category)
}

onMounted(() => {
  // 启动定时刷新（会在immediate=true时立即执行一次）
  startDataRefresh()
})

onUnmounted(() => {
  stopDataRefresh()
})
</script>

<style scoped lang="scss">
@use 'sass:color';
@use '@/styles/variables.scss' as *;
@use '@/styles/mixins.scss' as *;

.statistics-panel {
  @include card;
  padding: 1.5vh 1.5vw;
  position: absolute;
  top: 2vh;
  right: 2vw;
  width: 20vw;
  min-width: 300px;
  max-width: 400px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5vh;
  border-bottom: 1px solid $border-color;
  padding-bottom: 1vh;
}

.panel-title {
  @include title(3);
  margin: 0;
  color: $text-primary;
}

.panel-refresh {
  cursor: pointer;
  padding: 0.5vh 0.8vw;
  border-radius: $radius-sm;
  transition: all $transition-base;
  display: flex;
  align-items: center;
  justify-content: center;

  .refresh-icon {
    font-size: 1.2vw;
    display: inline-block;
    transition: transform $transition-base;
  }

  &:hover {
    background: rgba(64, 158, 255, 0.1);
    transform: scale(1.1);

    .refresh-icon {
      transform: rotate(180deg);
    }
  }

  &.refreshing .refresh-icon {
    animation: spin 1s linear infinite;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.panel-content {
  display: flex;
  flex-direction: column;
  gap: 1.5vh;
  flex: 1;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3vh 1vw;
  color: $text-secondary;
}

.loading-spinner {
  width: 3vw;
  height: 3vw;
  border: 3px solid rgba(64, 158, 255, 0.2);
  border-top-color: $color-primary;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1vh;
}

.loading-text,
.error-text {
  @include font-size($font-size-sm);
  margin-top: 1vh;
}

.error-icon {
  font-size: 3vw;
  margin-bottom: 1vh;
}

.retry-button {
  margin-top: 1.5vh;
  padding: 0.8vh 1.5vw;
  background: $color-primary;
  color: #fff;
  border: none;
  border-radius: $radius-sm;
  cursor: pointer;
  @include font-size($font-size-sm);
  transition: all $transition-base;

  &:hover {
    background: color.adjust($color-primary, $lightness: -10%);
    transform: translateY(-2px);
  }
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1vw;
  padding: 1.5vh 1vw;
  background: rgba(64, 158, 255, 0.1);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: $radius-md;
  transition: all $transition-base;
  cursor: pointer;
  position: relative;

  &:hover {
    background: rgba(64, 158, 255, 0.15);
    border-color: rgba(64, 158, 255, 0.5);
    transform: translateX(5px);
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
  }

  &:active {
    transform: translateX(3px) scale(0.98);
  }
}

.stat-icon {
  font-size: 2.5vw;
  min-width: 3vw;
  text-align: center;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.stat-info {
  flex: 1;
}

.stat-label {
  @include font-size($font-size-sm);
  color: $text-secondary;
  margin-bottom: 0.5vh;
  font-weight: 500;
}

.stat-value {
  @include font-size($font-size-2xl);
  color: $color-primary;
  font-weight: bold;
  margin-bottom: 0.3vh;
  @include glow($color-primary, 5px);
  line-height: 1.2;
}

.stat-desc {
  @include font-size($font-size-xs);
  color: $text-muted;
  line-height: 1.4;
}

.stat-trend {
  position: absolute;
  top: 0.5vh;
  right: 0.8vw;
  font-size: 1vw;
  color: #67c23a;

  .trend-up {
    display: inline-block;
    animation: pulse 2s ease-in-out infinite;
  }
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.6;
    transform: scale(1.1);
  }
}

.panel-footer {
  margin-top: 1.5vh;
  padding-top: 1vh;
  border-top: 1px solid $border-color;
  text-align: center;
}

.update-time {
  @include font-size($font-size-xs);
  color: $text-muted;
}
</style>

