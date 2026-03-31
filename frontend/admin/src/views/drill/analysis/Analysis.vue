<template>
  <div class="analysis">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>演练分析</h2>
    </div>

    <!-- 左右分栏布局 -->
    <el-row :gutter="20">
      <!-- 左侧：搜索和表格 -->
      <el-col :span="16">
        <!-- 搜索筛选区域 -->
        <el-card class="search-card">
          <el-form :model="searchForm" :inline="true">
            <el-form-item label="演练事件">
              <el-select
                v-model="selectedEventId"
                placeholder="请选择演练事件"
                clearable
                filterable
                style="width: 250px"
                @change="handleEventSelect"
              >
                <el-option
                  v-for="event in eventList"
                  :key="event.id"
                  :label="`${event.event_code} - ${event.event_name}`"
                  :value="event.id"
                />
              </el-select>
            </el-form-item>
            <el-form-item label="统计类型">
              <el-select v-model="searchForm.stat_type" placeholder="请选择" clearable style="width: 120px">
                <el-option label="日报" :value="1" />
                <el-option label="周报" :value="2" />
                <el-option label="月报" :value="3" />
                <el-option label="年报" :value="4" />
              </el-select>
            </el-form-item>
            <el-form-item label="演练单位">
              <el-input
                v-model="searchForm.organization_name"
                placeholder="请输入单位名称"
                clearable
                style="width: 200px"
                @keyup.enter="handleSearch"
              />
            </el-form-item>
            <el-form-item label="演练类型">
              <el-select v-model="searchForm.drill_type" placeholder="请选择" clearable style="width: 120px">
                <el-option label="桌面演练" :value="1" />
                <el-option label="功能演练" :value="2" />
                <el-option label="全面演练" :value="3" />
              </el-select>
            </el-form-item>
            <el-form-item label="事故类型">
              <el-input
                v-model="searchForm.accident_type"
                placeholder="请输入事故类型"
                clearable
                style="width: 150px"
                @keyup.enter="handleSearch"
              />
            </el-form-item>
            <el-form-item label="统计日期">
              <el-date-picker
                v-model="dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                value-format="YYYY-MM-DD"
                style="width: 300px"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleSearch">
                <el-icon><Search /></el-icon>
                搜索
              </el-button>
              <el-button @click="handleReset">
                <el-icon><Refresh /></el-icon>
                重置
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>

        <!-- 统计卡片 -->
        <el-row :gutter="20" class="stat-cards">
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-card-label">演练总数</div>
            <div class="stat-card-value">{{ summary.totalDrillCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-card-label">已完成</div>
            <div class="stat-card-value text-success">{{ summary.totalCompletedCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-card-label">优秀</div>
            <div class="stat-card-value text-primary">{{ summary.totalExcellentCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-card-label">良好</div>
            <div class="stat-card-value text-info">{{ summary.totalGoodCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-card-label">合格</div>
            <div class="stat-card-value text-warning">{{ summary.totalQualifiedCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-card-label">不合格</div>
            <div class="stat-card-value text-danger">{{ summary.totalUnqualifiedCount }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 平均得分卡片 -->
    <el-row :gutter="20" class="stat-cards" style="margin-top: 20px">
      <el-col :span="12">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-card-label">平均得分</div>
            <div class="stat-card-value" style="font-size: 32px">
              {{ summary.avgScore !== null ? summary.avgScore.toFixed(2) : '-' }}分
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="stat-card">
          <div class="stat-card-content">
            <div class="stat-card-label">完成率</div>
            <div class="stat-card-value" style="font-size: 32px">
              {{
                summary.totalDrillCount > 0
                  ? ((summary.totalCompletedCount / summary.totalDrillCount) * 100).toFixed(2)
                  : 0
              }}%
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

        <!-- 数据表格 -->
        <el-card class="table-card">
      <el-table
        v-loading="loading"
        :data="tableData"
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
        <el-table-column prop="organization_name" label="演练单位" width="150" show-overflow-tooltip />
        <el-table-column label="演练类型" width="100">
          <template #default="{ row }">
            {{ getDrillTypeDisplay(row.drill_type) }}
          </template>
        </el-table-column>
        <el-table-column prop="accident_type" label="事故类型" width="120" show-overflow-tooltip />
        <el-table-column prop="drill_count" label="演练次数" width="100" align="right" />
        <el-table-column prop="completed_count" label="已完成" width="100" align="right">
          <template #default="{ row }">
            <span class="text-success">{{ row.completed_count }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="excellent_count" label="优秀" width="80" align="right">
          <template #default="{ row }">
            <span class="text-primary">{{ row.excellent_count }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="good_count" label="良好" width="80" align="right">
          <template #default="{ row }">
            <span class="text-info">{{ row.good_count }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="qualified_count" label="合格" width="80" align="right">
          <template #default="{ row }">
            <span class="text-warning">{{ row.qualified_count }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="unqualified_count" label="不合格" width="80" align="right">
          <template #default="{ row }">
            <span class="text-danger">{{ row.unqualified_count }}</span>
          </template>
        </el-table-column>
        <el-table-column label="平均得分" width="100" align="right">
          <template #default="{ row }">
            {{ row.avg_score ? Number(row.avg_score).toFixed(2) : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" />
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
        </div>
      </el-card>
      </el-col>

      <!-- 右侧：信息栏 -->
      <el-col :span="8">
        <el-card class="info-card">
          <template #header>
            <div class="info-card-header">
              <span>演练事件信息</span>
            </div>
          </template>
          <div v-if="selectedEvent" class="info-content">
            <div class="event-name">
              <el-text type="primary" size="large" tag="div" style="font-weight: 600; margin-bottom: 16px">
                {{ selectedEvent.event_name }}
              </el-text>
              <el-text type="info" size="small" tag="div" style="margin-bottom: 20px">
                {{ selectedEvent.event_code }}
              </el-text>
            </div>
            <el-divider />
            <div class="analysis-info">
              <div class="info-title">统计分析</div>
              <div v-if="eventAnalysis" class="analysis-detail">
                <el-descriptions :column="1" border size="small">
                  <el-descriptions-item label="统计日期">
                    {{ eventAnalysis.stat_date }}
                  </el-descriptions-item>
                  <el-descriptions-item label="统计类型">
                    {{ getStatTypeDisplay(eventAnalysis.stat_type) }}
                  </el-descriptions-item>
                  <el-descriptions-item label="演练次数">
                    <el-text type="primary">{{ eventAnalysis.drill_count }}</el-text>
                  </el-descriptions-item>
                  <el-descriptions-item label="已完成">
                    <el-text type="success">{{ eventAnalysis.completed_count }}</el-text>
                  </el-descriptions-item>
                  <el-descriptions-item label="优秀">
                    <el-text type="primary">{{ eventAnalysis.excellent_count }}</el-text>
                  </el-descriptions-item>
                  <el-descriptions-item label="良好">
                    <el-text type="info">{{ eventAnalysis.good_count }}</el-text>
                  </el-descriptions-item>
                  <el-descriptions-item label="合格">
                    <el-text type="warning">{{ eventAnalysis.qualified_count }}</el-text>
                  </el-descriptions-item>
                  <el-descriptions-item label="不合格">
                    <el-text type="danger">{{ eventAnalysis.unqualified_count }}</el-text>
                  </el-descriptions-item>
                  <el-descriptions-item label="平均得分">
                    <el-text type="primary" style="font-weight: 600">
                      {{ eventAnalysis.avg_score ? Number(eventAnalysis.avg_score).toFixed(2) : '-' }}分
                    </el-text>
                  </el-descriptions-item>
                </el-descriptions>
              </div>
              <div v-else class="empty-state">
                <el-empty description="该演练事件暂无分析数据" :image-size="80" />
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <el-empty description="请选择演练事件查看详细信息" :image-size="100" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Refresh } from '@element-plus/icons-vue'
import { drillAnalysisApi, drillEventApi } from '@/api/modules/drill'
import type { DrillAnalysis, DrillAnalysisParams, StatType, DrillType, DrillEvent } from '@/types/modules/drill'

// 加载状态
const loading = ref(false)

// 演练事件列表（用于选择）
const eventList = ref<DrillEvent[]>([])
// 选中的演练事件ID
const selectedEventId = ref<number | undefined>(undefined)
// 选中的演练事件详情
const selectedEvent = ref<DrillEvent | null>(null)
// 当前选中事件的分析数据
const eventAnalysis = ref<DrillAnalysis | null>(null)

// 表格数据
const tableData = ref<DrillAnalysis[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive<DrillAnalysisParams & { organization_name?: string }>({
  stat_type: undefined,
  organization_id: undefined,
  organization_name: undefined,
  drill_type: undefined,
  accident_type: undefined,
  start_date: undefined,
  end_date: undefined,
})

const dateRange = ref<[string, string] | null>(null)

// 获取演练事件列表（用于下拉选择）
const fetchEventList = async () => {
  try {
    const response = await drillEventApi.getList({ page_size: 1000 })
    eventList.value = response.results
  } catch (error: any) {
    console.error('获取演练事件列表失败:', error)
  }
}

// 演练事件选择变化
const handleEventSelect = async (eventId: number | undefined) => {
  if (eventId) {
    // 加载事件详情
    try {
      const event = await drillEventApi.getDetail(eventId)
      selectedEvent.value = event
      // 加载该事件的分析数据（如果有）
      try {
        const analysisResponse = await drillAnalysisApi.getAnalysis({ 
          organization_id: event.organization_id,
          accident_type: event.accident_type || undefined,
        })
        // 如果返回的是数组，取第一个；如果是分页对象，取results的第一个
        if (Array.isArray(analysisResponse)) {
          const firstItem = analysisResponse.length > 0 ? analysisResponse[0] : undefined
          eventAnalysis.value = firstItem ?? null
        } else if (analysisResponse && typeof analysisResponse === 'object' && 'results' in analysisResponse) {
          const paginatedResponse = analysisResponse as { results?: DrillAnalysis[] }
          if (paginatedResponse.results && paginatedResponse.results.length > 0 && paginatedResponse.results[0]) {
            eventAnalysis.value = paginatedResponse.results[0]
          } else {
            eventAnalysis.value = null
          }
        } else {
          eventAnalysis.value = null
        }
      } catch (error: any) {
        eventAnalysis.value = null
      }
    } catch (error: any) {
      ElMessage.error(error.message || '获取事件详情失败')
      selectedEvent.value = null
      eventAnalysis.value = null
    }
  } else {
    // 清空选择
    selectedEvent.value = null
    eventAnalysis.value = null
  }
}

// 统计汇总数据
const summary = computed(() => {
  const s = {
    totalDrillCount: 0,
    totalCompletedCount: 0,
    totalExcellentCount: 0,
    totalGoodCount: 0,
    totalQualifiedCount: 0,
    totalUnqualifiedCount: 0,
    avgScore: null as number | null,
  }

  tableData.value.forEach((item) => {
    s.totalDrillCount += item.drill_count
    s.totalCompletedCount += item.completed_count
    s.totalExcellentCount += item.excellent_count
    s.totalGoodCount += item.good_count
    s.totalQualifiedCount += item.qualified_count
    s.totalUnqualifiedCount += item.unqualified_count
  })

  // 计算平均得分
  const itemsWithScore = tableData.value.filter((item) => item.avg_score !== null)
  if (itemsWithScore.length > 0) {
    const totalScore = itemsWithScore.reduce(
      (sum, item) => sum + Number(item.avg_score || 0) * item.drill_count,
      0
    )
    const totalCount = itemsWithScore.reduce((sum, item) => sum + item.drill_count, 0)
    s.avgScore = totalCount > 0 ? totalScore / totalCount : null
  }

  return s
})

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params: any = {
      ...searchForm,
    }
    // 移除 organization_name，因为API不支持
    delete params.organization_name
    
    const response = await drillAnalysisApi.getAnalysis(params)
    // 如果后端返回的是数组，直接使用；如果是分页对象，使用results
    if (Array.isArray(response)) {
      tableData.value = response
      pagination.total = response.length
    } else if (response && typeof response === 'object' && 'results' in response) {
      const paginatedResponse = response as { results?: DrillAnalysis[]; count?: number }
      tableData.value = paginatedResponse.results || []
      pagination.total = paginatedResponse.count || paginatedResponse.results?.length || 0
    } else {
      tableData.value = []
      pagination.total = 0
    }
  } catch (error: any) {
    ElMessage.error(error.message || '获取数据失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  if (dateRange.value) {
    searchForm.start_date = dateRange.value[0]
    searchForm.end_date = dateRange.value[1]
  } else {
    searchForm.start_date = undefined
    searchForm.end_date = undefined
  }
  pagination.page = 1
  fetchData()
}

// 重置
const handleReset = () => {
  selectedEventId.value = undefined
  selectedEvent.value = null
  eventAnalysis.value = null
  Object.assign(searchForm, {
    stat_type: undefined,
    organization_id: undefined,
    organization_name: undefined,
    drill_type: undefined,
    accident_type: undefined,
    start_date: undefined,
    end_date: undefined,
  })
  dateRange.value = null
  handleSearch()
}

// 分页变化
const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  pagination.page = 1
  fetchData()
}

const handlePageChange = (page: number) => {
  pagination.page = page
  fetchData()
}

// 获取统计类型显示
const getStatTypeDisplay = (type?: StatType) => {
  const typeMap: Record<StatType, string> = {
    1: '日报',
    2: '周报',
    3: '月报',
    4: '年报',
  }
  return typeMap[type || 1] || '-'
}

// 获取演练类型显示
const getDrillTypeDisplay = (type?: DrillType | null) => {
  if (!type) return '-'
  const typeMap: Record<DrillType, string> = {
    1: '桌面演练',
    2: '功能演练',
    3: '全面演练',
  }
  return typeMap[type] || '-'
}

// 初始化
onMounted(() => {
  fetchEventList()
  fetchData()
})
</script>

<style scoped lang="scss">
.analysis {
  .page-header {
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-size: 20px;
      font-weight: 500;
    }
  }

  .search-card {
    margin-bottom: 20px;
  }

  .stat-cards {
    margin-bottom: 20px;

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

          &.text-primary {
            color: #409eff;
          }

          &.text-info {
            color: #909399;
          }
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

  .text-success {
    color: #67c23a;
  }

  .text-warning {
    color: #e6a23c;
  }

  .text-danger {
    color: #f56c6c;
  }

  .text-primary {
    color: #409eff;
  }

  .text-info {
    color: #909399;
  }

  .info-card {
    height: calc(100vh - 200px);
    position: sticky;
    top: 20px;

    .info-card-header {
      font-weight: 600;
    }

    .info-content {
      .event-name {
        margin-bottom: 16px;
      }

      .analysis-info {
        .info-title {
          font-size: 16px;
          font-weight: 600;
          margin-bottom: 16px;
          color: #303133;
        }

        .analysis-detail {
          .el-descriptions {
            margin-bottom: 16px;
          }
        }

        .empty-state {
          padding: 40px 0;
          text-align: center;
        }
      }
    }

    .empty-state {
      padding: 60px 0;
    }
  }
}
</style>