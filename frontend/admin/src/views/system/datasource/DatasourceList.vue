<template>
  <div class="datasource-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>数据源管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增数据源
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="数据源类型">
          <el-select v-model="searchForm.source_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="API接口" :value="1" />
            <el-option label="数据库" :value="2" />
            <el-option label="文件" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="行业类型">
          <el-select v-model="searchForm.industry_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="气象" :value="1" />
            <el-option label="危化" :value="2" />
            <el-option label="防汛" :value="3" />
            <el-option label="交通运输" :value="4" />
            <el-option label="森林火灾" :value="5" />
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
            placeholder="请输入数据源编码/名称"
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
        <el-table-column prop="source_code" label="数据源编码" width="150" />
        <el-table-column prop="source_name" label="数据源名称" min-width="150" show-overflow-tooltip />
        <el-table-column prop="source_type_display" label="数据源类型" width="100" />
        <el-table-column prop="industry_type_display" label="行业类型" width="100" />
        <el-table-column label="连接信息" min-width="200" show-overflow-tooltip>
          <template #default="{ row }">
            <span v-if="row.source_type === 1">{{ row.api_url || '-' }}</span>
            <span v-else-if="row.source_type === 2">{{ row.db_host ? `${row.db_host}:${row.db_port || ''}/${row.db_name || ''}` : '-' }}</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="同步间隔" width="100" align="center">
          <template #default="{ row }">
            {{ row.sync_interval ? `${row.sync_interval}分钟` : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="last_sync_at" label="最后同步时间" width="160" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="success" link size="small" @click="handleSync(row)">
              同步
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
            <el-form-item label="数据源编码" prop="source_code">
              <el-input v-model="formData.source_code" placeholder="留空则自动生成" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="数据源名称" prop="source_name">
              <el-input v-model="formData.source_name" placeholder="请输入数据源名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="数据源类型" prop="source_type">
              <el-select v-model="formData.source_type" placeholder="请选择" style="width: 100%" @change="handleSourceTypeChange">
                <el-option label="API接口" :value="1" />
                <el-option label="数据库" :value="2" />
                <el-option label="文件" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="行业类型" prop="industry_type">
              <el-select v-model="formData.industry_type" placeholder="请选择" style="width: 100%">
                <el-option label="气象" :value="1" />
                <el-option label="危化" :value="2" />
                <el-option label="防汛" :value="3" />
                <el-option label="交通运输" :value="4" />
                <el-option label="森林火灾" :value="5" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- API接口类型字段 -->
        <template v-if="formData.source_type === 1">
          <el-form-item label="API接口地址" prop="api_url">
            <el-input v-model="formData.api_url" placeholder="请输入API接口地址" />
          </el-form-item>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="HTTP方法">
                <el-select v-model="formData.api_method" placeholder="请选择" style="width: 100%">
                  <el-option label="GET" value="GET" />
                  <el-option label="POST" value="POST" />
                  <el-option label="PUT" value="PUT" />
                  <el-option label="DELETE" value="DELETE" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="同步间隔（分钟）">
                <el-input-number v-model="formData.sync_interval" :min="1" style="width: 100%" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="API请求参数">
            <el-input
              v-model="formData.api_params"
              type="textarea"
              :rows="4"
              placeholder='请输入JSON格式的请求参数，如：{"key1":"value1","key2":"value2"}'
            />
          </el-form-item>
        </template>

        <!-- 数据库类型字段 -->
        <template v-if="formData.source_type === 2">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="数据库主机" prop="db_host">
                <el-input v-model="formData.db_host" placeholder="请输入数据库主机地址" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="数据库端口">
                <el-input-number v-model="formData.db_port" :min="1" :max="65535" style="width: 100%" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="数据库名称" prop="db_name">
                <el-input v-model="formData.db_name" placeholder="请输入数据库名称" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="数据表名" prop="db_table">
                <el-input v-model="formData.db_table" placeholder="请输入数据表名" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="数据库用户名" prop="db_user">
                <el-input v-model="formData.db_user" placeholder="请输入数据库用户名" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="数据库密码">
                <el-input
                  v-model="formData.db_password"
                  type="password"
                  placeholder="请输入数据库密码"
                  show-password
                />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="同步间隔（分钟）">
            <el-input-number v-model="formData.sync_interval" :min="1" style="width: 100%" />
          </el-form-item>
        </template>

        <!-- 文件类型字段 -->
        <template v-if="formData.source_type === 3">
          <el-form-item label="同步间隔（分钟）">
            <el-input-number v-model="formData.sync_interval" :min="1" style="width: 100%" />
          </el-form-item>
        </template>

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
        <el-form-item label="数据源描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入数据源描述"
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
    <el-dialog v-model="detailVisible" title="数据源详情" width="900px">
      <el-descriptions :column="2" border v-if="currentRow">
        <el-descriptions-item label="数据源编码">{{ currentRow.source_code }}</el-descriptions-item>
        <el-descriptions-item label="数据源名称">{{ currentRow.source_name }}</el-descriptions-item>
        <el-descriptions-item label="数据源类型">
          <el-tag :type="getSourceTypeTagType(currentRow.source_type)">
            {{ currentRow.source_type_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="行业类型">
          <el-tag>{{ currentRow.industry_type_display }}</el-tag>
        </el-descriptions-item>
        <template v-if="currentRow.source_type === 1">
          <el-descriptions-item label="API接口地址">{{ currentRow.api_url || '-' }}</el-descriptions-item>
          <el-descriptions-item label="HTTP方法">{{ currentRow.api_method || '-' }}</el-descriptions-item>
          <el-descriptions-item label="API请求参数" :span="2">
            <pre v-if="currentRow.api_params_dict">{{ JSON.stringify(currentRow.api_params_dict, null, 2) }}</pre>
            <span v-else>{{ currentRow.api_params || '-' }}</span>
          </el-descriptions-item>
        </template>
        <template v-if="currentRow.source_type === 2">
          <el-descriptions-item label="数据库主机">{{ currentRow.db_host || '-' }}</el-descriptions-item>
          <el-descriptions-item label="数据库端口">{{ currentRow.db_port || '-' }}</el-descriptions-item>
          <el-descriptions-item label="数据库名称">{{ currentRow.db_name || '-' }}</el-descriptions-item>
          <el-descriptions-item label="数据表名">{{ currentRow.db_table || '-' }}</el-descriptions-item>
          <el-descriptions-item label="数据库用户名">{{ currentRow.db_user || '-' }}</el-descriptions-item>
          <el-descriptions-item label="数据库密码">******</el-descriptions-item>
        </template>
        <el-descriptions-item label="同步间隔">
          {{ currentRow.sync_interval ? `${currentRow.sync_interval}分钟` : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="最后同步时间">{{ currentRow.last_sync_at || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow.status === 1 ? 'success' : 'danger'">
            {{ currentRow.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="数据源描述" :span="2">{{ currentRow.description || '-' }}</el-descriptions-item>
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
import { datasourceApi } from '@/api/modules/system'
import type { DataSource, DataSourceFormData, SourceType, IndustryType, Status } from '@/types/modules/system'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<DataSource[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive({
  source_type: undefined as SourceType | undefined,
  industry_type: undefined as IndustryType | undefined,
  status: undefined as Status | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增数据源')
const currentRow = ref<DataSource | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<DataSourceFormData>({
  source_code: '',
  source_name: '',
  source_type: 1,
  industry_type: 1,
  api_url: null,
  api_method: 'GET',
  api_params: null,
  db_host: null,
  db_port: null,
  db_name: null,
  db_user: null,
  db_password: null,
  db_table: null,
  sync_interval: 60,
  status: 1,
  description: null,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  source_name: [
    { required: true, message: '请输入数据源名称', trigger: 'blur' },
  ],
  source_type: [
    { required: true, message: '请选择数据源类型', trigger: 'change' },
  ],
  industry_type: [
    { required: true, message: '请选择行业类型', trigger: 'change' },
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' },
  ],
  api_url: [
    {
      required: true,
      message: '请输入API接口地址',
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (formData.source_type === 1 && !value) {
          callback(new Error('请输入API接口地址'))
        } else {
          callback()
        }
      },
    },
  ],
  db_host: [
    {
      required: true,
      message: '请输入数据库主机',
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (formData.source_type === 2 && !value) {
          callback(new Error('请输入数据库主机'))
        } else {
          callback()
        }
      },
    },
  ],
  db_name: [
    {
      required: true,
      message: '请输入数据库名称',
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (formData.source_type === 2 && !value) {
          callback(new Error('请输入数据库名称'))
        } else {
          callback()
        }
      },
    },
  ],
  db_table: [
    {
      required: true,
      message: '请输入数据表名',
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (formData.source_type === 2 && !value) {
          callback(new Error('请输入数据表名'))
        } else {
          callback()
        }
      },
    },
  ],
  db_user: [
    {
      required: true,
      message: '请输入数据库用户名',
      trigger: 'blur',
      validator: (rule, value, callback) => {
        if (formData.source_type === 2 && !value) {
          callback(new Error('请输入数据库用户名'))
        } else {
          callback()
        }
      },
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
    const response = await datasourceApi.getList(params)
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
    source_type: undefined,
    industry_type: undefined,
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
  dialogTitle.value = '新增数据源'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = async (row: DataSource) => {
  isEdit.value = true
  dialogTitle.value = '编辑数据源'
  currentRow.value = row
  
  try {
    const detail = await datasourceApi.getDetail(row.id)
    Object.assign(formData, {
      source_code: detail.source_code,
      source_name: detail.source_name,
      source_type: detail.source_type,
      industry_type: detail.industry_type,
      api_url: detail.api_url,
      api_method: detail.api_method || 'GET',
      api_params: detail.api_params,
      db_host: detail.db_host,
      db_port: detail.db_port,
      db_name: detail.db_name,
      db_user: detail.db_user,
      db_password: '', // 编辑时不显示密码
      db_table: detail.db_table,
      sync_interval: detail.sync_interval || 60,
      status: detail.status,
      description: detail.description,
      remark: detail.remark,
    })
    dialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取数据源详情失败')
  }
}

// 查看
const handleView = async (row: DataSource) => {
  try {
    const detail = await datasourceApi.getDetail(row.id)
    currentRow.value = detail
    detailVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取数据源详情失败')
  }
}

// 同步
const handleSync = async (row: DataSource) => {
  try {
    submitLoading.value = true
    await datasourceApi.sync(row.id)
    ElMessage.success('同步成功')
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '同步失败')
  } finally {
    submitLoading.value = false
  }
}

// 删除
const handleDelete = async (row: DataSource) => {
  try {
    await ElMessageBox.confirm('确定要删除该数据源吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await datasourceApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 数据源类型变化
const handleSourceTypeChange = () => {
  // 切换数据源类型时，清空相关字段
  if (formData.source_type === 1) {
    // API类型：清空数据库字段
    formData.db_host = null
    formData.db_port = null
    formData.db_name = null
    formData.db_user = null
    formData.db_password = null
    formData.db_table = null
  } else if (formData.source_type === 2) {
    // 数据库类型：清空API字段
    formData.api_url = null
    formData.api_method = 'GET'
    formData.api_params = null
  } else {
    // 文件类型：清空所有字段
    formData.api_url = null
    formData.api_method = 'GET'
    formData.api_params = null
    formData.db_host = null
    formData.db_port = null
    formData.db_name = null
    formData.db_user = null
    formData.db_password = null
    formData.db_table = null
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const data: DataSourceFormData = {
        source_name: formData.source_name,
        source_type: formData.source_type,
        industry_type: formData.industry_type,
        api_url: formData.api_url,
        api_method: formData.api_method,
        api_params: formData.api_params,
        db_host: formData.db_host,
        db_port: formData.db_port,
        db_name: formData.db_name,
        db_user: formData.db_user,
        db_password: formData.db_password || undefined, // 如果为空则不传
        db_table: formData.db_table,
        sync_interval: formData.sync_interval,
        status: formData.status,
        description: formData.description,
        remark: formData.remark,
      }
      
      if (isEdit.value && currentRow.value) {
        if (!formData.source_code) {
          data.source_code = currentRow.value.source_code
        }
        // 如果密码为空，则不更新密码
        if (!formData.db_password) {
          delete data.db_password
        }
        await datasourceApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        if (formData.source_code) {
          data.source_code = formData.source_code
        }
        await datasourceApi.create(data)
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
    source_code: '',
    source_name: '',
    source_type: 1,
    industry_type: 1,
    api_url: null,
    api_method: 'GET',
    api_params: null,
    db_host: null,
    db_port: null,
    db_name: null,
    db_user: null,
    db_password: null,
    db_table: null,
    sync_interval: 60,
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

// 获取数据源类型标签类型
const getSourceTypeTagType = (type: SourceType) => {
  const typeMap: Record<SourceType, string> = {
    1: 'primary', // API接口
    2: 'success', // 数据库
    3: 'warning', // 文件
  }
  return typeMap[type] || 'info'
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.datasource-list {
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
