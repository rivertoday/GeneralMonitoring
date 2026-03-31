<template>
  <div class="record-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>叫应记录管理</h2>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="叫应类型">
          <el-select v-model="searchForm.call_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="常态化叫应" :value="1" />
            <el-option label="非常态化叫应" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="叫应来源">
          <el-select v-model="searchForm.call_source" placeholder="请选择" clearable style="width: 150px">
            <el-option label="政策文件下发" :value="1" />
            <el-option label="一键叫应" :value="2" />
            <el-option label="预警触发" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="叫应渠道">
          <el-select v-model="searchForm.call_channel" placeholder="请选择" clearable style="width: 120px">
            <el-option label="系统消息" value="system" />
            <el-option label="短信" value="sms" />
            <el-option label="电话" value="phone" />
          </el-select>
        </el-form-item>
        <el-form-item label="叫应状态">
          <el-select v-model="searchForm.call_status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="待发送" :value="0" />
            <el-option label="发送中" :value="1" />
            <el-option label="发送成功" :value="2" />
            <el-option label="发送失败" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="接收状态">
          <el-select v-model="searchForm.receive_status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="未接收" :value="0" />
            <el-option label="已接收" :value="1" />
            <el-option label="未响应" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="响应状态">
          <el-select v-model="searchForm.response_status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="未响应" :value="0" />
            <el-option label="已响应" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="叫应时间">
          <el-date-picker
            v-model="dateRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 350px"
            @change="handleDateRangeChange"
          />
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入叫应编码/内容/描述"
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
        <el-table-column prop="call_code" label="叫应编码" width="150" />
        <el-table-column prop="call_type_display" label="叫应类型" width="120" />
        <el-table-column prop="call_source_display" label="叫应来源" width="120" />
        <el-table-column label="叫应对象/人员" width="150" show-overflow-tooltip>
          <template #default="{ row }">
            <span v-if="row.target_detail">{{ row.target_detail.target_name }}</span>
            <span v-else-if="row.person_detail">{{ row.person_detail.person_name }}</span>
            <span v-else-if="row.group_detail">{{ row.group_detail.group_name }}</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="call_channel" label="叫应渠道" width="100">
          <template #default="{ row }">
            <el-tag size="small">
              {{ getChannelDisplay(row.call_channel) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="call_content" label="叫应内容" min-width="200" show-overflow-tooltip />
        <el-table-column prop="call_time" label="叫应时间" width="160" />
        <el-table-column label="叫应状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getCallStatusTagType(row.call_status)" size="small">
              {{ row.call_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="接收状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getReceiveStatusTagType(row.receive_status)" size="small">
              {{ row.receive_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="receive_time" label="接收时间" width="160" />
        <el-table-column label="响应状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getResponseStatusTagType(row.response_status)" size="small">
              {{ row.response_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="response_time" label="响应时间" width="160" />
        <el-table-column prop="retry_count" label="重试次数" width="100" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button
              v-if="row.response_status === 0"
              type="success"
              link
              size="small"
              @click="handleResponse(row)"
            >
              响应
            </el-button>
            <el-button
              v-if="row.call_status === 3"
              type="warning"
              link
              size="small"
              @click="handleRetry(row)"
            >
              重试
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

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="叫应记录详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="叫应编码">{{ currentRow?.call_code }}</el-descriptions-item>
        <el-descriptions-item label="叫应类型">{{ currentRow?.call_type_display }}</el-descriptions-item>
        <el-descriptions-item label="叫应来源">{{ currentRow?.call_source_display }}</el-descriptions-item>
        <el-descriptions-item label="叫应渠道">
          <el-tag size="small">{{ getChannelDisplay(currentRow?.call_channel || '') }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="叫应时间">{{ currentRow?.call_time }}</el-descriptions-item>
        <el-descriptions-item label="叫应状态">
          <el-tag :type="getCallStatusTagType(currentRow?.call_status || 0)" size="small">
            {{ currentRow?.call_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="接收状态">
          <el-tag :type="getReceiveStatusTagType(currentRow?.receive_status || 0)" size="small">
            {{ currentRow?.receive_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="接收时间">{{ currentRow?.receive_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="响应状态">
          <el-tag :type="getResponseStatusTagType(currentRow?.response_status || 0)" size="small">
            {{ currentRow?.response_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="响应时间">{{ currentRow?.response_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="重试次数">{{ currentRow?.retry_count || 0 }}</el-descriptions-item>
        <el-descriptions-item label="最后重试时间">{{ currentRow?.last_retry_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="叫应对象" v-if="currentRow?.target_detail">
          {{ currentRow.target_detail.target_name }}
        </el-descriptions-item>
        <el-descriptions-item label="叫应人员" v-if="currentRow?.person_detail">
          {{ currentRow.person_detail.person_name }}
        </el-descriptions-item>
        <el-descriptions-item label="叫应分组" v-if="currentRow?.group_detail">
          {{ currentRow.group_detail.group_name }}
        </el-descriptions-item>
        <el-descriptions-item label="政策文件下发" v-if="currentRow?.policy_distribution_detail">
          {{ currentRow.policy_distribution_detail.distribution_code }}
        </el-descriptions-item>
        <el-descriptions-item label="预警ID" v-if="currentRow?.warning_id">
          {{ currentRow.warning_id }}
        </el-descriptions-item>
        <el-descriptions-item label="叫应内容" :span="2">{{ currentRow?.call_content }}</el-descriptions-item>
        <el-descriptions-item label="响应内容" :span="2">{{ currentRow?.response_content || '-' }}</el-descriptions-item>
        <el-descriptions-item label="错误信息" :span="2" v-if="currentRow?.error_message">
          <el-text type="danger">{{ currentRow.error_message }}</el-text>
        </el-descriptions-item>
        <el-descriptions-item label="外部叫应ID">{{ currentRow?.external_call_id || '-' }}</el-descriptions-item>
        <el-descriptions-item label="叫应描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 响应对话框 -->
    <el-dialog v-model="responseVisible" title="响应叫应记录" width="600px">
      <el-form ref="responseFormRef" :model="responseData" :rules="responseRules" label-width="120px">
        <el-form-item label="响应内容" prop="response_content">
          <el-input
            v-model="responseData.response_content"
            type="textarea"
            :rows="6"
            placeholder="请输入响应内容"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="responseVisible = false">取消</el-button>
        <el-button type="primary" :loading="responseLoading" @click="handleResponseConfirm">
          确定响应
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Search, Refresh } from '@element-plus/icons-vue'
import { callRecordApi } from '@/api/modules/call'
import type {
  CallRecord,
  CallRecordListParams,
  CallRecordResponseData,
  CallType,
  CallSource,
  CallStatus,
  ReceiveStatus,
  ResponseStatus,
  CallChannel,
} from '@/types/modules/call'

// 加载状态
const loading = ref(false)
const responseLoading = ref(false)

// 表格数据
const tableData = ref<CallRecord[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive<CallRecordListParams>({
  call_type: undefined,
  call_source: undefined,
  call_channel: undefined,
  call_status: undefined,
  receive_status: undefined,
  response_status: undefined,
  start_time: undefined,
  end_time: undefined,
  search: undefined,
})

// 日期范围
const dateRange = ref<[string, string] | null>(null)

// 对话框
const detailVisible = ref(false)
const responseVisible = ref(false)
const currentRow = ref<CallRecord | null>(null)
const responseRow = ref<CallRecord | null>(null)

// 响应表单
const responseFormRef = ref<FormInstance>()
const responseData = reactive<CallRecordResponseData>({
  response_content: '',
})

// 响应表单验证规则
const responseRules: FormRules = {
  response_content: [
    { required: true, message: '请输入响应内容', trigger: 'blur' },
  ],
}

// 获取渠道显示文本
const getChannelDisplay = (channel: CallChannel | string): string => {
  const channelMap: Record<string, string> = {
    system: '系统消息',
    sms: '短信',
    phone: '电话',
  }
  return channelMap[channel] || channel
}

// 获取叫应状态标签类型
const getCallStatusTagType = (status: CallStatus): string => {
  const typeMap: Record<CallStatus, string> = {
    0: 'info',    // 待发送
    1: 'warning', // 发送中
    2: 'success', // 发送成功
    3: 'danger',  // 发送失败
  }
  return typeMap[status] || 'info'
}

// 获取接收状态标签类型
const getReceiveStatusTagType = (status: ReceiveStatus): string => {
  const typeMap: Record<ReceiveStatus, string> = {
    0: 'info',    // 未接收
    1: 'success', // 已接收
    2: 'warning', // 未响应
  }
  return typeMap[status] || 'info'
}

// 获取响应状态标签类型
const getResponseStatusTagType = (status: ResponseStatus): string => {
  const typeMap: Record<ResponseStatus, string> = {
    0: 'info',    // 未响应
    1: 'success', // 已响应
  }
  return typeMap[status] || 'info'
}

// 日期范围变化
const handleDateRangeChange = (val: [string, string] | null) => {
  if (val) {
    searchForm.start_time = val[0]
    searchForm.end_time = val[1]
  } else {
    searchForm.start_time = undefined
    searchForm.end_time = undefined
  }
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params: CallRecordListParams = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm,
    }
    const response = await callRecordApi.getList(params)
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
    call_type: undefined,
    call_source: undefined,
    call_channel: undefined,
    call_status: undefined,
    receive_status: undefined,
    response_status: undefined,
    start_time: undefined,
    end_time: undefined,
    search: undefined,
  })
  dateRange.value = null
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

// 查看
const handleView = (row: CallRecord) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: CallRecord) => {
  try {
    await ElMessageBox.confirm('确定要删除该叫应记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await callRecordApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 响应
const handleResponse = (row: CallRecord) => {
  responseRow.value = row
  responseData.response_content = ''
  responseVisible.value = true
}

// 确认响应
const handleResponseConfirm = async () => {
  if (!responseFormRef.value || !responseRow.value) return
  try {
    await responseFormRef.value.validate()
    responseLoading.value = true
    await callRecordApi.response(responseRow.value.id, responseData)
    ElMessage.success('响应成功')
    responseVisible.value = false
    fetchData()
  } catch (error: any) {
    if (error !== false) {
      ElMessage.error(error.message || '响应失败')
    }
  } finally {
    responseLoading.value = false
  }
}

// 重试
const handleRetry = async (row: CallRecord) => {
  try {
    await ElMessageBox.confirm('确定要重试该叫应记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await callRecordApi.retry(row.id)
    ElMessage.success('重试成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '重试失败')
    }
  }
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.record-list {
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
