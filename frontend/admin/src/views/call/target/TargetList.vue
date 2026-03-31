<template>
  <div class="target-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>叫应对象管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增叫应对象
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="对象类型">
          <el-select v-model="searchForm.target_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="政府部门" :value="1" />
            <el-option label="企业单位" :value="2" />
            <el-option label="事业单位" :value="3" />
          </el-select>
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
            placeholder="请输入对象编码/名称/责任人/电话"
            clearable
            style="width: 250px"
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
        <el-table-column prop="target_code" label="对象编码" width="150" />
        <el-table-column prop="target_name" label="对象名称" width="150" />
        <el-table-column prop="target_type_display" label="对象类型" width="120" />
        <el-table-column prop="enterprise_name" label="企业名称" width="150" show-overflow-tooltip />
        <el-table-column prop="safety_person" label="安全责任人" width="120" />
        <el-table-column prop="contact_phone" label="联系电话" width="130" />
        <el-table-column prop="contact_address" label="联系地址" min-width="200" show-overflow-tooltip />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '启用' : '禁用' }}
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
            <el-button
              type="primary"
              link
              size="small"
              @click="handleUpdateStatus(row)"
            >
              {{ row.status === 1 ? '禁用' : '启用' }}
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
            <el-form-item label="对象编码" prop="target_code">
              <el-input v-model="formData.target_code" placeholder="请输入对象编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="对象名称" prop="target_name">
              <el-input v-model="formData.target_name" placeholder="请输入对象名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="对象类型" prop="target_type">
              <el-select v-model="formData.target_type" placeholder="请选择" style="width: 100%">
                <el-option label="政府部门" :value="1" />
                <el-option label="企业单位" :value="2" />
                <el-option label="事业单位" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-radio-group v-model="formData.status">
                <el-radio :label="1">启用</el-radio>
                <el-radio :label="0">禁用</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20" v-if="formData.target_type === 2">
          <el-col :span="12">
            <el-form-item label="企业名称">
              <el-input v-model="formData.enterprise_name" placeholder="请输入企业名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属组织ID">
              <el-input-number
                v-model="formData.organization_id"
                :min="1"
                placeholder="请输入所属组织ID"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="企业信息" v-if="formData.target_type === 2">
          <el-input
            v-model="formData.enterprise_info"
            type="textarea"
            :rows="3"
            placeholder="请输入企业信息"
          />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="安全责任人" prop="safety_person">
              <el-input v-model="formData.safety_person" placeholder="请输入安全责任人" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="contact_phone">
              <el-input v-model="formData.contact_phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="联系地址">
          <el-input v-model="formData.contact_address" placeholder="请输入联系地址" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入描述"
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
    <el-dialog v-model="detailVisible" title="叫应对象详情" width="800px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="对象编码">{{ currentRow?.target_code }}</el-descriptions-item>
        <el-descriptions-item label="对象名称">{{ currentRow?.target_name }}</el-descriptions-item>
        <el-descriptions-item label="对象类型">{{ currentRow?.target_type_display }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'info'">
            {{ currentRow?.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="所属组织ID">{{ currentRow?.organization_id || '-' }}</el-descriptions-item>
        <el-descriptions-item label="企业名称" v-if="currentRow?.target_type === 2">
          {{ currentRow?.enterprise_name || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="企业信息" :span="2" v-if="currentRow?.target_type === 2">
          {{ currentRow?.enterprise_info || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="安全责任人">{{ currentRow?.safety_person }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentRow?.contact_phone }}</el-descriptions-item>
        <el-descriptions-item label="联系地址" :span="2">{{ currentRow?.contact_address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
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
import { callTargetApi } from '@/api/modules/call'
import type { CallTarget, CallTargetListParams, CallTargetFormData } from '@/types/modules/call'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<CallTarget[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive<CallTargetListParams>({
  target_type: undefined,
  status: undefined,
  search: undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增叫应对象')
const currentRow = ref<CallTarget | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<CallTargetFormData>({
  target_code: '',
  target_name: '',
  target_type: 1,
  organization_id: null,
  enterprise_name: null,
  enterprise_info: null,
  safety_person: '',
  contact_phone: '',
  contact_address: null,
  description: null,
  status: 1,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  target_code: [
    { required: true, message: '请输入对象编码', trigger: 'blur' },
  ],
  target_name: [
    { required: true, message: '请输入对象名称', trigger: 'blur' },
  ],
  target_type: [
    { required: true, message: '请选择对象类型', trigger: 'change' },
  ],
  safety_person: [
    { required: true, message: '请输入安全责任人', trigger: 'blur' },
  ],
  contact_phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' },
  ],
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params: CallTargetListParams = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm,
    }
    const response = await callTargetApi.getList(params)
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
    target_type: undefined,
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
  dialogTitle.value = '新增叫应对象'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: CallTarget) => {
  isEdit.value = true
  dialogTitle.value = '编辑叫应对象'
  currentRow.value = row
  Object.assign(formData, {
    target_code: row.target_code,
    target_name: row.target_name,
    target_type: row.target_type,
    organization_id: row.organization_id,
    enterprise_name: row.enterprise_name,
    enterprise_info: row.enterprise_info,
    safety_person: row.safety_person,
    contact_phone: row.contact_phone,
    contact_address: row.contact_address,
    description: row.description,
    status: row.status,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: CallTarget) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: CallTarget) => {
  try {
    await ElMessageBox.confirm('确定要删除该叫应对象吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await callTargetApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 更新状态
const handleUpdateStatus = async (row: CallTarget) => {
  try {
    const newStatus: 0 | 1 = row.status === 1 ? 0 : 1
    await callTargetApi.partialUpdate(row.id, { status: newStatus })
    ElMessage.success('更新状态成功')
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '更新状态失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    submitLoading.value = true
    if (isEdit.value && currentRow.value) {
      await callTargetApi.update(currentRow.value.id, formData)
      ElMessage.success('更新成功')
    } else {
      await callTargetApi.create(formData)
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
    target_code: '',
    target_name: '',
    target_type: 1,
    organization_id: null,
    enterprise_name: null,
    enterprise_info: null,
    safety_person: '',
    contact_phone: '',
    contact_address: null,
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
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.target-list {
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
