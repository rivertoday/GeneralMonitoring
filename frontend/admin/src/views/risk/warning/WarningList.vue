<template>
  <div class="warning-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>风险预警</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增预警
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
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
        <el-form-item label="行业类型">
          <el-select v-model="searchForm.industry_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="森林火灾" :value="1" />
            <el-option label="防汛" :value="2" />
            <el-option label="交通运输" :value="3" />
            <el-option label="危险化学品" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="预警状态">
          <el-select v-model="searchForm.warning_status" placeholder="请选择" clearable style="width: 150px">
            <el-option label="未发布" :value="0" />
            <el-option label="已发布" :value="1" />
            <el-option label="处理中" :value="2" />
            <el-option label="已处置" :value="3" />
            <el-option label="已关闭" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="预警来源">
          <el-select v-model="searchForm.warning_source" placeholder="请选择" clearable style="width: 150px">
            <el-option label="自动生成" :value="1" />
            <el-option label="手动创建" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="预警时间">
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
            placeholder="请输入预警编码/标题/内容/地址"
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
        <el-table-column prop="warning_code" label="预警编码" width="150" />
        <el-table-column prop="warning_title" label="预警标题" min-width="200" show-overflow-tooltip />
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
        <el-table-column prop="industry_type_display" label="行业类型" width="100" />
        <el-table-column prop="warning_type" label="预警类型" width="120" />
        <el-table-column prop="street" label="所属街道" width="120" />
        <el-table-column prop="address" label="详细地址" min-width="150" show-overflow-tooltip />
        <el-table-column prop="warning_time" label="预警时间" width="160" />
        <el-table-column label="预警状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.warning_status)">
              {{ row.warning_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publish_time" label="发布时间" width="160" />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button
              v-if="row.warning_status === 0"
              type="success"
              link
              size="small"
              @click="handlePublish(row)"
            >
              发布
            </el-button>
            <el-button
              v-if="row.warning_status === 1 || row.warning_status === 2"
              type="warning"
              link
              size="small"
              @click="handleHandle(row)"
            >
              处置
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
            <el-form-item label="预警编码" prop="warning_code">
              <el-input v-model="formData.warning_code" placeholder="请输入预警编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预警标题" prop="warning_title">
              <el-input v-model="formData.warning_title" placeholder="请输入预警标题" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预警级别" prop="warning_level_id">
              <el-select v-model="formData.warning_level_id" placeholder="请选择" style="width: 100%">
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
            <el-form-item label="预警类型" prop="warning_type">
              <el-input v-model="formData.warning_type" placeholder="请输入预警类型" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预警分析类型">
              <el-select v-model="formData.warning_analysis_type" placeholder="请选择" clearable style="width: 100%">
                <el-option label="突出预警" :value="1" />
                <el-option label="同比预警" :value="2" />
                <el-option label="环比预警" :value="3" />
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
        <el-form-item label="预警时间" prop="warning_time">
          <el-date-picker
            v-model="formData.warning_time"
            type="datetime"
            placeholder="请选择预警时间"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="预警内容" prop="warning_content">
          <el-input
            v-model="formData.warning_content"
            type="textarea"
            :rows="4"
            placeholder="请输入预警内容"
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
    <el-dialog v-model="detailVisible" title="预警详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="预警编码">{{ currentRow?.warning_code }}</el-descriptions-item>
        <el-descriptions-item label="预警标题">{{ currentRow?.warning_title }}</el-descriptions-item>
        <el-descriptions-item label="预警级别">
          <el-tag
            v-if="currentRow?.warning_level_detail"
            :type="getLevelTagType(currentRow.warning_level_detail.level_color)"
          >
            {{ currentRow.warning_level_detail.level_name }}
          </el-tag>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="行业类型">{{ currentRow?.industry_type_display }}</el-descriptions-item>
        <el-descriptions-item label="预警类型">{{ currentRow?.warning_type }}</el-descriptions-item>
        <el-descriptions-item label="预警分析类型">
          {{ currentRow?.warning_analysis_type === 1 ? '突出预警' : currentRow?.warning_analysis_type === 2 ? '同比预警' : currentRow?.warning_analysis_type === 3 ? '环比预警' : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="所属街道">{{ currentRow?.street || '-' }}</el-descriptions-item>
        <el-descriptions-item label="详细地址">{{ currentRow?.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="经度">{{ currentRow?.longitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="纬度">{{ currentRow?.latitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="预警时间">{{ currentRow?.warning_time }}</el-descriptions-item>
        <el-descriptions-item label="预警来源">
          {{ currentRow?.warning_source === 1 ? '自动生成' : '手动创建' }}
        </el-descriptions-item>
        <el-descriptions-item label="预警状态">
          <el-tag :type="getStatusTagType(currentRow?.warning_status)">
            {{ currentRow?.warning_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="发布时间">{{ currentRow?.publish_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="响应时间">{{ currentRow?.response_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="处置时间">{{ currentRow?.handle_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="反馈时间">{{ currentRow?.feedback_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="预警内容" :span="2">{{ currentRow?.warning_content }}</el-descriptions-item>
        <el-descriptions-item label="处置结果" :span="2">{{ currentRow?.handle_result || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 发布对话框 -->
    <el-dialog v-model="publishVisible" title="发布预警" width="500px">
      <el-form ref="publishFormRef" :model="publishForm" label-width="100px">
        <el-form-item label="发布时间">
          <el-date-picker
            v-model="publishForm.publish_time"
            type="datetime"
            placeholder="请选择发布时间（留空则使用当前时间）"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="publishVisible = false">取消</el-button>
        <el-button type="primary" :loading="publishLoading" @click="handlePublishSubmit">
          确定发布
        </el-button>
      </template>
    </el-dialog>

    <!-- 处置对话框 -->
    <el-dialog v-model="handleVisible" title="处置预警" width="600px">
      <el-form ref="handleFormRef" :model="handleForm" :rules="handleFormRules" label-width="100px">
        <el-form-item label="处置状态" prop="warning_status">
          <el-select v-model="handleForm.warning_status" placeholder="请选择" style="width: 100%">
            <el-option label="处理中" :value="2" />
            <el-option label="已处置" :value="3" />
            <el-option label="已关闭" :value="4" />
          </el-select>
        </el-form-item>
        <el-form-item label="处置结果" prop="handle_result">
          <el-input
            v-model="handleForm.handle_result"
            type="textarea"
            :rows="5"
            placeholder="请输入处置结果"
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
import { riskWarningApi, warningLevelApi } from '@/api/modules/risk'
import type { RiskWarning, WarningLevel } from '@/types/modules/risk'
import type { PaginatedResponse } from '@/api/types'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)
const publishLoading = ref(false)
const handleLoading = ref(false)

// 表格数据
const tableData = ref<RiskWarning[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 预警级别列表
const warningLevels = ref<WarningLevel[]>([])

// 搜索表单
const searchForm = reactive({
  warning_level: undefined as number | undefined,
  industry_type: undefined as number | undefined,
  warning_status: undefined as number | undefined,
  warning_source: undefined as number | undefined,
  search: undefined as string | undefined,
})

// 时间范围
const timeRange = ref<[string, string] | null>(null)

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const publishVisible = ref(false)
const handleVisible = ref(false)
const dialogTitle = ref('新增预警')
const currentRow = ref<RiskWarning | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const publishFormRef = ref<FormInstance>()
const handleFormRef = ref<FormInstance>()
const formData = reactive({
  warning_code: '',
  warning_title: '',
  warning_level_id: undefined as number | undefined,
  industry_type: 1,
  warning_type: '',
  warning_analysis_type: undefined as 1 | 2 | 3 | undefined,
  longitude: null as number | null,
  latitude: null as number | null,
  street: null as string | null,
  address: null as string | null,
  warning_time: '',
  warning_content: '',
  remark: null as string | null,
})

const publishForm = reactive({
  publish_time: '',
})

const handleForm = reactive({
  warning_status: 2 as 2 | 3 | 4,
  handle_result: '',
})

// 表单验证规则
const formRules: FormRules = {
  warning_code: [
    { required: true, message: '请输入预警编码', trigger: 'blur' },
  ],
  warning_title: [
    { required: true, message: '请输入预警标题', trigger: 'blur' },
  ],
  warning_level_id: [
    { required: true, message: '请选择预警级别', trigger: 'change' },
  ],
  industry_type: [
    { required: true, message: '请选择行业类型', trigger: 'change' },
  ],
  warning_type: [
    { required: true, message: '请输入预警类型', trigger: 'blur' },
  ],
  warning_time: [
    { required: true, message: '请选择预警时间', trigger: 'change' },
  ],
  warning_content: [
    { required: true, message: '请输入预警内容', trigger: 'blur' },
  ],
}

const handleFormRules: FormRules = {
  warning_status: [
    { required: true, message: '请选择处置状态', trigger: 'change' },
  ],
  handle_result: [
    { required: true, message: '请输入处置结果', trigger: 'blur' },
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
    if (timeRange.value) {
      params.start_time = timeRange.value[0]
      params.end_time = timeRange.value[1]
    }
    const response = await riskWarningApi.getList(params)
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
    warning_level: undefined,
    industry_type: undefined,
    warning_status: undefined,
    warning_source: undefined,
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
  dialogTitle.value = '新增预警'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: RiskWarning) => {
  isEdit.value = true
  dialogTitle.value = '编辑预警'
  currentRow.value = row
  Object.assign(formData, {
    warning_code: row.warning_code,
    warning_title: row.warning_title,
    warning_level_id: row.warning_level_id,
    industry_type: row.industry_type,
    warning_type: row.warning_type,
    warning_analysis_type: row.warning_analysis_type,
    longitude: row.longitude,
    latitude: row.latitude,
    street: row.street,
    address: row.address,
    warning_time: row.warning_time,
    warning_content: row.warning_content,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: RiskWarning) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: RiskWarning) => {
  try {
    await ElMessageBox.confirm('确定要删除该预警吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await riskWarningApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 发布
const handlePublish = (row: RiskWarning) => {
  currentRow.value = row
  publishForm.publish_time = ''
  publishVisible.value = true
}

// 发布提交
const handlePublishSubmit = async () => {
  if (!currentRow.value) return

  publishLoading.value = true
  try {
    await riskWarningApi.publish(currentRow.value.id)
    ElMessage.success('发布成功')
    publishVisible.value = false
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '发布失败')
  } finally {
    publishLoading.value = false
  }
}

// 处置
const handleHandle = (row: RiskWarning) => {
  currentRow.value = row
  handleForm.warning_status = 2
  handleForm.handle_result = ''
  handleVisible.value = true
}

// 处置提交
const handleHandleSubmit = async () => {
  if (!handleFormRef.value || !currentRow.value) return

  await handleFormRef.value.validate(async (valid) => {
    if (!valid) return

    if (!currentRow.value) {
      ElMessage.warning('请选择要处置的预警事件')
      return
    }
    
    handleLoading.value = true
    try {
      await riskWarningApi.handle(currentRow.value.id, {
        handle_result: handleForm.handle_result,
      })
      ElMessage.success('处置成功')
      handleVisible.value = false
      fetchData()
    } catch (error: any) {
      ElMessage.error(error.message || '处置失败')
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
        warning_code: formData.warning_code,
        warning_title: formData.warning_title,
        warning_level_id: formData.warning_level_id,
        industry_type: formData.industry_type,
        warning_type: formData.warning_type,
        warning_analysis_type: formData.warning_analysis_type,
        longitude: formData.longitude,
        latitude: formData.latitude,
        street: formData.street,
        address: formData.address,
        warning_time: formData.warning_time,
        warning_content: formData.warning_content,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        await riskWarningApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await riskWarningApi.create(data)
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
    warning_code: '',
    warning_title: '',
    warning_level_id: undefined,
    industry_type: 1,
    warning_type: '',
    warning_analysis_type: undefined,
    longitude: null,
    latitude: null,
    street: null,
    address: null,
    warning_time: '',
    warning_content: '',
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

// 获取状态标签类型
const getStatusTagType = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: 'info',
    1: 'success',
    2: 'warning',
    3: 'success',
    4: 'info',
  }
  return statusMap[status || 0] || 'info'
}

// 初始化
onMounted(() => {
  fetchWarningLevels()
  fetchData()
})
</script>

<style scoped lang="scss">
.warning-list {
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
