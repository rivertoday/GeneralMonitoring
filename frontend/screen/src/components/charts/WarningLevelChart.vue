<template>
  <div class="warning-level-chart">
    <div class="chart-header">
      <h4 class="chart-title">预警级别分布</h4>
      <div class="chart-tabs">
        <button
          class="tab-btn"
          :class="{ active: chartType === 'pie' }"
          @click="chartType = 'pie'"
        >
          饼图
        </button>
        <button
          class="tab-btn"
          :class="{ active: chartType === 'bar' }"
          @click="chartType = 'bar'"
        >
          柱状图
        </button>
      </div>
    </div>
    <div ref="chartContainer" class="chart-container" v-show="hasData && !loading"></div>
    <div v-if="loading" class="chart-loading">加载中...</div>
    <div v-else-if="!hasData" class="chart-empty">暂无数据</div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

interface Props {
  statistics: {
    total: number
    byLevel: {
      1: number // 红色I级
      2: number // 橙色Ⅱ级
      3: number // 黄色Ⅲ级
      4: number // 蓝色Ⅳ级
    }
  }
}

const props = defineProps<Props>()

const chartContainer = ref<HTMLDivElement | null>(null)
let chartInstance: echarts.ECharts | null = null
const chartType = ref<'pie' | 'bar'>('pie')
const loading = ref(false)

// 预警级别配置
const LEVEL_CONFIG = {
  1: { name: 'I级', color: '#ff4d4f', label: '红色I级' },
  2: { name: 'Ⅱ级', color: '#ffa940', label: '橙色Ⅱ级' },
  3: { name: 'Ⅲ级', color: '#ffd666', label: '黄色Ⅲ级' },
  4: { name: 'Ⅳ级', color: '#1890ff', label: '蓝色Ⅳ级' },
}

// 计算是否有数据
const hasData = computed(() => {
  return props.statistics.total > 0
})

// 准备图表数据
const chartData = computed(() => {
  const data = []
  for (let level = 1; level <= 4; level++) {
    const count = props.statistics.byLevel[level as keyof typeof props.statistics.byLevel] || 0
    if (count > 0) {
      data.push({
        name: LEVEL_CONFIG[level as keyof typeof LEVEL_CONFIG].label,
        value: count,
        level: level,
      })
    }
  }
  return data
})

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) {
    return
  }

  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }

  chartInstance = echarts.init(chartContainer.value)
  updateChart()
  
  // 监听窗口大小变化
  window.addEventListener('resize', handleResize)
}

// 更新图表
const updateChart = () => {
  if (!chartInstance || !hasData.value) {
    return
  }

  const option = chartType.value === 'pie' ? getPieOption() : getBarOption()
  chartInstance.setOption(option, true)
}

// 饼图配置
const getPieOption = () => {
  return {
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
      right: 10,
      top: 'center',
      textStyle: {
        color: '#e0e0e0',
        fontSize: 12,
      },
      itemWidth: 12,
      itemHeight: 12,
    },
    series: [
      {
        name: '预警级别',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['40%', '50%'],
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
          fontSize: 12,
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
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
        data: chartData.value.map((item) => ({
          ...item,
          itemStyle: {
            color: LEVEL_CONFIG[item.level as keyof typeof LEVEL_CONFIG].color,
          },
        })),
      },
    ],
  }
}

// 柱状图配置
const getBarOption = () => {
  const categories = chartData.value.map((item) => item.name)
  const values = chartData.value.map((item) => item.value)
  const colors = chartData.value.map((item) => 
    LEVEL_CONFIG[item.level as keyof typeof LEVEL_CONFIG].color
  )

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: 'rgba(64, 158, 255, 0.5)',
      borderWidth: 1,
      textStyle: {
        color: '#fff',
      },
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%',
      top: '10%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        color: '#e0e0e0',
        fontSize: 12,
        rotate: 0,
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.2)',
        },
      },
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#e0e0e0',
        fontSize: 12,
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.2)',
        },
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.1)',
          type: 'dashed',
        },
      },
    },
    series: [
      {
        name: '预警数量',
        type: 'bar',
        data: values.map((value, index) => ({
          value,
          itemStyle: {
            color: colors[index],
            borderRadius: [4, 4, 0, 0],
          },
        })),
        label: {
          show: true,
          position: 'top',
          color: '#e0e0e0',
          fontSize: 12,
          formatter: '{c}',
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  }
}

// 处理窗口大小变化
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

// 监听图表类型变化
watch(chartType, () => {
  updateChart()
})

// 监听统计数据变化
watch(
  () => props.statistics,
  () => {
    updateChart()
  },
  { deep: true }
)

onMounted(() => {
  nextTick(() => {
    initChart()
  })
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;
@use '@/styles/mixins.scss' as *;

.warning-level-chart {
  padding: 1.5vh 1.5vw;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5vh;
  padding-bottom: 1vh;
  border-bottom: 1px solid $border-color;
}

.chart-title {
  @include title(4);
  margin: 0;
  color: $text-primary;
}

.chart-tabs {
  display: flex;
  gap: 0.5vw;
}

.tab-btn {
  padding: 0.5vh 1vw;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: $radius-sm;
  color: $text-secondary;
  font-size: 12px;
  cursor: pointer;
  transition: all $transition-base;

  &:hover {
    background: rgba(64, 158, 255, 0.1);
    border-color: rgba(64, 158, 255, 0.3);
    color: $color-primary;
  }

  &.active {
    background: rgba(64, 158, 255, 0.2);
    border-color: $color-primary;
    color: $color-primary;
    font-weight: 600;
  }
}

.chart-container {
  flex: 1;
  min-height: 0;
  width: 100%;
}

.chart-loading,
.chart-empty {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  color: $text-muted;
  @include font-size($font-size-sm);
}
</style>

