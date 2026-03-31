<template>
  <div class="plan-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>应急预案</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增预案
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="预案类型">
          <el-select v-model="searchForm.plan_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="综合应急预案" :value="1" />
            <el-option label="专项应急预案" :value="2" />
            <el-option label="现场处置方案" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="行业类型">
          <el-select v-model="searchForm.industry_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="森林火灾" :value="1" />
            <el-option label="防汛" :value="2" />
            <el-option label="交通运输" :value="3" />
            <el-option label="危险化学品" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="预案状态">
          <el-select v-model="searchForm.plan_status" placeholder="请选择" clearable style="width: 150px">
            <el-option label="草稿" :value="0" />
            <el-option label="已发布" :value="1" />
            <el-option label="已修订" :value="2" />
            <el-option label="已废止" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入预案编码/名称"
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
        <el-table-column prop="plan_code" label="预案编码" width="150" />
        <el-table-column prop="plan_name" label="预案名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="plan_type_display" label="预案类型" width="120" />
        <el-table-column prop="industry_type_display" label="行业类型" width="100" />
        <el-table-column prop="version" label="版本号" width="100" />
        <el-table-column prop="organization_name" label="所属部门" width="150" show-overflow-tooltip />
        <el-table-column label="预案状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.plan_status)">
              {{ row.plan_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publish_time" label="发布时间" width="160" />
        <el-table-column prop="effective_time" label="生效时间" width="160" />
        <el-table-column label="操作" width="350" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button
              v-if="row.plan_status === 0"
              type="primary"
              link
              size="small"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              v-if="row.plan_status === 0"
              type="success"
              link
              size="small"
              @click="handlePublish(row)"
            >
              发布
            </el-button>
            <el-button
              v-if="row.plan_status === 1"
              type="warning"
              link
              size="small"
              @click="handleRevise(row)"
            >
              修订
            </el-button>
            <el-button
              v-if="row.plan_status === 1 || row.plan_status === 2"
              type="danger"
              link
              size="small"
              @click="handleAbolish(row)"
            >
              废止
            </el-button>
            <el-button type="info" link size="small" @click="handleViewStructure(row)">
              结构
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
            <el-form-item label="预案编码" prop="plan_code">
              <el-input v-model="formData.plan_code" placeholder="请输入预案编码" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预案名称" prop="plan_name">
              <el-input v-model="formData.plan_name" placeholder="请输入预案名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预案类型" prop="plan_type">
              <el-select v-model="formData.plan_type" placeholder="请选择" style="width: 100%">
                <el-option label="综合应急预案" :value="1" />
                <el-option label="专项应急预案" :value="2" />
                <el-option label="现场处置方案" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="行业类型">
              <el-select v-model="formData.industry_type" placeholder="请选择" clearable style="width: 100%">
                <el-option label="森林火灾" :value="1" />
                <el-option label="防汛" :value="2" />
                <el-option label="交通运输" :value="3" />
                <el-option label="危险化学品" :value="4" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="版本号" prop="version">
              <el-input v-model="formData.version" placeholder="请输入版本号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属部门">
              <el-input v-model="formData.organization_id" placeholder="请输入部门ID" type="number" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="生效时间">
          <el-date-picker
            v-model="formData.effective_time"
            type="datetime"
            placeholder="请选择生效时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="失效时间">
          <el-date-picker
            v-model="formData.expire_time"
            type="datetime"
            placeholder="请选择失效时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="预案摘要">
          <el-input
            v-model="formData.plan_summary"
            type="textarea"
            :rows="4"
            placeholder="请输入预案摘要"
          />
        </el-form-item>
        <el-form-item label="预案描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入预案描述"
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
    <el-dialog v-model="detailVisible" title="预案详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="预案编码">{{ currentRow?.plan_code }}</el-descriptions-item>
        <el-descriptions-item label="预案名称">{{ currentRow?.plan_name }}</el-descriptions-item>
        <el-descriptions-item label="预案类型">{{ currentRow?.plan_type_display }}</el-descriptions-item>
        <el-descriptions-item label="行业类型">{{ currentRow?.industry_type_display || '-' }}</el-descriptions-item>
        <el-descriptions-item label="版本号">{{ currentRow?.version }}</el-descriptions-item>
        <el-descriptions-item label="所属部门">{{ currentRow?.organization_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="预案状态">
          <el-tag :type="getStatusTagType(currentRow?.plan_status)">
            {{ currentRow?.plan_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="发布时间">{{ currentRow?.publish_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="生效时间">{{ currentRow?.effective_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="失效时间">{{ currentRow?.expire_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建人">{{ currentRow?.create_user_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="审批人">{{ currentRow?.approve_user_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="审批时间">{{ currentRow?.approve_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="预案摘要" :span="2">{{ currentRow?.plan_summary || '-' }}</el-descriptions-item>
        <el-descriptions-item label="预案描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="修订原因" :span="2">{{ currentRow?.revision_reason || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 发布对话框 -->
    <el-dialog v-model="publishVisible" title="发布预案" width="500px">
      <el-alert
        type="info"
        :closable="false"
        show-icon
        style="margin-bottom: 20px"
      >
        发布后预案将生效，请确认预案信息无误。
      </el-alert>
      <template #footer>
        <el-button @click="publishVisible = false">取消</el-button>
        <el-button type="primary" :loading="publishLoading" @click="handlePublishSubmit">
          确定发布
        </el-button>
      </template>
    </el-dialog>

    <!-- 修订对话框 -->
    <el-dialog v-model="reviseVisible" title="修订预案" width="600px">
      <el-form ref="reviseFormRef" :model="reviseForm" :rules="reviseFormRules" label-width="120px">
        <el-form-item label="修订原因" prop="revision_reason">
          <el-input
            v-model="reviseForm.revision_reason"
            type="textarea"
            :rows="4"
            placeholder="请输入修订原因"
          />
        </el-form-item>
        <el-form-item label="新版本号">
          <el-input v-model="reviseForm.version" placeholder="请输入新版本号，留空自动递增" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="reviseVisible = false">取消</el-button>
        <el-button type="primary" :loading="reviseLoading" @click="handleReviseSubmit">
          确定修订
        </el-button>
      </template>
    </el-dialog>

    <!-- 废止对话框 -->
    <el-dialog v-model="abolishVisible" title="废止预案" width="600px">
      <el-form ref="abolishFormRef" :model="abolishForm" label-width="120px">
        <el-form-item label="废止原因">
          <el-input
            v-model="abolishForm.reason"
            type="textarea"
            :rows="4"
            placeholder="请输入废止原因"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="abolishVisible = false">取消</el-button>
        <el-button type="danger" :loading="abolishLoading" @click="handleAbolishSubmit">
          确定废止
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { emergencyPlanApi } from '@/api/modules/plan'
import type { EmergencyPlan, EmergencyPlanFormData } from '@/types/modules/plan'
import type { PaginatedResponse } from '@/api/types'

const router = useRouter()

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)
const publishLoading = ref(false)
const reviseLoading = ref(false)
const abolishLoading = ref(false)

// 表格数据
const tableData = ref<EmergencyPlan[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive({
  plan_type: undefined as number | undefined,
  industry_type: undefined as number | undefined,
  plan_status: undefined as number | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const publishVisible = ref(false)
const reviseVisible = ref(false)
const abolishVisible = ref(false)
const dialogTitle = ref('新增预案')
const currentRow = ref<EmergencyPlan | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const reviseFormRef = ref<FormInstance>()
const abolishFormRef = ref<FormInstance>()
const formData = reactive<EmergencyPlanFormData>({
  plan_code: '',
  plan_name: '',
  plan_type: 1,
  industry_type: null,
  organization_id: null,
  version: '1.0',
  plan_file_path: null,
  plan_file_name: null,
  plan_summary: null,
  effective_time: null,
  expire_time: null,
  description: null,
  remark: null,
})

const reviseForm = reactive({
  revision_reason: '',
  version: '',
})

const abolishForm = reactive({
  reason: '',
})

// 表单验证规则
const formRules: FormRules = {
  plan_code: [
    { required: true, message: '请输入预案编码', trigger: 'blur' },
  ],
  plan_name: [
    { required: true, message: '请输入预案名称', trigger: 'blur' },
  ],
  plan_type: [
    { required: true, message: '请选择预案类型', trigger: 'change' },
  ],
  version: [
    { required: true, message: '请输入版本号', trigger: 'blur' },
  ],
}

const reviseFormRules: FormRules = {
  revision_reason: [
    { required: true, message: '请输入修订原因', trigger: 'blur' },
  ],
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
    const response = await emergencyPlanApi.getList(params)
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
    plan_type: undefined,
    industry_type: undefined,
    plan_status: undefined,
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
  dialogTitle.value = '新增预案'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: EmergencyPlan) => {
  isEdit.value = true
  dialogTitle.value = '编辑预案'
  currentRow.value = row
  Object.assign(formData, {
    plan_code: row.plan_code,
    plan_name: row.plan_name,
    plan_type: row.plan_type,
    industry_type: row.industry_type,
    organization_id: row.organization_id,
    version: row.version,
    plan_file_path: row.plan_file_path,
    plan_file_name: row.plan_file_name,
    plan_summary: row.plan_summary,
    effective_time: row.effective_time,
    expire_time: row.expire_time,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: EmergencyPlan) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: EmergencyPlan) => {
  try {
    await ElMessageBox.confirm('确定要删除该预案吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await emergencyPlanApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 发布
const handlePublish = (row: EmergencyPlan) => {
  currentRow.value = row
  publishVisible.value = true
}

// 发布提交
const handlePublishSubmit = async () => {
  if (!currentRow.value) return

  publishLoading.value = true
  try {
    await emergencyPlanApi.publish(currentRow.value.id)
    ElMessage.success('发布成功')
    publishVisible.value = false
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '发布失败')
  } finally {
    publishLoading.value = false
  }
}

// 修订
const handleRevise = (row: EmergencyPlan) => {
  currentRow.value = row
  reviseForm.revision_reason = ''
  reviseForm.version = ''
  reviseVisible.value = true
}

// 修订提交
const handleReviseSubmit = async () => {
  if (!reviseFormRef.value || !currentRow.value) return

  await reviseFormRef.value.validate(async (valid) => {
    if (!valid) return

    reviseLoading.value = true
    try {
      await emergencyPlanApi.revise(currentRow.value!.id, {
        revision_reason: reviseForm.revision_reason,
        version: reviseForm.version || undefined,
      })
      ElMessage.success('修订成功')
      reviseVisible.value = false
      fetchData()
    } catch (error: any) {
      ElMessage.error(error.message || '修订失败')
    } finally {
      reviseLoading.value = false
    }
  })
}

// 废止
const handleAbolish = (row: EmergencyPlan) => {
  currentRow.value = row
  abolishForm.reason = ''
  abolishVisible.value = true
}

// 废止提交
const handleAbolishSubmit = async () => {
  if (!currentRow.value) return

  abolishLoading.value = true
  try {
    await emergencyPlanApi.abolish(currentRow.value.id, abolishForm.reason || undefined)
    ElMessage.success('废止成功')
    abolishVisible.value = false
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '废止失败')
  } finally {
    abolishLoading.value = false
  }
}

// 查看结构
const handleViewStructure = (row: EmergencyPlan) => {
  router.push({
    name: 'PlanStructure',
    query: { plan_id: row.id },
  })
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const data: EmergencyPlanFormData = {
        plan_name: formData.plan_name,
        plan_type: formData.plan_type,
        industry_type: formData.industry_type,
        organization_id: formData.organization_id,
        version: formData.version,
        plan_file_path: formData.plan_file_path,
        plan_file_name: formData.plan_file_name,
        plan_summary: formData.plan_summary,
        effective_time: formData.effective_time,
        expire_time: formData.expire_time,
        description: formData.description,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        data.plan_code = formData.plan_code
        await emergencyPlanApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        data.plan_code = formData.plan_code
        await emergencyPlanApi.create(data)
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
    plan_code: '',
    plan_name: '',
    plan_type: 1,
    industry_type: null,
    organization_id: null,
    version: '1.0',
    plan_file_path: null,
    plan_file_name: null,
    plan_summary: null,
    effective_time: null,
    expire_time: null,
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
    1: 'success',
    2: 'warning',
    3: 'danger',
  }
  return statusMap[status || 0] || 'info'
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.plan-list {
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
