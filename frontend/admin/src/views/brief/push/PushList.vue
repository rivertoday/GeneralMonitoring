<template>
  <div class="push-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>简报推送</h2>
      <el-button type="primary" @click="handlePush">
        <el-icon><Plus /></el-icon>
        推送简报
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="简报">
          <el-select v-model="searchForm.brief_id" placeholder="请选择简报" clearable filterable style="width: 200px">
            <el-option
              v-for="brief in briefList"
              :key="brief.id"
              :label="brief.brief_title"
              :value="brief.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="推送目标类型">
          <el-select v-model="searchForm.push_target_type" placeholder="请选择" clearable style="width: 120px">
            <el-option label="用户" :value="1" />
            <el-option label="角色" :value="2" />
            <el-option label="组织" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="推送渠道">
          <el-select v-model="searchForm.push_channel" placeholder="请选择" clearable style="width: 120px">
            <el-option label="系统消息" value="system" />
            <el-option label="短信" value="sms" />
            <el-option label="邮件" value="email" />
          </el-select>
        </el-form-item>
        <el-form-item label="推送状态">
          <el-select v-model="searchForm.push_status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="待推送" :value="0" />
            <el-option label="推送中" :value="1" />
            <el-option label="推送成功" :value="2" />
            <el-option label="推送失败" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="阅读状态">
          <el-select v-model="searchForm.read_status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="未读" :value="0" />
            <el-option label="已读" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="推送时间">
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
        <el-table-column prop="id" label="记录ID" width="100" />
        <el-table-column label="简报" min-width="200">
          <template #default="{ row }">
            <span v-if="row.brief_detail">{{ row.brief_detail.brief_title }}</span>
            <span v-else>简报ID: {{ row.brief_id }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="push_target_type_display" label="推送目标" width="100" />
        <el-table-column prop="target_id" label="目标ID" width="100" />
        <el-table-column prop="push_channel_display" label="推送渠道" width="100" />
        <el-table-column label="推送状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getPushStatusTagType(row.push_status)">
              {{ row.push_status_display || getPushStatusDisplay(row.push_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="push_time" label="推送时间" width="160">
          <template #default="{ row }">
            {{ row.push_time || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="阅读状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.read_status === 1 ? 'success' : 'info'">
              {{ row.read_status_display || (row.read_status === 1 ? '已读' : '未读') }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="read_time" label="阅读时间" width="160">
          <template #default="{ row }">
            {{ row.read_time || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="error_message" label="错误信息" min-width="200" show-overflow-tooltip>
          <template #default="{ row }">
            <span v-if="row.error_message" class="text-danger">{{ row.error_message }}</span>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button
              v-if="row.read_status === 0"
              type="success"
              link
              size="small"
              @click="handleMarkRead(row)"
            >
              标记已读
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

    <!-- 推送简报对话框 -->
    <el-dialog v-model="pushVisible" title="推送简报" width="600px">
      <el-form ref="pushFormRef" :model="pushForm" :rules="pushFormRules" label-width="120px">
        <el-form-item label="选择简报" prop="brief_id">
          <el-select v-model="pushForm.brief_id" placeholder="请选择简报" filterable style="width: 100%">
            <el-option
              v-for="brief in briefList"
              :key="brief.id"
              :label="brief.brief_title"
              :value="brief.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="推送目标类型" prop="push_target_type">
          <el-select v-model="pushForm.push_target_type" placeholder="请选择" style="width: 100%">
            <el-option label="用户" :value="1" />
            <el-option label="角色" :value="2" />
            <el-option label="组织" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="推送目标ID列表" prop="target_ids">
          <el-input
            v-model="pushForm.target_ids"
            type="textarea"
            :rows="4"
            placeholder='请输入推送目标ID列表（JSON数组），例如：[1, 2, 3]'
          />
          <div class="form-tip">JSON数组格式，根据推送目标类型填写对应的ID列表</div>
        </el-form-item>
        <el-form-item label="推送渠道" prop="push_channel">
          <el-checkbox-group v-model="pushChannelList">
            <el-checkbox label="system">系统消息</el-checkbox>
            <el-checkbox label="sms">短信</el-checkbox>
            <el-checkbox label="email">邮件</el-checkbox>
          </el-checkbox-group>
          <div class="form-tip">可以选择多个推送渠道</div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="pushVisible = false">取消</el-button>
        <el-button type="primary" :loading="pushLoading" @click="handlePushSubmit">
          推送
        </el-button>
      </template>
    </el-dialog>

    <!-- 详情对话框 -->
    <el-dialog v-model="detailVisible" title="推送记录详情" width="800px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="记录ID">{{ currentRow?.id }}</el-descriptions-item>
        <el-descriptions-item label="简报">
          {{ currentRow?.brief_detail?.brief_title || `简报ID: ${currentRow?.brief_id}` }}
        </el-descriptions-item>
        <el-descriptions-item label="推送目标类型">{{ currentRow?.push_target_type_display }}</el-descriptions-item>
        <el-descriptions-item label="目标ID">{{ currentRow?.target_id }}</el-descriptions-item>
        <el-descriptions-item label="推送渠道">{{ currentRow?.push_channel_display }}</el-descriptions-item>
        <el-descriptions-item label="推送状态">
          <el-tag :type="getPushStatusTagType(currentRow?.push_status)">
            {{ currentRow?.push_status_display || getPushStatusDisplay(currentRow?.push_status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="推送时间">
          {{ currentRow?.push_time || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="阅读状态">
          <el-tag :type="currentRow?.read_status === 1 ? 'success' : 'info'">
            {{ currentRow?.read_status_display || (currentRow?.read_status === 1 ? '已读' : '未读') }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="阅读时间">
          {{ currentRow?.read_time || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="消息ID">
          {{ currentRow?.message_id || '-' }}
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.error_message"
          label="错误信息"
          :span="2"
        >
          <span class="text-danger">{{ currentRow.error_message }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">
          {{ currentRow?.remark || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { briefPushApi, briefDataApi } from '@/api/modules/brief'
import type {
  BriefPush,
  BriefPushListParams,
  BriefPushCreateParams,
  BriefData,
} from '@/types/modules/brief'

// 加载状态
const loading = ref(false)
const pushLoading = ref(false)

// 表格数据
const tableData = ref<BriefPush[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 简报列表
const briefList = ref<BriefData[]>([])

// 搜索表单
const searchForm = reactive<BriefPushListParams>({
  brief_id: undefined,
  push_target_type: undefined,
  push_channel: undefined,
  push_status: undefined,
  read_status: undefined,
  start_time: undefined,
  end_time: undefined,
})

// 时间范围
const timeRange = ref<[string, string] | null>(null)

// 对话框
const detailVisible = ref(false)
const pushVisible = ref(false)
const currentRow = ref<BriefPush | null>(null)

// 推送表单
const pushFormRef = ref<FormInstance>()
const pushForm = reactive<BriefPushCreateParams>({
  brief_id: 0,
  push_target_type: 1,
  target_ids: [],
  push_channel: [],
})

// 推送渠道列表（用于复选框）
const pushChannelList = ref<string[]>([])

// 监听推送渠道变化，同步到pushForm
watch(
  pushChannelList,
  (newVal) => {
    pushForm.push_channel = newVal
  },
  { deep: true }
)

// 推送表单验证规则
const pushFormRules: FormRules = {
  brief_id: [
    { required: true, message: '请选择简报', trigger: 'change' },
    { type: 'number', min: 1, message: '请选择有效的简报', trigger: 'change' },
  ],
  push_target_type: [
    { required: true, message: '请选择推送目标类型', trigger: 'change' },
  ],
  target_ids: [
    { required: true, message: '请输入推送目标ID列表', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (!value) {
          callback(new Error('请输入推送目标ID列表'))
          return
        }
        try {
          const ids = JSON.parse(value)
          if (!Array.isArray(ids) || ids.length === 0) {
            callback(new Error('推送目标ID列表必须是包含至少一个ID的数组'))
            return
          }
          callback()
        } catch (e) {
          callback(new Error('推送目标ID列表必须是有效的JSON数组格式'))
        }
      },
      trigger: 'blur',
    },
  ],
  push_channel: [
    { required: true, message: '请至少选择一个推送渠道', trigger: 'change' },
  ],
}

// 获取简报列表
const fetchBriefList = async () => {
  try {
    const response = await briefDataApi.getList({ page_size: 100, status: 1 }) // 获取已推送的简报
    briefList.value = response.results
  } catch (error: any) {
    console.error('获取简报列表失败:', error)
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
    const response = await briefPushApi.getList(params)
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
    brief_id: undefined,
    push_target_type: undefined,
    push_channel: undefined,
    push_status: undefined,
    read_status: undefined,
    start_time: undefined,
    end_time: undefined,
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

// 查看
const handleView = (row: BriefPush) => {
  currentRow.value = row
  detailVisible.value = true
}

// 标记已读
const handleMarkRead = async (row: BriefPush) => {
  try {
    await briefPushApi.markRead({ push_id: row.id })
    ElMessage.success('标记已读成功')
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '标记已读失败')
  }
}

// 删除
const handleDelete = async (row: BriefPush) => {
  try {
    await ElMessageBox.confirm('确定要删除该推送记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await briefPushApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 推送简报
const handlePush = () => {
  pushForm.brief_id = 0
  pushForm.push_target_type = 1
  pushForm.target_ids = []
  pushForm.push_channel = []
  pushChannelList.value = []
  pushVisible.value = true
}

// 推送提交
const handlePushSubmit = async () => {
  if (!pushFormRef.value) return

  await pushFormRef.value.validate(async (valid) => {
    if (!valid) return

    // 验证推送渠道
    if (pushChannelList.value.length === 0) {
      ElMessage.warning('请至少选择一个推送渠道')
      return
    }

    // 解析目标ID列表
    let targetIds: number[] = []
    try {
      targetIds = JSON.parse(pushForm.target_ids as any)
      if (!Array.isArray(targetIds) || targetIds.length === 0) {
        ElMessage.warning('推送目标ID列表必须是包含至少一个ID的数组')
        return
      }
    } catch (e) {
      ElMessage.warning('推送目标ID列表必须是有效的JSON数组格式')
      return
    }

    pushLoading.value = true
    try {
      const data: BriefPushCreateParams = {
        brief_id: pushForm.brief_id,
        push_target_type: pushForm.push_target_type,
        target_ids: targetIds,
        push_channel: pushForm.push_channel,
      }
      await briefPushApi.push(data)
      ElMessage.success('推送成功')
      pushVisible.value = false
      fetchData()
    } catch (error: any) {
      ElMessage.error(error.message || '推送失败')
    } finally {
      pushLoading.value = false
    }
  })
}

// 获取推送状态显示
const getPushStatusDisplay = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: '待推送',
    1: '推送中',
    2: '推送成功',
    3: '推送失败',
  }
  return statusMap[status ?? 0] || '-'
}

// 获取推送状态标签类型
const getPushStatusTagType = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: 'info',
    1: 'warning',
    2: 'success',
    3: 'danger',
  }
  return statusMap[status ?? 0] || 'info'
}

// 初始化
onMounted(() => {
  fetchBriefList()
  fetchData()
})
</script>

<style scoped lang="scss">
.push-list {
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

  .text-muted {
    color: #909399;
  }

  .text-danger {
    color: #f56c6c;
  }

  .form-tip {
    font-size: 12px;
    color: #909399;
    margin-top: 5px;
  }
}
</style>
