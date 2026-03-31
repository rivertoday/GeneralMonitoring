<template>
  <div class="statistics">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>统计分析</h2>
    </div>

    <!-- 选项卡切换 -->
    <el-tabs v-model="activeTab" class="statistics-tabs">
      <!-- 报警统计分析 -->
      <el-tab-pane label="报警统计分析" name="alarm">
        <!-- 搜索筛选区域 -->
        <el-card class="search-card">
          <el-form :model="alarmSearchForm" :inline="true">
            <el-form-item label="统计类型">
              <el-select v-model="alarmSearchForm.stat_type" placeholder="请选择" clearable style="width: 120px">
                <el-option label="日报" :value="1" />
                <el-option label="周报" :value="2" />
                <el-option label="月报" :value="3" />
                <el-option label="年报" :value="4" />
              </el-select>
            </el-form-item>
            <el-form-item label="行业类型">
              <el-select v-model="alarmSearchForm.industry_type" placeholder="请选择" clearable style="width: 150px">
                <el-option label="森林火灾" :value="1" />
                <el-option label="防汛" :value="2" />
                <el-option label="交通运输" :value="3" />
                <el-option label="危险化学品" :value="4" />
              </el-select>
            </el-form-item>
            <el-form-item label="所属街道">
              <el-input
                v-model="alarmSearchForm.street"
                placeholder="请输入街道"
                clearable
                style="width: 150px"
              />
            </el-form-item>
            <el-form-item label="统计日期">
              <el-date-picker
                v-model="alarmDateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="YYYY-MM-DD"
                style="width: 300px"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleAlarmSearch">
                <el-icon><Search /></el-icon>
                搜索
              </el-button>
              <el-button @click="handleAlarmReset">
                <el-icon><Refresh /></el-icon>
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 统计卡片 -->
        <el-row :gutter="20" class="stat-cards">
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-card-content">
                <div class="stat-card-label">报警总数</div>
                <div class="stat-card-value">{{ alarmSummary.total }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-card-content">
                <div class="stat-card-label">未处理</div>
                <div class="stat-card-value text-warning">{{ alarmSummary.unhandled }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-card-content">
                <div class="stat-card-label">已处理</div>
                <div class="stat-card-value text-success">{{ alarmSummary.handled }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="stat-card">
              <div class="stat-card-content">
                <div class="stat-card-label">平均处理时间</div>
                <div class="stat-card-value">
                  {{ alarmSummary.avgHandleTime ? `${alarmSummary.avgHandleTime}分钟` : '-' }}
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 数据表格 -->
        <el-card class="table-card">
          <el-table
            v-loading="alarmLoading"
            :data="alarmTableData"
            stripe
            border
            style="width: 100%"
          >
            <el-table-column prop="stat_date" label="统计日期" width="120" />
            <el-table-column label="统计类型" width="100">
              <template #default="{ row }">
                {{ getStatTypeDisplay(row.stat_type) }}
              </template>
            </el-table-column>
            <el-table-column prop="industry_type_display" label="行业类型" width="120" />
            <el-table-column prop="street" label="所属街道" width="120" />
            <el-table-column prop="alarm_count" label="报警总数" width="100" align="right" />
            <el-table-column prop="unhandled_count" label="未处理" width="100" align="right">
              <template #default="{ row }">
                <span class="text-warning">{{ row.unhandled_count }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="handling_count" label="处理中" width="100" align="right" />
            <el-table-column prop="handled_count" label="已处理" width="100" align="right">
              <template #default="{ row }">
                <span class="text-success">{{ row.handled_count }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="ignored_count" label="已忽略" width="100" align="right" />
            <el-table-column label="平均处理时间" width="120" align="right">
              <template #default="{ row }">
                {{ row.avg_handle_time ? `${row.avg_handle_time}分钟` : '-' }}
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="160" />
          </el-table>

          <!-- 分页 -->
          <div class="pagination">
            <el-pagination
              v-model:current-page="alarmPagination.page"
              v-model:page-size="alarmPagination.pageSize"
              :total="alarmPagination.total"
              :page-sizes="[10, 20, 50, 100]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleAlarmSizeChange"
              @current-change="handleAlarmPageChange"
            />
          </div>
        </el-card>
      </el-tab-pane>

      <!-- 预警统计分析 -->
      <el-tab-pane label="预警统计分析" name="warning">
        <!-- 搜索筛选区域 -->
        <el-card class="search-card">
          <el-form :model="warningSearchForm" :inline="true">
            <el-form-item label="分析类型" prop="analysis_type">
              <el-select v-model="warningSearchForm.analysis_type" placeholder="请选择" style="width: 150px">
                <el-option label="突出预警" :value="1" />
                <el-option label="同比预警" :value="2" />
                <el-option label="环比预警" :value="3" />
              </el-select>
            </el-form-item>
            <el-form-item label="行业类型">
              <el-select v-model="warningSearchForm.industry_type" placeholder="请选择" clearable style="width: 150px">
                <el-option label="森林火灾" :value="1" />
                <el-option label="防汛" :value="2" />
                <el-option label="交通运输" :value="3" />
                <el-option label="危险化学品" :value="4" />
              </el-select>
            </el-form-item>
            <el-form-item label="预警类型">
              <el-input
                v-model="warningSearchForm.warning_type"
                placeholder="请输入预警类型"
                clearable
                style="width: 150px"
              />
            </el-form-item>
            <el-form-item label="所属街道">
              <el-input
                v-model="warningSearchForm.street"
                placeholder="请输入街道"
                clearable
                style="width: 150px"
              />
            </el-form-item>
            <el-form-item label="预警时间">
              <el-date-picker
                v-model="warningTimeRange"
                type="datetimerange"
                range-separator="至"
                start-placeholder="开始时间"
                end-placeholder="结束时间"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 350px"
              />
            </el-form-item>
            <el-form-item
              v-if="warningSearchForm.analysis_type === 2 || warningSearchForm.analysis_type === 3"
              label="对比时间"
            >
              <el-date-picker
                v-model="compareTimeRange"
                type="datetimerange"
                range-separator="至"
                start-placeholder="对比开始时间"
                end-placeholder="对比结束时间"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 350px"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleWarningAnalysis">
                <el-icon><Search /></el-icon>
                分析
              </el-button>
              <el-button @click="handleWarningReset">
                <el-icon><Refresh /></el-icon>
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 分析结果 -->
        <el-card v-if="warningAnalysisResult" class="analysis-result-card">
          <template #header>
            <div class="card-header">
              <span>分析结果</span>
              <el-tag :type="getAnalysisTypeTagType(warningSearchForm.analysis_type)">
                {{ getAnalysisTypeDisplay(warningSearchForm.analysis_type) }}
              </el-tag>
            </div>
          </template>

          <el-descriptions :column="3" border>
            <el-descriptions-item label="当前时间段预警数量">
              {{ warningAnalysisResult.current_count || 0 }}
            </el-descriptions-item>
            <el-descriptions-item
              v-if="warningSearchForm.analysis_type === 2 || warningSearchForm.analysis_type === 3"
              label="对比时间段预警数量"
            >
              {{ warningAnalysisResult.compare_count || 0 }}
            </el-descriptions-item>
            <el-descriptions-item
              v-if="warningSearchForm.analysis_type === 2 || warningSearchForm.analysis_type === 3"
              label="变化趋势"
            >
              <el-tag
                :type="
                  warningAnalysisResult.change_rate && warningAnalysisResult.change_rate > 0
                    ? 'danger'
                    : 'success'
                "
              >
                {{
                  warningAnalysisResult.change_rate
                    ? `${warningAnalysisResult.change_rate > 0 ? '+' : ''}${(
                        warningAnalysisResult.change_rate * 100
                      ).toFixed(2)}%`
                    : '-'
                }}
              </el-tag>
            </el-descriptions-item>
          </el-descriptions>

          <!-- 预警列表 -->
          <div v-if="warningAnalysisData.length > 0" class="warning-analysis-list">
            <h4>预警数据</h4>
            <el-table :data="warningAnalysisData" stripe border style="width: 100%" max-height="400">
              <el-table-column prop="warning_code" label="预警编码" width="150" />
              <el-table-column prop="warning_title" label="预警标题" min-width="200" show-overflow-tooltip />
              <el-table-column label="预警级别" width="120">
                <template #default="{ row }">
                  <el-tag
                    v-if="row.warning_level_detail"
                    :type="getLevelTagType(row.warning_level_detail.level_color)"
                  >
                    {{ row.warning_level_detail.level_name }}
                  </el-tag>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column prop="industry_type_display" label="行业类型" width="120" />
              <el-table-column prop="warning_type" label="预警类型" width="120" />
              <el-table-column prop="street" label="所属街道" width="120" />
              <el-table-column prop="warning_time" label="预警时间" width="160" />
            </el-table>
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Refresh } from '@element-plus/icons-vue'
import { riskStatisticsApi, warningLevelApi } from '@/api/modules/risk'
import type {
  AlarmStatistics,
  AlarmStatisticsParams,
  WarningAnalysisParams,
  RiskWarning,
  WarningLevel,
} from '@/types/modules/risk'

// 当前选项卡
const activeTab = ref('alarm')

// 预警级别列表
const warningLevels = ref<WarningLevel[]>([])

// ========== 报警统计分析 ==========
const alarmLoading = ref(false)
const alarmTableData = ref<AlarmStatistics[]>([])
const alarmPagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

const alarmSearchForm = reactive<AlarmStatisticsParams>({
  stat_type: undefined,
  industry_type: undefined,
  street: undefined,
  start_date: undefined,
  end_date: undefined,
})

const alarmDateRange = ref<[string, string] | null>(null)

// 报警汇总数据
const alarmSummary = computed(() => {
  const summary = {
    total: 0,
    unhandled: 0,
    handled: 0,
    avgHandleTime: 0,
  }
  alarmTableData.value.forEach((item) => {
    summary.total += item.alarm_count
    summary.unhandled += item.unhandled_count
    summary.handled += item.handled_count
  })
  // 计算平均处理时间
  const itemsWithTime = alarmTableData.value.filter((item) => item.avg_handle_time !== null)
  if (itemsWithTime.length > 0) {
    summary.avgHandleTime = Math.round(
      itemsWithTime.reduce((sum, item) => sum + (item.avg_handle_time || 0), 0) /
        itemsWithTime.length
    )
  }
  return summary
})

// ========== 预警统计分析 ==========
const warningLoading = ref(false)
const warningSearchForm = reactive<WarningAnalysisParams>({
  analysis_type: 1,
  industry_type: undefined,
  warning_type: undefined,
  street: undefined,
  start_time: undefined,
  end_time: undefined,
  compare_time: undefined,
})

const warningTimeRange = ref<[string, string] | null>(null)
const compareTimeRange = ref<[string, string] | null>(null)
const warningAnalysisResult = ref<any>(null)
const warningAnalysisData = ref<RiskWarning[]>([])

// 获取预警级别列表
const fetchWarningLevels = async () => {
  try {
    const response = await warningLevelApi.getList({ page_size: 100, status: 1 })
    warningLevels.value = response.results
  } catch (error: any) {
    console.error('获取预警级别失败:', error)
  }
}

// 获取报警统计数据
const fetchAlarmStatistics = async () => {
  alarmLoading.value = true
  try {
    const params: any = {
      page: alarmPagination.page,
      page_size: alarmPagination.pageSize,
      stat_type: alarmSearchForm.stat_type,
      industry_type: alarmSearchForm.industry_type,
      street: alarmSearchForm.street,
      start_date: alarmSearchForm.start_date,
      end_date: alarmSearchForm.end_date,
    }
    const response = await riskStatisticsApi.getAlarmStatistics(params)
    alarmTableData.value = response.results
    alarmPagination.total = response.count
  } catch (error: any) {
    ElMessage.error(error.message || '获取报警统计数据失败')
  } finally {
    alarmLoading.value = false
  }
}

// 报警统计分析搜索
const handleAlarmSearch = () => {
  if (alarmDateRange.value) {
    alarmSearchForm.start_date = alarmDateRange.value[0]
    alarmSearchForm.end_date = alarmDateRange.value[1]
  } else {
    alarmSearchForm.start_date = undefined
    alarmSearchForm.end_date = undefined
  }
  alarmPagination.page = 1
  fetchAlarmStatistics()
}

// 报警统计分析重置
const handleAlarmReset = () => {
  Object.assign(alarmSearchForm, {
    stat_type: undefined,
    industry_type: undefined,
    street: undefined,
    start_date: undefined,
    end_date: undefined,
  })
  alarmDateRange.value = null
  handleAlarmSearch()
}

// 报警统计分析分页
const handleAlarmSizeChange = (size: number) => {
  alarmPagination.pageSize = size
  alarmPagination.page = 1
  fetchAlarmStatistics()
}

const handleAlarmPageChange = (page: number) => {
  alarmPagination.page = page
  fetchAlarmStatistics()
}

// 预警统计分析
const handleWarningAnalysis = async () => {
  if (!warningTimeRange.value) {
    ElMessage.warning('请选择预警时间范围')
    return
  }

  warningLoading.value = true
  try {
    const params: WarningAnalysisParams = {
      analysis_type: warningSearchForm.analysis_type,
      industry_type: warningSearchForm.industry_type,
      warning_type: warningSearchForm.warning_type,
      street: warningSearchForm.street,
      start_time: warningTimeRange.value[0],
      end_time: warningTimeRange.value[1],
    }

    // 同比或环比分析需要对比时间段
    if (
      (warningSearchForm.analysis_type === 2 || warningSearchForm.analysis_type === 3) &&
      compareTimeRange.value
    ) {
      params.compare_time = `${compareTimeRange.value[0]},${compareTimeRange.value[1]}`
    }

    const response = await riskStatisticsApi.getWarningAnalysis(params)
    warningAnalysisResult.value = response.summary || {}
    warningAnalysisData.value = response.data || []
    ElMessage.success('分析完成')
  } catch (error: any) {
    ElMessage.error(error.message || '预警分析失败')
  } finally {
    warningLoading.value = false
  }
}

// 预警统计分析重置
const handleWarningReset = () => {
  Object.assign(warningSearchForm, {
    analysis_type: 1,
    industry_type: undefined,
    warning_type: undefined,
    street: undefined,
    start_time: undefined,
    end_time: undefined,
    compare_time: undefined,
  })
  warningTimeRange.value = null
  compareTimeRange.value = null
  warningAnalysisResult.value = null
  warningAnalysisData.value = []
}

// 获取统计类型显示
const getStatTypeDisplay = (type?: number) => {
  const typeMap: Record<number, string> = {
    1: '日报',
    2: '周报',
    3: '月报',
    4: '年报',
  }
  return typeMap[type || 0] || '-'
}

// 获取分析类型显示
const getAnalysisTypeDisplay = (type?: number) => {
  const typeMap: Record<number, string> = {
    1: '突出预警',
    2: '同比预警',
    3: '环比预警',
  }
  return typeMap[type || 0] || '-'
}

// 获取分析类型标签类型
const getAnalysisTypeTagType = (type?: number) => {
  const typeMap: Record<number, string> = {
    1: 'info',
    2: 'warning',
    3: 'success',
  }
  return typeMap[type || 0] || 'info'
}

// 获取级别标签类型
const getLevelTagType = (color: string) => {
  const colorMap: Record<string, string> = {
    red: 'danger',
    orange: 'warning',
    yellow: 'warning',
    blue: 'info',
  }
  return colorMap[color] || 'info'
}

// 初始化
onMounted(() => {
  fetchWarningLevels()
  fetchAlarmStatistics()
})
</script>

<style scoped lang="scss">
.statistics {
  .page-header {
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-size: 20px;
      font-weight: 500;
    }
  }

  .statistics-tabs {
    .search-card {
      margin-bottom: 20px;
    }

    .stat-cards {
      margin-bottom: 20px;
    }

    .stat-card {
      .stat-card-content {
        text-align: center;

        .stat-card-label {
          font-size: 14px;
          color: #909399;
          margin-bottom: 10px;
        }

        .stat-card-value {
          font-size: 28px;
          font-weight: 600;
          color: #303133;

          &.text-success {
            color: #67c23a;
          }

          &.text-warning {
            color: #e6a23c;
          }

          &.text-danger {
            color: #f56c6c;
          }
        }
      }
    }

    .table-card {
      .pagination {
        margin-top: 20px;
        display: flex;
        justify-content: flex-end;
      }
    }

    .analysis-result-card {
      margin-top: 20px;

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .warning-analysis-list {
        margin-top: 20px;

        h4 {
          margin: 0 0 15px 0;
          font-size: 16px;
          font-weight: 500;
        }
      }
    }
  }

  .text-success {
    color: #67c23a;
  }

  .text-warning {
    color: #e6a23c;
  }

  .text-danger {
    color: #f56c6c;
  }
}
</style>
