<template>
  <div class="shelter-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>避难场所</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增场所
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="场所类型">
          <el-select v-model="searchForm.shelter_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="公园" :value="1" />
            <el-option label="广场" :value="2" />
            <el-option label="体育场" :value="3" />
            <el-option label="学校" :value="4" />
            <el-option label="其他" :value="5" />
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
            placeholder="请输入场所编码/名称"
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
        <el-table-column prop="shelter_code" label="场所编码" width="150" />
        <el-table-column prop="shelter_name" label="场所名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="shelter_type_display" label="场所类型" width="120" />
        <el-table-column prop="street" label="所属街道" width="120" />
        <el-table-column prop="address" label="详细地址" min-width="150" show-overflow-tooltip />
        <el-table-column prop="capacity" label="容纳能力(人)" width="120" />
        <el-table-column prop="area" label="占地面积(㎡)" width="120" />
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
            <el-form-item label="场所编码" prop="shelter_code">
              <el-input v-model="formData.shelter_code" placeholder="请输入场所编码" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="场所名称" prop="shelter_name">
              <el-input v-model="formData.shelter_name" placeholder="请输入场所名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="场所类型" prop="shelter_type">
              <el-select v-model="formData.shelter_type" placeholder="请选择" style="width: 100%">
                <el-option label="公园" :value="1" />
                <el-option label="广场" :value="2" />
                <el-option label="体育场" :value="3" />
                <el-option label="学校" :value="4" />
                <el-option label="其他" :value="5" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="容纳能力(人)" prop="capacity">
              <el-input-number
                v-model="formData.capacity"
                :min="0"
                placeholder="请输入容纳能力"
                style="width: 100%"
              />
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
            <el-form-item label="占地面积(㎡)">
              <el-input-number
                v-model="formData.area"
                :precision="2"
                :min="0"
                placeholder="请输入占地面积"
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
        <el-form-item label="设施信息">
          <el-input
            v-model="formData.facilities"
            type="textarea"
            :rows="4"
            placeholder="请输入设施信息（JSON格式）"
          />
        </el-form-item>
        <el-form-item label="场所描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入场所描述"
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
    <el-dialog v-model="detailVisible" title="场所详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="场所编码">{{ currentRow?.shelter_code }}</el-descriptions-item>
        <el-descriptions-item label="场所名称">{{ currentRow?.shelter_name }}</el-descriptions-item>
        <el-descriptions-item label="场所类型">{{ currentRow?.shelter_type_display }}</el-descriptions-item>
        <el-descriptions-item label="容纳能力(人)">{{ currentRow?.capacity }}</el-descriptions-item>
        <el-descriptions-item label="所属街道">{{ currentRow?.street || '-' }}</el-descriptions-item>
        <el-descriptions-item label="详细地址">{{ currentRow?.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="经度">{{ currentRow?.longitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="纬度">{{ currentRow?.latitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="占地面积(㎡)">{{ currentRow?.area || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系人">{{ currentRow?.contact_person || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentRow?.contact_phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'info'">
            {{ currentRow?.status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.facilities" label="设施信息" :span="2">
          {{ currentRow.facilities }}
        </el-descriptions-item>
        <el-descriptions-item label="场所描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
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
import { shelterApi } from '@/api/modules/safety'
import type { Shelter, ShelterFormData } from '@/types/modules/safety'
import type { PaginatedResponse } from '@/api/types'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<Shelter[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive({
  shelter_type: undefined as number | undefined,
  street: undefined as string | undefined,
  status: undefined as number | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增场所')
const currentRow = ref<Shelter | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<ShelterFormData>({
  shelter_code: '',
  shelter_name: '',
  shelter_type: 1,
  longitude: null,
  latitude: null,
  street: null,
  address: null,
  capacity: 0,
  area: null,
  facilities: null,
  contact_person: null,
  contact_phone: null,
  description: null,
  status: 1,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  shelter_code: [
    { required: true, message: '请输入场所编码', trigger: 'blur' },
  ],
  shelter_name: [
    { required: true, message: '请输入场所名称', trigger: 'blur' },
  ],
  shelter_type: [
    { required: true, message: '请选择场所类型', trigger: 'change' },
  ],
  capacity: [
    { required: true, message: '请输入容纳能力', trigger: 'blur' },
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
    const response = await shelterApi.getList(params)
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
    shelter_type: undefined,
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
  dialogTitle.value = '新增场所'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: Shelter) => {
  isEdit.value = true
  dialogTitle.value = '编辑场所'
  currentRow.value = row
  Object.assign(formData, {
    shelter_code: row.shelter_code,
    shelter_name: row.shelter_name,
    shelter_type: row.shelter_type,
    longitude: row.longitude,
    latitude: row.latitude,
    street: row.street,
    address: row.address,
    capacity: row.capacity,
    area: row.area,
    facilities: row.facilities,
    contact_person: row.contact_person,
    contact_phone: row.contact_phone,
    description: row.description,
    status: row.status,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: Shelter) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: Shelter) => {
  try {
    await ElMessageBox.confirm('确定要删除该场所吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await shelterApi.delete(row.id)
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
      const data: ShelterFormData = {
        shelter_name: formData.shelter_name,
        shelter_type: formData.shelter_type,
        longitude: formData.longitude,
        latitude: formData.latitude,
        street: formData.street,
        address: formData.address,
        capacity: formData.capacity,
        area: formData.area,
        facilities: formData.facilities,
        contact_person: formData.contact_person,
        contact_phone: formData.contact_phone,
        description: formData.description,
        status: formData.status,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        data.shelter_code = formData.shelter_code
        await shelterApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        data.shelter_code = formData.shelter_code
        await shelterApi.create(data)
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
    shelter_code: '',
    shelter_name: '',
    shelter_type: 1,
    longitude: null,
    latitude: null,
    street: null,
    address: null,
    capacity: 0,
    area: null,
    facilities: null,
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

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.shelter-list {
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
