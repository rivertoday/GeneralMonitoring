<template>
  <div class="warning-progress-chart">
    <div class="chart-header">
      <h4 class="chart-title">预警处置进度</h4>
    </div>
    <div class="progress-content">
      <!-- 总体进度 -->
      <div class="overall-progress">
        <div class="progress-label">总体处置进度</div>
        <div class="progress-bar-wrapper">
          <div class="progress-bar" :style="{ width: overallProgress + '%' }">
            <span class="progress-text">{{ overallProgress }}%</span>
          </div>
        </div>
        <div class="progress-stats">
          <span class="stat-item">已处置: {{ handledCount }}</span>
          <span class="stat-item">待处置: {{ pendingCount }}</span>
        </div>
      </div>

      <!-- 状态分布 -->
      <div class="status-distribution">
        <div
          v-for="status in statusList"
          :key="status.value"
          class="status-item"
        >
          <div class="status-header">
            <span class="status-icon" :style="{ color: status.color }">{{ status.icon }}</span>
            <span class="status-name">{{ status.label }}</span>
            <span class="status-count">{{ status.count }}</span>
          </div>
          <div class="status-bar-wrapper">
            <div
              class="status-bar"
              :style="{
                width: status.percentage + '%',
                backgroundColor: status.color,
              }"
            ></div>
          </div>
          <div class="status-percentage">{{ status.percentage }}%</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  statistics: {
    total: number
    byStatus: {
      0: number // 未发布
      1: number // 已发布
      2: number // 处理中
      3: number // 已处置
      4: number // 已关闭
    }
  }
}

const props = defineProps<Props>()

// 预警状态配置
const STATUS_CONFIG = {
  0: { label: '未发布', icon: '⏸️', color: '#999999' },
  1: { label: '已发布', icon: '📢', color: '#1890ff' },
  2: { label: '处理中', icon: '⚙️', color: '#ffa940' },
  3: { label: '已处置', icon: '✅', color: '#52c41a' },
  4: { label: '已关闭', icon: '🔒', color: '#8c8c8c' },
}

// 计算总体处置进度（已处置 + 已关闭 / 总数）
const overallProgress = computed(() => {
  if (props.statistics.total === 0) return 0
  const handled = props.statistics.byStatus[3] + props.statistics.byStatus[4]
  return Math.round((handled / props.statistics.total) * 100)
})

// 计算已处置数量
const handledCount = computed(() => {
  return props.statistics.byStatus[3] + props.statistics.byStatus[4]
})

// 计算待处置数量
const pendingCount = computed(() => {
  return props.statistics.total - handledCount.value
})

// 计算状态列表
const statusList = computed(() => {
  const list = []
  for (let status = 0; status <= 4; status++) {
    const count = props.statistics.byStatus[status as keyof typeof props.statistics.byStatus] || 0
    const config = STATUS_CONFIG[status as keyof typeof STATUS_CONFIG]
    const percentage = props.statistics.total > 0 
      ? Math.round((count / props.statistics.total) * 100) 
      : 0
    
    list.push({
      value: status,
      label: config.label,
      icon: config.icon,
      color: config.color,
      count,
      percentage,
    })
  }
  return list
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;
@use '@/styles/mixins.scss' as *;

.warning-progress-chart {
  @include card;
  padding: 1.5vh 1.5vw;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chart-header {
  margin-bottom: 1.5vh;
  padding-bottom: 1vh;
  border-bottom: 1px solid $border-color;
}

.chart-title {
  @include title(4);
  margin: 0;
  color: $text-primary;
}

.progress-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2vh;
}

.overall-progress {
  padding: 1.5vh 1vw;
  background: rgba(64, 158, 255, 0.1);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: $radius-md;
}

.progress-label {
  @include font-size($font-size-sm);
  color: $text-secondary;
  margin-bottom: 1vh;
  font-weight: 500;
}

.progress-bar-wrapper {
  width: 100%;
  height: 30px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: $radius-sm;
  overflow: hidden;
  position: relative;
  margin-bottom: 0.8vh;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #52c41a 0%, #73d13d 100%);
  border-radius: $radius-sm;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: width 0.5s ease;
  position: relative;
  @include glow(#52c41a, 3px);
}

.progress-text {
  color: #fff;
  font-size: 13px;
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.progress-stats {
  display: flex;
  gap: 2vw;
  @include font-size($font-size-xs);
  color: $text-secondary;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5vw;
}

.status-distribution {
  display: flex;
  flex-direction: column;
  gap: 1.5vh;
}

.status-item {
  display: flex;
  flex-direction: column;
  gap: 0.5vh;
}

.status-header {
  display: flex;
  align-items: center;
  gap: 0.8vw;
  @include font-size($font-size-sm);
}

.status-icon {
  font-size: 18px;
  flex-shrink: 0;
}

.status-name {
  flex: 1;
  color: $text-primary;
  font-weight: 500;
}

.status-count {
  color: $color-primary;
  font-weight: bold;
  min-width: 40px;
  text-align: right;
}

.status-bar-wrapper {
  width: 100%;
  height: 20px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: $radius-sm;
  overflow: hidden;
}

.status-bar {
  height: 100%;
  border-radius: $radius-sm;
  transition: width 0.5s ease;
}

.status-percentage {
  @include font-size($font-size-xs);
  color: $text-muted;
  text-align: right;
  padding-right: 0.5vw;
}
</style>

