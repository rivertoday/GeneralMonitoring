<template>
  <div class="template-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>简报模板</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增模板
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="模板类型">
          <el-select v-model="searchForm.template_type" placeholder="请选择" clearable style="width: 180px">
            <el-option label="常态化运行报告" :value="1" />
            <el-option label="非常态化突发预警简报" :value="2" />
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
        <el-form-item label="时间维度">
          <el-select v-model="searchForm.time_dimension" placeholder="请选择" clearable style="width: 120px">
            <el-option label="日" value="day" />
            <el-option label="周" value="week" />
            <el-option label="月" value="month" />
            <el-option label="年" value="year" />
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
            placeholder="请输入模板编码/名称/描述"
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
        <el-table-column prop="template_code" label="模板编码" width="150" />
        <el-table-column prop="template_name" label="模板名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="template_type_display" label="模板类型" width="180" />
        <el-table-column prop="industry_type_display" label="行业类型" width="120" />
        <el-table-column label="时间维度" width="100">
          <template #default="{ row }">
            {{ getTimeDimensionDisplay(row.time_dimension) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="模板描述" min-width="200" show-overflow-tooltip />
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
            <el-form-item label="模板编码" prop="template_code">
              <el-input v-model="formData.template_code" placeholder="请输入模板编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="模板名称" prop="template_name">
              <el-input v-model="formData.template_name" placeholder="请输入模板名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="模板类型" prop="template_type">
              <el-select v-model="formData.template_type" placeholder="请选择" style="width: 100%">
                <el-option label="常态化运行报告" :value="1" />
                <el-option label="非常态化突发预警简报" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="行业类型">
              <el-select v-model="formData.industry_type" placeholder="请选择（留空表示全部）" clearable style="width: 100%">
                <el-option label="森林火灾" :value="1" />
                <el-option label="防汛" :value="2" />
                <el-option label="交通运输" :value="3" />
                <el-option label="危险化学品" :value="4" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20" v-if="formData.template_type === 1">
          <el-col :span="12">
            <el-form-item label="时间维度">
              <el-select v-model="formData.time_dimension" placeholder="请选择（常态化模板）" clearable style="width: 100%">
                <el-option label="日" value="day" />
                <el-option label="周" value="week" />
                <el-option label="月" value="month" />
                <el-option label="年" value="year" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="模板内容" prop="template_content">
          <el-input
            v-model="formData.template_content"
            type="textarea"
            :rows="10"
            placeholder="请输入模板内容，支持变量占位符，例如：{报警次数}、{预警次数}、{风险隐患数量}等"
          />
          <div class="form-tip">支持变量占位符，变量名用大括号包裹，如：{报警次数}、{预警次数}、{时间}等</div>
        </el-form-item>
        <el-form-item label="变量说明">
          <el-input
            v-model="formData.variables"
            type="textarea"
            :rows="4"
            placeholder='请输入变量说明（JSON格式），例如：{"报警次数": "周期内报警总数", "预警次数": "周期内预警总数"}'
          />
          <div class="form-tip">JSON格式，说明模板内容中可用的变量及其含义</div>
        </el-form-item>
        <el-form-item label="数据配置">
          <el-input
            v-model="formData.data_config"
            type="textarea"
            :rows="4"
            placeholder='请输入数据配置（JSON格式），定义需要统计的数据项'
          />
          <div class="form-tip">JSON格式，定义需要统计的数据项，如：{"alarm": true, "warning": true, "risk": true}</div>
        </el-form-item>
        <el-form-item label="区域维度配置">
          <el-input
            v-model="formData.region_dimension"
            type="textarea"
            :rows="3"
            placeholder='请输入区域维度配置（JSON格式，可选）'
          />
          <div class="form-tip">JSON格式，定义区域维度统计配置（可选）</div>
        </el-form-item>
        <el-form-item label="行业维度配置">
          <el-input
            v-model="formData.industry_dimension"
            type="textarea"
            :rows="3"
            placeholder='请输入行业维度配置（JSON格式，可选）'
          />
          <div class="form-tip">JSON格式，定义行业维度统计配置（可选）</div>
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
        <el-form-item label="模板描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入模板描述"
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
    <el-dialog v-model="detailVisible" title="模板详情" width="1200px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="模板编码">{{ currentRow?.template_code }}</el-descriptions-item>
        <el-descriptions-item label="模板名称">{{ currentRow?.template_name }}</el-descriptions-item>
        <el-descriptions-item label="模板类型">{{ currentRow?.template_type_display }}</el-descriptions-item>
        <el-descriptions-item label="行业类型">
          {{ currentRow?.industry_type_display || '全部' }}
        </el-descriptions-item>
        <el-descriptions-item label="时间维度">
          {{ getTimeDimensionDisplay(currentRow?.time_dimension) }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'info'">
            {{ currentRow?.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="模板内容" :span="2">
          <pre class="template-content-preview">{{ currentRow?.template_content }}</pre>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.variables"
          label="变量说明"
          :span="2"
        >
          <pre class="json-preview">{{ formatJson(currentRow.variables) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.data_config"
          label="数据配置"
          :span="2"
        >
          <pre class="json-preview">{{ formatJson(currentRow.data_config) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.region_dimension"
          label="区域维度配置"
          :span="2"
        >
          <pre class="json-preview">{{ formatJson(currentRow.region_dimension) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item
          v-if="currentRow?.industry_dimension"
          label="行业维度配置"
          :span="2"
        >
          <pre class="json-preview">{{ formatJson(currentRow.industry_dimension) }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="模板描述" :span="2">
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { briefTemplateApi } from '@/api/modules/brief'
import type { BriefTemplate, BriefTemplateFormData } from '@/types/modules/brief'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<BriefTemplate[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive({
  template_type: undefined as 1 | 2 | undefined,
  industry_type: undefined as number | undefined,
  time_dimension: undefined as string | undefined,
  status: undefined as 0 | 1 | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增模板')
const currentRow = ref<BriefTemplate | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<BriefTemplateFormData>({
  template_code: '',
  template_name: '',
  template_type: 1,
  industry_type: null,
  time_dimension: null,
  region_dimension: null,
  industry_dimension: null,
  template_content: '',
  variables: null,
  data_config: null,
  status: 1,
  description: null,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  template_code: [
    { required: true, message: '请输入模板编码', trigger: 'blur' },
  ],
  template_name: [
    { required: true, message: '请输入模板名称', trigger: 'blur' },
  ],
  template_type: [
    { required: true, message: '请选择模板类型', trigger: 'change' },
  ],
  template_content: [
    { required: true, message: '请输入模板内容', trigger: 'blur' },
  ],
  variables: [
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
          callback(new Error('变量说明必须是有效的JSON格式'))
        }
      },
      trigger: 'blur',
    },
  ],
  data_config: [
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
          callback(new Error('数据配置必须是有效的JSON格式'))
        }
      },
      trigger: 'blur',
    },
  ],
  region_dimension: [
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
          callback(new Error('区域维度配置必须是有效的JSON格式'))
        }
      },
      trigger: 'blur',
    },
  ],
  industry_dimension: [
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
          callback(new Error('行业维度配置必须是有效的JSON格式'))
        }
      },
      trigger: 'blur',
    },
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
    const response = await briefTemplateApi.getList(params)
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
    template_type: undefined,
    industry_type: undefined,
    time_dimension: undefined,
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
  dialogTitle.value = '新增模板'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: BriefTemplate) => {
  isEdit.value = true
  dialogTitle.value = '编辑模板'
  currentRow.value = row
  Object.assign(formData, {
    template_code: row.template_code,
    template_name: row.template_name,
    template_type: row.template_type,
    industry_type: row.industry_type,
    time_dimension: row.time_dimension,
    region_dimension: row.region_dimension,
    industry_dimension: row.industry_dimension,
    template_content: row.template_content,
    variables: row.variables,
    data_config: row.data_config,
    status: row.status,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: BriefTemplate) => {
  currentRow.value = row
  detailVisible.value = true
}

// 切换状态
const handleToggleStatus = async (row: BriefTemplate) => {
  try {
    const newStatus = row.status === 1 ? 0 : 1
    await briefTemplateApi.update(row.id, { status: newStatus })
    ElMessage.success(newStatus === 1 ? '启用成功' : '禁用成功')
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

// 删除
const handleDelete = async (row: BriefTemplate) => {
  try {
    await ElMessageBox.confirm('确定要删除该简报模板吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await briefTemplateApi.delete(row.id)
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
      const data: BriefTemplateFormData = {
        template_code: formData.template_code,
        template_name: formData.template_name,
        template_type: formData.template_type,
        industry_type: formData.industry_type,
        time_dimension: formData.time_dimension,
        region_dimension: formData.region_dimension,
        industry_dimension: formData.industry_dimension,
        template_content: formData.template_content,
        variables: formData.variables,
        data_config: formData.data_config,
        status: formData.status,
        description: formData.description,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        await briefTemplateApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await briefTemplateApi.create(data)
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
    template_code: '',
    template_name: '',
    template_type: 1,
    industry_type: null,
    time_dimension: null,
    region_dimension: null,
    industry_dimension: null,
    template_content: '',
    variables: null,
    data_config: null,
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

// 获取时间维度显示
const getTimeDimensionDisplay = (dimension: string | null | undefined) => {
  if (!dimension) return '-'
  const dimensionMap: Record<string, string> = {
    day: '日',
    week: '周',
    month: '月',
    year: '年',
  }
  return dimensionMap[dimension] || dimension
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.template-list {
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

  .template-content-preview {
    background: #f5f7fa;
    padding: 10px;
    border-radius: 4px;
    font-size: 14px;
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 300px;
    overflow: auto;
    margin: 0;
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
