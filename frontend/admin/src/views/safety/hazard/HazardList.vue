<template>
  <div class="hazard-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>危险源</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增危险源
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="危险源类型">
          <el-select v-model="searchForm.source_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="重大危险源" :value="1" />
            <el-option label="一般危险源" :value="2" />
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
        <el-form-item label="风险等级">
          <el-select v-model="searchForm.risk_level" placeholder="请选择" clearable style="width: 120px">
            <el-option label="高" :value="1" />
            <el-option label="中" :value="2" />
            <el-option label="低" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属街道">
          <el-input
            v-model="searchForm.street"
            placeholder="请输入街道"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="启用" :value="1" />
            <el-option label="禁用" :value="0" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入危险源编码/名称"
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
        <el-table-column prop="source_code" label="危险源编码" width="150" />
        <el-table-column prop="source_name" label="危险源名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="source_type_display" label="危险源类型" width="120" />
        <el-table-column prop="industry_type_display" label="行业类型" width="120" />
        <el-table-column prop="organization_name" label="所属企业" width="150" show-overflow-tooltip />
        <el-table-column prop="street" label="所属街道" width="120" />
        <el-table-column prop="address" label="详细地址" min-width="150" show-overflow-tooltip />
        <el-table-column label="风险等级" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.risk_level" :type="getRiskLevelTagType(row.risk_level)">
              {{ row.risk_level_display }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="contact_person" label="联系人" width="100" />
        <el-table-column prop="contact_phone" label="联系电话" width="120" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status_display }}
            </el-tag>
          </template>
        </el-table-column>
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
            <el-form-item label="危险源编码" prop="source_code">
              <el-input v-model="formData.source_code" placeholder="请输入危险源编码" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="危险源名称" prop="source_name">
              <el-input v-model="formData.source_name" placeholder="请输入危险源名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="危险源类型" prop="source_type">
              <el-select v-model="formData.source_type" placeholder="请选择" style="width: 100%">
                <el-option label="重大危险源" :value="1" />
                <el-option label="一般危险源" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="行业类型" prop="industry_type">
              <el-select v-model="formData.industry_type" placeholder="请选择" style="width: 100%">
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
            <el-form-item label="所属企业" prop="organization_id">
              <el-input
                v-model="formData.organization_id"
                placeholder="请输入企业ID"
                type="number"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="风险等级">
              <el-select v-model="formData.risk_level" placeholder="请选择" clearable style="width: 100%">
                <el-option label="高" :value="1" />
                <el-option label="中" :value="2" />
                <el-option label="低" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="经度">
              <el-input-number
                v-model="formData.longitude"
                :precision="7"
                :step="0.0000001"
                :min="-180"
                :max="180"
                placeholder="请输入经度"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="纬度">
              <el-input-number
                v-model="formData.latitude"
                :precision="7"
                :step="0.0000001"
                :min="-90"
                :max="90"
                placeholder="请输入纬度"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属街道">
              <el-input v-model="formData.street" placeholder="请输入所属街道" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="详细地址">
              <el-input v-model="formData.address" placeholder="请输入详细地址" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="联系人">
              <el-input v-model="formData.contact_person" placeholder="请输入联系人" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话">
              <el-input v-model="formData.contact_phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="状态">
          <el-radio-group v-model="formData.status">
            <el-radio :label="1">启用</el-radio>
            <el-radio :label="0">禁用</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="危险类别">
          <el-input v-model="formData.hazard_category" placeholder="请输入危险类别" />
        </el-form-item>
        <el-form-item label="危险描述">
          <el-input
            v-model="formData.hazard_description"
            type="textarea"
            :rows="4"
            placeholder="请输入危险描述"
          />
        </el-form-item>
        <el-form-item label="控制措施">
          <el-input
            v-model="formData.control_measures"
            type="textarea"
            :rows="4"
            placeholder="请输入控制措施"
          />
        </el-form-item>
        <el-form-item label="应急预案">
          <el-input v-model="formData.emergency_plan" placeholder="请输入应急预案" />
        </el-form-item>
        <el-form-item label="危险源描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入危险源描述"
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
    <el-dialog v-model="detailVisible" title="危险源详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="危险源编码">{{ currentRow?.source_code }}</el-descriptions-item>
        <el-descriptions-item label="危险源名称">{{ currentRow?.source_name }}</el-descriptions-item>
        <el-descriptions-item label="危险源类型">{{ currentRow?.source_type_display }}</el-descriptions-item>
        <el-descriptions-item label="行业类型">{{ currentRow?.industry_type_display }}</el-descriptions-item>
        <el-descriptions-item label="所属企业">{{ currentRow?.organization_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="风险等级">
          <el-tag v-if="currentRow?.risk_level" :type="getRiskLevelTagType(currentRow.risk_level)">
            {{ currentRow.risk_level_display }}
          </el-tag>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="所属街道">{{ currentRow?.street || '-' }}</el-descriptions-item>
        <el-descriptions-item label="详细地址">{{ currentRow?.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="经度">{{ currentRow?.longitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="纬度">{{ currentRow?.latitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系人">{{ currentRow?.contact_person || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentRow?.contact_phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'info'">
            {{ currentRow?.status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.hazard_category" label="危险类别" :span="2">
          {{ currentRow.hazard_category }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.hazard_description" label="危险描述" :span="2">
          {{ currentRow.hazard_description }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.control_measures" label="控制措施" :span="2">
          {{ currentRow.control_measures }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.emergency_plan" label="应急预案" :span="2">
          {{ currentRow.emergency_plan }}
        </el-descriptions-item>
        <el-descriptions-item label="危险源描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
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
import { hazardSourceApi } from '@/api/modules/safety'
import type { HazardSource, HazardSourceFormData } from '@/types/modules/safety'
import type { PaginatedResponse } from '@/api/types'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<HazardSource[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive({
  source_type: undefined as number | undefined,
  industry_type: undefined as number | undefined,
  risk_level: undefined as number | undefined,
  street: undefined as string | undefined,
  status: undefined as number | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增危险源')
const currentRow = ref<HazardSource | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<HazardSourceFormData>({
  source_code: '',
  source_name: '',
  source_type: 1,
  industry_type: 1,
  organization_id: 0,
  longitude: null,
  latitude: null,
  street: null,
  address: null,
  risk_level: null,
  hazard_category: null,
  hazard_description: null,
  control_measures: null,
  emergency_plan: null,
  contact_person: null,
  contact_phone: null,
  description: null,
  status: 1,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  source_code: [
    { required: true, message: '请输入危险源编码', trigger: 'blur' },
  ],
  source_name: [
    { required: true, message: '请输入危险源名称', trigger: 'blur' },
  ],
  source_type: [
    { required: true, message: '请选择危险源类型', trigger: 'change' },
  ],
  industry_type: [
    { required: true, message: '请选择行业类型', trigger: 'change' },
  ],
  organization_id: [
    { required: true, message: '请输入所属企业ID', trigger: 'blur' },
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
    const response = await hazardSourceApi.getList(params)
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
    source_type: undefined,
    industry_type: undefined,
    risk_level: undefined,
    street: undefined,
    status: undefined,
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
  dialogTitle.value = '新增危险源'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: HazardSource) => {
  isEdit.value = true
  dialogTitle.value = '编辑危险源'
  currentRow.value = row
  Object.assign(formData, {
    source_code: row.source_code,
    source_name: row.source_name,
    source_type: row.source_type,
    industry_type: row.industry_type,
    organization_id: row.organization_id,
    longitude: row.longitude,
    latitude: row.latitude,
    street: row.street,
    address: row.address,
    risk_level: row.risk_level,
    hazard_category: row.hazard_category,
    hazard_description: row.hazard_description,
    control_measures: row.control_measures,
    emergency_plan: row.emergency_plan,
    contact_person: row.contact_person,
    contact_phone: row.contact_phone,
    description: row.description,
    status: row.status,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: HazardSource) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: HazardSource) => {
  try {
    await ElMessageBox.confirm('确定要删除该危险源吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await hazardSourceApi.delete(row.id)
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
      const data: HazardSourceFormData = {
        source_name: formData.source_name,
        source_type: formData.source_type,
        industry_type: formData.industry_type,
        organization_id: formData.organization_id,
        longitude: formData.longitude,
        latitude: formData.latitude,
        street: formData.street,
        address: formData.address,
        risk_level: formData.risk_level,
        hazard_category: formData.hazard_category,
        hazard_description: formData.hazard_description,
        control_measures: formData.control_measures,
        emergency_plan: formData.emergency_plan,
        contact_person: formData.contact_person,
        contact_phone: formData.contact_phone,
        description: formData.description,
        status: formData.status,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        data.source_code = formData.source_code
        await hazardSourceApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        data.source_code = formData.source_code
        await hazardSourceApi.create(data)
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
    source_code: '',
    source_name: '',
    source_type: 1,
    industry_type: 1,
    organization_id: 0,
    longitude: null,
    latitude: null,
    street: null,
    address: null,
    risk_level: null,
    hazard_category: null,
    hazard_description: null,
    control_measures: null,
    emergency_plan: null,
    contact_person: null,
    contact_phone: null,
    description: null,
    status: 1,
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

// 获取风险等级标签类型
const getRiskLevelTagType = (riskLevel: number) => {
  const levelMap: Record<number, string> = {
    1: 'danger',
    2: 'warning',
    3: 'info',
  }
  return levelMap[riskLevel] || 'info'
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.hazard-list {
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
