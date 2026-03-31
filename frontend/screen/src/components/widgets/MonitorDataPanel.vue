<template>
  <div class="monitor-data-panel">
    <div class="panel-header">
      <h3 class="panel-title">实时监测数据</h3>
      <div class="panel-subtitle">监测点状态统计</div>
    </div>
    <div class="panel-content">
      <!-- 总体统计 -->
      <div class="overview-stats">
        <div class="stat-card total">
          <div class="stat-icon">📊</div>
          <div class="stat-info">
            <div class="stat-label">监测点总数</div>
            <div class="stat-value">{{ statistics.total_count || 0 }}</div>
          </div>
        </div>
        <div class="stat-card online">
          <div class="stat-icon">🟢</div>
          <div class="stat-info">
            <div class="stat-label">在线监测点</div>
            <div class="stat-value">{{ statistics.online_count || 0 }}</div>
            <div class="stat-desc">在线率: {{ statistics.online_rate || 0 }}%</div>
          </div>
        </div>
        <div class="stat-card offline">
          <div class="stat-icon">🔴</div>
          <div class="stat-info">
            <div class="stat-label">离线监测点</div>
            <div class="stat-value">{{ statistics.offline_count || 0 }}</div>
          </div>
        </div>
      </div>

      <!-- Tab切换：报警记录统计 / 预警级别分布 -->
      <div class="chart-tabs-section">
        <div class="chart-tabs-header">
          <button
            class="chart-tab-btn"
            :class="{ active: chartTab === 'alarm' }"
            @click="chartTab = 'alarm'"
          >
            报警记录统计
          </button>
          <button
            class="chart-tab-btn"
            :class="{ active: chartTab === 'warning' }"
            @click="chartTab = 'warning'"
          >
            预警级别分布
          </button>
        </div>
        <div class="chart-tabs-content">
          <!-- 报警记录统计饼图 -->
          <div v-show="chartTab === 'alarm'" class="chart-wrapper">
            <div ref="alarmChartContainer" class="chart-container" v-show="hasAlarmData && !loading"></div>
            <div v-if="loading" class="chart-loading">加载中...</div>
            <div v-else-if="!hasAlarmData" class="chart-empty">暂无数据</div>
          </div>
          <!-- 预警级别分布饼图 -->
          <div v-show="chartTab === 'warning'" class="chart-wrapper">
            <div ref="warningChartContainer" class="chart-container" v-show="hasWarningData && !loading"></div>
            <div v-if="loading" class="chart-loading">加载中...</div>
            <div v-else-if="!hasWarningData" class="chart-empty">暂无数据</div>
          </div>
        </div>
      </div>
    </div>
    <!-- 最后更新时间 -->
    <div class="panel-footer" v-if="lastUpdateTime">
      <div class="update-time">更新于: {{ formatUpdateTime(lastUpdateTime) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getVideoMonitorStatistics, type VideoMonitorStatistics } from '@/api/modules/safety'
import { useAlarmMarkers } from '@/composables/useAlarmMarkers'
import { ALARM_STATUS_COLORS } from '@/composables/useAlarmMarkers'
import { useRefreshStrategy } from '@/composables/useRefreshStrategy'

interface Props {
  warningStatistics?: {
    total: number
    byLevel: Record<number, number>
  }
}

const props = withDefaults(defineProps<Props>(), {
  warningStatistics: () => ({ total: 0, byLevel: {} }),
})

const statistics = ref<VideoMonitorStatistics>({
  total_count: 0,
  online_count: 0,
  offline_count: 0,
  online_rate: 0,
  type_stats: [],
  industry_stats: [],
})

// 使用报警记录统计
const { alarmStatistics, loadAlarmRecords } = useAlarmMarkers()

// Tab切换
const chartTab = ref<'alarm' | 'warning'>('alarm')
const loading = ref(false)

// 图表容器和实例
const alarmChartContainer = ref<HTMLDivElement | null>(null)
const warningChartContainer = ref<HTMLDivElement | null>(null)
let alarmChartInstance: echarts.ECharts | null = null
let warningChartInstance: echarts.ECharts | null = null

// 计算是否有数据
const hasAlarmData = computed(() => alarmStatistics.value.total > 0)
const hasWarningData = computed(() => props.warningStatistics.total > 0)

// 报警记录饼图数据
const alarmChartData = computed(() => {
  const data = []
  const statusConfig = {
    0: { name: '未处理', color: ALARM_STATUS_COLORS[0] },
    1: { name: '处理中', color: ALARM_STATUS_COLORS[1] },
    2: { name: '已处理', color: ALARM_STATUS_COLORS[2] },
    3: { name: '已忽略', color: ALARM_STATUS_COLORS[3] },
  }
  
  for (let status = 0; status <= 3; status++) {
    const count = (alarmStatistics.value.byStatus as Record<number, number>)[status] || 0
    if (count > 0) {
      data.push({
        name: statusConfig[status as keyof typeof statusConfig].name,
        value: count,
        status: status,
        itemStyle: {
          color: statusConfig[status as keyof typeof statusConfig].color,
        },
      })
    }
  }
  return data
})

// 预警级别饼图数据
const warningChartData = computed(() => {
  const data = []
  const levelConfig = {
    1: { name: '红色I级', color: '#ff4d4f' },
    2: { name: '橙色Ⅱ级', color: '#ffa940' },
    3: { name: '黄色Ⅲ级', color: '#ffd666' },
    4: { name: '蓝色Ⅳ级', color: '#1890ff' },
  }
  
  for (let level = 1; level <= 4; level++) {
    const count = props.warningStatistics.byLevel[level] || 0
    if (count > 0) {
      data.push({
        name: levelConfig[level as keyof typeof levelConfig].name,
        value: count,
        level: level,
        itemStyle: {
          color: levelConfig[level as keyof typeof levelConfig].color,
        },
      })
    }
  }
  return data
})

// 初始化报警记录饼图
const initAlarmChart = () => {
  if (!alarmChartContainer.value) return
  
  if (alarmChartInstance) {
    alarmChartInstance.dispose()
    alarmChartInstance = null
  }
  
  alarmChartInstance = echarts.init(alarmChartContainer.value)
  updateAlarmChart()
}

// 更新报警记录饼图
const updateAlarmChart = () => {
  if (!alarmChartInstance || !hasAlarmData.value) return
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: 'rgba(64, 158, 255, 0.5)',
      borderWidth: 1,
      textStyle: {
        color: '#fff',
      },
    },
    legend: {
      orient: 'vertical',
      right: 5,
      top: 'center',
      textStyle: {
        color: '#e0e0e0',
        fontSize: 11,
      },
      itemWidth: 10,
      itemHeight: 10,
    },
    series: [
      {
        name: '报警状态',
        type: 'pie',
        radius: ['35%', '65%'],
        center: ['45%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: 'rgba(0, 0, 0, 0.3)',
          borderWidth: 2,
        },
        label: {
          show: true,
          formatter: '{b}\n{c} ({d}%)',
          color: '#e0e0e0',
          fontSize: 11,
        },
        labelLine: {
          show: true,
          lineStyle: {
            color: '#e0e0e0',
          },
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold',
          },
          itemStyle: {
            shadowBlur: 20,
            shadowOffsetX: 0,
            shadowOffsetY: 0,
            shadowColor: 'rgba(0, 0, 0, 0.8)',
          },
          scale: true,
          scaleSize: 10,
        },
        data: alarmChartData.value,
      },
    ],
  }
  
  alarmChartInstance.setOption(option, true)
}

// 初始化预警级别饼图
const initWarningChart = () => {
  if (!warningChartContainer.value) return
  
  if (warningChartInstance) {
    warningChartInstance.dispose()
    warningChartInstance = null
  }
  
  warningChartInstance = echarts.init(warningChartContainer.value)
  updateWarningChart()
}

// 更新预警级别饼图
const updateWarningChart = () => {
  if (!warningChartInstance || !hasWarningData.value) return
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: 'rgba(64, 158, 255, 0.5)',
      borderWidth: 1,
      textStyle: {
        color: '#fff',
      },
    },
    legend: {
      orient: 'vertical',
      right: 5,
      top: 'center',
      textStyle: {
        color: '#e0e0e0',
        fontSize: 11,
      },
      itemWidth: 10,
      itemHeight: 10,
    },
    series: [
      {
        name: '预警级别',
        type: 'pie',
        radius: ['35%', '65%'],
        center: ['45%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 8,
          borderColor: 'rgba(0, 0, 0, 0.3)',
          borderWidth: 2,
        },
        label: {
          show: true,
          formatter: '{b}\n{c} ({d}%)',
          color: '#e0e0e0',
          fontSize: 11,
        },
        labelLine: {
          show: true,
          lineStyle: {
            color: '#e0e0e0',
          },
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold',
          },
          itemStyle: {
            shadowBlur: 20,
            shadowOffsetX: 0,
            shadowOffsetY: 0,
            shadowColor: 'rgba(0, 0, 0, 0.8)',
          },
          scale: true,
          scaleSize: 10,
        },
        data: warningChartData.value,
      },
    ],
  }
  
  warningChartInstance.setOption(option, true)
}

// 处理窗口大小变化
const handleResize = () => {
  if (alarmChartInstance) {
    alarmChartInstance.resize()
  }
  if (warningChartInstance) {
    warningChartInstance.resize()
  }
}

// 监听数据变化和 tab 切换
watch([alarmChartData, () => chartTab.value], () => {
  if (chartTab.value === 'alarm') {
    nextTick(() => {
      if (hasAlarmData.value && alarmChartContainer.value) {
        if (!alarmChartInstance) {
          initAlarmChart()
        } else {
          updateAlarmChart()
        }
      }
    })
  }
}, { immediate: true })

watch([warningChartData, () => chartTab.value], () => {
  if (chartTab.value === 'warning') {
    nextTick(() => {
      if (hasWarningData.value && warningChartContainer.value) {
        if (!warningChartInstance) {
          initWarningChart()
        } else {
          updateWarningChart()
        }
      }
    })
  }
}, { immediate: true })


// 加载统计数据
const loadStatistics = async () => {
  try {
    console.log('开始加载视频监控统计...')
    const data = await getVideoMonitorStatistics()
    statistics.value = data
    
    // 验证数据有效性
    if (!data || typeof data.total_count !== 'number') {
      console.warn('视频监控统计格式错误，返回空数据')
      statistics.value = {
        total_count: 0,
        online_count: 0,
        offline_count: 0,
        online_rate: 0,
        type_stats: [],
        industry_stats: [],
      }
      return
    }
    
    console.log('视频监控统计加载成功:', {
      total: data.total_count,
      online: data.online_count,
      offline: data.offline_count,
      onlineRate: data.online_rate,
      industryCount: data.industry_stats.length,
    })
    
    // 验证行业统计数据
    if (data.industry_stats && data.industry_stats.length > 0) {
      const industryNames: Record<number, string> = {
        1: '森林火灾',
        2: '防汛',
        3: '交通运输',
        4: '危险化学品',
      }
      const industryStr = data.industry_stats
        .map(item => `${industryNames[item.industry_type] || '未知'}: ${item.count}`)
        .join(', ')
      console.log(`行业统计: ${industryStr}`)
    }
  } catch (error) {
    console.error('加载视频监控统计失败:', error)
    // API失败时，清空数据，不显示模拟数据
    statistics.value = {
      total_count: 0,
      online_count: 0,
      offline_count: 0,
      online_rate: 0,
      type_stats: [],
      industry_stats: [],
    }
    
    // 可以在这里添加错误提示，例如使用 ElMessage
    if (window.console && console.error) {
      console.error('视频监控统计加载失败，请检查后端API是否正常', error)
    }
  }
}

// 格式化更新时间
const formatUpdateTime = (date: Date | null): string => {
  if (!date) return ''
  const hours = String(date.getHours()).padStart(2, '0')
  const minutes = String(date.getMinutes()).padStart(2, '0')
  const seconds = String(date.getSeconds()).padStart(2, '0')
  return `${hours}:${minutes}:${seconds}`
}

// 使用刷新策略（实时数据，30秒刷新一次）
const { startRefresh: startDataRefresh, stopRefresh: stopDataRefresh, lastUpdateTime } = useRefreshStrategy(
  async () => {
    await Promise.all([
      loadStatistics(),
      loadAlarmRecords(),
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

onMounted(() => {
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
  
  // 启动定时刷新（会在immediate=true时立即执行一次）
  startDataRefresh()
})

// 监听 tab 切换，初始化对应图表
watch(() => chartTab.value, (newTab) => {
  nextTick(() => {
    if (newTab === 'alarm' && hasAlarmData.value && alarmChartContainer.value && !alarmChartInstance) {
      initAlarmChart()
    } else if (newTab === 'warning' && hasWarningData.value && warningChartContainer.value && !warningChartInstance) {
      initWarningChart()
    }
  })
})

onUnmounted(() => {
  stopDataRefresh()
  
  window.removeEventListener('resize', handleResize)
  
  if (alarmChartInstance) {
    alarmChartInstance.dispose()
    alarmChartInstance = null
  }
  if (warningChartInstance) {
    warningChartInstance.dispose()
    warningChartInstance = null
  }
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;
@use '@/styles/mixins.scss' as *;

.monitor-data-panel {
  @include card;
  padding: 1.5vh 1.5vw;
  position: absolute;
  top: 2vh;
  left: 2vw;
  width: 20vw;
  min-width: 280px;
  max-width: 360px;
  z-index: 1000;
  max-height: 85vh;
  overflow-y: auto;
}

.panel-header {
  margin-bottom: 1.5vh;
  border-bottom: 1px solid $border-color;
  padding-bottom: 1vh;
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
  gap: 2vh;
}

.overview-stats {
  display: flex;
  flex-direction: column;
  gap: 1.2vh;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 1vw;
  padding: 1.5vh 1.2vw;
  background: rgba(64, 158, 255, 0.1);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: $radius-md;
  transition: all $transition-base;

  &:hover {
    background: rgba(64, 158, 255, 0.15);
    border-color: rgba(64, 158, 255, 0.5);
    transform: translateX(5px);
  }

  &.total {
    border-left: 4px solid #409eff;
  }

  &.online {
    border-left: 4px solid #52c41a;
  }

  &.offline {
    border-left: 4px solid #ff4d4f;
  }
}

.stat-icon {
  font-size: 2.5vw;
  min-width: 3vw;
  text-align: center;
}

.stat-info {
  flex: 1;
}

.stat-label {
  @include font-size($font-size-sm);
  color: $text-secondary;
  margin-bottom: 0.5vh;
}

.stat-value {
  @include font-size($font-size-2xl);
  color: $color-primary;
  font-weight: bold;
  margin-bottom: 0.3vh;
  @include glow($color-primary, 5px);
}

.stat-desc {
  @include font-size($font-size-xs);
  color: $text-muted;
}

.alarm-stats {
  margin-top: 1vh;
  margin-bottom: 1vh;
}

.alarm-stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1vh;
}

.alarm-stat-card {
  display: flex;
  align-items: center;
  gap: 0.8vw;
  padding: 1.2vh 1vw;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: $radius-sm;
  transition: all $transition-base;

  &:hover {
    background: rgba(64, 158, 255, 0.1);
    border-color: rgba(64, 158, 255, 0.3);
  }

  &.total {
    border-left: 3px solid #409eff;
  }

  &.unhandled {
    border-left: 3px solid #ff4d4f;
  }

  &.handling {
    border-left: 3px solid #ffa940;
  }

  &.handled {
    border-left: 3px solid #52c41a;
  }
}

.alarm-stat-icon {
  font-size: 2vw;
  min-width: 2.5vw;
  text-align: center;
  flex-shrink: 0;
}

.alarm-stat-info {
  flex: 1;
  min-width: 0;
}

.alarm-stat-label {
  @include font-size($font-size-xs);
  color: $text-secondary;
  margin-bottom: 0.3vh;
}

.alarm-stat-value {
  @include font-size($font-size-lg);
  color: $color-primary;
  font-weight: bold;
  @include glow($color-primary, 3px);
}

.chart-tabs-section {
  margin-top: 1vh;
  margin-bottom: 1vh;
}

.chart-tabs-header {
  display: flex;
  gap: 0.5vw;
  margin-bottom: 1vh;
  border-bottom: 1px solid $border-color;
  padding-bottom: 0.8vh;
}

.chart-tab-btn {
  flex: 1;
  padding: 0.8vh 0.8vw;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: $text-secondary;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all $transition-base;
  text-align: center;
  white-space: nowrap;

  &:hover {
    color: $color-primary;
    background: rgba(64, 158, 255, 0.1);
  }

  &.active {
    color: $color-primary;
    border-bottom-color: $color-primary;
    font-weight: 600;
  }
}

.chart-tabs-content {
  min-height: 200px;
  position: relative;
}

.chart-wrapper {
  width: 100%;
  height: 100%;
}

.chart-container {
  width: 100%;
  height: 220px;
  min-height: 180px;
}

.panel-footer {
  margin-top: 1vh;
  padding-top: 1vh;
  border-top: 1px solid rgba(64, 158, 255, 0.2);
  text-align: center;
}

.update-time {
  @include font-size($font-size-xs);
  color: $text-secondary;
  opacity: 0.8;
}

.chart-loading,
.chart-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 220px;
  min-height: 180px;
  color: $text-muted;
  @include font-size($font-size-sm);
}
</style>

