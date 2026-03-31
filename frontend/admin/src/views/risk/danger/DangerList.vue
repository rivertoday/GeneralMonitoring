<template>
  <div class="danger-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>隐患排查</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增隐患
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="监测点">
          <el-select
            v-model="searchForm.monitor_id"
            placeholder="请选择监测点"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="monitor in monitors"
              :key="monitor.id"
              :label="monitor.monitor_name"
              :value="monitor.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="隐患等级">
          <el-select v-model="searchForm.danger_level" placeholder="请选择" clearable style="width: 120px">
            <el-option label="重大" :value="1" />
            <el-option label="较大" :value="2" />
            <el-option label="一般" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="隐患类别">
          <el-input
            v-model="searchForm.danger_category"
            placeholder="请输入隐患类别"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="隐患状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="待整改" :value="0" />
            <el-option label="整改中" :value="1" />
            <el-option label="已完成" :value="2" />
            <el-option label="已关闭" :value="3" />
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
        <el-form-item label="发现时间">
          <el-date-picker
            v-model="timeRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 350px"
          />
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入隐患编码/名称/描述"
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
        <el-table-column prop="danger_code" label="隐患编码" width="150" />
        <el-table-column prop="danger_name" label="隐患名称" min-width="200" show-overflow-tooltip />
        <el-table-column label="监测点" width="150">
          <template #default="{ row }">
            <span v-if="row.monitor_detail">{{ row.monitor_detail.monitor_name }}</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="企业" width="150">
          <template #default="{ row }">
            <span v-if="row.organization_name">{{ row.organization_name }}</span>
            <span v-else>企业ID: {{ row.organization_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="隐患等级" width="100">
          <template #default="{ row }">
            <el-tag :type="getDangerLevelTagType(row.danger_level)">
              {{ row.danger_level_display || getDangerLevelDisplay(row.danger_level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="danger_category" label="隐患类别" width="120" />
        <el-table-column prop="street" label="所属街道" width="120" />
        <el-table-column prop="address" label="详细地址" min-width="150" show-overflow-tooltip />
        <el-table-column prop="discover_time" label="发现时间" width="160" />
        <el-table-column label="发现人" width="100">
          <template #default="{ row }">
            <span v-if="row.discover_user_name">{{ row.discover_user_name }}</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="隐患状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.status)">
              {{ row.status_display || getStatusDisplay(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button
              v-if="row.status === 0 || row.status === 1"
              type="warning"
              link
              size="small"
              @click="handleUpdateStatus(row, 2)"
            >
              标记完成
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
            <el-form-item label="隐患编码" prop="danger_code">
              <el-input v-model="formData.danger_code" placeholder="请输入隐患编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="隐患名称" prop="danger_name">
              <el-input v-model="formData.danger_name" placeholder="请输入隐患名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="监测点" prop="monitor_id">
              <el-select
                v-model="formData.monitor_id"
                placeholder="请选择监测点（重点监测类型）"
                filterable
                style="width: 100%"
              >
                <el-option
                  v-for="monitor in monitors"
                  :key="monitor.id"
                  :label="monitor.monitor_name"
                  :value="monitor.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="企业ID" prop="organization_id">
              <el-input-number
                v-model="formData.organization_id"
                :min="1"
                placeholder="请输入企业ID"
                style="width: 100%"
              />
              <div class="form-tip">注意：需要先选择对应的企业组织</div>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="隐患等级" prop="danger_level">
              <el-select v-model="formData.danger_level" placeholder="请选择" style="width: 100%">
                <el-option label="重大" :value="1" />
                <el-option label="较大" :value="2" />
                <el-option label="一般" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="隐患类别">
              <el-input v-model="formData.danger_category" placeholder="请输入隐患类别" />
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
        <el-form-item label="发现时间" prop="discover_time">
          <el-date-picker
            v-model="formData.discover_time"
            type="datetime"
            placeholder="请选择发现时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="隐患描述" prop="danger_description">
          <el-input
            v-model="formData.danger_description"
            type="textarea"
            :rows="4"
            placeholder="请输入隐患描述"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="formData.status" placeholder="请选择" style="width: 100%">
            <el-option label="待整改" :value="0" />
            <el-option label="整改中" :value="1" />
            <el-option label="已完成" :value="2" />
            <el-option label="已关闭" :value="3" />
          </el-select>
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
    <el-dialog v-model="detailVisible" title="隐患详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="隐患编码">{{ currentRow?.danger_code }}</el-descriptions-item>
        <el-descriptions-item label="隐患名称">{{ currentRow?.danger_name }}</el-descriptions-item>
        <el-descriptions-item label="监测点">
          {{ currentRow?.monitor_detail?.monitor_name || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="企业">
          {{ currentRow?.organization_name || `企业ID: ${currentRow?.organization_id}` }}
        </el-descriptions-item>
        <el-descriptions-item label="隐患等级">
          <el-tag :type="getDangerLevelTagType(currentRow?.danger_level || 1)">
            {{ currentRow?.danger_level_display || getDangerLevelDisplay(currentRow?.danger_level) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="隐患类别">
          {{ currentRow?.danger_category || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="行业类型">
          {{ currentRow?.industry_type_display || '危险化学品' }}
        </el-descriptions-item>
        <el-descriptions-item label="所属街道">
          {{ currentRow?.street || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="详细地址">
          {{ currentRow?.address || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="经度">{{ currentRow?.longitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="纬度">{{ currentRow?.latitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="发现时间">{{ currentRow?.discover_time }}</el-descriptions-item>
        <el-descriptions-item label="发现人">
          {{ currentRow?.discover_user_name || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="隐患状态">
          <el-tag :type="getStatusTagType(currentRow?.status)">
            {{ currentRow?.status_display || getStatusDisplay(currentRow?.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="隐患描述" :span="2">
          {{ currentRow?.danger_description }}
        </el-descriptions-item>
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
import { riskHiddenDangerApi, riskMonitorApi } from '@/api/modules/risk'
import type { RiskHiddenDanger, RiskHiddenDangerFormData, RiskMonitor } from '@/types/modules/risk'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<RiskHiddenDanger[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 监测点列表（重点监测类型）
const monitors = ref<RiskMonitor[]>([])

// 搜索表单
const searchForm = reactive({
  monitor_id: undefined as number | undefined,
  danger_level: undefined as 1 | 2 | 3 | undefined,
  danger_category: undefined as string | undefined,
  status: undefined as 0 | 1 | 2 | 3 | undefined,
  street: undefined as string | undefined,
  search: undefined as string | undefined,
})

// 时间范围
const timeRange = ref<[string, string] | null>(null)

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增隐患')
const currentRow = ref<RiskHiddenDanger | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<RiskHiddenDangerFormData>({
  danger_code: '',
  danger_name: '',
  monitor_id: 0,
  organization_id: 0,
  longitude: null,
  latitude: null,
  street: null,
  address: null,
  danger_level: 1,
  danger_category: null,
  danger_description: '',
  discover_time: '',
  discover_user_id: null,
  status: 0,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  danger_code: [
    { required: true, message: '请输入隐患编码', trigger: 'blur' },
  ],
  danger_name: [
    { required: true, message: '请输入隐患名称', trigger: 'blur' },
  ],
  monitor_id: [
    { required: true, message: '请选择监测点', trigger: 'change' },
  ],
  organization_id: [
    { required: true, message: '请输入企业ID', trigger: 'blur' },
    { type: 'number', min: 1, message: '企业ID必须大于0', trigger: 'blur' },
  ],
  danger_level: [
    { required: true, message: '请选择隐患等级', trigger: 'change' },
  ],
  danger_description: [
    { required: true, message: '请输入隐患描述', trigger: 'blur' },
  ],
  discover_time: [
    { required: true, message: '请选择发现时间', trigger: 'change' },
  ],
}

// 获取监测点列表（重点监测类型）
const fetchMonitors = async () => {
  try {
    const response = await riskMonitorApi.getList({
      monitor_type: 3, // 重点监测
      industry_type: 4, // 危险化学品
      page_size: 100,
      status: 1,
    })
    monitors.value = response.results
  } catch (error: any) {
    console.error('获取监测点列表失败:', error)
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
    if (timeRange.value) {
      params.start_time = timeRange.value[0]
      params.end_time = timeRange.value[1]
    }
    const response = await riskHiddenDangerApi.getList(params)
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
    monitor_id: undefined,
    danger_level: undefined,
    danger_category: undefined,
    status: undefined,
    street: undefined,
    search: undefined,
  })
  timeRange.value = null
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
  dialogTitle.value = '新增隐患'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: RiskHiddenDanger) => {
  isEdit.value = true
  dialogTitle.value = '编辑隐患'
  currentRow.value = row
  Object.assign(formData, {
    danger_code: row.danger_code,
    danger_name: row.danger_name,
    monitor_id: row.monitor_id,
    organization_id: row.organization_id,
    longitude: row.longitude,
    latitude: row.latitude,
    street: row.street,
    address: row.address,
    danger_level: row.danger_level,
    danger_category: row.danger_category,
    danger_description: row.danger_description,
    discover_time: row.discover_time,
    discover_user_id: row.discover_user_id,
    status: row.status,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: RiskHiddenDanger) => {
  currentRow.value = row
  detailVisible.value = true
}

// 更新状态
const handleUpdateStatus = async (row: RiskHiddenDanger, newStatus: 0 | 1 | 2 | 3) => {
  try {
    await riskHiddenDangerApi.update(row.id, { status: newStatus })
    ElMessage.success('状态更新成功')
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

// 删除
const handleDelete = async (row: RiskHiddenDanger) => {
  try {
    await ElMessageBox.confirm('确定要删除该隐患吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await riskHiddenDangerApi.delete(row.id)
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
      const data: RiskHiddenDangerFormData = {
        danger_code: formData.danger_code,
        danger_name: formData.danger_name,
        monitor_id: formData.monitor_id,
        organization_id: formData.organization_id,
        longitude: formData.longitude,
        latitude: formData.latitude,
        street: formData.street,
        address: formData.address,
        danger_level: formData.danger_level,
        danger_category: formData.danger_category,
        danger_description: formData.danger_description,
        discover_time: formData.discover_time,
        discover_user_id: formData.discover_user_id,
        status: formData.status,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        await riskHiddenDangerApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await riskHiddenDangerApi.create(data)
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
    danger_code: '',
    danger_name: '',
    monitor_id: 0,
    organization_id: 0,
    longitude: null,
    latitude: null,
    street: null,
    address: null,
    danger_level: 1,
    danger_category: null,
    danger_description: '',
    discover_time: '',
    discover_user_id: null,
    status: 0,
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

// 获取隐患等级标签类型
const getDangerLevelTagType = (level?: number) => {
  const levelMap: Record<number, string> = {
    1: 'danger', // 重大
    2: 'warning', // 较大
    3: 'info', // 一般
  }
  return levelMap[level || 0] || 'info'
}

// 获取隐患等级显示
const getDangerLevelDisplay = (level?: number) => {
  const levelMap: Record<number, string> = {
    1: '重大',
    2: '较大',
    3: '一般',
  }
  return levelMap[level || 0] || '-'
}

// 获取状态标签类型
const getStatusTagType = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: 'info', // 待整改
    1: 'warning', // 整改中
    2: 'success', // 已完成
    3: 'info', // 已关闭
  }
  return statusMap[status ?? 0] || 'info'
}

// 获取状态显示
const getStatusDisplay = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: '待整改',
    1: '整改中',
    2: '已完成',
    3: '已关闭',
  }
  return statusMap[status ?? 0] || '-'
}

// 初始化
onMounted(() => {
  fetchMonitors()
  fetchData()
})
</script>

<style scoped lang="scss">
.danger-list {
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

  .form-tip {
    font-size: 12px;
    color: #909399;
    margin-top: 5px;
  }
}
</style>
