<template>
  <div class="strategy-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>简报策略</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增策略
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="策略类型">
          <el-select v-model="searchForm.strategy_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="常态化策略" :value="1" />
            <el-option label="非常态化策略" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="报告类型">
          <el-select v-model="searchForm.report_type" placeholder="请选择" clearable style="width: 120px">
            <el-option label="日报" value="daily" />
            <el-option label="周报" value="weekly" />
            <el-option label="月报" value="monthly" />
            <el-option label="年报" value="yearly" />
          </el-select>
        </el-form-item>
        <el-form-item label="触发类型">
          <el-select v-model="searchForm.trigger_type" placeholder="请选择" clearable style="width: 120px">
            <el-option label="定时触发" :value="1" />
            <el-option label="事件触发" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="禁用" :value="0" />
            <el-option label="启用" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入策略编码/名称/描述"
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
        <el-table-column prop="strategy_code" label="策略编码" width="150" />
        <el-table-column prop="strategy_name" label="策略名称" min-width="150" show-overflow-tooltip />
        <el-table-column label="关联模板" width="150">
          <template #default="{ row }">
            <span v-if="row.template_detail">{{ row.template_detail.template_name }}</span>
            <span v-else>模板ID: {{ row.template_id }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="strategy_type_display" label="策略类型" width="120" />
        <el-table-column label="报告类型" width="100">
          <template #default="{ row }">
            {{ getReportTypeDisplay(row.report_type) }}
          </template>
        </el-table-column>
        <el-table-column prop="trigger_type_display" label="触发类型" width="100" />
        <el-table-column prop="push_target_type_display" label="推送目标" width="100" />
        <el-table-column label="推送渠道" width="150">
          <template #default="{ row }">
            <el-tag v-for="channel in parseJsonArray(row.push_channel)" :key="channel" size="small" style="margin-right: 5px">
              {{ getPushChannelDisplay(channel) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="next_execute_at" label="下次执行时间" width="160">
          <template #default="{ row }">
            {{ row.next_execute_at || '-' }}
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
              :type="row.status === 1 ? 'warning' : 'success'"
              link
              size="small"
              @click="handleToggleStatus(row)"
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
      width="1200px"
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
            <el-form-item label="策略编码" prop="strategy_code">
              <el-input v-model="formData.strategy_code" placeholder="请输入策略编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="策略名称" prop="strategy_name">
              <el-input v-model="formData.strategy_name" placeholder="请输入策略名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="关联模板" prop="template_id">
              <el-select v-model="formData.template_id" placeholder="请选择模板" filterable style="width: 100%">
                <el-option
                  v-for="template in templateList"
                  :key="template.id"
                  :label="template.template_name"
                  :value="template.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="策略类型" prop="strategy_type">
              <el-select v-model="formData.strategy_type" placeholder="请选择" style="width: 100%">
                <el-option label="常态化策略" :value="1" />
                <el-option label="非常态化策略" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <!-- 常态化策略配置 -->
        <template v-if="formData.strategy_type === 1">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="报告类型" prop="report_type">
                <el-select v-model="formData.report_type" placeholder="请选择" style="width: 100%">
                  <el-option label="日报" value="daily" />
                  <el-option label="周报" value="weekly" />
                  <el-option label="月报" value="monthly" />
                  <el-option label="年报" value="yearly" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </template>
        <!-- 非常态化策略配置 -->
        <template v-if="formData.strategy_type === 2">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="触发类型" prop="trigger_type">
                <el-select v-model="formData.trigger_type" placeholder="请选择" style="width: 100%">
                  <el-option label="定时触发" :value="1" />
                  <el-option label="事件触发" :value="2" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </template>
        <el-form-item label="触发配置">
          <el-input
            v-model="formData.trigger_config"
            type="textarea"
            :rows="4"
            placeholder='请输入触发配置（JSON格式），例如：{"trigger_time": "08:00", "timezone": "Asia/Shanghai"}'
          />
          <div class="form-tip">JSON格式，包含触发时间、触发条件等配置</div>
        </el-form-item>
        <!-- 过滤条件 -->
        <el-divider>过滤条件</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预警类型过滤">
              <el-input
                v-model="formData.warning_type_filter"
                type="textarea"
                :rows="3"
                placeholder='请输入预警类型过滤（JSON数组），例如：["火灾", "洪水"]'
              />
              <div class="form-tip">JSON数组格式，非常态化策略使用</div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预警级别过滤">
              <el-input
                v-model="formData.warning_level_filter"
                type="textarea"
                :rows="3"
                placeholder='请输入预警级别过滤（JSON数组），例如：["红色", "橙色"]'
              />
              <div class="form-tip">JSON数组格式，非常态化策略使用</div>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="行业过滤">
              <el-input
                v-model="formData.industry_filter"
                type="textarea"
                :rows="3"
                placeholder='请输入行业过滤（JSON数组），例如：[1, 2, 3]'
              />
              <div class="form-tip">JSON数组格式，1-森林火灾，2-防汛，3-交通运输，4-危险化学品</div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="区域过滤">
              <el-input
                v-model="formData.region_filter"
                type="textarea"
                :rows="3"
                placeholder='请输入区域过滤（JSON数组），例如：["街道1", "街道2"]'
              />
              <div class="form-tip">JSON数组格式，街道名称列表</div>
            </el-form-item>
          </el-col>
        </el-row>
        <!-- 推送配置 -->
        <el-divider>推送配置</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="推送目标类型" prop="push_target_type">
              <el-select v-model="formData.push_target_type" placeholder="请选择" style="width: 100%">
                <el-option label="指定用户" :value="1" />
                <el-option label="指定角色" :value="2" />
                <el-option label="指定组织" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="推送目标ID列表" prop="push_target_ids">
              <el-input
                v-model="formData.push_target_ids"
                type="textarea"
                :rows="3"
                placeholder='请输入推送目标ID列表（JSON数组），例如：[1, 2, 3]'
              />
              <div class="form-tip">JSON数组格式，根据推送目标类型填写对应的ID列表</div>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="推送渠道" prop="push_channel">
          <el-checkbox-group v-model="pushChannelList">
            <el-checkbox label="system">系统消息</el-checkbox>
            <el-checkbox label="sms">短信</el-checkbox>
            <el-checkbox label="email">邮件</el-checkbox>
          </el-checkbox-group>
          <div class="form-tip">可以选择多个推送渠道</div>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="formData.status" placeholder="请选择" style="width: 100%">
                <el-option label="禁用" :value="0" />
                <el-option label="启用" :value="1" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="策略描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入策略描述"
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
    <el-dialog v-model="detailVisible" title="策略详情" width="1200px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="策略编码">{{ currentRow?.strategy_code }}</el-descriptions-item>
        <el-descriptions-item label="策略名称">{{ currentRow?.strategy_name }}</el-descriptions-item>
        <el-descriptions-item label="关联模板">
          {{ currentRow?.template_detail?.template_name || `模板ID: ${currentRow?.template_id}` }}
        </el-descriptions-item>
        <el-descriptions-item label="策略类型">{{ currentRow?.strategy_type_display }}</el-descriptions-item>
        <el-descriptions-item label="报告类型">
          {{ getReportTypeDisplay(currentRow?.report_type) }}
        </el-descriptions-item>
        <el-descriptions-item label="触发类型">{{ currentRow?.trigger_type_display }}</el-descriptions-item>
        <el-descriptions-item label="推送目标类型">{{ currentRow?.push_target_type_display }}</el-descriptions-item>
        <el-descriptions-item label="推送渠道">
          <el-tag
            v-for="channel in parseJsonArray(currentRow?.push_channel)"
            :key="channel"
            size="small"
            style="margin-right: 5px"
          >
            {{ getPushChannelDisplay(channel) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'info'">
            {{ currentRow?.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="最后执行时间">
          {{ currentRow?.last_execute_at || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="下次执行时间">
          {{ currentRow?.next_execute_at || '-' }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.trigger_config" label="触发配置" :span="2">
          <pre class="json-preview">{{ formatJson(currentRow.trigger_config) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.warning_type_filter"
          label="预警类型过滤"
          :span="2"
        >
          <pre class="json-preview">{{ formatJson(currentRow.warning_type_filter) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.warning_level_filter"
          label="预警级别过滤"
          :span="2"
        >
          <pre class="json-preview">{{ formatJson(currentRow.warning_level_filter) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.industry_filter" label="行业过滤" :span="2">
          <pre class="json-preview">{{ formatJson(currentRow.industry_filter) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow?.region_filter" label="区域过滤" :span="2">
          <pre class="json-preview">{{ formatJson(currentRow.region_filter) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="策略描述" :span="2">
          {{ currentRow?.description || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { briefStrategyApi, briefTemplateApi } from '@/api/modules/brief'
import type {
  BriefStrategy,
  BriefStrategyFormData,
  BriefTemplate,
} from '@/types/modules/brief'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<BriefStrategy[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 模板列表
const templateList = ref<BriefTemplate[]>([])

// 搜索表单
const searchForm = reactive({
  strategy_type: undefined as 1 | 2 | undefined,
  report_type: undefined as string | undefined,
  trigger_type: undefined as 1 | 2 | undefined,
  status: undefined as 0 | 1 | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增策略')
const currentRow = ref<BriefStrategy | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<BriefStrategyFormData>({
  strategy_code: '',
  strategy_name: '',
  template_id: 0,
  strategy_type: 1,
  report_type: null,
  trigger_type: 1,
  trigger_config: null,
  warning_type_filter: null,
  warning_level_filter: null,
  industry_filter: null,
  region_filter: null,
  push_target_type: 1,
  push_target_ids: null,
  push_channel: null,
  message_template_id: null,
  status: 1,
  description: null,
  remark: null,
})

// 推送渠道列表（用于复选框）
const pushChannelList = ref<string[]>([])

// 监听推送渠道变化，同步到formData
watch(
  pushChannelList,
  (newVal) => {
    if (newVal.length > 0) {
      formData.push_channel = JSON.stringify(newVal)
    } else {
      formData.push_channel = null
    }
  },
  { deep: true }
)

// 表单验证规则
const formRules: FormRules = {
  strategy_code: [
    { required: true, message: '请输入策略编码', trigger: 'blur' },
  ],
  strategy_name: [
    { required: true, message: '请输入策略名称', trigger: 'blur' },
  ],
  template_id: [
    { required: true, message: '请选择关联模板', trigger: 'change' },
    { type: 'number', min: 1, message: '请选择有效的模板', trigger: 'change' },
  ],
  strategy_type: [
    { required: true, message: '请选择策略类型', trigger: 'change' },
  ],
  push_target_type: [
    { required: true, message: '请选择推送目标类型', trigger: 'change' },
  ],
  push_channel: [
    { required: true, message: '请至少选择一个推送渠道', trigger: 'change' },
  ],
}

// 获取模板列表
const fetchTemplateList = async () => {
  try {
    const response = await briefTemplateApi.getList({ page_size: 100, status: 1 })
    templateList.value = response.results
  } catch (error: any) {
    console.error('获取模板列表失败:', error)
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
    const response = await briefStrategyApi.getList(params)
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
    strategy_type: undefined,
    report_type: undefined,
    trigger_type: undefined,
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
  dialogTitle.value = '新增策略'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: BriefStrategy) => {
  isEdit.value = true
  dialogTitle.value = '编辑策略'
  currentRow.value = row
  Object.assign(formData, {
    strategy_code: row.strategy_code,
    strategy_name: row.strategy_name,
    template_id: row.template_id,
    strategy_type: row.strategy_type,
    report_type: row.report_type,
    trigger_type: row.trigger_type,
    trigger_config: row.trigger_config,
    warning_type_filter: row.warning_type_filter,
    warning_level_filter: row.warning_level_filter,
    industry_filter: row.industry_filter,
    region_filter: row.region_filter,
    push_target_type: row.push_target_type,
    push_target_ids: row.push_target_ids,
    push_channel: row.push_channel,
    message_template_id: row.message_template_id,
    status: row.status,
    description: row.description,
    remark: row.remark,
  })
  // 解析推送渠道
  if (row.push_channel) {
    pushChannelList.value = parseJsonArray(row.push_channel)
  } else {
    pushChannelList.value = []
  }
  dialogVisible.value = true
}

// 查看
const handleView = (row: BriefStrategy) => {
  currentRow.value = row
  detailVisible.value = true
}

// 切换状态
const handleToggleStatus = async (row: BriefStrategy) => {
  try {
    const newStatus = row.status === 1 ? 0 : 1
    await briefStrategyApi.update(row.id, { status: newStatus })
    ElMessage.success(newStatus === 1 ? '启用成功' : '禁用成功')
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

// 删除
const handleDelete = async (row: BriefStrategy) => {
  try {
    await ElMessageBox.confirm('确定要删除该简报策略吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await briefStrategyApi.delete(row.id)
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

    // 验证推送渠道
    if (pushChannelList.value.length === 0) {
      ElMessage.warning('请至少选择一个推送渠道')
      return
    }

    submitLoading.value = true
    try {
      const data: BriefStrategyFormData = {
        strategy_code: formData.strategy_code,
        strategy_name: formData.strategy_name,
        template_id: formData.template_id,
        strategy_type: formData.strategy_type,
        report_type: formData.report_type,
        trigger_type: formData.trigger_type,
        trigger_config: formData.trigger_config,
        warning_type_filter: formData.warning_type_filter,
        warning_level_filter: formData.warning_level_filter,
        industry_filter: formData.industry_filter,
        region_filter: formData.region_filter,
        push_target_type: formData.push_target_type,
        push_target_ids: formData.push_target_ids,
        push_channel: formData.push_channel,
        message_template_id: formData.message_template_id,
        status: formData.status,
        description: formData.description,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        await briefStrategyApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await briefStrategyApi.create(data)
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
    strategy_code: '',
    strategy_name: '',
    template_id: 0,
    strategy_type: 1,
    report_type: null,
    trigger_type: 1,
    trigger_config: null,
    warning_type_filter: null,
    warning_level_filter: null,
    industry_filter: null,
    region_filter: null,
    push_target_type: 1,
    push_target_ids: null,
    push_channel: null,
    message_template_id: null,
    status: 1,
    description: null,
    remark: null,
  })
  pushChannelList.value = []
  formRef.value?.clearValidate()
  currentRow.value = null
}

// 对话框关闭
const handleDialogClose = () => {
  resetForm()
  isEdit.value = false
}

// 格式化JSON
const formatJson = (jsonStr: string | null | undefined) => {
  if (!jsonStr) return '-'
  try {
    const obj = JSON.parse(jsonStr)
    return JSON.stringify(obj, null, 2)
  } catch (e) {
    return jsonStr
  }
}

// 解析JSON数组
const parseJsonArray = (jsonStr: string | null | undefined): string[] => {
  if (!jsonStr) return []
  try {
    const arr = JSON.parse(jsonStr)
    return Array.isArray(arr) ? arr : []
  } catch (e) {
    return []
  }
}

// 获取报告类型显示
const getReportTypeDisplay = (reportType: string | null | undefined) => {
  if (!reportType) return '-'
  const typeMap: Record<string, string> = {
    daily: '日报',
    weekly: '周报',
    monthly: '月报',
    yearly: '年报',
  }
  return typeMap[reportType] || reportType
}

// 获取推送渠道显示
const getPushChannelDisplay = (channel: string) => {
  const channelMap: Record<string, string> = {
    system: '系统消息',
    sms: '短信',
    email: '邮件',
  }
  return channelMap[channel] || channel
}

// 初始化
onMounted(() => {
  fetchTemplateList()
  fetchData()
})
</script>

<style scoped lang="scss">
.strategy-list {
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

  .json-preview {
    background: #f5f7fa;
    padding: 10px;
    border-radius: 4px;
    font-size: 12px;
    max-height: 300px;
    overflow: auto;
    margin: 0;
  }
}
</style>
