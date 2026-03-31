<template>
  <div class="resource-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>安全资源</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增资源
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="资源类型">
          <el-select v-model="searchForm.resource_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="救援队伍" :value="1" />
            <el-option label="应急专家" :value="2" />
            <el-option label="物资装备" :value="3" />
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
            placeholder="请输入资源编码/名称"
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
        <el-table-column prop="resource_code" label="资源编码" width="150" />
        <el-table-column prop="resource_name" label="资源名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="resource_type_display" label="资源类型" width="120" />
        <el-table-column prop="sub_type_display" label="子类型" width="120" />
        <el-table-column prop="street" label="所属街道" width="120" />
        <el-table-column prop="address" label="详细地址" min-width="150" show-overflow-tooltip />
        <el-table-column prop="organization_name" label="所属组织" width="150" show-overflow-tooltip />
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
            <el-form-item label="资源编码" prop="resource_code">
              <el-input v-model="formData.resource_code" placeholder="请输入资源编码" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="资源名称" prop="resource_name">
              <el-input v-model="formData.resource_name" placeholder="请输入资源名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="资源类型" prop="resource_type">
              <el-select v-model="formData.resource_type" placeholder="请选择" style="width: 100%" @change="handleResourceTypeChange">
                <el-option label="救援队伍" :value="1" />
                <el-option label="应急专家" :value="2" />
                <el-option label="物资装备" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="子类型" prop="sub_type">
              <el-select v-model="formData.sub_type" placeholder="请选择" clearable style="width: 100%">
                <el-option
                  v-for="option in subTypeOptions"
                  :key="option.value"
                  :label="option.label"
                  :value="option.value"
                />
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
            <el-form-item label="所属组织">
              <el-input
                v-model="formData.organization_id"
                placeholder="请输入组织ID"
                type="number"
                style="width: 100%"
              />
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
        
        <!-- 救援队伍特有字段 -->
        <template v-if="formData.resource_type === 1">
          <el-form-item label="人数">
            <el-input-number
              v-model="formData.capacity"
              :min="0"
              placeholder="请输入人数"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="装备信息">
            <el-input
              v-model="formData.equipment_info"
              type="textarea"
              :rows="4"
              placeholder="请输入装备信息（JSON格式）"
            />
          </el-form-item>
        </template>

        <!-- 应急专家特有字段 -->
        <template v-if="formData.resource_type === 2">
          <el-form-item label="专家领域">
            <el-input v-model="formData.expert_field" placeholder="请输入专家领域" />
          </el-form-item>
          <el-form-item label="专家级别">
            <el-input v-model="formData.expert_level" placeholder="请输入专家级别" />
          </el-form-item>
        </template>

        <!-- 物资装备特有字段 -->
        <template v-if="formData.resource_type === 3">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="数量">
                <el-input-number
                  v-model="formData.quantity"
                  :min="0"
                  placeholder="请输入数量"
                  style="width: 100%"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="单位">
                <el-input v-model="formData.unit" placeholder="请输入单位" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="装备信息">
            <el-input
              v-model="formData.equipment_info"
              type="textarea"
              :rows="4"
              placeholder="请输入装备信息（JSON格式）"
            />
          </el-form-item>
        </template>

        <el-form-item label="资源描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入资源描述"
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
    <el-dialog v-model="detailVisible" title="资源详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="资源编码">{{ currentRow?.resource_code }}</el-descriptions-item>
        <el-descriptions-item label="资源名称">{{ currentRow?.resource_name }}</el-descriptions-item>
        <el-descriptions-item label="资源类型">{{ currentRow?.resource_type_display }}</el-descriptions-item>
        <el-descriptions-item label="子类型">{{ currentRow?.sub_type_display || '-' }}</el-descriptions-item>
        <el-descriptions-item label="所属街道">{{ currentRow?.street || '-' }}</el-descriptions-item>
        <el-descriptions-item label="详细地址">{{ currentRow?.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="经度">{{ currentRow?.longitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="纬度">{{ currentRow?.latitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="所属组织">{{ currentRow?.organization_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系人">{{ currentRow?.contact_person || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentRow?.contact_phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'info'">
            {{ currentRow?.status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.resource_type === 1" label="人数">
          {{ currentRow?.capacity || '-' }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.resource_type === 2" label="专家领域">
          {{ currentRow?.expert_field || '-' }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.resource_type === 2" label="专家级别">
          {{ currentRow?.expert_level || '-' }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.resource_type === 3" label="数量">
          {{ currentRow?.quantity || '-' }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.resource_type === 3" label="单位">
          {{ currentRow?.unit || '-' }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.equipment_info" label="装备信息" :span="2">
          {{ currentRow?.equipment_info }}
        </el-descriptions-item>
        <el-descriptions-item label="资源描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { safetyResourceApi } from '@/api/modules/safety'
import type { SafetyResource, SafetyResourceFormData } from '@/types/modules/safety'
import type { PaginatedResponse } from '@/api/types'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<SafetyResource[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive({
  resource_type: undefined as number | undefined,
  street: undefined as string | undefined,
  status: undefined as number | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增资源')
const currentRow = ref<SafetyResource | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<SafetyResourceFormData>({
  resource_code: '',
  resource_name: '',
  resource_type: 1,
  sub_type: null,
  longitude: null,
  latitude: null,
  street: null,
  address: null,
  organization_id: null,
  contact_person: null,
  contact_phone: null,
  capacity: null,
  equipment_info: null,
  expert_field: null,
  expert_level: null,
  quantity: null,
  unit: null,
  status: 1,
  description: null,
  remark: null,
})

// 子类型选项
const subTypeOptions = computed(() => {
  if (formData.resource_type === 1) {
    // 救援队伍
    return [
      { label: '危化品', value: '危化品' },
      { label: '消防', value: '消防' },
      { label: '应急抢险', value: '应急抢险' },
      { label: '医疗', value: '医疗' },
      { label: '社会救援', value: '社会救援' },
    ]
  } else if (formData.resource_type === 2) {
    // 应急专家
    return [
      { label: '行业专家', value: '行业专家' },
      { label: '救援专家', value: '救援专家' },
      { label: '技术专家', value: '技术专家' },
    ]
  } else if (formData.resource_type === 3) {
    // 物资装备
    return [
      { label: '个人防护', value: '个人防护' },
      { label: '抢险救援', value: '抢险救援' },
      { label: '食品', value: '食品' },
      { label: '药品', value: '药品' },
      { label: '饮用水', value: '饮用水' },
      { label: '人员庇护', value: '人员庇护' },
    ]
  }
  return []
})

// 表单验证规则
const formRules: FormRules = {
  resource_code: [
    { required: true, message: '请输入资源编码', trigger: 'blur' },
  ],
  resource_name: [
    { required: true, message: '请输入资源名称', trigger: 'blur' },
  ],
  resource_type: [
    { required: true, message: '请选择资源类型', trigger: 'change' },
  ],
}

// 资源类型变化
const handleResourceTypeChange = () => {
  formData.sub_type = null
  formData.capacity = null
  formData.equipment_info = null
  formData.expert_field = null
  formData.expert_level = null
  formData.quantity = null
  formData.unit = null
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
    const response = await safetyResourceApi.getList(params)
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
    resource_type: undefined,
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
  dialogTitle.value = '新增资源'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: SafetyResource) => {
  isEdit.value = true
  dialogTitle.value = '编辑资源'
  currentRow.value = row
  Object.assign(formData, {
    resource_code: row.resource_code,
    resource_name: row.resource_name,
    resource_type: row.resource_type,
    sub_type: row.sub_type,
    longitude: row.longitude,
    latitude: row.latitude,
    street: row.street,
    address: row.address,
    organization_id: row.organization_id,
    contact_person: row.contact_person,
    contact_phone: row.contact_phone,
    capacity: row.capacity,
    equipment_info: row.equipment_info,
    expert_field: row.expert_field,
    expert_level: row.expert_level,
    quantity: row.quantity,
    unit: row.unit,
    status: row.status,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: SafetyResource) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: SafetyResource) => {
  try {
    await ElMessageBox.confirm('确定要删除该资源吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await safetyResourceApi.delete(row.id)
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
      const data: SafetyResourceFormData = {
        resource_name: formData.resource_name,
        resource_type: formData.resource_type,
        sub_type: formData.sub_type,
        longitude: formData.longitude,
        latitude: formData.latitude,
        street: formData.street,
        address: formData.address,
        organization_id: formData.organization_id,
        contact_person: formData.contact_person,
        contact_phone: formData.contact_phone,
        status: formData.status,
        description: formData.description,
        remark: formData.remark,
      }
      
      // 根据资源类型添加特有字段
      if (formData.resource_type === 1) {
        data.capacity = formData.capacity
        data.equipment_info = formData.equipment_info
      } else if (formData.resource_type === 2) {
        data.expert_field = formData.expert_field
        data.expert_level = formData.expert_level
      } else if (formData.resource_type === 3) {
        data.quantity = formData.quantity
        data.unit = formData.unit
        data.equipment_info = formData.equipment_info
      }

      if (isEdit.value && currentRow.value) {
        data.resource_code = formData.resource_code
        await safetyResourceApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        data.resource_code = formData.resource_code
        await safetyResourceApi.create(data)
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
    resource_code: '',
    resource_name: '',
    resource_type: 1,
    sub_type: null,
    longitude: null,
    latitude: null,
    street: null,
    address: null,
    organization_id: null,
    contact_person: null,
    contact_phone: null,
    capacity: null,
    equipment_info: null,
    expert_field: null,
    expert_level: null,
    quantity: null,
    unit: null,
    status: 1,
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

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.resource-list {
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
