<template>
  <div class="data-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>简报数据</h2>
      <el-button type="primary" @click="handleGenerate">
        <el-icon><Plus /></el-icon>
        生成简报
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="简报类型">
          <el-select v-model="searchForm.brief_type" placeholder="请选择" clearable style="width: 180px">
            <el-option label="常态化运行报告" :value="1" />
            <el-option label="非常态化突发预警简报" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="报告类型">
          <el-select v-model="searchForm.report_type" placeholder="请选择" clearable style="width: 120px">
            <el-option label="日报" value="daily" />
            <el-option label="周报" value="weekly" />
            <el-option label="月报" value="monthly" />
            <el-option label="年报" value="yearly" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="未推送" :value="0" />
            <el-option label="已推送" :value="1" />
            <el-option label="已查看" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="关联模板">
          <el-select v-model="searchForm.template_id" placeholder="请选择" clearable filterable style="width: 180px">
            <el-option
              v-for="template in templateList"
              :key="template.id"
              :label="template.template_name"
              :value="template.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="报告日期">
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
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入简报编码/标题"
            clearable
            style="width: 200px"
            @keyup.enter="handleSearch"
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

    <!-- 数据表格 -->
    <el-card class="table-card">
      <el-table
        v-loading="loading"
        :data="tableData"
        stripe
        border
        style="width: 100%"
      >
        <el-table-column prop="brief_code" label="简报编码" width="150" />
        <el-table-column prop="brief_title" label="简报标题" min-width="200" show-overflow-tooltip />
        <el-table-column label="关联模板" width="150">
          <template #default="{ row }">
            <span v-if="row.template_detail">{{ row.template_detail.template_name }}</span>
            <span v-else>模板ID: {{ row.template_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="关联策略" width="150">
          <template #default="{ row }">
            <span v-if="row.strategy_detail">{{ row.strategy_detail.strategy_name }}</span>
            <span v-else-if="row.strategy_id">策略ID: {{ row.strategy_id }}</span>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="brief_type_display" label="简报类型" width="180" />
        <el-table-column label="报告类型" width="100">
          <template #default="{ row }">
            {{ getReportTypeDisplay(row.report_type) }}
          </template>
        </el-table-column>
        <el-table-column prop="report_date" label="报告日期" width="120" />
        <el-table-column prop="alarm_count" label="报警次数" width="100" align="right" />
        <el-table-column prop="warning_count" label="预警次数" width="100" align="right" />
        <el-table-column prop="risk_count" label="风险隐患" width="100" align="right" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">
              {{ row.status_display || getStatusDisplay(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="附件" width="80">
          <template #default="{ row }">
            <el-button
              v-if="row.attachment_url"
              type="primary"
              link
              size="small"
              @click="handleDownload(row)"
            >
              下载
            </el-button>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="generate_time" label="生成时间" width="160" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="danger" link size="small" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
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

    <!-- 生成简报对话框 -->
    <el-dialog v-model="generateVisible" title="生成简报" width="600px">
      <el-form ref="generateFormRef" :model="generateForm" :rules="generateFormRules" label-width="120px">
        <el-form-item label="关联模板" prop="template_id">
          <el-select v-model="generateForm.template_id" placeholder="请选择模板" filterable style="width: 100%">
            <el-option
              v-for="template in templateList"
              :key="template.id"
              :label="template.template_name"
              :value="template.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="关联策略">
          <el-select v-model="generateForm.strategy_id" placeholder="请选择策略（可选）" clearable filterable style="width: 100%">
            <el-option
              v-for="strategy in strategyList"
              :key="strategy.id"
              :label="strategy.strategy_name"
              :value="strategy.id"
            />
          </el-select>
          <div class="form-tip">如果选择策略，将按照策略配置自动生成简报</div>
        </el-form-item>
        <el-form-item label="报告日期" prop="report_date">
          <el-date-picker
            v-model="generateForm.report_date"
            type="date"
            placeholder="请选择报告日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="报告周期开始">
          <el-date-picker
            v-model="generateForm.report_period_start"
            type="datetime"
            placeholder="请选择报告周期开始时间（可选）"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="报告周期结束">
          <el-date-picker
            v-model="generateForm.report_period_end"
            type="datetime"
            placeholder="请选择报告周期结束时间（可选）"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="generateVisible = false">取消</el-button>
        <el-button type="primary" :loading="generateLoading" @click="handleGenerateSubmit">
          生成
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="简报详情" width="1200px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="简报编码">{{ currentRow?.brief_code }}</el-descriptions-item>
        <el-descriptions-item label="简报标题">{{ currentRow?.brief_title }}</el-descriptions-item>
        <el-descriptions-item label="关联模板">
          {{ currentRow?.template_detail?.template_name || `模板ID: ${currentRow?.template_id}` }}
        </el-descriptions-item>
        <el-descriptions-item label="关联策略">
          <span v-if="currentRow?.strategy_detail">{{ currentRow.strategy_detail.strategy_name }}</span>
          <span v-else-if="currentRow?.strategy_id">策略ID: {{ currentRow.strategy_id }}</span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="简报类型">{{ currentRow?.brief_type_display }}</el-descriptions-item>
        <el-descriptions-item label="报告类型">
          {{ getReportTypeDisplay(currentRow?.report_type) }}
        </el-descriptions-item>
        <el-descriptions-item label="报告日期">{{ currentRow?.report_date }}</el-descriptions-item>
        <el-descriptions-item label="生成时间">{{ currentRow?.generate_time }}</el-descriptions-item>
        <el-descriptions-item label="报告周期开始">
          {{ currentRow?.report_period_start || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="报告周期结束">
          {{ currentRow?.report_period_end || '-' }}
        </el-descriptions-item>
        <el-descriptions-item prop="alarm_count" label="报警次数">{{ currentRow?.alarm_count || 0 }}</el-descriptions-item>
        <el-descriptions-item prop="warning_count" label="预警次数">{{ currentRow?.warning_count || 0 }}</el-descriptions-item>
        <el-descriptions-item prop="risk_count" label="风险隐患数量">{{ currentRow?.risk_count || 0 }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusTagType(currentRow?.status)">
            {{ currentRow?.status_display || getStatusDisplay(currentRow?.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="附件">
          <el-button
            v-if="currentRow?.attachment_url"
            type="primary"
            link
            size="small"
            @click="handleDownload(currentRow!)"
          >
            下载附件
          </el-button>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="简报内容" :span="2">
          <div class="brief-content-preview">{{ currentRow?.brief_content }}</div>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.data_summary"
          label="数据摘要"
          :span="2"
        >
          <pre class="json-preview">{{ formatJson(currentRow.data_summary) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.industry_data"
          label="行业维度数据"
          :span="2"
        >
          <pre class="json-preview">{{ formatJson(currentRow.industry_data) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.region_data"
          label="区域维度数据"
          :span="2"
        >
          <pre class="json-preview">{{ formatJson(currentRow.region_data) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.time_data"
          label="时间维度数据"
          :span="2"
        >
          <pre class="json-preview">{{ formatJson(currentRow.time_data) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="简报描述" :span="2">
          {{ currentRow?.description || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { briefDataApi, briefTemplateApi, briefStrategyApi } from '@/api/modules/brief'
import type {
  BriefData,
  BriefDataListParams,
  BriefDataGenerateParams,
  BriefTemplate,
  BriefStrategy,
} from '@/types/modules/brief'
import dayjs from 'dayjs'

// 加载状态
const loading = ref(false)
const generateLoading = ref(false)

// 表格数据
const tableData = ref<BriefData[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 模板列表和策略列表
const templateList = ref<BriefTemplate[]>([])
const strategyList = ref<BriefStrategy[]>([])

// 搜索表单
const searchForm = reactive<BriefDataListParams>({
  brief_type: undefined,
  report_type: undefined,
  status: undefined,
  template_id: undefined,
  start_date: undefined,
  end_date: undefined,
  search: undefined,
})

// 日期范围
const dateRange = ref<[string, string] | null>(null)

// 对话框
const detailVisible = ref(false)
const generateVisible = ref(false)
const currentRow = ref<BriefData | null>(null)

// 生成表单
const generateFormRef = ref<FormInstance>()
const generateForm = reactive<BriefDataGenerateParams>({
  template_id: 0,
  strategy_id: null,
  report_date: dayjs().format('YYYY-MM-DD'),
  report_period_start: undefined,
  report_period_end: undefined,
})

// 生成表单验证规则
const generateFormRules: FormRules = {
  template_id: [
    { required: true, message: '请选择关联模板', trigger: 'change' },
    { type: 'number', min: 1, message: '请选择有效的模板', trigger: 'change' },
  ],
  report_date: [
    { required: true, message: '请选择报告日期', trigger: 'change' },
  ],
}

// 获取模板列表
const fetchTemplateList = async () => {
  try {
    const response = await briefTemplateApi.getList({ page_size: 100, status: 1 })
    templateList.value = response.results
  } catch (error: any) {
    console.error('获取模板列表失败:', error)
  }
}

// 获取策略列表
const fetchStrategyList = async () => {
  try {
    const response = await briefStrategyApi.getList({ page_size: 100, status: 1 })
    strategyList.value = response.results
  } catch (error: any) {
    console.error('获取策略列表失败:', error)
  }
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params: any = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm,
    }
    if (dateRange.value) {
      params.start_date = dateRange.value[0]
      params.end_date = dateRange.value[1]
    }
    const response = await briefDataApi.getList(params)
    tableData.value = response.results
    pagination.total = response.count
  } catch (error: any) {
    ElMessage.error(error.message || '获取数据失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

// 重置
const handleReset = () => {
  Object.assign(searchForm, {
    brief_type: undefined,
    report_type: undefined,
    status: undefined,
    template_id: undefined,
    start_date: undefined,
    end_date: undefined,
    search: undefined,
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

// 查看
const handleView = (row: BriefData) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: BriefData) => {
  try {
    await ElMessageBox.confirm('确定要删除该简报数据吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await briefDataApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 生成简报
const handleGenerate = () => {
  generateForm.template_id = 0
  generateForm.strategy_id = null
  generateForm.report_date = dayjs().format('YYYY-MM-DD')
  generateForm.report_period_start = undefined
  generateForm.report_period_end = undefined
  generateVisible.value = true
}

// 生成提交
const handleGenerateSubmit = async () => {
  if (!generateFormRef.value) return

  await generateFormRef.value.validate(async (valid) => {
    if (!valid) return

    generateLoading.value = true
    try {
      const data: BriefDataGenerateParams = {
        template_id: generateForm.template_id,
        strategy_id: generateForm.strategy_id,
        report_date: generateForm.report_date,
        report_period_start: generateForm.report_period_start,
        report_period_end: generateForm.report_period_end,
      }
      await briefDataApi.generate(data)
      ElMessage.success('简报生成成功')
      generateVisible.value = false
      fetchData()
    } catch (error: any) {
      ElMessage.error(error.message || '简报生成失败')
    } finally {
      generateLoading.value = false
    }
  })
}

// 下载附件
const handleDownload = (row: BriefData) => {
  if (row.attachment_url) {
    window.open(row.attachment_url, '_blank')
  } else {
    ElMessage.warning('附件不存在')
  }
}

// 格式化JSON
const formatJson = (jsonStr: string | null | undefined) => {
  if (!jsonStr) return '-'
  try {
    const obj = JSON.parse(jsonStr)
    return JSON.stringify(obj, null, 2)
  } catch (e) {
    return jsonStr
  }
}

// 获取报告类型显示
const getReportTypeDisplay = (reportType: string | null | undefined) => {
  if (!reportType) return '-'
  const typeMap: Record<string, string> = {
    daily: '日报',
    weekly: '周报',
    monthly: '月报',
    yearly: '年报',
  }
  return typeMap[reportType] || reportType
}

// 获取状态显示
const getStatusDisplay = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: '未推送',
    1: '已推送',
    2: '已查看',
  }
  return statusMap[status ?? 0] || '-'
}

// 获取状态标签类型
const getStatusTagType = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: 'info',
    1: 'success',
    2: 'warning',
  }
  return statusMap[status ?? 0] || 'info'
}

// 初始化
onMounted(() => {
  fetchTemplateList()
  fetchStrategyList()
  fetchData()
})
</script>

<style scoped lang="scss">
.data-list {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
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

  .table-card {
    .pagination {
      margin-top: 20px;
      display: flex;
      justify-content: flex-end;
    }
  }

  .text-muted {
    color: #909399;
  }

  .form-tip {
    font-size: 12px;
    color: #909399;
    margin-top: 5px;
  }

  .brief-content-preview {
    background: #f5f7fa;
    padding: 10px;
    border-radius: 4px;
    font-size: 14px;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 400px;
    overflow: auto;
  }

  .json-preview {
    background: #f5f7fa;
    padding: 10px;
    border-radius: 4px;
    font-size: 12px;
    max-height: 300px;
    overflow: auto;
    margin: 0;
  }
}
</style>
