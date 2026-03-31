<template>
  <div class="summary-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>演练总结</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增总结
      </el-button>
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
            <el-form-item label="总体等级">
              <el-select v-model="searchForm.overall_level" placeholder="请选择" clearable style="width: 150px">
                <el-option label="优秀" :value="1" />
                <el-option label="良好" :value="2" />
                <el-option label="合格" :value="3" />
                <el-option label="不合格" :value="4" />
              </el-select>
            </el-form-item>
            <el-form-item label="关键词">
              <el-input
                v-model="searchForm.search"
                placeholder="请输入总结标题/描述"
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
        <el-table-column prop="event_name" label="演练事件名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="summary_title" label="总结标题" min-width="200" show-overflow-tooltip />
        <el-table-column label="总体得分" width="100">
          <template #default="{ row }">
            <span v-if="row.overall_score">{{ row.overall_score }}分</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="总体等级" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.overall_level" :type="getLevelTagType(row.overall_level)">
              {{ row.overall_level_display }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="summary_user_name" label="总结人" width="120" />
        <el-table-column prop="summary_time" label="总结时间" width="160" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
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
            <div class="summary-info">
              <div class="info-title">演练总结</div>
              <div v-if="eventSummary" class="summary-detail">
                <el-descriptions :column="1" border size="small">
                  <el-descriptions-item label="总结标题">
                    {{ eventSummary.summary_title }}
                  </el-descriptions-item>
                  <el-descriptions-item label="总体得分">
                    <span v-if="eventSummary.overall_score">{{ eventSummary.overall_score }}分</span>
                    <span v-else>-</span>
                  </el-descriptions-item>
                  <el-descriptions-item label="总体等级">
                    <el-tag v-if="eventSummary.overall_level" :type="getLevelTagType(eventSummary.overall_level)" size="small">
                      {{ eventSummary.overall_level_display }}
                    </el-tag>
                    <span v-else>-</span>
                  </el-descriptions-item>
                  <el-descriptions-item label="总结人">
                    {{ eventSummary.summary_user_name || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="总结时间">
                    {{ eventSummary.summary_time }}
                  </el-descriptions-item>
                </el-descriptions>
                <div style="margin-top: 16px">
                  <el-button type="primary" size="small" @click="handleView(eventSummary)">
                    查看详情
                  </el-button>
                  <el-button type="primary" size="small" @click="handleEdit(eventSummary)">
                    编辑
                  </el-button>
                </div>
              </div>
              <div v-else class="empty-state">
                <el-empty description="该演练事件暂无总结" :image-size="80" />
                <el-button type="primary" size="small" style="margin-top: 16px" @click="handleCreateForEvent">
                  创建总结
                </el-button>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <el-empty description="请选择演练事件查看详细信息" :image-size="100" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="1000px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="150px"
      >
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="演练事件" prop="event_id">
              <el-select
                v-model="formData.event_id"
                placeholder="请选择演练事件"
                filterable
                style="width: 100%"
                @change="handleEventChange"
              >
                <el-option
                  v-for="event in eventList"
                  :key="event.id"
                  :label="`${event.event_code} - ${event.event_name}`"
                  :value="event.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="总结标题" prop="summary_title">
          <el-input v-model="formData.summary_title" placeholder="请输入总结标题" />
        </el-form-item>

        <!-- 评价维度 -->
        <el-divider content-position="left">评价维度</el-divider>

        <!-- 内部沟通和传递是否顺畅 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="内部沟通和传递是否顺畅">
              <el-select v-model="formData.communication_status" placeholder="请选择" clearable style="width: 100%">
                <el-option label="顺畅" :value="1" />
                <el-option label="一般" :value="2" />
                <el-option label="不顺畅" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-form-item label="内部沟通评价说明">
              <el-input
                v-model="formData.communication_comment"
                type="textarea"
                :rows="2"
                placeholder="请输入内部沟通评价说明"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 各级人员对预案的熟悉程度 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="各级人员对预案的熟悉程度">
              <el-select v-model="formData.plan_familiarity" placeholder="请选择" clearable style="width: 100%">
                <el-option label="熟悉" :value="1" />
                <el-option label="一般" :value="2" />
                <el-option label="不熟悉" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-form-item label="预案熟悉程度评价说明">
              <el-input
                v-model="formData.plan_familiarity_comment"
                type="textarea"
                :rows="2"
                placeholder="请输入预案熟悉程度评价说明"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 预案的可操作性 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="预案的可操作性">
              <el-select v-model="formData.plan_operability" placeholder="请选择" clearable style="width: 100%">
                <el-option label="可操作" :value="1" />
                <el-option label="一般" :value="2" />
                <el-option label="不可操作" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-form-item label="预案可操作性评价说明">
              <el-input
                v-model="formData.plan_operability_comment"
                type="textarea"
                :rows="2"
                placeholder="请输入预案可操作性评价说明"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 各级部门的职责定位是否明确 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="各级部门的职责定位是否明确">
              <el-select v-model="formData.duty_clarity" placeholder="请选择" clearable style="width: 100%">
                <el-option label="明确" :value="1" />
                <el-option label="一般" :value="2" />
                <el-option label="不明确" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-form-item label="职责定位评价说明">
              <el-input
                v-model="formData.duty_clarity_comment"
                type="textarea"
                :rows="2"
                placeholder="请输入职责定位评价说明"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 应急指挥是否科学 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="应急指挥是否科学">
              <el-select v-model="formData.command_science" placeholder="请选择" clearable style="width: 100%">
                <el-option label="科学" :value="1" />
                <el-option label="一般" :value="2" />
                <el-option label="不科学" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-form-item label="应急指挥评价说明">
              <el-input
                v-model="formData.command_science_comment"
                type="textarea"
                :rows="2"
                placeholder="请输入应急指挥评价说明"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 应急处置是否得当 -->
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="应急处置是否得当">
              <el-select v-model="formData.disposal_appropriateness" placeholder="请选择" clearable style="width: 100%">
                <el-option label="得当" :value="1" />
                <el-option label="一般" :value="2" />
                <el-option label="不得当" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-form-item label="应急处置评价说明">
              <el-input
                v-model="formData.disposal_appropriateness_comment"
                type="textarea"
                :rows="2"
                placeholder="请输入应急处置评价说明"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 总体评价 -->
        <el-divider content-position="left">总体评价</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="总体得分">
              <el-input-number
                v-model="formData.overall_score"
                :min="0"
                :max="100"
                :precision="2"
                placeholder="请输入总体得分（0-100）"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="总体等级">
              <el-select v-model="formData.overall_level" placeholder="请选择" clearable style="width: 100%">
                <el-option label="优秀" :value="1" />
                <el-option label="良好" :value="2" />
                <el-option label="合格" :value="3" />
                <el-option label="不合格" :value="4" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 分析总结 -->
        <el-divider content-position="left">分析总结</el-divider>
        <el-form-item label="存在的问题分析">
          <el-input
            v-model="formData.problems_analysis"
            type="textarea"
            :rows="4"
            placeholder="请输入存在的问题分析"
          />
        </el-form-item>
        <el-form-item label="改进建议">
          <el-input
            v-model="formData.improvement_suggestions"
            type="textarea"
            :rows="4"
            placeholder="请输入改进建议"
          />
        </el-form-item>
        <el-form-item label="企业演练总结报告内容">
          <el-input
            v-model="formData.enterprise_summary"
            type="textarea"
            :rows="4"
            placeholder="请输入企业演练总结报告内容"
          />
        </el-form-item>
        <el-form-item label="监管单位意见">
          <el-input
            v-model="formData.supervisor_opinion"
            type="textarea"
            :rows="4"
            placeholder="请输入监管单位意见"
          />
        </el-form-item>
        <el-form-item label="总结描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入总结描述"
          />
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            v-model="formData.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitLoading" @click="handleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="演练总结详情" width="1000px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="演练事件名称">{{ currentRow?.event_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="总结标题">{{ currentRow?.summary_title }}</el-descriptions-item>
        <el-descriptions-item label="总体得分">
          <span v-if="currentRow?.overall_score">{{ currentRow.overall_score }}分</span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="总体等级">
          <el-tag v-if="currentRow?.overall_level" :type="getLevelTagType(currentRow.overall_level)">
            {{ currentRow.overall_level_display }}
          </el-tag>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="总结人">{{ currentRow?.summary_user_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="总结时间">{{ currentRow?.summary_time }}</el-descriptions-item>
        <el-descriptions-item label="内部沟通和传递是否顺畅">
          <span v-if="currentRow?.communication_status">
            {{ currentRow.communication_status === 1 ? '顺畅' : currentRow.communication_status === 2 ? '一般' : '不顺畅' }}
          </span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="内部沟通评价说明" :span="2">
          {{ currentRow?.communication_comment || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="各级人员对预案的熟悉程度">
          <span v-if="currentRow?.plan_familiarity">
            {{ currentRow.plan_familiarity === 1 ? '熟悉' : currentRow.plan_familiarity === 2 ? '一般' : '不熟悉' }}
          </span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="预案熟悉程度评价说明" :span="2">
          {{ currentRow?.plan_familiarity_comment || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="预案的可操作性">
          <span v-if="currentRow?.plan_operability">
            {{ currentRow.plan_operability === 1 ? '可操作' : currentRow.plan_operability === 2 ? '一般' : '不可操作' }}
          </span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="预案可操作性评价说明" :span="2">
          {{ currentRow?.plan_operability_comment || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="各级部门的职责定位是否明确">
          <span v-if="currentRow?.duty_clarity">
            {{ currentRow.duty_clarity === 1 ? '明确' : currentRow.duty_clarity === 2 ? '一般' : '不明确' }}
          </span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="职责定位评价说明" :span="2">
          {{ currentRow?.duty_clarity_comment || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="应急指挥是否科学">
          <span v-if="currentRow?.command_science">
            {{ currentRow.command_science === 1 ? '科学' : currentRow.command_science === 2 ? '一般' : '不科学' }}
          </span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="应急指挥评价说明" :span="2">
          {{ currentRow?.command_science_comment || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="应急处置是否得当">
          <span v-if="currentRow?.disposal_appropriateness">
            {{ currentRow.disposal_appropriateness === 1 ? '得当' : currentRow.disposal_appropriateness === 2 ? '一般' : '不得当' }}
          </span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="应急处置评价说明" :span="2">
          {{ currentRow?.disposal_appropriateness_comment || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="存在的问题分析" :span="2">
          {{ currentRow?.problems_analysis || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="改进建议" :span="2">
          {{ currentRow?.improvement_suggestions || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="企业演练总结报告内容" :span="2">
          {{ currentRow?.enterprise_summary || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="监管单位意见" :span="2">
          {{ currentRow?.supervisor_opinion || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="总结描述" :span="2">
          {{ currentRow?.description || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">
          {{ currentRow?.remark || '-' }}
        </el-descriptions-item>
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
import { drillSummaryApi, drillEventApi } from '@/api/modules/drill'
import { useAuthStore } from '@/store/modules/auth'
import type { DrillSummary, DrillSummaryFormData, DrillEvent } from '@/types/modules/drill'

const authStore = useAuthStore()

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<DrillSummary[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 演练事件列表（用于选择）
const eventList = ref<DrillEvent[]>([])
// 选中的演练事件ID
const selectedEventId = ref<number | undefined>(undefined)
// 选中的演练事件详情
const selectedEvent = ref<DrillEvent | null>(null)
// 当前选中事件的总结
const eventSummary = ref<DrillSummary | null>(null)

// 搜索表单
const searchForm = reactive({
  event_id: undefined as number | undefined,
  overall_level: undefined as number | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增演练总结')
const currentRow = ref<DrillSummary | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<DrillSummaryFormData>({
  event_id: 0,
  summary_title: '',
  communication_status: null,
  communication_comment: null,
  plan_familiarity: null,
  plan_familiarity_comment: null,
  plan_operability: null,
  plan_operability_comment: null,
  duty_clarity: null,
  duty_clarity_comment: null,
  command_science: null,
  command_science_comment: null,
  disposal_appropriateness: null,
  disposal_appropriateness_comment: null,
  problems_analysis: null,
  improvement_suggestions: null,
  overall_score: null,
  overall_level: null,
  enterprise_summary: null,
  supervisor_opinion: null,
  description: null,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  event_id: [
    { required: true, message: '请选择演练事件', trigger: 'change' },
  ],
  summary_title: [
    { required: true, message: '请输入总结标题', trigger: 'blur' },
  ],
}

// 获取演练事件列表（用于下拉选择）
const fetchEventList = async () => {
  try {
    const response = await drillEventApi.getList({ page_size: 1000 })
    eventList.value = response.results
  } catch (error: any) {
    console.error('获取演练事件列表失败:', error)
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
    const response = await drillSummaryApi.getList(params)
    tableData.value = response.results
    pagination.total = response.count
  } catch (error: any) {
    ElMessage.error(error.message || '获取数据失败')
  } finally {
    loading.value = false
  }
}

// 演练事件选择变化
const handleEventSelect = async (eventId: number | undefined) => {
  if (eventId) {
    // 更新搜索表单
    searchForm.event_id = eventId
    // 加载事件详情
    try {
      const event = await drillEventApi.getDetail(eventId)
      selectedEvent.value = event
      // 加载该事件的总结（如果有）
      try {
        const summaryResponse = await drillSummaryApi.getList({ event_id: eventId, page_size: 1 })
        if (summaryResponse.results && summaryResponse.results.length > 0) {
          eventSummary.value = summaryResponse.results[0] || null
        } else {
          eventSummary.value = null
        }
      } catch (error: any) {
        eventSummary.value = null
      }
    } catch (error: any) {
      ElMessage.error(error.message || '获取事件详情失败')
      selectedEvent.value = null
      eventSummary.value = null
    }
    // 刷新表格数据
    handleSearch()
  } else {
    // 清空选择
    selectedEvent.value = null
    eventSummary.value = null
    searchForm.event_id = undefined
    handleSearch()
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  fetchData()
}

// 重置
const handleReset = () => {
  selectedEventId.value = undefined
  selectedEvent.value = null
  eventSummary.value = null
  Object.assign(searchForm, {
    event_id: undefined,
    overall_level: undefined,
    search: undefined,
  })
  handleSearch()
}

// 为选中事件创建总结
const handleCreateForEvent = () => {
  if (selectedEvent.value) {
    isEdit.value = false
    dialogTitle.value = '新增演练总结'
    resetForm()
    formData.event_id = selectedEvent.value.id
    dialogVisible.value = true
  }
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

// 新增
const handleCreate = () => {
  isEdit.value = false
  dialogTitle.value = '新增演练总结'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: DrillSummary) => {
  isEdit.value = true
  dialogTitle.value = '编辑演练总结'
  currentRow.value = row
  Object.assign(formData, {
    event_id: row.event_id,
    summary_title: row.summary_title,
    communication_status: row.communication_status,
    communication_comment: row.communication_comment,
    plan_familiarity: row.plan_familiarity,
    plan_familiarity_comment: row.plan_familiarity_comment,
    plan_operability: row.plan_operability,
    plan_operability_comment: row.plan_operability_comment,
    duty_clarity: row.duty_clarity,
    duty_clarity_comment: row.duty_clarity_comment,
    command_science: row.command_science,
    command_science_comment: row.command_science_comment,
    disposal_appropriateness: row.disposal_appropriateness,
    disposal_appropriateness_comment: row.disposal_appropriateness_comment,
    problems_analysis: row.problems_analysis,
    improvement_suggestions: row.improvement_suggestions,
    overall_score: row.overall_score ? Number(row.overall_score) : null,
    overall_level: row.overall_level,
    enterprise_summary: row.enterprise_summary,
    supervisor_opinion: row.supervisor_opinion,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: DrillSummary) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: DrillSummary) => {
  try {
    await ElMessageBox.confirm('确定要删除该演练总结吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await drillSummaryApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
    // 如果当前有选中的事件，刷新右侧信息栏
    if (selectedEventId.value) {
      handleEventSelect(selectedEventId.value)
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 演练事件变化
const handleEventChange = (eventId: number) => {
  // 可以选择加载事件详情
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const data: DrillSummaryFormData = {
        event_id: formData.event_id,
        summary_title: formData.summary_title,
        communication_status: formData.communication_status,
        communication_comment: formData.communication_comment,
        plan_familiarity: formData.plan_familiarity,
        plan_familiarity_comment: formData.plan_familiarity_comment,
        plan_operability: formData.plan_operability,
        plan_operability_comment: formData.plan_operability_comment,
        duty_clarity: formData.duty_clarity,
        duty_clarity_comment: formData.duty_clarity_comment,
        command_science: formData.command_science,
        command_science_comment: formData.command_science_comment,
        disposal_appropriateness: formData.disposal_appropriateness,
        disposal_appropriateness_comment: formData.disposal_appropriateness_comment,
        problems_analysis: formData.problems_analysis,
        improvement_suggestions: formData.improvement_suggestions,
        overall_score: formData.overall_score ? formData.overall_score.toString() : null,
        overall_level: formData.overall_level,
        enterprise_summary: formData.enterprise_summary,
        supervisor_opinion: formData.supervisor_opinion,
        description: formData.description,
        remark: formData.remark,
      }
      
      if (isEdit.value && currentRow.value) {
        await drillSummaryApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await drillSummaryApi.create(data)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchData()
      // 如果当前有选中的事件，刷新右侧信息栏
      if (selectedEventId.value) {
        handleEventSelect(selectedEventId.value)
      }
    } catch (error: any) {
      ElMessage.error(error.message || '操作失败')
    } finally {
      submitLoading.value = false
    }
  })
}

// 重置表单
const resetForm = () => {
  Object.assign(formData, {
    event_id: 0,
    summary_title: '',
    communication_status: null,
    communication_comment: null,
    plan_familiarity: null,
    plan_familiarity_comment: null,
    plan_operability: null,
    plan_operability_comment: null,
    duty_clarity: null,
    duty_clarity_comment: null,
    command_science: null,
    command_science_comment: null,
    disposal_appropriateness: null,
    disposal_appropriateness_comment: null,
    problems_analysis: null,
    improvement_suggestions: null,
    overall_score: null,
    overall_level: null,
    enterprise_summary: null,
    supervisor_opinion: null,
    description: null,
    remark: null,
  })
  formRef.value?.clearValidate()
  currentRow.value = null
}

// 对话框关闭
const handleDialogClose = () => {
  resetForm()
  isEdit.value = false
}

// 获取评价等级标签类型
const getLevelTagType = (level?: number) => {
  const levelMap: Record<number, string> = {
    1: 'success', // 优秀
    2: 'primary', // 良好
    3: 'warning', // 合格
    4: 'danger', // 不合格
  }
  return levelMap[level || 0] || 'info'
}

// 初始化
onMounted(() => {
  fetchEventList()
  fetchData()
})
</script>

<style scoped lang="scss">
.summary-list {
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

      .summary-info {
        .info-title {
          font-size: 16px;
          font-weight: 600;
          margin-bottom: 16px;
          color: #303133;
        }

        .summary-detail {
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