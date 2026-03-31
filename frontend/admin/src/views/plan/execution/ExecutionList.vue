<template>
  <div class="execution-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>预案执行</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增执行记录
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="预案">
          <el-select
            v-model="searchForm.plan_id"
            placeholder="请选择预案"
            clearable
            filterable
            style="width: 250px"
          >
            <el-option
              v-for="plan in planList"
              :key="plan.id"
              :label="`${plan.plan_code} - ${plan.plan_name}`"
              :value="plan.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="执行类型">
          <el-select v-model="searchForm.execution_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="演练执行" :value="1" />
            <el-option label="实战执行" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="执行状态">
          <el-select v-model="searchForm.execution_status" placeholder="请选择" clearable style="width: 150px">
            <el-option label="未开始" :value="0" />
            <el-option label="执行中" :value="1" />
            <el-option label="已完成" :value="2" />
            <el-option label="已终止" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入执行编码"
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
        <el-table-column prop="execution_code" label="执行编码" width="150" />
        <el-table-column prop="plan_name" label="所属预案" width="200" show-overflow-tooltip />
        <el-table-column prop="warning_title" label="关联预警" width="200" show-overflow-tooltip />
        <el-table-column prop="execution_type_display" label="执行类型" width="120" />
        <el-table-column label="执行状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.execution_status)">
              {{ row.execution_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="command_user_name" label="指挥人" width="120" />
        <el-table-column prop="current_flow_name" label="当前流程" width="150" show-overflow-tooltip />
        <el-table-column prop="start_time" label="开始时间" width="160" />
        <el-table-column prop="end_time" label="结束时间" width="160" />
        <el-table-column prop="duration" label="执行时长(分钟)" width="130" />
        <el-table-column label="操作" width="350" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button
              v-if="row.execution_status === 0"
              type="success"
              link
              size="small"
              @click="handleStart(row)"
            >
              启动
            </el-button>
            <el-button
              v-if="row.execution_status === 1"
              type="warning"
              link
              size="small"
              @click="handleUpdateStatus(row)"
            >
              更新状态
            </el-button>
            <el-button
              v-if="row.execution_status === 1"
              type="success"
              link
              size="small"
              @click="handleComplete(row)"
            >
              完成
            </el-button>
            <el-button
              v-if="row.execution_status === 0 || row.execution_status === 1"
              type="danger"
              link
              size="small"
              @click="handleTerminate(row)"
            >
              终止
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
        <el-form-item label="预案" prop="plan_id">
          <el-select
            v-model="formData.plan_id"
            placeholder="请选择预案"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="plan in planList"
              :key="plan.id"
              :label="`${plan.plan_code} - ${plan.plan_name}`"
              :value="plan.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="关联预警">
          <el-input
            v-model="formData.warning_id"
            placeholder="请输入预警ID（可选）"
            type="number"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="执行类型" prop="execution_type">
          <el-select v-model="formData.execution_type" placeholder="请选择" style="width: 100%">
            <el-option label="演练执行" :value="1" />
            <el-option label="实战执行" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="指挥人" prop="command_user_id">
          <el-input
            v-model="formData.command_user_id"
            placeholder="请输入指挥人ID"
            type="number"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="执行描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="4"
            placeholder="请输入执行描述"
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
    <el-dialog v-model="detailVisible" title="执行详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="执行编码">{{ currentRow?.execution_code }}</el-descriptions-item>
        <el-descriptions-item label="所属预案">{{ currentRow?.plan_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="关联预警">{{ currentRow?.warning_title || '-' }}</el-descriptions-item>
        <el-descriptions-item label="执行类型">{{ currentRow?.execution_type_display }}</el-descriptions-item>
        <el-descriptions-item label="执行状态">
          <el-tag :type="getStatusTagType(currentRow?.execution_status)">
            {{ currentRow?.execution_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="指挥人">{{ currentRow?.command_user_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="当前流程">{{ currentRow?.current_flow_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="开始时间">{{ currentRow?.start_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="结束时间">{{ currentRow?.end_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="执行时长">
          {{ currentRow?.duration ? `${currentRow.duration} 分钟` : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="执行描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="执行结果" :span="2">{{ currentRow?.execution_result || '-' }}</el-descriptions-item>
        <el-descriptions-item label="执行总结" :span="2">{{ currentRow?.execution_summary || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 更新状态对话框 -->
    <el-dialog v-model="statusVisible" title="更新执行状态" width="600px">
      <el-form ref="statusFormRef" :model="statusForm" :rules="statusFormRules" label-width="120px">
        <el-form-item label="执行状态" prop="execution_status">
          <el-select v-model="statusForm.execution_status" placeholder="请选择" style="width: 100%">
            <el-option label="执行中" :value="1" />
            <el-option label="已完成" :value="2" />
            <el-option label="已终止" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="当前流程">
          <el-input
            v-model="statusForm.current_flow_id"
            placeholder="请输入当前流程ID（可选）"
            type="number"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="执行结果">
          <el-input
            v-model="statusForm.execution_result"
            type="textarea"
            :rows="4"
            placeholder="请输入执行结果（可选）"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="statusVisible = false">取消</el-button>
        <el-button type="primary" :loading="statusLoading" @click="handleStatusSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 完成执行对话框 -->
    <el-dialog v-model="completeVisible" title="完成执行" width="600px">
      <el-form ref="completeFormRef" :model="completeForm" label-width="120px">
        <el-form-item label="执行总结">
          <el-input
            v-model="completeForm.execution_summary"
            type="textarea"
            :rows="6"
            placeholder="请输入执行总结"
          />
        </el-form-item>
        <el-form-item label="执行结果">
          <el-input
            v-model="completeForm.execution_result"
            type="textarea"
            :rows="4"
            placeholder="请输入执行结果"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="completeVisible = false">取消</el-button>
        <el-button type="primary" :loading="completeLoading" @click="handleCompleteSubmit">
          确定完成
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { emergencyPlanApi, planExecutionApi } from '@/api/modules/plan'
import type { EmergencyPlan, PlanExecution, PlanExecutionFormData } from '@/types/modules/plan'
import type { PaginatedResponse } from '@/api/types'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)
const statusLoading = ref(false)
const completeLoading = ref(false)

// 表格数据
const tableData = ref<PlanExecution[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 预案列表
const planList = ref<EmergencyPlan[]>([])

// 搜索表单
const searchForm = reactive({
  plan_id: undefined as number | undefined,
  execution_type: undefined as number | undefined,
  execution_status: undefined as number | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const statusVisible = ref(false)
const completeVisible = ref(false)
const dialogTitle = ref('新增执行记录')
const currentRow = ref<PlanExecution | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const statusFormRef = ref<FormInstance>()
const completeFormRef = ref<FormInstance>()
const formData = reactive<PlanExecutionFormData>({
  plan_id: 0,
  warning_id: null,
  execution_type: 1,
  command_user_id: 0,
  description: null,
  remark: null,
})

const statusForm = reactive({
  execution_status: 1,
  current_flow_id: undefined as number | undefined,
  execution_result: '',
})

const completeForm = reactive({
  execution_summary: '',
  execution_result: '',
})

// 表单验证规则
const formRules: FormRules = {
  plan_id: [
    { required: true, message: '请选择预案', trigger: 'change' },
  ],
  execution_type: [
    { required: true, message: '请选择执行类型', trigger: 'change' },
  ],
  command_user_id: [
    { required: true, message: '请输入指挥人ID', trigger: 'blur' },
  ],
}

const statusFormRules: FormRules = {
  execution_status: [
    { required: true, message: '请选择执行状态', trigger: 'change' },
  ],
}

// 获取预案列表
const fetchPlanList = async () => {
  try {
    const response = await emergencyPlanApi.getList({ page_size: 1000 })
    planList.value = response.results
  } catch (error: any) {
    ElMessage.error(error.message || '获取预案列表失败')
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
    const response = await planExecutionApi.getList(params)
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
    plan_id: undefined,
    execution_type: undefined,
    execution_status: undefined,
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
  dialogTitle.value = '新增执行记录'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: PlanExecution) => {
  isEdit.value = true
  dialogTitle.value = '编辑执行记录'
  currentRow.value = row
  Object.assign(formData, {
    plan_id: row.plan_id,
    warning_id: row.warning_id,
    execution_type: row.execution_type,
    command_user_id: row.command_user_id,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: PlanExecution) => {
  currentRow.value = row
  detailVisible.value = true
}

// 启动
const handleStart = async (row: PlanExecution) => {
  try {
    await ElMessageBox.confirm('确定要启动该执行记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await planExecutionApi.start(row.id)
    ElMessage.success('启动成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '启动失败')
    }
  }
}

// 更新状态
const handleUpdateStatus = (row: PlanExecution) => {
  currentRow.value = row
  statusForm.execution_status = row.execution_status
  statusForm.current_flow_id = row.current_flow_id || undefined
  statusForm.execution_result = row.execution_result || ''
  statusVisible.value = true
}

// 更新状态提交
const handleStatusSubmit = async () => {
  if (!statusFormRef.value || !currentRow.value) return

  await statusFormRef.value.validate(async (valid) => {
    if (!valid) return

    statusLoading.value = true
    try {
      await planExecutionApi.updateStatus(currentRow.value!.id, statusForm.execution_status, {
        current_flow_id: statusForm.current_flow_id,
        execution_result: statusForm.execution_result || undefined,
      })
      ElMessage.success('更新成功')
      statusVisible.value = false
      fetchData()
    } catch (error: any) {
      ElMessage.error(error.message || '更新失败')
    } finally {
      statusLoading.value = false
    }
  })
}

// 完成
const handleComplete = (row: PlanExecution) => {
  currentRow.value = row
  completeForm.execution_summary = row.execution_summary || ''
  completeForm.execution_result = row.execution_result || ''
  completeVisible.value = true
}

// 完成提交
const handleCompleteSubmit = async () => {
  if (!currentRow.value) return

  completeLoading.value = true
  try {
    await planExecutionApi.complete(currentRow.value.id, {
      execution_summary: completeForm.execution_summary || undefined,
      execution_result: completeForm.execution_result || undefined,
    })
    ElMessage.success('完成成功')
    completeVisible.value = false
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '完成失败')
  } finally {
    completeLoading.value = false
  }
}

// 终止
const handleTerminate = async (row: PlanExecution) => {
  try {
    await ElMessageBox.confirm('确定要终止该执行记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await planExecutionApi.updateStatus(row.id, 3)
    ElMessage.success('终止成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '终止失败')
    }
  }
}

// 删除
const handleDelete = async (row: PlanExecution) => {
  try {
    await ElMessageBox.confirm('确定要删除该执行记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await planExecutionApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const data: PlanExecutionFormData = {
        plan_id: formData.plan_id,
        warning_id: formData.warning_id,
        execution_type: formData.execution_type,
        command_user_id: formData.command_user_id,
        description: formData.description,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        await planExecutionApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await planExecutionApi.create(data)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchData()
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
    plan_id: 0,
    warning_id: null,
    execution_type: 1,
    command_user_id: 0,
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

// 获取状态标签类型
const getStatusTagType = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: 'info',
    1: 'warning',
    2: 'success',
    3: 'danger',
  }
  return statusMap[status || 0] || 'info'
}

// 初始化
onMounted(() => {
  fetchPlanList()
  fetchData()
})
</script>

<style scoped lang="scss">
.execution-list {
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
