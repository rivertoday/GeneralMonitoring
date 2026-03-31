<template>
  <div class="monitor-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>风险监测</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增监测点
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="监测类型">
          <el-select v-model="searchForm.monitor_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="实时监测" :value="1" />
            <el-option label="全域监测" :value="2" />
            <el-option label="重点监测" :value="3" />
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
        <el-form-item label="在线状态">
          <el-select v-model="searchForm.online_status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="在线" :value="1" />
            <el-option label="离线" :value="0" />
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
            placeholder="请输入监测点编码/名称/地址"
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
        <el-table-column prop="monitor_code" label="监测点编码" width="150" />
        <el-table-column prop="monitor_name" label="监测点名称" width="150" />
        <el-table-column prop="monitor_type_display" label="监测类型" width="100" />
        <el-table-column prop="industry_type_display" label="行业类型" width="100" />
        <el-table-column prop="street" label="所属街道" width="120" />
        <el-table-column prop="address" label="详细地址" min-width="150" show-overflow-tooltip />
        <el-table-column label="监测数值" width="120">
          <template #default="{ row }">
            <span v-if="row.monitor_value !== null">
              {{ row.monitor_value }} {{ row.monitor_unit || '' }}
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="阈值范围" width="150">
          <template #default="{ row }">
            <span v-if="row.threshold_min !== null || row.threshold_max !== null">
              {{ row.threshold_min ?? '-' }} ~ {{ row.threshold_max ?? '-' }}
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="在线状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.online_status === 1 ? 'success' : 'danger'">
              {{ row.online_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_data_time" label="最后数据时间" width="160" />
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
              {{ row.online_status === 1 ? '设为离线' : '设为在线' }}
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
            <el-form-item label="监测点编码" prop="monitor_code">
              <el-input v-model="formData.monitor_code" placeholder="请输入监测点编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="监测点名称" prop="monitor_name">
              <el-input v-model="formData.monitor_name" placeholder="请输入监测点名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="监测类型" prop="monitor_type">
              <el-select v-model="formData.monitor_type" placeholder="请选择" style="width: 100%">
                <el-option label="实时监测" :value="1" />
                <el-option label="全域监测" :value="2" />
                <el-option label="重点监测" :value="3" />
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
            <el-form-item label="经度" prop="longitude">
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
            <el-form-item label="纬度" prop="latitude">
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
            <el-form-item label="监测单位">
              <el-input v-model="formData.monitor_unit" placeholder="请输入监测单位" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="监测数值">
              <el-input-number
                v-model="formData.monitor_value"
                :precision="2"
                placeholder="请输入监测数值"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="阈值下限">
              <el-input-number
                v-model="formData.threshold_min"
                :precision="2"
                placeholder="请输入阈值下限"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="阈值上限">
              <el-input-number
                v-model="formData.threshold_max"
                :precision="2"
                placeholder="请输入阈值上限"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="在线状态">
              <el-radio-group v-model="formData.online_status">
                <el-radio :label="1">在线</el-radio>
                <el-radio :label="0">离线</el-radio>
              </el-radio-group>
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
    <el-dialog v-model="detailVisible" title="监测点详情" width="800px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="监测点编码">{{ currentRow?.monitor_code }}</el-descriptions-item>
        <el-descriptions-item label="监测点名称">{{ currentRow?.monitor_name }}</el-descriptions-item>
        <el-descriptions-item label="监测类型">{{ currentRow?.monitor_type_display }}</el-descriptions-item>
        <el-descriptions-item label="行业类型">{{ currentRow?.industry_type_display }}</el-descriptions-item>
        <el-descriptions-item label="所属街道">{{ currentRow?.street || '-' }}</el-descriptions-item>
        <el-descriptions-item label="详细地址">{{ currentRow?.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="经度">{{ currentRow?.longitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="纬度">{{ currentRow?.latitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="监测数值">
          {{ currentRow && currentRow.monitor_value !== null ? `${currentRow.monitor_value} ${currentRow.monitor_unit || ''}` : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="阈值范围">
          {{ currentRow && (currentRow.threshold_min !== null || currentRow.threshold_max !== null)
            ? `${currentRow.threshold_min ?? '-'} ~ ${currentRow.threshold_max ?? '-'}`
            : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="在线状态">
          <el-tag :type="currentRow?.online_status === 1 ? 'success' : 'danger'">
            {{ currentRow?.online_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="最后数据时间">{{ currentRow?.last_data_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'info'">
            {{ currentRow?.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
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
import { riskMonitorApi } from '@/api/modules/risk'
import type { RiskMonitor, RiskMonitorListParams, RiskMonitorFormData } from '@/types/modules/risk'
import type { PaginatedResponse } from '@/api/types'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<RiskMonitor[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive<RiskMonitorListParams>({
  monitor_type: undefined,
  industry_type: undefined,
  online_status: undefined,
  status: undefined,
  search: undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增监测点')
const currentRow = ref<RiskMonitor | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<RiskMonitorFormData>({
  monitor_code: '',
  monitor_name: '',
  monitor_type: 1,
  industry_type: 1,
  data_source_id: null,
  longitude: null,
  latitude: null,
  street: null,
  address: null,
  monitor_value: null,
  monitor_unit: null,
  threshold_min: null,
  threshold_max: null,
  online_status: 1,
  status: 1,
  description: null,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  monitor_code: [
    { required: true, message: '请输入监测点编码', trigger: 'blur' },
  ],
  monitor_name: [
    { required: true, message: '请输入监测点名称', trigger: 'blur' },
  ],
  monitor_type: [
    { required: true, message: '请选择监测类型', trigger: 'change' },
  ],
  industry_type: [
    { required: true, message: '请选择行业类型', trigger: 'change' },
  ],
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params: RiskMonitorListParams = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm,
    }
    const response = await riskMonitorApi.getList(params)
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
    monitor_type: undefined,
    industry_type: undefined,
    online_status: undefined,
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
  dialogTitle.value = '新增监测点'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: RiskMonitor) => {
  isEdit.value = true
  dialogTitle.value = '编辑监测点'
  currentRow.value = row
  Object.assign(formData, {
    monitor_code: row.monitor_code,
    monitor_name: row.monitor_name,
    monitor_type: row.monitor_type,
    industry_type: row.industry_type,
    data_source_id: row.data_source_id,
    longitude: row.longitude,
    latitude: row.latitude,
    street: row.street,
    address: row.address,
    monitor_value: row.monitor_value,
    monitor_unit: row.monitor_unit,
    threshold_min: row.threshold_min,
    threshold_max: row.threshold_max,
    online_status: row.online_status,
    status: row.status,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: RiskMonitor) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: RiskMonitor) => {
  try {
    await ElMessageBox.confirm('确定要删除该监测点吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await riskMonitorApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 更新状态
const handleUpdateStatus = async (row: RiskMonitor) => {
  try {
    const newStatus: 0 | 1 = row.online_status === 1 ? 0 : 1
    await riskMonitorApi.updateStatus(row.id, newStatus)
    ElMessage.success('更新状态成功')
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '更新状态失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      if (isEdit.value && currentRow.value) {
        await riskMonitorApi.update(currentRow.value.id, formData)
        ElMessage.success('更新成功')
      } else {
        await riskMonitorApi.create(formData)
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
    monitor_code: '',
    monitor_name: '',
    monitor_type: 1,
    industry_type: 1,
    data_source_id: null,
    longitude: null,
    latitude: null,
    street: null,
    address: null,
    monitor_value: null,
    monitor_unit: null,
    threshold_min: null,
    threshold_max: null,
    online_status: 1,
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
.monitor-list {
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
