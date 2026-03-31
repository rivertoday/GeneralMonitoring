<template>
  <div class="template-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>消息模板管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增模板
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="模板类型">
          <el-select v-model="searchForm.template_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="系统消息" :value="1" />
            <el-option label="短信" :value="2" />
            <el-option label="邮件" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="消息类型">
          <el-select v-model="searchForm.message_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="预警通知" :value="1" />
            <el-option label="报警通知" :value="2" />
            <el-option label="简报推送" :value="3" />
            <el-option label="叫应通知" :value="4" />
            <el-option label="其他" :value="5" />
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
            placeholder="请输入模板编码/名称/内容"
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
        <el-table-column prop="template_code" label="模板编码" width="180" />
        <el-table-column prop="template_name" label="模板名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="template_type_display" label="模板类型" width="100" />
        <el-table-column prop="message_type_display" label="消息类型" width="100" />
        <el-table-column prop="subject" label="消息主题" min-width="150" show-overflow-tooltip />
        <el-table-column label="消息内容" min-width="200" show-overflow-tooltip>
          <template #default="{ row }">
            <span v-if="row.content && row.content.length > 50">
              {{ row.content.substring(0, 50) }}...
            </span>
            <span v-else>{{ row.content || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="操作" width="250" fixed="right">
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
            <el-form-item label="模板编码" prop="template_code">
              <el-input v-model="formData.template_code" placeholder="留空则自动生成" :disabled="isEdit" />
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
              <el-select v-model="formData.template_type" placeholder="请选择" style="width: 100%" @change="handleTemplateTypeChange">
                <el-option label="系统消息" :value="1" />
                <el-option label="短信" :value="2" />
                <el-option label="邮件" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="消息类型" prop="message_type">
              <el-select v-model="formData.message_type" placeholder="请选择" style="width: 100%">
                <el-option label="预警通知" :value="1" />
                <el-option label="报警通知" :value="2" />
                <el-option label="简报推送" :value="3" />
                <el-option label="叫应通知" :value="4" />
                <el-option label="其他" :value="5" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <!-- 邮件类型需要显示主题 -->
        <el-form-item v-if="formData.template_type === 3" label="消息主题">
          <el-input v-model="formData.subject" placeholder="请输入消息主题" />
        </el-form-item>
        <el-form-item label="消息内容" prop="content">
          <el-input
            v-model="formData.content"
            type="textarea"
            :rows="6"
            placeholder="请输入消息内容，支持变量占位符，如：{变量名}"
          />
          <div style="margin-top: 5px; color: #909399; font-size: 12px">
            提示：使用 {变量名} 作为占位符，例如：{user_name}、{event_name} 等
          </div>
        </el-form-item>
        <el-form-item label="变量说明">
          <el-input
            v-model="formData.variables"
            type="textarea"
            :rows="4"
            placeholder='请输入JSON格式的变量说明，如：{"user_name":"用户名","event_name":"事件名称"}'
          />
          <div style="margin-top: 5px; color: #909399; font-size: 12px">
            提示：JSON格式，用于说明模板中可用的变量及其含义
          </div>
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="formData.status" placeholder="请选择状态" style="width: 100%">
                <el-option label="启用" :value="1" />
                <el-option label="禁用" :value="0" />
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
    <el-dialog v-model="detailVisible" title="消息模板详情" width="900px">
      <el-descriptions :column="2" border v-if="currentRow">
        <el-descriptions-item label="模板编码">{{ currentRow.template_code }}</el-descriptions-item>
        <el-descriptions-item label="模板名称">{{ currentRow.template_name }}</el-descriptions-item>
        <el-descriptions-item label="模板类型">
          <el-tag :type="getTemplateTypeTagType(currentRow.template_type)">
            {{ currentRow.template_type_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="消息类型">
          <el-tag :type="getMessageTypeTagType(currentRow.message_type)">
            {{ currentRow.message_type_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow.subject" label="消息主题" :span="2">
          {{ currentRow.subject }}
        </el-descriptions-item>
        <el-descriptions-item label="消息内容" :span="2">
          <pre style="white-space: pre-wrap; word-wrap: break-word; margin: 0">{{ currentRow.content }}</pre>
        </el-descriptions-item>
        <el-descriptions-item label="变量说明" :span="2">
          <pre v-if="currentRow.variables_dict" style="white-space: pre-wrap; word-wrap: break-word; margin: 0">
            {{ JSON.stringify(currentRow.variables_dict, null, 2) }}
          </pre>
          <span v-else>{{ currentRow.variables || '-' }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow.status === 1 ? 'success' : 'danger'">
            {{ currentRow.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="模板描述" :span="2">{{ currentRow.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { messageTemplateApi } from '@/api/modules/system'
import type { MessageTemplate, MessageTemplateFormData, TemplateType, MessageType, Status } from '@/types/modules/system'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<MessageTemplate[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive({
  template_type: undefined as TemplateType | undefined,
  message_type: undefined as MessageType | undefined,
  status: undefined as Status | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增模板')
const currentRow = ref<MessageTemplate | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<MessageTemplateFormData>({
  template_code: '',
  template_name: '',
  template_type: 1,
  message_type: 1,
  subject: null,
  content: '',
  variables: null,
  status: 1,
  description: null,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  template_name: [
    { required: true, message: '请输入模板名称', trigger: 'blur' },
  ],
  template_type: [
    { required: true, message: '请选择模板类型', trigger: 'change' },
  ],
  message_type: [
    { required: true, message: '请选择消息类型', trigger: 'change' },
  ],
  content: [
    { required: true, message: '请输入消息内容', trigger: 'blur' },
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' },
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
    const response = await messageTemplateApi.getList(params)
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
    message_type: undefined,
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
const handleEdit = async (row: MessageTemplate) => {
  isEdit.value = true
  dialogTitle.value = '编辑模板'
  currentRow.value = row
  
  try {
    const detail = await messageTemplateApi.getDetail(row.id)
    Object.assign(formData, {
      template_code: detail.template_code,
      template_name: detail.template_name,
      template_type: detail.template_type,
      message_type: detail.message_type,
      subject: detail.subject,
      content: detail.content,
      variables: detail.variables,
      status: detail.status,
      description: detail.description,
      remark: detail.remark,
    })
    dialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取模板详情失败')
  }
}

// 查看
const handleView = async (row: MessageTemplate) => {
  try {
    const detail = await messageTemplateApi.getDetail(row.id)
    currentRow.value = detail
    detailVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取模板详情失败')
  }
}

// 删除
const handleDelete = async (row: MessageTemplate) => {
  try {
    await ElMessageBox.confirm('确定要删除该消息模板吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await messageTemplateApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 模板类型变化
const handleTemplateTypeChange = () => {
  // 如果切换到非邮件类型，清空主题
  if (formData.template_type !== 3) {
    formData.subject = null
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const data: MessageTemplateFormData = {
        template_name: formData.template_name,
        template_type: formData.template_type,
        message_type: formData.message_type,
        subject: formData.subject,
        content: formData.content,
        variables: formData.variables,
        status: formData.status,
        description: formData.description,
        remark: formData.remark,
      }
      
      if (isEdit.value && currentRow.value) {
        if (formData.template_code) {
          data.template_code = formData.template_code
        }
        await messageTemplateApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        if (formData.template_code) {
          data.template_code = formData.template_code
        }
        await messageTemplateApi.create(data)
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
    message_type: 1,
    subject: null,
    content: '',
    variables: null,
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

// 获取模板类型标签类型
const getTemplateTypeTagType = (type: TemplateType) => {
  const typeMap: Record<TemplateType, string> = {
    1: 'primary', // 系统消息
    2: 'success', // 短信
    3: 'warning', // 邮件
  }
  return typeMap[type] || 'info'
}

// 获取消息类型标签类型
const getMessageTypeTagType = (type: MessageType) => {
  const typeMap: Record<MessageType, string> = {
    1: 'warning', // 预警通知
    2: 'danger', // 报警通知
    3: 'info', // 简报推送
    4: 'primary', // 叫应通知
    5: '', // 其他
  }
  return typeMap[type] || 'info'
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
}
</style>
