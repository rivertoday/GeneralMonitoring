<template>
  <div class="task-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>预案任务</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增任务
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
        <el-form-item label="任务类型">
          <el-select v-model="searchForm.task_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="信息收集" :value="1" />
            <el-option label="决策指挥" :value="2" />
            <el-option label="资源调配" :value="3" />
            <el-option label="现场处置" :value="4" />
            <el-option label="其他" :value="5" />
          </el-select>
        </el-form-item>
        <el-form-item label="优先级">
          <el-select v-model="searchForm.priority" placeholder="请选择" clearable style="width: 120px">
            <el-option label="高" :value="1" />
            <el-option label="中" :value="2" />
            <el-option label="低" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入任务编码/名称"
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
        <el-table-column prop="task_code" label="任务编码" width="150" />
        <el-table-column prop="task_name" label="任务名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="plan_name" label="所属预案" width="200" show-overflow-tooltip />
        <el-table-column prop="flow_name" label="关联流程" width="150" show-overflow-tooltip />
        <el-table-column prop="task_type_display" label="任务类型" width="120" />
        <el-table-column prop="organization_name" label="负责组织" width="150" show-overflow-tooltip />
        <el-table-column prop="assign_user_name" label="执行人" width="120" />
        <el-table-column prop="assign_role_name" label="执行角色" width="120" />
        <el-table-column label="优先级" width="100">
          <template #default="{ row }">
            <el-tag :type="getPriorityTagType(row.priority)">
              {{ row.priority_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="estimated_time" label="预计时间(分钟)" width="130" />
        <el-table-column label="操作" width="200" fixed="right">
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
          <el-col :span="12">
            <el-form-item label="预案" prop="plan_id">
              <el-select
                v-model="formData.plan_id"
                placeholder="请选择预案"
                filterable
                style="width: 100%"
                @change="handlePlanChange"
              >
                <el-option
                  v-for="plan in planList"
                  :key="plan.id"
                  :label="`${plan.plan_code} - ${plan.plan_name}`"
                  :value="plan.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="关联流程">
              <el-select
                v-model="formData.flow_id"
                placeholder="请选择流程"
                clearable
                filterable
                style="width: 100%"
                :disabled="!formData.plan_id"
              >
                <el-option
                  v-for="flow in flowList"
                  :key="flow.id"
                  :label="`${flow.flow_code} - ${flow.flow_name}`"
                  :value="flow.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="任务编码" prop="task_code">
              <el-input v-model="formData.task_code" placeholder="请输入任务编码" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="任务名称" prop="task_name">
              <el-input v-model="formData.task_name" placeholder="请输入任务名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="任务类型" prop="task_type">
              <el-select v-model="formData.task_type" placeholder="请选择" style="width: 100%">
                <el-option label="信息收集" :value="1" />
                <el-option label="决策指挥" :value="2" />
                <el-option label="资源调配" :value="3" />
                <el-option label="现场处置" :value="4" />
                <el-option label="其他" :value="5" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="优先级">
              <el-select v-model="formData.priority" placeholder="请选择" style="width: 100%">
                <el-option label="高" :value="1" />
                <el-option label="中" :value="2" />
                <el-option label="低" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="负责组织">
              <el-input
                v-model="formData.organization_id"
                placeholder="请输入组织ID"
                type="number"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="执行人">
              <el-input
                v-model="formData.assign_user_id"
                placeholder="请输入用户ID"
                type="number"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="执行角色">
          <el-input
            v-model="formData.assign_role_id"
            placeholder="请输入角色ID"
            type="number"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="预计完成时间(分钟)">
          <el-input-number
            v-model="formData.estimated_time"
            :min="1"
            placeholder="预计完成时间"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="排序顺序">
          <el-input-number
            v-model="formData.sort_order"
            :min="0"
            placeholder="用于排序"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="任务描述">
          <el-input
            v-model="formData.task_description"
            type="textarea"
            :rows="4"
            placeholder="请输入任务描述"
          />
        </el-form-item>
        <el-form-item label="任务要求">
          <el-input
            v-model="formData.task_requirement"
            type="textarea"
            :rows="4"
            placeholder="请输入任务要求"
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
    <el-dialog v-model="detailVisible" title="任务详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="任务编码">{{ currentRow?.task_code }}</el-descriptions-item>
        <el-descriptions-item label="任务名称">{{ currentRow?.task_name }}</el-descriptions-item>
        <el-descriptions-item label="所属预案">{{ currentRow?.plan_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="关联流程">{{ currentRow?.flow_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="任务类型">{{ currentRow?.task_type_display }}</el-descriptions-item>
        <el-descriptions-item label="优先级">
          <el-tag :type="getPriorityTagType(currentRow?.priority)">
            {{ currentRow?.priority_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="负责组织">{{ currentRow?.organization_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="执行人">{{ currentRow?.assign_user_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="执行角色">{{ currentRow?.assign_role_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="预计完成时间">
          {{ currentRow?.estimated_time ? `${currentRow.estimated_time} 分钟` : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="排序顺序">{{ currentRow?.sort_order || 0 }}</el-descriptions-item>
        <el-descriptions-item label="任务描述" :span="2">{{ currentRow?.task_description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="任务要求" :span="2">{{ currentRow?.task_requirement || '-' }}</el-descriptions-item>
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
import { emergencyPlanApi, planFlowApi, planTaskApi } from '@/api/modules/plan'
import type { EmergencyPlan, PlanFlow, PlanTask, PlanTaskFormData } from '@/types/modules/plan'
import type { PaginatedResponse } from '@/api/types'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<PlanTask[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 预案列表和流程列表
const planList = ref<EmergencyPlan[]>([])
const flowList = ref<PlanFlow[]>([])

// 搜索表单
const searchForm = reactive({
  plan_id: undefined as number | undefined,
  task_type: undefined as number | undefined,
  priority: undefined as number | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增任务')
const currentRow = ref<PlanTask | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<PlanTaskFormData>({
  plan_id: 0,
  flow_id: null,
  task_code: '',
  task_name: '',
  task_type: 1,
  organization_id: null,
  assign_user_id: null,
  assign_role_id: null,
  task_description: null,
  task_requirement: null,
  estimated_time: null,
  priority: 3,
  sort_order: 0,
  description: null,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  plan_id: [
    { required: true, message: '请选择预案', trigger: 'change' },
  ],
  task_code: [
    { required: true, message: '请输入任务编码', trigger: 'blur' },
  ],
  task_name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' },
  ],
  task_type: [
    { required: true, message: '请选择任务类型', trigger: 'change' },
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

// 获取流程列表
const fetchFlowList = async (planId: number) => {
  try {
    const response = await planFlowApi.getList(planId)
    flowList.value = response
  } catch (error: any) {
    ElMessage.error(error.message || '获取流程列表失败')
  }
}

// 预案变化
const handlePlanChange = () => {
  formData.flow_id = null
  if (formData.plan_id) {
    fetchFlowList(formData.plan_id)
  } else {
    flowList.value = []
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
    const response = await planTaskApi.getList(params)
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
    task_type: undefined,
    priority: undefined,
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
  dialogTitle.value = '新增任务'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: PlanTask) => {
  isEdit.value = true
  dialogTitle.value = '编辑任务'
  currentRow.value = row
  formData.plan_id = row.plan_id
  if (row.plan_id) {
    fetchFlowList(row.plan_id)
  }
  Object.assign(formData, {
    flow_id: row.flow_id,
    task_code: row.task_code,
    task_name: row.task_name,
    task_type: row.task_type,
    organization_id: row.organization_id,
    assign_user_id: row.assign_user_id,
    assign_role_id: row.assign_role_id,
    task_description: row.task_description,
    task_requirement: row.task_requirement,
    estimated_time: row.estimated_time,
    priority: row.priority,
    sort_order: row.sort_order,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: PlanTask) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: PlanTask) => {
  try {
    await ElMessageBox.confirm('确定要删除该任务吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await planTaskApi.delete(row.id)
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
      const data: PlanTaskFormData = {
        plan_id: formData.plan_id,
        flow_id: formData.flow_id,
        task_name: formData.task_name,
        task_type: formData.task_type,
        organization_id: formData.organization_id,
        assign_user_id: formData.assign_user_id,
        assign_role_id: formData.assign_role_id,
        task_description: formData.task_description,
        task_requirement: formData.task_requirement,
        estimated_time: formData.estimated_time,
        priority: formData.priority,
        sort_order: formData.sort_order,
        description: formData.description,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        data.task_code = formData.task_code
        await planTaskApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        data.task_code = formData.task_code
        await planTaskApi.create(data)
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
    flow_id: null,
    task_code: '',
    task_name: '',
    task_type: 1,
    organization_id: null,
    assign_user_id: null,
    assign_role_id: null,
    task_description: null,
    task_requirement: null,
    estimated_time: null,
    priority: 3,
    sort_order: 0,
    description: null,
    remark: null,
  })
  formRef.value?.clearValidate()
  currentRow.value = null
  flowList.value = []
}

// 对话框关闭
const handleDialogClose = () => {
  resetForm()
  isEdit.value = false
}

// 获取优先级标签类型
const getPriorityTagType = (priority?: number) => {
  const priorityMap: Record<number, string> = {
    1: 'danger',
    2: 'warning',
    3: 'info',
  }
  return priorityMap[priority || 3] || 'info'
}

// 初始化
onMounted(() => {
  fetchPlanList()
  fetchData()
})
</script>

<style scoped lang="scss">
.task-list {
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
