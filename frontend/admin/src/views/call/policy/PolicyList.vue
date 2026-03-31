<template>
  <div class="policy-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>政策文件管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增政策文件
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="文件类型">
          <el-input
            v-model="searchForm.file_type"
            placeholder="请输入文件类型"
            clearable
            style="width: 150px"
          />
        </el-form-item>
        <el-form-item label="发布状态">
          <el-select v-model="searchForm.publish_status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="未发布" :value="0" />
            <el-option label="已发布" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="上传时间">
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
            placeholder="请输入文件编码/名称/政策标题"
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
        <el-table-column prop="file_code" label="文件编码" width="150" />
        <el-table-column prop="file_name" label="文件名称" width="200" show-overflow-tooltip />
        <el-table-column prop="policy_title" label="政策标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="file_type" label="文件类型" width="100" />
        <el-table-column label="文件大小" width="120">
          <template #default="{ row }">
            <span v-if="row.file_size">{{ formatFileSize(row.file_size) }}</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="upload_user_name" label="上传人" width="120" />
        <el-table-column prop="upload_time" label="上传时间" width="160" />
        <el-table-column label="发布状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.publish_status === 1 ? 'success' : 'info'">
              {{ row.publish_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="publish_time" label="发布时间" width="160" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button
              v-if="row.publish_status === 0"
              type="success"
              link
              size="small"
              @click="handlePublish(row)"
            >
              发布
            </el-button>
            <el-button type="primary" link size="small" @click="handleDownload(row)">
              下载
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
            <el-form-item label="文件编码" prop="file_code">
              <el-input v-model="formData.file_code" placeholder="请输入文件编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="政策标题" prop="policy_title">
              <el-input v-model="formData.policy_title" placeholder="请输入政策标题" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="文件上传" prop="file">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            :limit="1"
            :file-list="fileList"
          >
            <template #trigger>
              <el-button type="primary">选择文件</el-button>
            </template>
            <template #tip>
              <div class="el-upload__tip">请上传政策文件（支持PDF、Word、Excel等格式）</div>
            </template>
          </el-upload>
          <div v-if="uploadProgress > 0 && uploadProgress < 100" class="upload-progress">
            <el-progress :percentage="uploadProgress" />
          </div>
        </el-form-item>
        <el-form-item label="政策内容">
          <el-input
            v-model="formData.policy_content"
            type="textarea"
            :rows="5"
            placeholder="请输入政策内容（文本提取）"
          />
        </el-form-item>
        <el-form-item label="政策要求">
          <el-input
            v-model="formData.policy_requirement"
            type="textarea"
            :rows="5"
            placeholder="请输入政策要求"
          />
        </el-form-item>
        <el-form-item label="文件描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入文件描述"
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
    <el-dialog v-model="detailVisible" title="政策文件详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="文件编码">{{ currentRow?.file_code }}</el-descriptions-item>
        <el-descriptions-item label="文件名称">{{ currentRow?.file_name }}</el-descriptions-item>
        <el-descriptions-item label="政策标题">{{ currentRow?.policy_title }}</el-descriptions-item>
        <el-descriptions-item label="文件类型">{{ currentRow?.file_type || '-' }}</el-descriptions-item>
        <el-descriptions-item label="文件大小">
          {{ currentRow?.file_size ? formatFileSize(currentRow.file_size) : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="文件扩展名">{{ currentRow?.file_ext || '-' }}</el-descriptions-item>
        <el-descriptions-item label="上传人">{{ currentRow?.upload_user_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="上传时间">{{ currentRow?.upload_time }}</el-descriptions-item>
        <el-descriptions-item label="发布状态">
          <el-tag :type="currentRow?.publish_status === 1 ? 'success' : 'info'">
            {{ currentRow?.publish_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="发布时间">{{ currentRow?.publish_time || '-' }}</el-descriptions-item>
        <el-descriptions-item label="政策内容" :span="2">{{ currentRow?.policy_content || '-' }}</el-descriptions-item>
        <el-descriptions-item label="政策要求" :span="2">{{ currentRow?.policy_requirement || '-' }}</el-descriptions-item>
        <el-descriptions-item label="文件描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 发布对话框 -->
    <el-dialog v-model="publishVisible" title="发布政策文件" width="500px">
      <el-form ref="publishFormRef" :model="publishData" label-width="120px">
        <el-form-item label="发布时间">
          <el-date-picker
            v-model="publishData.publish_time"
            type="datetime"
            placeholder="选择发布时间（不选则使用当前时间）"
            value-format="YYYY-MM-DD HH:mm:ss"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="publishVisible = false">取消</el-button>
        <el-button type="primary" :loading="publishLoading" @click="handlePublishConfirm">
          确定发布
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules, type UploadFile, type UploadFiles } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { policyFileApi } from '@/api/modules/call'
import type { PolicyFile, PolicyFileListParams, PolicyFileFormData, PolicyFilePublishData } from '@/types/modules/call'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)
const publishLoading = ref(false)

// 表格数据
const tableData = ref<PolicyFile[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive<PolicyFileListParams>({
  file_type: undefined,
  publish_status: undefined,
  start_time: undefined,
  end_time: undefined,
  search: undefined,
})

// 日期范围
const dateRange = ref<[string, string] | null>(null)

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const publishVisible = ref(false)
const dialogTitle = ref('新增政策文件')
const currentRow = ref<PolicyFile | null>(null)
const publishRow = ref<PolicyFile | null>(null)
const isEdit = ref(false)

// 文件上传
const uploadRef = ref()
const fileList = ref<UploadFile[]>([])
const uploadProgress = ref(0)
const currentFile = ref<File | null>(null)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<PolicyFileFormData>({
  file_code: '',
  file_name: '',
  file_path: '',
  file_size: null,
  file_type: null,
  file_ext: null,
  policy_title: '',
  policy_content: null,
  policy_requirement: null,
  description: null,
  remark: null,
})

// 发布表单
const publishFormRef = ref<FormInstance>()
const publishData = reactive<PolicyFilePublishData>({
  publish_time: null,
})

// 表单验证规则
const formRules: FormRules = {
  file_code: [
    { required: true, message: '请输入文件编码', trigger: 'blur' },
  ],
  policy_title: [
    { required: true, message: '请输入政策标题', trigger: 'blur' },
  ],
  file: [
    { required: true, message: '请上传文件', trigger: 'change' },
  ],
}

// 格式化文件大小
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

// 文件变化
const handleFileChange = (file: UploadFile) => {
  currentFile.value = file.raw as File
  if (currentFile.value) {
    formData.file_name = currentFile.value.name
    const ext = currentFile.value.name.split('.').pop()?.toLowerCase() || ''
    formData.file_ext = ext
    // 根据扩展名判断文件类型
    const typeMap: Record<string, string> = {
      pdf: 'PDF',
      doc: 'Word',
      docx: 'Word',
      xls: 'Excel',
      xlsx: 'Excel',
      txt: '文本',
    }
    formData.file_type = typeMap[ext] || '其他'
  }
}

// 文件移除
const handleFileRemove = () => {
  currentFile.value = null
  formData.file_name = ''
  formData.file_path = ''
  formData.file_size = null
  formData.file_type = null
  formData.file_ext = null
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
    const params: PolicyFileListParams = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm,
    }
    const response = await policyFileApi.getList(params)
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
    file_type: undefined,
    publish_status: undefined,
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

// 新增
const handleCreate = () => {
  isEdit.value = false
  dialogTitle.value = '新增政策文件'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: PolicyFile) => {
  isEdit.value = true
  dialogTitle.value = '编辑政策文件'
  currentRow.value = row
  Object.assign(formData, {
    file_code: row.file_code,
    file_name: row.file_name,
    file_path: row.file_path,
    file_size: row.file_size,
    file_type: row.file_type,
    file_ext: row.file_ext,
    policy_title: row.policy_title,
    policy_content: row.policy_content,
    policy_requirement: row.policy_requirement,
    description: row.description,
    remark: row.remark,
  })
  // 编辑时不需要重新上传文件
  fileList.value = []
  currentFile.value = null
  dialogVisible.value = true
}

// 查看
const handleView = (row: PolicyFile) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: PolicyFile) => {
  try {
    await ElMessageBox.confirm('确定要删除该政策文件吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await policyFileApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 发布
const handlePublish = (row: PolicyFile) => {
  publishRow.value = row
  publishData.publish_time = null
  publishVisible.value = true
}

// 确认发布
const handlePublishConfirm = async () => {
  if (!publishRow.value) return
  try {
    publishLoading.value = true
    await policyFileApi.publish(publishRow.value.id, publishData)
    ElMessage.success('发布成功')
    publishVisible.value = false
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '发布失败')
  } finally {
    publishLoading.value = false
  }
}

// 下载
const handleDownload = async (row: PolicyFile) => {
  try {
    // 这里需要根据实际的文件下载接口调整
    // 假设后端提供了文件下载接口
    const downloadUrl = `${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'}${import.meta.env.VITE_API_PREFIX || '/api/v1'}${row.file_path}`
    window.open(downloadUrl, '_blank')
  } catch (error: any) {
    ElMessage.error(error.message || '下载失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    
    // 如果是新增且有文件，需要先上传文件
    if (!isEdit.value && currentFile.value) {
      submitLoading.value = true
      uploadProgress.value = 0
      
      try {
        const uploadResult = await policyFileApi.upload(
          currentFile.value,
          (progressEvent) => {
            if (progressEvent.total) {
              uploadProgress.value = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            }
          }
        )
        
        // 使用上传结果填充文件信息
        formData.file_path = uploadResult.file_path
        formData.file_name = uploadResult.file_name
        formData.file_size = uploadResult.file_size
        formData.file_type = uploadResult.file_type
        formData.file_ext = uploadResult.file_ext
      } catch (error: any) {
        ElMessage.error(error.message || '文件上传失败')
        return
      } finally {
        uploadProgress.value = 0
      }
    }
    
    submitLoading.value = true
    if (isEdit.value && currentRow.value) {
      await policyFileApi.update(currentRow.value.id, formData)
      ElMessage.success('更新成功')
    } else {
      await policyFileApi.create(formData)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchData()
  } catch (error: any) {
    if (error !== false) {
      ElMessage.error(error.message || '操作失败')
    }
  } finally {
    submitLoading.value = false
  }
}

// 重置表单
const resetForm = () => {
  Object.assign(formData, {
    file_code: '',
    file_name: '',
    file_path: '',
    file_size: null,
    file_type: null,
    file_ext: null,
    policy_title: '',
    policy_content: null,
    policy_requirement: null,
    description: null,
    remark: null,
  })
  fileList.value = []
  currentFile.value = null
  uploadProgress.value = 0
  formRef.value?.clearValidate()
  currentRow.value = null
}

// 对话框关闭
const handleDialogClose = () => {
  resetForm()
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.policy-list {
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

  .upload-progress {
    margin-top: 10px;
  }
}
</style>
