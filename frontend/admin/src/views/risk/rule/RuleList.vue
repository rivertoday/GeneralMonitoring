<template>
  <div class="rule-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>预警规则</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增规则
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="规则类型">
          <el-select v-model="searchForm.rule_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="预警生成规则" :value="1" />
            <el-option label="预警处置规则" :value="2" />
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
        <el-form-item label="预警级别">
          <el-select v-model="searchForm.warning_level" placeholder="请选择" clearable style="width: 150px">
            <el-option
              v-for="level in warningLevels"
              :key="level.id"
              :label="level.level_name"
              :value="level.id"
            />
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
            placeholder="请输入规则编码/名称/描述"
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
        <el-table-column prop="rule_code" label="规则编码" width="150" />
        <el-table-column prop="rule_name" label="规则名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="rule_type_display" label="规则类型" width="120" />
        <el-table-column prop="industry_type_display" label="行业类型" width="100" />
        <el-table-column label="预警级别" width="120">
          <template #default="{ row }">
            <el-tag
              v-if="row.warning_level_detail"
              :type="getLevelTagType(row.warning_level_detail.level_color)"
            >
              {{ row.warning_level_detail.level_name }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="时间要求" width="200">
          <template #default="{ row }">
            <div v-if="row.rule_type === 2">
              <div v-if="row.response_time">响应: {{ row.response_time }}分钟</div>
              <div v-if="row.handle_time">处置: {{ row.handle_time }}分钟</div>
              <div v-if="row.feedback_time">反馈: {{ row.feedback_time }}分钟</div>
              <span v-if="!row.response_time && !row.handle_time && !row.feedback_time">-</span>
            </div>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="规则描述" min-width="200" show-overflow-tooltip />
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
      width="1000px"
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
            <el-form-item label="规则编码" prop="rule_code">
              <el-input v-model="formData.rule_code" placeholder="请输入规则编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="规则名称" prop="rule_name">
              <el-input v-model="formData.rule_name" placeholder="请输入规则名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="规则类型" prop="rule_type">
              <el-select v-model="formData.rule_type" placeholder="请选择" style="width: 100%">
                <el-option label="预警生成规则" :value="1" />
                <el-option label="预警处置规则" :value="2" />
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
            <el-form-item label="预警级别">
              <el-select v-model="formData.warning_level_id" placeholder="请选择" clearable style="width: 100%">
                <el-option
                  v-for="level in warningLevels"
                  :key="level.id"
                  :label="level.level_name"
                  :value="level.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="formData.status" placeholder="请选择" style="width: 100%">
                <el-option label="禁用" :value="0" />
                <el-option label="启用" :value="1" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="规则条件配置" prop="condition_config">
          <el-input
            v-model="formData.condition_config"
            type="textarea"
            :rows="6"
            placeholder='请输入JSON格式的规则条件配置，例如：{"alarm_frequency": 3, "alarm_duration": 10, "monitor_ids": [1, 2, 3]}'
          />
          <div class="form-tip">JSON格式，包含报警频率、报警时长、报警设备等条件</div>
        </el-form-item>
        <el-form-item
          v-if="formData.rule_type === 2"
          label="规则动作配置"
        >
          <el-input
            v-model="formData.action_config"
            type="textarea"
            :rows="4"
            placeholder='请输入JSON格式的规则动作配置（可选）'
          />
          <div class="form-tip">JSON格式，包含响应时间、处置时间、反馈时间等要求（可选）</div>
        </el-form-item>
        <el-row v-if="formData.rule_type === 2" :gutter="20">
          <el-col :span="8">
            <el-form-item label="响应时间(分钟)">
              <el-input-number
                v-model="formData.response_time"
                :min="0"
                placeholder="请输入响应时间要求"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="处置时间(分钟)">
              <el-input-number
                v-model="formData.handle_time"
                :min="0"
                placeholder="请输入处置时间要求"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="反馈时间(分钟)">
              <el-input-number
                v-model="formData.feedback_time"
                :min="0"
                placeholder="请输入反馈时间要求"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="规则描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入规则描述"
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
    <el-dialog v-model="detailVisible" title="规则详情" width="1000px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="规则编码">{{ currentRow?.rule_code }}</el-descriptions-item>
        <el-descriptions-item label="规则名称">{{ currentRow?.rule_name }}</el-descriptions-item>
        <el-descriptions-item label="规则类型">{{ currentRow?.rule_type_display }}</el-descriptions-item>
        <el-descriptions-item label="行业类型">{{ currentRow?.industry_type_display }}</el-descriptions-item>
        <el-descriptions-item label="预警级别">
          <el-tag
            v-if="currentRow?.warning_level_detail"
            :type="getLevelTagType(currentRow.warning_level_detail.level_color)"
          >
            {{ currentRow.warning_level_detail.level_name }}
          </el-tag>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'info'">
            {{ currentRow?.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.rule_type === 2"
          label="响应时间要求"
        >
          {{ currentRow?.response_time ? `${currentRow.response_time}分钟` : '-' }}
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.rule_type === 2"
          label="处置时间要求"
        >
          {{ currentRow?.handle_time ? `${currentRow.handle_time}分钟` : '-' }}
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.rule_type === 2"
          label="反馈时间要求"
        >
          {{ currentRow?.feedback_time ? `${currentRow.feedback_time}分钟` : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="规则描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="规则条件配置" :span="2">
          <pre class="json-preview">{{ formatJson(currentRow?.condition_config) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.action_config"
          label="规则动作配置"
          :span="2"
        >
          <pre class="json-preview">{{ formatJson(currentRow.action_config) }}</pre>
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
import { warningRuleApi, warningLevelApi } from '@/api/modules/risk'
import type { WarningRule, WarningLevel } from '@/types/modules/risk'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<WarningRule[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 预警级别列表
const warningLevels = ref<WarningLevel[]>([])

// 搜索表单
const searchForm = reactive({
  rule_type: undefined as 1 | 2 | undefined,
  industry_type: undefined as number | undefined,
  warning_level: undefined as number | undefined,
  status: undefined as 0 | 1 | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增规则')
const currentRow = ref<WarningRule | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive({
  rule_code: '',
  rule_name: '',
  rule_type: 1 as 1 | 2,
  industry_type: 1,
  warning_level_id: undefined as number | undefined,
  condition_config: '',
  action_config: null as string | null,
  response_time: null as number | null,
  handle_time: null as number | null,
  feedback_time: null as number | null,
  status: 1,
  description: null as string | null,
  remark: null as string | null,
})

// 表单验证规则
const formRules: FormRules = {
  rule_code: [
    { required: true, message: '请输入规则编码', trigger: 'blur' },
  ],
  rule_name: [
    { required: true, message: '请输入规则名称', trigger: 'blur' },
  ],
  rule_type: [
    { required: true, message: '请选择规则类型', trigger: 'change' },
  ],
  industry_type: [
    { required: true, message: '请选择行业类型', trigger: 'change' },
  ],
  condition_config: [
    { required: true, message: '请输入规则条件配置', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (!value) {
          callback()
          return
        }
        try {
          JSON.parse(value)
          callback()
        } catch (e) {
          callback(new Error('规则条件配置必须是有效的JSON格式'))
        }
      },
      trigger: 'blur',
    },
  ],
  action_config: [
    {
      validator: (rule, value, callback) => {
        if (!value) {
          callback()
          return
        }
        try {
          JSON.parse(value)
          callback()
        } catch (e) {
          callback(new Error('规则动作配置必须是有效的JSON格式'))
        }
      },
      trigger: 'blur',
    },
  ],
}

// 获取预警级别列表
const fetchWarningLevels = async () => {
  try {
    const response = await warningLevelApi.getList({ page_size: 100, status: 1 })
    warningLevels.value = response.results
  } catch (error: any) {
    console.error('获取预警级别失败:', error)
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
    const response = await warningRuleApi.getList(params)
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
    rule_type: undefined,
    industry_type: undefined,
    warning_level: undefined,
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
  dialogTitle.value = '新增规则'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: WarningRule) => {
  isEdit.value = true
  dialogTitle.value = '编辑规则'
  currentRow.value = row
  Object.assign(formData, {
    rule_code: row.rule_code,
    rule_name: row.rule_name,
    rule_type: row.rule_type,
    industry_type: row.industry_type,
    warning_level_id: row.warning_level || undefined,
    condition_config: row.condition_config,
    action_config: row.action_config,
    response_time: row.response_time,
    handle_time: row.handle_time,
    feedback_time: row.feedback_time,
    status: row.status,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: WarningRule) => {
  currentRow.value = row
  detailVisible.value = true
}

// 切换状态
const handleToggleStatus = async (row: WarningRule) => {
  try {
    const newStatus = row.status === 1 ? 0 : 1
    await warningRuleApi.update(row.id, { status: newStatus })
    ElMessage.success(newStatus === 1 ? '启用成功' : '禁用成功')
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

// 删除
const handleDelete = async (row: WarningRule) => {
  try {
    await ElMessageBox.confirm('确定要删除该规则吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await warningRuleApi.delete(row.id)
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
      const data: any = {
        rule_code: formData.rule_code,
        rule_name: formData.rule_name,
        rule_type: formData.rule_type,
        industry_type: formData.industry_type,
        warning_level_id: formData.warning_level_id,
        condition_config: formData.condition_config,
        action_config: formData.action_config || null,
        response_time: formData.response_time,
        handle_time: formData.handle_time,
        feedback_time: formData.feedback_time,
        status: formData.status,
        description: formData.description,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        await warningRuleApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await warningRuleApi.create(data)
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
    rule_code: '',
    rule_name: '',
    rule_type: 1,
    industry_type: 1,
    warning_level_id: undefined,
    condition_config: '',
    action_config: null,
    response_time: null,
    handle_time: null,
    feedback_time: null,
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

// 获取级别标签类型
const getLevelTagType = (color: string) => {
  const colorMap: Record<string, string> = {
    red: 'danger',
    orange: 'warning',
    yellow: 'warning',
    blue: 'info',
  }
  return colorMap[color] || 'info'
}

// 初始化
onMounted(() => {
  fetchWarningLevels()
  fetchData()
})
</script>

<style scoped lang="scss">
.rule-list {
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
