<template>
  <div class="alarm-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>报警管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增报警
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="监测点">
          <el-select
            v-model="searchForm.monitor"
            placeholder="请选择"
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
        <el-form-item label="行业类型">
          <el-select v-model="searchForm.industry_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="森林火灾" :value="1" />
            <el-option label="防汛" :value="2" />
            <el-option label="交通运输" :value="3" />
            <el-option label="危险化学品" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="报警类型">
          <el-input
            v-model="searchForm.alarm_type"
            placeholder="请输入报警类型"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="报警状态">
          <el-select v-model="searchForm.alarm_status" placeholder="请选择" clearable style="width: 150px">
            <el-option label="未处理" :value="0" />
            <el-option label="处理中" :value="1" />
            <el-option label="已处理" :value="2" />
            <el-option label="已忽略" :value="3" />
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
        <el-form-item label="报警时间">
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
            placeholder="请输入报警编码/描述/地址"
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
        <el-table-column prop="alarm_code" label="报警编码" width="150" />
        <el-table-column label="监测点" width="150">
          <template #default="{ row }">
            {{ row.monitor_detail?.monitor_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="industry_type_display" label="行业类型" width="100" />
        <el-table-column prop="alarm_type" label="报警类型" width="120" />
        <el-table-column label="报警数值" width="120">
          <template #default="{ row }">
            <span v-if="row.alarm_value !== null">
              {{ row.alarm_value }}
              <span v-if="row.monitor_detail?.monitor_unit">{{ row.monitor_detail.monitor_unit }}</span>
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="阈值" width="120">
          <template #default="{ row }">
            <span v-if="row.threshold_value !== null">
              {{ row.threshold_value }}
              <span v-if="row.monitor_detail?.monitor_unit">{{ row.monitor_detail.monitor_unit }}</span>
            </span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="street" label="所属街道" width="120" />
        <el-table-column prop="address" label="详细地址" min-width="150" show-overflow-tooltip />
        <el-table-column prop="alarm_time" label="报警时间" width="160" />
        <el-table-column label="持续时间" width="100">
          <template #default="{ row }">
            <span v-if="row.alarm_duration !== null">{{ row.alarm_duration }}分钟</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="报警状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.alarm_status)">
              {{ row.alarm_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="handle_time" label="处理时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button
              v-if="row.alarm_status === 0 || row.alarm_status === 1"
              type="warning"
              link
              size="small"
              @click="handleHandle(row)"
            >
              处理
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
            <el-form-item label="报警编码" prop="alarm_code">
              <el-input v-model="formData.alarm_code" placeholder="请输入报警编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="监测点" prop="monitor_id">
              <el-select
                v-model="formData.monitor_id"
                placeholder="请选择"
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
        </el-row>
        <el-row :gutter="20">
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
          <el-col :span="12">
            <el-form-item label="报警类型" prop="alarm_type">
              <el-input v-model="formData.alarm_type" placeholder="请输入报警类型" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="报警数值">
              <el-input-number
                v-model="formData.alarm_value"
                :precision="2"
                :step="0.01"
                placeholder="请输入报警数值"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="阈值数值">
              <el-input-number
                v-model="formData.threshold_value"
                :precision="2"
                :step="0.01"
                placeholder="请输入阈值数值"
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
            <el-form-item label="报警时间" prop="alarm_time">
              <el-date-picker
                v-model="formData.alarm_time"
                type="datetime"
                placeholder="请选择报警时间"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="持续时间(分钟)">
              <el-input-number
                v-model="formData.alarm_duration"
                :min="0"
                placeholder="请输入持续时间"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="报警描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入报警描述"
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
    <el-dialog v-model="detailVisible" title="报警详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="报警编码">{{ currentRow?.alarm_code }}</el-descriptions-item>
        <el-descriptions-item label="监测点">
          {{ currentRow?.monitor_detail?.monitor_name || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="行业类型">{{ currentRow?.industry_type_display }}</el-descriptions-item>
        <el-descriptions-item label="报警类型">{{ currentRow?.alarm_type }}</el-descriptions-item>
        <el-descriptions-item label="报警数值">
          <span v-if="currentRow && currentRow.alarm_value !== null">
            {{ currentRow.alarm_value }}
            <span v-if="currentRow.monitor_detail?.monitor_unit">{{ currentRow.monitor_detail.monitor_unit }}</span>
          </span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="阈值数值">
          <span v-if="currentRow && currentRow.threshold_value !== null">
            {{ currentRow.threshold_value }}
            <span v-if="currentRow.monitor_detail?.monitor_unit">{{ currentRow.monitor_detail.monitor_unit }}</span>
          </span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="所属街道">{{ currentRow?.street || '-' }}</el-descriptions-item>
        <el-descriptions-item label="详细地址">{{ currentRow?.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="经度">{{ currentRow?.longitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="纬度">{{ currentRow?.latitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="报警时间">{{ currentRow?.alarm_time }}</el-descriptions-item>
        <el-descriptions-item label="持续时间">
          <span v-if="currentRow && currentRow.alarm_duration !== null">{{ currentRow.alarm_duration }}分钟</span>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="报警状态">
          <el-tag :type="getStatusTagType(currentRow?.alarm_status)">
            {{ currentRow?.alarm_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="处理时间">{{ currentRow?.handle_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="反馈时间">{{ currentRow?.feedback_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="报警描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="处理结果" :span="2">{{ currentRow?.handle_result || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 处理对话框 -->
    <el-dialog v-model="handleVisible" title="处理报警" width="600px">
      <el-form ref="handleFormRef" :model="handleForm" :rules="handleFormRules" label-width="100px">
        <el-form-item label="处理状态" prop="alarm_status">
          <el-select v-model="handleForm.alarm_status" placeholder="请选择" style="width: 100%">
            <el-option label="处理中" :value="1" />
            <el-option label="已处理" :value="2" />
            <el-option label="已忽略" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="处理结果" prop="handle_result">
          <el-input
            v-model="handleForm.handle_result"
            type="textarea"
            :rows="5"
            placeholder="请输入处理结果"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="handleVisible = false">取消</el-button>
        <el-button type="primary" :loading="handleLoading" @click="handleHandleSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { alarmRecordApi, riskMonitorApi } from '@/api/modules/risk'
import type { AlarmRecord, RiskMonitor } from '@/types/modules/risk'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)
const handleLoading = ref(false)

// 表格数据
const tableData = ref<AlarmRecord[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 监测点列表
const monitors = ref<RiskMonitor[]>([])

// 搜索表单
const searchForm = reactive({
  monitor: undefined as number | undefined,
  industry_type: undefined as number | undefined,
  alarm_type: undefined as string | undefined,
  alarm_status: undefined as number | undefined,
  street: undefined as string | undefined,
  search: undefined as string | undefined,
})

// 时间范围
const timeRange = ref<[string, string] | null>(null)

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const handleVisible = ref(false)
const dialogTitle = ref('新增报警')
const currentRow = ref<AlarmRecord | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const handleFormRef = ref<FormInstance>()
const formData = reactive({
  alarm_code: '',
  monitor_id: undefined as number | undefined,
  industry_type: 1,
  alarm_type: '',
  alarm_value: null as number | null,
  threshold_value: null as number | null,
  longitude: null as number | null,
  latitude: null as number | null,
  street: null as string | null,
  address: null as string | null,
  alarm_time: '',
  alarm_duration: null as number | null,
  description: null as string | null,
  remark: null as string | null,
})

const handleForm = reactive({
  alarm_status: 1 as 1 | 2 | 3,
  handle_result: '',
})

// 表单验证规则
const formRules: FormRules = {
  alarm_code: [
    { required: true, message: '请输入报警编码', trigger: 'blur' },
  ],
  monitor_id: [
    { required: true, message: '请选择监测点', trigger: 'change' },
  ],
  industry_type: [
    { required: true, message: '请选择行业类型', trigger: 'change' },
  ],
  alarm_type: [
    { required: true, message: '请输入报警类型', trigger: 'blur' },
  ],
  alarm_time: [
    { required: true, message: '请选择报警时间', trigger: 'change' },
  ],
}

const handleFormRules: FormRules = {
  alarm_status: [
    { required: true, message: '请选择处理状态', trigger: 'change' },
  ],
  handle_result: [
    { required: true, message: '请输入处理结果', trigger: 'blur' },
  ],
}

// 获取监测点列表
const fetchMonitors = async () => {
  try {
    const response = await riskMonitorApi.getList({ page_size: 1000, status: 1 })
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
    const response = await alarmRecordApi.getList(params)
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
    monitor: undefined,
    industry_type: undefined,
    alarm_type: undefined,
    alarm_status: undefined,
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
  dialogTitle.value = '新增报警'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: AlarmRecord) => {
  isEdit.value = true
  dialogTitle.value = '编辑报警'
  currentRow.value = row
  Object.assign(formData, {
    alarm_code: row.alarm_code,
    monitor_id: row.monitor_id,
    industry_type: row.industry_type,
    alarm_type: row.alarm_type,
    alarm_value: row.alarm_value,
    threshold_value: row.threshold_value,
    longitude: row.longitude,
    latitude: row.latitude,
    street: row.street,
    address: row.address,
    alarm_time: row.alarm_time,
    alarm_duration: row.alarm_duration,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: AlarmRecord) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: AlarmRecord) => {
  try {
    await ElMessageBox.confirm('确定要删除该报警记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await alarmRecordApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 处理
const handleHandle = (row: AlarmRecord) => {
  currentRow.value = row
  handleForm.alarm_status = row.alarm_status === 0 ? 1 : row.alarm_status
  handleForm.handle_result = ''
  handleVisible.value = true
}

// 处理提交
const handleHandleSubmit = async () => {
  if (!handleFormRef.value || !currentRow.value) return

  await handleFormRef.value.validate(async (valid) => {
    if (!valid) return

    if (!currentRow.value) {
      ElMessage.warning('请选择要处理的报警记录')
      return
    }
    
    handleLoading.value = true
    try {
      await alarmRecordApi.handle(currentRow.value.id, {
        alarm_status: handleForm.alarm_status,
        handle_result: handleForm.handle_result,
      })
      ElMessage.success('处理成功')
      handleVisible.value = false
      fetchData()
    } catch (error: any) {
      ElMessage.error(error.message || '处理失败')
    } finally {
      handleLoading.value = false
    }
  })
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const data: any = {
        alarm_code: formData.alarm_code,
        monitor_id: formData.monitor_id,
        industry_type: formData.industry_type,
        alarm_type: formData.alarm_type,
        alarm_value: formData.alarm_value,
        threshold_value: formData.threshold_value,
        longitude: formData.longitude,
        latitude: formData.latitude,
        street: formData.street,
        address: formData.address,
        alarm_time: formData.alarm_time,
        alarm_duration: formData.alarm_duration,
        description: formData.description,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        await alarmRecordApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await alarmRecordApi.create(data)
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
    alarm_code: '',
    monitor_id: undefined,
    industry_type: 1,
    alarm_type: '',
    alarm_value: null,
    threshold_value: null,
    longitude: null,
    latitude: null,
    street: null,
    address: null,
    alarm_time: '',
    alarm_duration: null,
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
    3: 'info',
  }
  return statusMap[status || 0] || 'info'
}

// 初始化
onMounted(() => {
  fetchMonitors()
  fetchData()
})
</script>

<style scoped lang="scss">
.alarm-list {
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
