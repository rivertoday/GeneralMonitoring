<template>
  <div class="evaluation-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>演练评价</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增评价
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
            <el-form-item label="节点类型">
              <el-select v-model="searchForm.node_type" placeholder="请选择" clearable style="width: 150px">
                <el-option label="信息收集" :value="1" />
                <el-option label="决策指挥" :value="2" />
                <el-option label="资源调配" :value="3" />
                <el-option label="现场处置" :value="4" />
                <el-option label="其他" :value="5" />
              </el-select>
            </el-form-item>
            <el-form-item label="评价等级">
              <el-select v-model="searchForm.evaluation_level" placeholder="请选择" clearable style="width: 150px">
                <el-option label="优秀" :value="1" />
                <el-option label="良好" :value="2" />
                <el-option label="合格" :value="3" />
                <el-option label="不合格" :value="4" />
              </el-select>
            </el-form-item>
            <el-form-item label="关键词">
              <el-input
                v-model="searchForm.search"
                placeholder="请输入节点名称/评价项"
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
        <el-table-column prop="node_name" label="演练节点名称" width="150" />
        <el-table-column prop="node_type_display" label="节点类型" width="120" />
        <el-table-column prop="evaluation_item" label="评价项" width="150" show-overflow-tooltip />
        <el-table-column label="评价得分" width="100">
          <template #default="{ row }">
            <span v-if="row.evaluation_score">{{ row.evaluation_score }}分</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="评价等级" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.evaluation_level" :type="getLevelTagType(row.evaluation_level)">
              {{ row.evaluation_level_display }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="evaluator_name" label="评价人" width="120" />
        <el-table-column prop="evaluation_time" label="评价时间" width="160" />
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
            <div class="evaluation-list-info">
              <div class="info-title">评价列表</div>
              <div v-if="eventEvaluations.length === 0" class="empty-state">
                <el-empty description="暂无评价数据" :image-size="80" />
              </div>
              <div v-else class="evaluation-items">
                <div
                  v-for="evaluation in eventEvaluations"
                  :key="evaluation.id"
                  class="evaluation-item"
                  @click="handleView(evaluation)"
                >
                  <div class="evaluation-item-header">
                    <span class="node-name">{{ evaluation.node_name }}</span>
                    <el-tag v-if="evaluation.evaluation_level" :type="getLevelTagType(evaluation.evaluation_level)" size="small">
                      {{ evaluation.evaluation_level_display }}
                    </el-tag>
                  </div>
                  <div class="evaluation-item-content">
                    <el-text type="info" size="small">{{ evaluation.evaluation_item }}</el-text>
                  </div>
                  <div class="evaluation-item-footer">
                    <el-text v-if="evaluation.evaluation_score" type="primary" size="small">
                      {{ evaluation.evaluation_score }}分
                    </el-text>
                    <el-text type="info" size="small">{{ evaluation.evaluation_time }}</el-text>
                  </div>
                </div>
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
      width="900px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="120px"
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
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="演练节点名称" prop="node_name">
              <el-input v-model="formData.node_name" placeholder="请输入演练节点名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="节点类型" prop="node_type">
              <el-select v-model="formData.node_type" placeholder="请选择" style="width: 100%">
                <el-option label="信息收集" :value="1" />
                <el-option label="决策指挥" :value="2" />
                <el-option label="资源调配" :value="3" />
                <el-option label="现场处置" :value="4" />
                <el-option label="其他" :value="5" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="评价项" prop="evaluation_item">
          <el-input v-model="formData.evaluation_item" placeholder="请输入评价项" />
        </el-form-item>
        <el-form-item label="评价内容" prop="evaluation_content">
          <el-input
            v-model="formData.evaluation_content"
            type="textarea"
            :rows="4"
            placeholder="请输入评价内容"
          />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="评价得分">
              <el-input-number
                v-model="formData.evaluation_score"
                :min="0"
                :max="100"
                :precision="2"
                placeholder="请输入评价得分（0-100）"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="评价等级">
              <el-select v-model="formData.evaluation_level" placeholder="请选择" clearable style="width: 100%">
                <el-option label="优秀" :value="1" />
                <el-option label="良好" :value="2" />
                <el-option label="合格" :value="3" />
                <el-option label="不合格" :value="4" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="评价描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入评价描述"
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
    <el-dialog v-model="detailVisible" title="演练评价详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="演练事件名称">{{ currentRow?.event_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="演练节点名称">{{ currentRow?.node_name }}</el-descriptions-item>
        <el-descriptions-item label="节点类型">{{ currentRow?.node_type_display }}</el-descriptions-item>
        <el-descriptions-item label="评价项">{{ currentRow?.evaluation_item }}</el-descriptions-item>
        <el-descriptions-item label="评价得分">
          <span v-if="currentRow?.evaluation_score">{{ currentRow.evaluation_score }}分</span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="评价等级">
          <el-tag v-if="currentRow?.evaluation_level" :type="getLevelTagType(currentRow.evaluation_level)">
            {{ currentRow.evaluation_level_display }}
          </el-tag>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="评价人">{{ currentRow?.evaluator_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="评价时间">{{ currentRow?.evaluation_time }}</el-descriptions-item>
        <el-descriptions-item label="评价内容" :span="2">{{ currentRow?.evaluation_content }}</el-descriptions-item>
        <el-descriptions-item label="评价描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
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
import { drillEvaluationApi, drillEventApi } from '@/api/modules/drill'
import { useAuthStore } from '@/store/modules/auth'
import type { DrillEvaluation, DrillEvaluationFormData, DrillEvent } from '@/types/modules/drill'

const authStore = useAuthStore()

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<DrillEvaluation[]>([])
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
// 当前选中事件的评价列表
const eventEvaluations = ref<DrillEvaluation[]>([])

// 搜索表单
const searchForm = reactive({
  event_id: undefined as number | undefined,
  node_type: undefined as number | undefined,
  evaluation_level: undefined as number | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增演练评价')
const currentRow = ref<DrillEvaluation | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<DrillEvaluationFormData>({
  event_id: 0,
  node_name: '',
  node_type: 1,
  evaluation_item: '',
  evaluation_content: '',
  evaluation_score: null,
  evaluation_level: null,
  description: null,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  event_id: [
    { required: true, message: '请选择演练事件', trigger: 'change' },
  ],
  node_name: [
    { required: true, message: '请输入演练节点名称', trigger: 'blur' },
  ],
  node_type: [
    { required: true, message: '请选择节点类型', trigger: 'change' },
  ],
  evaluation_item: [
    { required: true, message: '请输入评价项', trigger: 'blur' },
  ],
  evaluation_content: [
    { required: true, message: '请输入评价内容', trigger: 'blur' },
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
    const response = await drillEvaluationApi.getList(params)
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
      // 加载该事件的所有评价
      const evalResponse = await drillEvaluationApi.getList({ event_id: eventId, page_size: 1000 })
      eventEvaluations.value = evalResponse.results
    } catch (error: any) {
      ElMessage.error(error.message || '获取事件详情失败')
      selectedEvent.value = null
      eventEvaluations.value = []
    }
    // 刷新表格数据
    handleSearch()
  } else {
    // 清空选择
    selectedEvent.value = null
    eventEvaluations.value = []
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
  eventEvaluations.value = []
  Object.assign(searchForm, {
    event_id: undefined,
    node_type: undefined,
    evaluation_level: undefined,
    search: undefined,
  })
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

// 新增
const handleCreate = () => {
  isEdit.value = false
  dialogTitle.value = '新增演练评价'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: DrillEvaluation) => {
  isEdit.value = true
  dialogTitle.value = '编辑演练评价'
  currentRow.value = row
  Object.assign(formData, {
    event_id: row.event_id,
    node_name: row.node_name,
    node_type: row.node_type,
    evaluation_item: row.evaluation_item,
    evaluation_content: row.evaluation_content,
    evaluation_score: row.evaluation_score ? Number(row.evaluation_score) : null,
    evaluation_level: row.evaluation_level,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: DrillEvaluation) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: DrillEvaluation) => {
  try {
    await ElMessageBox.confirm('确定要删除该演练评价吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await drillEvaluationApi.delete(row.id)
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
  // 可以选择加载事件详情，显示事件名称等
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const data: DrillEvaluationFormData = {
        event_id: formData.event_id,
        node_name: formData.node_name,
        node_type: formData.node_type,
        evaluation_item: formData.evaluation_item,
        evaluation_content: formData.evaluation_content,
        evaluation_score: formData.evaluation_score ? formData.evaluation_score.toString() : null,
        evaluation_level: formData.evaluation_level,
        description: formData.description,
        remark: formData.remark,
      }
      
      if (isEdit.value && currentRow.value) {
        await drillEvaluationApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await drillEvaluationApi.create(data)
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
    node_name: '',
    node_type: 1,
    evaluation_item: '',
    evaluation_content: '',
    evaluation_score: null,
    evaluation_level: null,
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
.evaluation-list {
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

      .evaluation-list-info {
        .info-title {
          font-size: 16px;
          font-weight: 600;
          margin-bottom: 16px;
          color: #303133;
        }

        .empty-state {
          padding: 40px 0;
        }

        .evaluation-items {
          .evaluation-item {
            padding: 12px;
            margin-bottom: 12px;
            border: 1px solid #e4e7ed;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s;

            &:hover {
              border-color: #409eff;
              background-color: #f5f7fa;
            }

            .evaluation-item-header {
              display: flex;
              justify-content: space-between;
              align-items: center;
              margin-bottom: 8px;

              .node-name {
                font-weight: 600;
                color: #303133;
              }
            }

            .evaluation-item-content {
              margin-bottom: 8px;
              color: #606266;
            }

            .evaluation-item-footer {
              display: flex;
              justify-content: space-between;
              align-items: center;
              font-size: 12px;
            }
          }
        }
      }
    }

    .empty-state {
      padding: 60px 0;
    }
  }
}
</style>

