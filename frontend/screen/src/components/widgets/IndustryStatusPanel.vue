<template>
  <div class="industry-status-panel">
    <div class="panel-header">
      <h3 class="panel-title">行业态势</h3>
      <div class="panel-subtitle">最新态势数据</div>
    </div>
    <div class="panel-content">
      <div
        v-for="industry in industryList"
        :key="industry.id"
        class="industry-card"
        :class="getIndustryClass(industry.industry_type)"
      >
        <div class="industry-header">
          <div class="industry-icon">{{ getIndustryIcon(industry.industry_type) }}</div>
          <div class="industry-info">
            <div class="industry-name">{{ industry.industry_type_display }}</div>
            <div class="industry-date">{{ formatDate(industry.stat_date) }}</div>
          </div>
        </div>
        <div class="industry-stats">
          <div class="stat-row">
            <div class="stat-item">
              <div class="stat-label">报警</div>
              <div class="stat-value alarm">{{ industry.alarm_count || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">预警</div>
              <div class="stat-value warning">{{ industry.warning_count || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">风险</div>
              <div class="stat-value risk">{{ industry.risk_count || 0 }}</div>
            </div>
          </div>
        </div>
        <div class="risk-levels">
          <div class="risk-level-item red">
            <span class="risk-label">I级</span>
            <span class="risk-value">{{ industry.risk_level_1_count || 0 }}</span>
          </div>
          <div class="risk-level-item orange">
            <span class="risk-label">Ⅱ级</span>
            <span class="risk-value">{{ industry.risk_level_2_count || 0 }}</span>
          </div>
          <div class="risk-level-item yellow">
            <span class="risk-label">Ⅲ级</span>
            <span class="risk-value">{{ industry.risk_level_3_count || 0 }}</span>
          </div>
          <div class="risk-level-item blue">
            <span class="risk-label">Ⅳ级</span>
            <span class="risk-value">{{ industry.risk_level_4_count || 0 }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { getLatestIndustryStatus, type IndustryStatus } from '@/api/modules/safety'

const industryList = ref<IndustryStatus[]>([])

// 行业类型映射
const INDUSTRY_TYPES = {
  1: { name: '森林火灾', icon: '🔥', class: 'forest-fire' },
  2: { name: '防汛', icon: '🌊', class: 'flood-control' },
  3: { name: '交通运输', icon: '🚗', class: 'transportation' },
  4: { name: '危险化学品', icon: '⚠️', class: 'hazardous-chemicals' },
} as const

// 获取行业图标
const getIndustryIcon = (type: number): string => {
  return INDUSTRY_TYPES[type as keyof typeof INDUSTRY_TYPES]?.icon || '📊'
}

// 获取行业样式类
const getIndustryClass = (type: number): string => {
  return INDUSTRY_TYPES[type as keyof typeof INDUSTRY_TYPES]?.class || ''
}

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  })
}

// 加载行业态势数据
const loadIndustryStatus = async () => {
  try {
    console.log('开始加载行业态势数据...')
    const data = await getLatestIndustryStatus()
    
    if (!data || !Array.isArray(data)) {
      console.warn('行业态势数据格式错误，返回空数组')
      industryList.value = []
      return
    }
    
    // 按行业类型排序，确保显示顺序一致（1-森林火灾，2-防汛，3-交通运输，4-危险化学品）
    const sortedData = data.sort((a, b) => a.industry_type - b.industry_type)
    
    // 只取每个行业的最新一条数据（按日期降序排列后取第一条）
    const latestData: IndustryStatus[] = []
    const seenTypes = new Set<number>()
    
    // 先按日期降序排序，再按行业类型排序
    const sortedByDate = sortedData.sort((a, b) => {
      const dateCompare = new Date(b.stat_date).getTime() - new Date(a.stat_date).getTime()
      if (dateCompare !== 0) return dateCompare
      return a.industry_type - b.industry_type
    })
    
    for (const item of sortedByDate) {
      if (!seenTypes.has(item.industry_type)) {
        latestData.push(item)
        seenTypes.add(item.industry_type)
      }
    }
    
    // 确保四个行业都有数据（如果某个行业没有数据，创建一个空数据占位）
    const expectedTypes = [1, 2, 3, 4] // 森林火灾、防汛、交通运输、危险化学品
    const finalData: IndustryStatus[] = []
    
    for (const type of expectedTypes) {
      const existing = latestData.find(item => item.industry_type === type)
      if (existing) {
        finalData.push(existing)
      } else {
        // 如果某个行业没有数据，创建一个空数据占位（可选，或者直接跳过）
        console.warn(`行业类型 ${type} 没有数据`)
      }
    }
    
    industryList.value = finalData
    
    console.log('行业态势数据加载成功:', {
      total: finalData.length,
      industries: finalData.map(item => ({
        id: item.id,
        industry_type: item.industry_type,
        industry_type_display: item.industry_type_display,
        stat_date: item.stat_date,
        alarm_count: item.alarm_count,
        warning_count: item.warning_count,
        risk_count: item.risk_count,
      })),
    })
    
    // 验证是否包含所有四个行业
    if (finalData.length < 4) {
      console.warn(`警告：只加载了 ${finalData.length} 个行业的数据，期望4个行业`)
    }
  } catch (error) {
    console.error('加载行业态势数据失败:', error)
    // API失败时，清空数据并显示错误提示
    industryList.value = []
    
    // 可以在这里添加错误提示，例如使用 ElMessage
    if (window.console && console.error) {
      console.error('行业态势数据加载失败，请检查后端API是否正常', error)
    }
  }
}

let refreshTimer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  loadIndustryStatus()
  // 每1分钟刷新一次数据
  refreshTimer = setInterval(loadIndustryStatus, 60000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;
@use '@/styles/mixins.scss' as *;

.industry-status-panel {
  @include card;
  padding: 1vh 1vw;
  position: absolute;
  top: 2vh;
  left: 2vw;
  width: 24vw;
  min-width: 320px;
  max-width: 420px;
  z-index: 1000;
  max-height: 75vh;
  overflow-y: auto;
}

.panel-header {
  margin-bottom: 1vh;
  border-bottom: 1px solid $border-color;
  padding-bottom: 0.8vh;
}

.panel-title {
  @include title(3);
  margin: 0 0 0.5vh 0;
  color: $text-primary;
}

.panel-subtitle {
  @include font-size($font-size-sm);
  color: $text-secondary;
}

.panel-content {
  display: flex;
  flex-direction: column;
  gap: 1vh;
}

.industry-card {
  background: rgba(64, 158, 255, 0.1);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: $radius-md;
  padding: 1vh 0.8vw;
  transition: all $transition-base;

  &:hover {
    background: rgba(64, 158, 255, 0.15);
    border-color: rgba(64, 158, 255, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.2);
  }

  &.forest-fire {
    border-left: 4px solid #ff4d4f;
  }

  &.flood-control {
    border-left: 4px solid #1890ff;
  }

  &.transportation {
    border-left: 4px solid #faad14;
  }

  &.hazardous-chemicals {
    border-left: 4px solid #ff7875;
  }
}

.industry-header {
  display: flex;
  align-items: center;
  gap: 0.8vw;
  margin-bottom: 0.8vh;
}

.industry-icon {
  font-size: 2vw;
  min-width: 2.5vw;
  text-align: center;
}

.industry-info {
  flex: 1;
}

.industry-name {
  @include font-size($font-size-base);
  font-weight: 600;
  color: $text-primary;
  margin-bottom: 0.3vh;
}

.industry-date {
  @include font-size($font-size-xs);
  color: $text-muted;
}

.industry-stats {
  margin-bottom: 0.8vh;
}

.stat-row {
  display: flex;
  gap: 0.6vw;
}

.stat-item {
  flex: 1;
  text-align: center;
  padding: 0.6vh 0.4vw;
  background: rgba(0, 0, 0, 0.2);
  border-radius: $radius-sm;
}

.stat-label {
  @include font-size($font-size-xs);
  color: $text-secondary;
  margin-bottom: 0.3vh;
}

.stat-value {
  @include font-size($font-size-lg);
  font-weight: bold;

  &.alarm {
    color: #ff4d4f;
  }

  &.warning {
    color: #faad14;
  }

  &.risk {
    color: #ff7875;
  }
}

.risk-levels {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 0.4vw;
}

.risk-level-item {
  text-align: center;
  padding: 0.5vh 0.2vw;
  border-radius: $radius-sm;
  font-size: 10px;

  &.red {
    background: rgba(255, 0, 0, 0.15);
    border: 1px solid rgba(255, 0, 0, 0.3);
  }

  &.orange {
    background: rgba(255, 165, 0, 0.15);
    border: 1px solid rgba(255, 165, 0, 0.3);
  }

  &.yellow {
    background: rgba(255, 255, 0, 0.15);
    border: 1px solid rgba(255, 255, 0, 0.3);
  }

  &.blue {
    background: rgba(0, 0, 255, 0.15);
    border: 1px solid rgba(0, 0, 255, 0.3);
  }
}

.risk-label {
  display: block;
  color: $text-secondary;
  margin-bottom: 0.15vh;
  font-size: 9px;
}

.risk-value {
  display: block;
  font-weight: bold;
  color: $text-primary;
  font-size: 11px;
}
</style>

