<template>
  <div class="group-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>叫应分组管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增叫应分组
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="分组类型">
          <el-select v-model="searchForm.group_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="常态化分组" :value="1" />
            <el-option label="非常态化分组" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="事件级别">
          <el-select v-model="searchForm.event_level" placeholder="请选择" clearable style="width: 150px">
            <el-option label="红色I级" :value="1" />
            <el-option label="橙色Ⅱ级" :value="2" />
            <el-option label="黄色Ⅲ级" :value="3" />
            <el-option label="蓝色Ⅳ级" :value="4" />
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
            placeholder="请输入分组编码/名称/描述"
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
        <el-table-column prop="group_code" label="分组编码" width="150" />
        <el-table-column prop="group_name" label="分组名称" width="150" />
        <el-table-column prop="group_type_display" label="分组类型" width="120" />
        <el-table-column prop="event_level_display" label="事件级别" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.event_level" :type="getEventLevelTagType(row.event_level)">
              {{ row.event_level_display }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="分组描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="sort_order" label="排序顺序" width="100" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'info'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button
              type="primary"
              link
              size="small"
              @click="handleUpdateStatus(row)"
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
            <el-form-item label="分组编码" prop="group_code">
              <el-input v-model="formData.group_code" placeholder="请输入分组编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="分组名称" prop="group_name">
              <el-input v-model="formData.group_name" placeholder="请输入分组名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分组类型" prop="group_type">
              <el-select v-model="formData.group_type" placeholder="请选择" style="width: 100%">
                <el-option label="常态化分组" :value="1" />
                <el-option label="非常态化分组" :value="2" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="事件级别" v-if="formData.group_type === 2">
              <el-select v-model="formData.event_level" placeholder="请选择" clearable style="width: 100%">
                <el-option label="红色I级" :value="1" />
                <el-option label="橙色Ⅱ级" :value="2" />
                <el-option label="黄色Ⅲ级" :value="3" />
                <el-option label="蓝色Ⅳ级" :value="4" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
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
          <el-col :span="12">
            <el-form-item label="状态">
              <el-radio-group v-model="formData.status">
                <el-radio :label="1">启用</el-radio>
                <el-radio :label="0">禁用</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="分组描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入分组描述"
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
    <el-dialog v-model="detailVisible" title="叫应分组详情" width="800px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="分组编码">{{ currentRow?.group_code }}</el-descriptions-item>
        <el-descriptions-item label="分组名称">{{ currentRow?.group_name }}</el-descriptions-item>
        <el-descriptions-item label="分组类型">{{ currentRow?.group_type_display }}</el-descriptions-item>
        <el-descriptions-item label="事件级别">
          <el-tag v-if="currentRow?.event_level" :type="getEventLevelTagType(currentRow.event_level)">
            {{ currentRow.event_level_display }}
          </el-tag>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="排序顺序">{{ currentRow?.sort_order }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'info'">
            {{ currentRow?.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="分组描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { callGroupApi } from '@/api/modules/call'
import type { CallGroup, CallGroupListParams, CallGroupFormData, EventLevel } from '@/types/modules/call'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<CallGroup[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive<CallGroupListParams>({
  group_type: undefined,
  event_level: undefined,
  status: undefined,
  search: undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增叫应分组')
const currentRow = ref<CallGroup | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<CallGroupFormData>({
  group_code: '',
  group_name: '',
  group_type: 1,
  event_level: null,
  description: null,
  status: 1,
  sort_order: 0,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  group_code: [
    { required: true, message: '请输入分组编码', trigger: 'blur' },
  ],
  group_name: [
    { required: true, message: '请输入分组名称', trigger: 'blur' },
  ],
  group_type: [
    { required: true, message: '请选择分组类型', trigger: 'change' },
  ],
}

// 获取事件级别标签类型
const getEventLevelTagType = (level: EventLevel): string => {
  const typeMap: Record<EventLevel, string> = {
    1: 'danger',   // 红色I级
    2: 'warning', // 橙色Ⅱ级
    3: 'warning', // 黄色Ⅲ级
    4: 'info',     // 蓝色Ⅳ级
  }
  return typeMap[level] || 'info'
}

// 监听分组类型变化，如果是常态化分组，清空事件级别
watch(() => formData.group_type, (newType) => {
  if (newType === 1) {
    formData.event_level = null
  }
})

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params: CallGroupListParams = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm,
    }
    const response = await callGroupApi.getList(params)
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
    group_type: undefined,
    event_level: undefined,
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
  dialogTitle.value = '新增叫应分组'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: CallGroup) => {
  isEdit.value = true
  dialogTitle.value = '编辑叫应分组'
  currentRow.value = row
  Object.assign(formData, {
    group_code: row.group_code,
    group_name: row.group_name,
    group_type: row.group_type,
    event_level: row.event_level,
    description: row.description,
    status: row.status,
    sort_order: row.sort_order,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: CallGroup) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: CallGroup) => {
  try {
    await ElMessageBox.confirm('确定要删除该叫应分组吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await callGroupApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 更新状态
const handleUpdateStatus = async (row: CallGroup) => {
  try {
    const newStatus: 0 | 1 = row.status === 1 ? 0 : 1
    await callGroupApi.partialUpdate(row.id, { status: newStatus })
    ElMessage.success('更新状态成功')
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '更新状态失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
    submitLoading.value = true
    if (isEdit.value && currentRow.value) {
      await callGroupApi.update(currentRow.value.id, formData)
      ElMessage.success('更新成功')
    } else {
      await callGroupApi.create(formData)
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
    group_code: '',
    group_name: '',
    group_type: 1,
    event_level: null,
    description: null,
    status: 1,
    sort_order: 0,
    remark: null,
  })
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
.group-list {
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
