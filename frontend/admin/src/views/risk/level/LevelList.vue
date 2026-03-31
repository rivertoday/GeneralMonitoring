<template>
  <div class="level-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>预警级别</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增级别
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="预警颜色">
          <el-select v-model="searchForm.level_color" placeholder="请选择" clearable style="width: 150px">
            <el-option label="红色" value="red" />
            <el-option label="橙色" value="orange" />
            <el-option label="黄色" value="yellow" />
            <el-option label="蓝色" value="blue" />
          </el-select>
        </el-form-item>
        <el-form-item label="严重程度">
          <el-select v-model="searchForm.severity" placeholder="请选择" clearable style="width: 150px">
            <el-option label="特别严重" :value="1" />
            <el-option label="严重" :value="2" />
            <el-option label="较重" :value="3" />
            <el-option label="一般" :value="4" />
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
            placeholder="请输入级别编码/名称/描述"
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
        <el-table-column prop="level_code" label="级别编码" width="120" />
        <el-table-column prop="level_name" label="级别名称" width="150" />
        <el-table-column label="预警颜色" width="120">
          <template #default="{ row }">
            <el-tag :type="getLevelTagType(row.level_color)">
              {{ row.level_color_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="严重程度" width="120">
          <template #default="{ row }">
            <span>{{ getSeverityDisplay(row.severity) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="response_org" label="响应组织要求" min-width="200" show-overflow-tooltip />
        <el-table-column label="响应时间要求" width="120">
          <template #default="{ row }">
            <span v-if="row.response_time">{{ row.response_time }}分钟</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="sort_order" label="排序顺序" width="100" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="级别描述" min-width="200" show-overflow-tooltip />
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
      width="800px"
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
            <el-form-item label="级别编码" prop="level_code">
              <el-input v-model="formData.level_code" placeholder="请输入级别编码（如：I、II、III、IV）" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="级别名称" prop="level_name">
              <el-input v-model="formData.level_name" placeholder="请输入级别名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="预警颜色" prop="level_color">
              <el-select v-model="formData.level_color" placeholder="请选择" style="width: 100%">
                <el-option label="红色" value="red" />
                <el-option label="橙色" value="orange" />
                <el-option label="黄色" value="yellow" />
                <el-option label="蓝色" value="blue" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="严重程度" prop="severity">
              <el-select v-model="formData.severity" placeholder="请选择" style="width: 100%">
                <el-option label="特别严重" :value="1" />
                <el-option label="严重" :value="2" />
                <el-option label="较重" :value="3" />
                <el-option label="一般" :value="4" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="响应组织要求">
          <el-input
            v-model="formData.response_org"
            type="textarea"
            :rows="3"
            placeholder="请输入响应组织要求（如：由高新区应急局牵头，相关行业监管部门和企事业主体单位配合）"
          />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="响应时间要求(分钟)">
              <el-input-number
                v-model="formData.response_time"
                :min="0"
                placeholder="请输入响应时间要求"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="排序顺序">
              <el-input-number
                v-model="formData.sort_order"
                :min="0"
                placeholder="请输入排序顺序"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="状态" prop="status">
          <el-select v-model="formData.status" placeholder="请选择" style="width: 100%">
            <el-option label="禁用" :value="0" />
            <el-option label="启用" :value="1" />
          </el-select>
        </el-form-item>
        <el-form-item label="级别描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入级别描述"
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
    <el-dialog v-model="detailVisible" title="预警级别详情" width="800px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="级别编码">{{ currentRow?.level_code }}</el-descriptions-item>
        <el-descriptions-item label="级别名称">{{ currentRow?.level_name }}</el-descriptions-item>
        <el-descriptions-item label="预警颜色">
          <el-tag :type="getLevelTagType(currentRow?.level_color || '')">
            {{ currentRow?.level_color_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="严重程度">
          {{ getSeverityDisplay(currentRow?.severity) }}
        </el-descriptions-item>
        <el-descriptions-item label="响应组织要求" :span="2">
          {{ currentRow?.response_org || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="响应时间要求">
          {{ currentRow?.response_time ? `${currentRow.response_time}分钟` : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="排序顺序">
          {{ currentRow?.sort_order || 0 }}
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'info'">
            {{ currentRow?.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="级别描述" :span="2">
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
import { warningLevelApi } from '@/api/modules/risk'
import type { WarningLevel } from '@/types/modules/risk'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<WarningLevel[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive({
  level_color: undefined as 'red' | 'orange' | 'yellow' | 'blue' | undefined,
  severity: undefined as 1 | 2 | 3 | 4 | undefined,
  status: undefined as 0 | 1 | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增级别')
const currentRow = ref<WarningLevel | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive({
  level_code: '',
  level_name: '',
  level_color: 'red' as 'red' | 'orange' | 'yellow' | 'blue',
  severity: 1 as 1 | 2 | 3 | 4,
  response_org: null as string | null,
  response_time: null as number | null,
  sort_order: 0,
  status: 1,
  description: null as string | null,
  remark: null as string | null,
})

// 表单验证规则
const formRules: FormRules = {
  level_code: [
    { required: true, message: '请输入级别编码', trigger: 'blur' },
  ],
  level_name: [
    { required: true, message: '请输入级别名称', trigger: 'blur' },
  ],
  level_color: [
    { required: true, message: '请选择预警颜色', trigger: 'change' },
  ],
  severity: [
    { required: true, message: '请选择严重程度', trigger: 'change' },
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
    const response = await warningLevelApi.getList(params)
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
    level_color: undefined,
    severity: undefined,
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
  dialogTitle.value = '新增级别'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: WarningLevel) => {
  isEdit.value = true
  dialogTitle.value = '编辑级别'
  currentRow.value = row
  Object.assign(formData, {
    level_code: row.level_code,
    level_name: row.level_name,
    level_color: row.level_color,
    severity: row.severity,
    response_org: row.response_org,
    response_time: row.response_time,
    sort_order: row.sort_order,
    status: row.status,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: WarningLevel) => {
  currentRow.value = row
  detailVisible.value = true
}

// 切换状态
const handleToggleStatus = async (row: WarningLevel) => {
  try {
    const newStatus = row.status === 1 ? 0 : 1
    await warningLevelApi.update(row.id, { status: newStatus })
    ElMessage.success(newStatus === 1 ? '启用成功' : '禁用成功')
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '操作失败')
  }
}

// 删除
const handleDelete = async (row: WarningLevel) => {
  try {
    await ElMessageBox.confirm('确定要删除该预警级别吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await warningLevelApi.delete(row.id)
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
        level_code: formData.level_code,
        level_name: formData.level_name,
        level_color: formData.level_color,
        severity: formData.severity,
        response_org: formData.response_org,
        response_time: formData.response_time,
        sort_order: formData.sort_order,
        status: formData.status,
        description: formData.description,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        await warningLevelApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await warningLevelApi.create(data)
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
    level_code: '',
    level_name: '',
    level_color: 'red',
    severity: 1,
    response_org: null,
    response_time: null,
    sort_order: 0,
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

// 获取严重程度显示
const getSeverityDisplay = (severity?: number) => {
  const severityMap: Record<number, string> = {
    1: '特别严重',
    2: '严重',
    3: '较重',
    4: '一般',
  }
  return severityMap[severity || 0] || '-'
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.level-list {
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
