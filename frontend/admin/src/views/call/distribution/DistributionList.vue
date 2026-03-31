<template>
  <div class="distribution-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>政策文件下发管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增政策下发
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="政策文件">
          <el-select
            v-model="searchForm.policy_file_id"
            placeholder="请选择"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="file in policyFileOptions"
              :key="file.id"
              :label="file.policy_title"
              :value="file.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="叫应对象">
          <el-select
            v-model="searchForm.target_id"
            placeholder="请选择"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="target in targetOptions"
              :key="target.id"
              :label="target.target_name"
              :value="target.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="反馈状态">
          <el-select v-model="searchForm.feedback_status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="未反馈" :value="0" />
            <el-option label="已反馈" :value="1" />
            <el-option label="超时未反馈" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="督办状态">
          <el-select v-model="searchForm.supervise_status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="无需督办" :value="0" />
            <el-option label="待督办" :value="1" />
            <el-option label="已督办" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="下发时间">
          <el-date-picker
            v-model="dateRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 350px"
            @change="handleDateRangeChange"
          />
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入下发编码/描述"
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
        <el-table-column prop="distribution_code" label="下发编码" width="150" />
        <el-table-column label="政策文件" width="200" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.policy_file_detail?.policy_title || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="叫应对象" width="150" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.target_detail?.target_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="feedback_deadline" label="反馈截止时间" width="160" />
        <el-table-column prop="distribution_time" label="下发时间" width="160" />
        <el-table-column prop="distribution_user_name" label="下发人" width="120" />
        <el-table-column label="反馈状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getFeedbackStatusTagType(row.feedback_status)">
              {{ row.feedback_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="feedback_time" label="反馈时间" width="160" />
        <el-table-column label="督办状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getSuperviseStatusTagType(row.supervise_status)">
              {{ row.supervise_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button
              v-if="row.feedback_status === 0"
              type="success"
              link
              size="small"
              @click="handleFeedback(row)"
            >
              反馈
            </el-button>
            <el-button
              v-if="row.supervise_status === 1"
              type="warning"
              link
              size="small"
              @click="handleSupervise(row)"
            >
              督办
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

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="800px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="120px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="下发编码" prop="distribution_code">
              <el-input v-model="formData.distribution_code" placeholder="请输入下发编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="政策文件" prop="policy_file_id">
              <el-select
                v-model="formData.policy_file_id"
                placeholder="请选择政策文件"
                filterable
                style="width: 100%"
              >
                <el-option
                  v-for="file in policyFileOptions"
                  :key="file.id"
                  :label="file.policy_title"
                  :value="file.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="叫应对象" prop="target_id">
              <el-select
                v-model="formData.target_id"
                placeholder="请选择叫应对象"
                filterable
                style="width: 100%"
              >
                <el-option
                  v-for="target in targetOptions"
                  :key="target.id"
                  :label="target.target_name"
                  :value="target.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="反馈截止时间" prop="feedback_deadline">
              <el-date-picker
                v-model="formData.feedback_deadline"
                type="datetime"
                placeholder="选择反馈截止时间"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="反馈内容要求">
          <el-input
            v-model="formData.feedback_content"
            type="textarea"
            :rows="4"
            placeholder="请输入反馈内容要求"
          />
        </el-form-item>
        <el-form-item label="下发描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入下发描述"
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
    <el-dialog v-model="detailVisible" title="政策文件下发详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="下发编码">{{ currentRow?.distribution_code }}</el-descriptions-item>
        <el-descriptions-item label="政策文件">
          {{ currentRow?.policy_file_detail?.policy_title || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="叫应对象">
          {{ currentRow?.target_detail?.target_name || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="反馈截止时间">{{ currentRow?.feedback_deadline }}</el-descriptions-item>
        <el-descriptions-item label="下发时间">{{ currentRow?.distribution_time }}</el-descriptions-item>
        <el-descriptions-item label="下发人">{{ currentRow?.distribution_user_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="反馈状态">
          <el-tag :type="getFeedbackStatusTagType(currentRow?.feedback_status || 0)">
            {{ currentRow?.feedback_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="反馈时间">{{ currentRow?.feedback_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="督办状态">
          <el-tag :type="getSuperviseStatusTagType(currentRow?.supervise_status || 0)">
            {{ currentRow?.supervise_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="督办时间">{{ currentRow?.supervise_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="督办人">{{ currentRow?.supervise_user_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="反馈内容要求" :span="2">{{ currentRow?.feedback_content || '-' }}</el-descriptions-item>
        <el-descriptions-item label="实际反馈内容" :span="2">{{ currentRow?.feedback_content_actual || '-' }}</el-descriptions-item>
        <el-descriptions-item label="下发描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 反馈对话框 -->
    <el-dialog v-model="feedbackVisible" title="反馈政策文件下发" width="600px">
      <el-form ref="feedbackFormRef" :model="feedbackData" :rules="feedbackRules" label-width="120px">
        <el-form-item label="实际反馈内容" prop="feedback_content_actual">
          <el-input
            v-model="feedbackData.feedback_content_actual"
            type="textarea"
            :rows="6"
            placeholder="请输入实际反馈内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="feedbackVisible = false">取消</el-button>
        <el-button type="primary" :loading="feedbackLoading" @click="handleFeedbackConfirm">
          确定反馈
        </el-button>
      </template>
    </el-dialog>

    <!-- 督办对话框 -->
    <el-dialog v-model="superviseVisible" title="督办政策文件下发" width="500px">
      <el-form ref="superviseFormRef" :model="superviseData" :rules="superviseRules" label-width="120px">
        <el-form-item label="督办人ID" prop="supervise_user_id">
          <el-input-number
            v-model="superviseData.supervise_user_id"
            :min="1"
            placeholder="请输入督办人ID"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="superviseVisible = false">取消</el-button>
        <el-button type="primary" :loading="superviseLoading" @click="handleSuperviseConfirm">
          确定督办
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import {
  policyDistributionApi,
  policyFileApi,
  callTargetApi,
} from '@/api/modules/call'
import type {
  PolicyDistribution,
  PolicyDistributionListParams,
  PolicyDistributionFormData,
  PolicyDistributionFeedbackData,
  PolicyDistributionSuperviseData,
  FeedbackStatus,
  SuperviseStatus,
} from '@/types/modules/call'
import type { PolicyFile } from '@/types/modules/call'
import type { CallTarget } from '@/types/modules/call'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)
const feedbackLoading = ref(false)
const superviseLoading = ref(false)

// 表格数据
const tableData = ref<PolicyDistribution[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 选项数据
const policyFileOptions = ref<PolicyFile[]>([])
const targetOptions = ref<CallTarget[]>([])

// 搜索表单
const searchForm = reactive<PolicyDistributionListParams>({
  policy_file_id: undefined,
  target_id: undefined,
  feedback_status: undefined,
  supervise_status: undefined,
  start_time: undefined,
  end_time: undefined,
  search: undefined,
})

// 日期范围
const dateRange = ref<[string, string] | null>(null)

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const feedbackVisible = ref(false)
const superviseVisible = ref(false)
const dialogTitle = ref('新增政策下发')
const currentRow = ref<PolicyDistribution | null>(null)
const feedbackRow = ref<PolicyDistribution | null>(null)
const superviseRow = ref<PolicyDistribution | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<PolicyDistributionFormData>({
  distribution_code: '',
  policy_file_id: 0,
  target_id: 0,
  feedback_content: null,
  feedback_deadline: '',
  description: null,
  remark: null,
})

// 反馈表单
const feedbackFormRef = ref<FormInstance>()
const feedbackData = reactive<PolicyDistributionFeedbackData>({
  feedback_content_actual: '',
})

// 督办表单
const superviseFormRef = ref<FormInstance>()
const superviseData = reactive<PolicyDistributionSuperviseData>({
  supervise_user_id: 0,
})

// 表单验证规则
const formRules: FormRules = {
  distribution_code: [
    { required: true, message: '请输入下发编码', trigger: 'blur' },
  ],
  policy_file_id: [
    { required: true, message: '请选择政策文件', trigger: 'change' },
  ],
  target_id: [
    { required: true, message: '请选择叫应对象', trigger: 'change' },
  ],
  feedback_deadline: [
    { required: true, message: '请选择反馈截止时间', trigger: 'change' },
  ],
}

// 反馈表单验证规则
const feedbackRules: FormRules = {
  feedback_content_actual: [
    { required: true, message: '请输入实际反馈内容', trigger: 'blur' },
  ],
}

// 督办表单验证规则
const superviseRules: FormRules = {
  supervise_user_id: [
    { required: true, message: '请输入督办人ID', trigger: 'blur' },
  ],
}

// 获取反馈状态标签类型
const getFeedbackStatusTagType = (status: FeedbackStatus): string => {
  const typeMap: Record<FeedbackStatus, string> = {
    0: 'info',    // 未反馈
    1: 'success', // 已反馈
    2: 'danger',  // 超时未反馈
  }
  return typeMap[status] || 'info'
}

// 获取督办状态标签类型
const getSuperviseStatusTagType = (status: SuperviseStatus): string => {
  const typeMap: Record<SuperviseStatus, string> = {
    0: 'info',    // 无需督办
    1: 'warning', // 待督办
    2: 'success', // 已督办
  }
  return typeMap[status] || 'info'
}

// 获取政策文件列表
const fetchPolicyFiles = async () => {
  try {
    const response = await policyFileApi.getList({ page_size: 1000, publish_status: 1 })
    policyFileOptions.value = response.results
  } catch (error: any) {
    console.error('获取政策文件列表失败:', error)
  }
}

// 获取叫应对象列表
const fetchTargets = async () => {
  try {
    const response = await callTargetApi.getList({ page_size: 1000, status: 1 })
    targetOptions.value = response.results
  } catch (error: any) {
    console.error('获取叫应对象列表失败:', error)
  }
}

// 日期范围变化
const handleDateRangeChange = (val: [string, string] | null) => {
  if (val) {
    searchForm.start_time = val[0]
    searchForm.end_time = val[1]
  } else {
    searchForm.start_time = undefined
    searchForm.end_time = undefined
  }
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params: PolicyDistributionListParams = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm,
    }
    const response = await policyDistributionApi.getList(params)
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
    policy_file_id: undefined,
    target_id: undefined,
    feedback_status: undefined,
    supervise_status: undefined,
    start_time: undefined,
    end_time: undefined,
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

// 新增
const handleCreate = () => {
  isEdit.value = false
  dialogTitle.value = '新增政策下发'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: PolicyDistribution) => {
  isEdit.value = true
  dialogTitle.value = '编辑政策下发'
  currentRow.value = row
  Object.assign(formData, {
    distribution_code: row.distribution_code,
    policy_file_id: row.policy_file_id,
    target_id: row.target_id,
    feedback_content: row.feedback_content,
    feedback_deadline: row.feedback_deadline,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: PolicyDistribution) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: PolicyDistribution) => {
  try {
    await ElMessageBox.confirm('确定要删除该政策文件下发吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await policyDistributionApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 反馈
const handleFeedback = (row: PolicyDistribution) => {
  feedbackRow.value = row
  feedbackData.feedback_content_actual = ''
  feedbackVisible.value = true
}

// 确认反馈
const handleFeedbackConfirm = async () => {
  if (!feedbackFormRef.value || !feedbackRow.value) return
  try {
    await feedbackFormRef.value.validate()
    feedbackLoading.value = true
    await policyDistributionApi.feedback(feedbackRow.value.id, feedbackData)
    ElMessage.success('反馈成功')
    feedbackVisible.value = false
    fetchData()
  } catch (error: any) {
    if (error !== false) {
      ElMessage.error(error.message || '反馈失败')
    }
  } finally {
    feedbackLoading.value = false
  }
}

// 督办
const handleSupervise = (row: PolicyDistribution) => {
  superviseRow.value = row
  superviseData.supervise_user_id = 0
  superviseVisible.value = true
}

// 确认督办
const handleSuperviseConfirm = async () => {
  if (!superviseFormRef.value || !superviseRow.value) return
  try {
    await superviseFormRef.value.validate()
    superviseLoading.value = true
    await policyDistributionApi.supervise(superviseRow.value.id, superviseData)
    ElMessage.success('督办成功')
    superviseVisible.value = false
    fetchData()
  } catch (error: any) {
    if (error !== false) {
      ElMessage.error(error.message || '督办失败')
    }
  } finally {
    superviseLoading.value = false
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    submitLoading.value = true
    if (isEdit.value && currentRow.value) {
      await policyDistributionApi.update(currentRow.value.id, formData)
      ElMessage.success('更新成功')
    } else {
      await policyDistributionApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error: any) {
    if (error !== false) {
      ElMessage.error(error.message || '操作失败')
    }
  } finally {
    submitLoading.value = false
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(formData, {
    distribution_code: '',
    policy_file_id: 0,
    target_id: 0,
    feedback_content: null,
    feedback_deadline: '',
    description: null,
    remark: null,
  })
  formRef.value?.clearValidate()
  currentRow.value = null
}

// 对话框关闭
const handleDialogClose = () => {
  resetForm()
}

// 初始化
onMounted(() => {
  fetchPolicyFiles()
  fetchTargets()
  fetchData()
})
</script>

<style scoped lang="scss">
.distribution-list {
  padding: 20px;

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
}
</style>
