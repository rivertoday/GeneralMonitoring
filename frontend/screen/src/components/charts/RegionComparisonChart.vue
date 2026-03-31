<template>
  <div class="region-comparison-chart">
    <div class="chart-header">
      <h4 class="chart-title">区域态势对比</h4>
      <div class="chart-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          class="tab-btn"
          :class="{ active: currentTab === tab.value }"
          @click="currentTab = tab.value"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>
    <div ref="chartContainer" class="chart-container" v-show="regionStatusList.length > 0 && !loading"></div>
    <div v-if="loading" class="chart-loading">加载中...</div>
    <div v-else-if="!regionStatusList.length" class="chart-empty">暂无数据</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { getColorMapData, type RegionStatus } from '@/api/modules/safety'

// 移除 props，改为从API获取数据
// interface Props {
//   data: RegionStatus[]
// }
// const props = defineProps<Props>()

const chartContainer = ref<HTMLDivElement | null>(null)
let chartInstance: echarts.ECharts | null = null
const currentTab = ref<'alarm' | 'warning' | 'risk' | 'risk_level'>('alarm')
const regionStatusList = ref<RegionStatus[]>([])
const loading = ref(false)

const tabs = [
  { label: '报警数量', value: 'alarm' as const },
  { label: '预警数量', value: 'warning' as const },
  { label: '风险数量', value: 'risk' as const },
  { label: '风险等级', value: 'risk_level' as const },
]

// 初始化图表
const initChart = () => {
  if (!chartContainer.value) {
    console.warn('图表容器不存在，无法初始化图表')
    return
  }

  if (chartInstance) {
    console.log('图表已存在，先销毁旧实例')
    chartInstance.dispose()
    chartInstance = null
  }

  console.log('初始化图表实例', {
    containerWidth: chartContainer.value.offsetWidth,
    containerHeight: chartContainer.value.offsetHeight
  })
  
  chartInstance = echarts.init(chartContainer.value)
  updateChart()
}

// 更新图表
const updateChart = () => {
  if (!chartInstance) {
    console.warn('图表实例不存在，无法更新图表')
    return
  }
  
  if (!regionStatusList.value.length) {
    console.warn('区域态势数据为空，跳过图表更新')
    return
  }

  // 验证数据准确性
  const isValid = validateChartData()
  if (!isValid) {
    console.warn('[数据验证] 数据验证失败，但继续更新图表')
  }

  const option = getChartOption()
  console.log('更新图表配置', {
    dataLength: regionStatusList.value.length,
    currentTab: currentTab.value,
    streets: regionStatusList.value.map(r => r.street),
    dataValid: isValid,
  })
  
  chartInstance.setOption(option, true)
  
  // 验证图表渲染后的数据一致性
  setTimeout(() => {
    if (chartInstance) {
      chartInstance.resize()
      
      // 获取图表实际渲染的数据
      const chartOption = chartInstance.getOption()
      if (chartOption && Array.isArray(chartOption)) {
        const series = chartOption[0]?.series?.[0]
        if (series && series.data) {
          console.log('[数据验证] 图表渲染数据验证:', {
            xAxisData: chartOption[0]?.xAxis?.[0]?.data || [],
            seriesData: series.data || [],
            dataMatch: (chartOption[0]?.xAxis?.[0]?.data?.length || 0) === (series.data?.length || 0),
          })
        }
      }
    }
  }, 100)
}

/**
 * 验证图表数据准确性
 */
const validateChartData = () => {
  if (!regionStatusList.value.length) {
    console.warn('[数据验证] 区域态势数据为空，跳过验证')
    return false
  }

  const streets = regionStatusList.value.map((item) => item.street)
  
  // 验证数据完整性
  const validationResults = {
    total: regionStatusList.value.length,
    streets: streets.length,
    dataConsistency: true,
    dataMapping: [] as Array<{
      street: string
      alarm_count: number
      warning_count: number
      risk_count: number
      risk_level_total: number
      risk_level_breakdown: {
        level1: number
        level2: number
        level3: number
        level4: number
      }
    }>,
    errors: [] as string[],
  }

  // 验证每个区域的数据
  regionStatusList.value.forEach((item, index) => {
    // 验证字段完整性
    if (typeof item.alarm_count !== 'number') {
      validationResults.errors.push(`区域 ${item.street}: alarm_count 不是数字类型`)
      validationResults.dataConsistency = false
    }
    if (typeof item.warning_count !== 'number') {
      validationResults.errors.push(`区域 ${item.street}: warning_count 不是数字类型`)
      validationResults.dataConsistency = false
    }
    if (typeof item.risk_count !== 'number') {
      validationResults.errors.push(`区域 ${item.street}: risk_count 不是数字类型`)
      validationResults.dataConsistency = false
    }
    if (typeof item.risk_level_1_count !== 'number' || 
        typeof item.risk_level_2_count !== 'number' ||
        typeof item.risk_level_3_count !== 'number' ||
        typeof item.risk_level_4_count !== 'number') {
      validationResults.errors.push(`区域 ${item.street}: 风险等级数量字段不完整`)
      validationResults.dataConsistency = false
    }

    // 计算风险等级总数
    const riskLevelTotal = (item.risk_level_1_count || 0) + 
                          (item.risk_level_2_count || 0) + 
                          (item.risk_level_3_count || 0) + 
                          (item.risk_level_4_count || 0)

    validationResults.dataMapping.push({
      street: item.street,
      alarm_count: item.alarm_count || 0,
      warning_count: item.warning_count || 0,
      risk_count: item.risk_count || 0,
      risk_level_total: riskLevelTotal,
      risk_level_breakdown: {
        level1: item.risk_level_1_count || 0,
        level2: item.risk_level_2_count || 0,
        level3: item.risk_level_3_count || 0,
        level4: item.risk_level_4_count || 0,
      },
    })

    // 验证街道名称唯一性
    const duplicateStreets = streets.filter(s => s === item.street)
    if (duplicateStreets.length > 1) {
      validationResults.errors.push(`区域名称重复: ${item.street}`)
      validationResults.dataConsistency = false
    }
  })

  // 验证X轴和Y轴数据长度一致
  if (streets.length !== regionStatusList.value.length) {
    validationResults.errors.push(`X轴数据长度(${streets.length})与Y轴数据长度(${regionStatusList.value.length})不一致`)
    validationResults.dataConsistency = false
  }

  // 输出验证结果
  if (validationResults.errors.length > 0) {
    console.error('[数据验证] ❌ 数据验证失败:', {
      errors: validationResults.errors,
      dataMapping: validationResults.dataMapping,
    })
    return false
  } else {
    console.log('[数据验证] ✅ 数据验证通过:', {
      total: validationResults.total,
      dataMapping: validationResults.dataMapping,
    })
    return true
  }
}

// 获取图表配置
const getChartOption = () => {
  const streets = regionStatusList.value.map((item) => item.street)
  
  let data: number[] = []
  let title = ''
  let color = '#409eff'
  let dataField = '' // 用于验证的数据字段名称

  switch (currentTab.value) {
    case 'alarm':
      data = regionStatusList.value.map((item) => item.alarm_count || 0)
      title = '报警数量对比'
      color = '#ff4d4f'
      dataField = 'alarm_count'
      break
    case 'warning':
      data = regionStatusList.value.map((item) => item.warning_count || 0)
      title = '预警数量对比'
      color = '#faad14'
      dataField = 'warning_count'
      break
    case 'risk':
      data = regionStatusList.value.map((item) => item.risk_count || 0)
      title = '风险数量对比'
      color = '#ff7875'
      dataField = 'risk_count'
      break
    case 'risk_level':
      // 风险等级：计算总风险等级数量（I级+II级+III级+IV级）
      data = regionStatusList.value.map((item) => {
        const total = (item.risk_level_1_count || 0) + 
                     (item.risk_level_2_count || 0) + 
                     (item.risk_level_3_count || 0) + 
                     (item.risk_level_4_count || 0)
        return total
      })
      title = '风险等级总数对比'
      color = '#722ed1'
      dataField = 'risk_level_total'
      break
  }

  // 验证当前标签的数据准确性
  console.log(`[数据验证] 当前标签 "${title}" 数据验证:`, {
    tab: currentTab.value,
    dataField,
    streetsCount: streets.length,
    dataCount: data.length,
    dataMapping: streets.map((street, index) => ({
      street,
      value: data[index],
      sourceData: regionStatusList.value[index],
    })),
    totalValue: data.reduce((sum, val) => sum + val, 0),
  })

  return {
    title: {
      text: title,
      left: 'center',
      top: 10,
      textStyle: {
        color: '#e0e0e0',
        fontSize: 16,
        fontWeight: 'bold',
      },
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
      },
      backgroundColor: 'rgba(0, 20, 40, 0.9)',
      borderColor: 'rgba(64, 158, 255, 0.5)',
      borderWidth: 1,
      textStyle: {
        color: '#e0e0e0',
      },
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%',
      top: '20%',
      containLabel: true,
    },
    xAxis: {
      type: 'category',
      data: streets,
      axisLabel: {
        color: '#999',
        rotate: 45,
        fontSize: 12,
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
        color: '#999',
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
        },
      },
    },
    series: [
      {
        name: title,
        type: 'bar',
        data: data,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: color },
            { offset: 1, color: color + '80' },
          ]),
          borderRadius: [4, 4, 0, 0],
        },
        label: {
          show: true,
          position: 'top',
          color: '#e0e0e0',
          fontSize: 12,
        },
        emphasis: {
          itemStyle: {
            color: color,
          },
        },
      },
    ],
  }
}

// 加载区域态势数据
const loadRegionStatus = async () => {
  try {
    loading.value = true
    console.log('开始加载区域态势对比数据...')
    const data = await getColorMapData()
    
    if (!data || !Array.isArray(data)) {
      console.warn('区域态势数据格式错误，返回空数组')
      regionStatusList.value = []
      return
    }
    
    regionStatusList.value = data
    console.log('区域态势对比数据加载成功:', {
      total: data.length,
      regions: data.map(r => ({
        id: r.id,
        street: r.street,
        alarm_count: r.alarm_count,
        warning_count: r.warning_count,
        risk_count: r.risk_count,
        risk_level_1_count: r.risk_level_1_count,
        risk_level_2_count: r.risk_level_2_count,
        risk_level_3_count: r.risk_level_3_count,
        risk_level_4_count: r.risk_level_4_count,
      })),
    })
    
    // 验证加载的数据准确性
    console.log('[数据验证] 开始验证加载的数据...')
    validateChartData()
    
    // 数据加载完成后，等待 DOM 更新，然后初始化或更新图表
    await nextTick()
    // 再等待一个 tick，确保 DOM 完全渲染
    await new Promise(resolve => setTimeout(resolve, 0))
    
    // 如果图表还未初始化且容器已存在，则初始化图表
    if (!chartInstance && chartContainer.value) {
      console.log('数据加载完成，初始化图表', {
        containerExists: !!chartContainer.value,
        dataLength: regionStatusList.value.length
      })
      initChart()
    } else if (chartInstance) {
      // 如果图表已初始化，直接更新
      console.log('数据加载完成，更新图表', {
        dataLength: regionStatusList.value.length
      })
      updateChart()
    } else {
      console.warn('图表容器不存在或图表未初始化', {
        containerExists: !!chartContainer.value,
        chartInstanceExists: !!chartInstance
      })
    }
  } catch (error) {
    console.error('加载区域态势对比数据失败:', error)
    // API失败时，清空数据
    regionStatusList.value = []
    
    if (window.console && console.error) {
      console.error('区域态势对比数据加载失败，请检查后端API是否正常', error)
    }
  } finally {
    loading.value = false
  }
}

// 监听数据变化
watch(
  () => regionStatusList.value,
  () => {
    // 数据变化时，如果图表未初始化且容器已存在，则初始化图表
    if (!chartInstance && chartContainer.value && regionStatusList.value.length > 0) {
      nextTick(() => {
        initChart()
      })
    } else if (chartInstance) {
      // 如果图表已初始化，直接更新
      updateChart()
    }
  },
  { deep: true }
)

// 监听标签切换
watch(currentTab, (newTab, oldTab) => {
  console.log(`[数据验证] 标签切换: ${oldTab} -> ${newTab}`)
  updateChart()
})

// 窗口大小变化时调整图表
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

let refreshTimer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  window.addEventListener('resize', handleResize)
  // 先加载数据，数据加载完成后再初始化图表（在 loadRegionStatus 中处理）
  loadRegionStatus()
  // 每5分钟刷新一次数据
  refreshTimer = setInterval(loadRegionStatus, 300000) // 5分钟 = 300000毫秒
})

onUnmounted(() => {
  // 清除定时器
  if (refreshTimer) {
    clearInterval(refreshTimer)
    refreshTimer = null
  }
  
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;

.region-comparison-chart {
  background: rgba(0, 20, 40, 0.85);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: 8px;
  padding: 16px;
  backdrop-filter: blur(10px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.chart-header {
  margin-bottom: 16px;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #409eff;
  margin: 0 0 12px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(64, 158, 255, 0.2);
}

.chart-tabs {
  display: flex;
  gap: 8px;
}

.tab-btn {
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

.chart-container {
  width: 100%;
  height: 300px;
  min-height: 300px;
}

.chart-loading,
.chart-empty {
  width: 100%;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 14px;
}
</style>

