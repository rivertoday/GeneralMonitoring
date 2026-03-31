<template>
  <div class="person-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>叫应人员管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增叫应人员
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="所属分组">
          <el-select v-model="searchForm.group_id" placeholder="请选择" clearable style="width: 150px">
            <el-option
              v-for="group in groupOptions"
              :key="group.id"
              :label="group.group_name"
              :value="group.id"
            />
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
            placeholder="请输入人员编码/姓名/手机号"
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
        <el-table-column prop="person_code" label="人员编码" width="150" />
        <el-table-column prop="person_name" label="人员姓名" width="120" />
        <el-table-column prop="group_name" label="所属分组" width="150" />
        <el-table-column prop="rank" label="职级" width="100" />
        <el-table-column prop="mobile_phone" label="手机号码" width="130" />
        <el-table-column prop="office_phone" label="办公电话" width="130" />
        <el-table-column prop="contact_address" label="通讯地址" min-width="200" show-overflow-tooltip />
        <el-table-column prop="event_level_display" label="事件级别" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.event_level" :type="getEventLevelTagType(row.event_level)">
              {{ row.event_level_display }}
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
            <el-form-item label="人员编码" prop="person_code">
              <el-input v-model="formData.person_code" placeholder="请输入人员编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="人员姓名" prop="person_name">
              <el-input v-model="formData.person_name" placeholder="请输入人员姓名" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所属分组">
              <el-select v-model="formData.group_id" placeholder="请选择" clearable style="width: 100%">
                <el-option
                  v-for="group in groupOptions"
                  :key="group.id"
                  :label="group.group_name"
                  :value="group.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="职级">
              <el-input v-model="formData.rank" placeholder="请输入职级" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号码" prop="mobile_phone">
              <el-input v-model="formData.mobile_phone" placeholder="请输入手机号码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="办公电话">
              <el-input v-model="formData.office_phone" placeholder="请输入办公电话" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="事件级别">
              <el-select v-model="formData.event_level" placeholder="请选择" clearable style="width: 100%">
                <el-option label="红色I级" :value="1" />
                <el-option label="橙色Ⅱ级" :value="2" />
                <el-option label="黄色Ⅲ级" :value="3" />
                <el-option label="蓝色Ⅳ级" :value="4" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属组织ID">
              <el-input-number
                v-model="formData.organization_id"
                :min="1"
                placeholder="请输入所属组织ID"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="通讯地址">
          <el-input v-model="formData.contact_address" placeholder="请输入通讯地址" />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="状态">
              <el-radio-group v-model="formData.status">
                <el-radio :label="1">启用</el-radio>
                <el-radio :label="0">禁用</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入描述"
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
    <el-dialog v-model="detailVisible" title="叫应人员详情" width="800px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="人员编码">{{ currentRow?.person_code }}</el-descriptions-item>
        <el-descriptions-item label="人员姓名">{{ currentRow?.person_name }}</el-descriptions-item>
        <el-descriptions-item label="所属分组">{{ currentRow?.group_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="职级">{{ currentRow?.rank || '-' }}</el-descriptions-item>
        <el-descriptions-item label="手机号码">{{ currentRow?.mobile_phone }}</el-descriptions-item>
        <el-descriptions-item label="办公电话">{{ currentRow?.office_phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="通讯地址" :span="2">{{ currentRow?.contact_address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="事件级别">
          <el-tag v-if="currentRow?.event_level" :type="getEventLevelTagType(currentRow.event_level)">
            {{ currentRow.event_level_display }}
          </el-tag>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="所属组织ID">{{ currentRow?.organization_id || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'info'">
            {{ currentRow?.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
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
import { callPersonApi, callGroupApi } from '@/api/modules/call'
import type { CallPerson, CallPersonListParams, CallPersonFormData, EventLevel, CallGroup } from '@/types/modules/call'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<CallPerson[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 分组选项（需要从API获取，这里先使用空数组）
const groupOptions = ref<Array<{ id: number; group_name: string }>>([])

// 搜索表单
const searchForm = reactive<CallPersonListParams>({
  group_id: undefined,
  event_level: undefined,
  status: undefined,
  search: undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增叫应人员')
const currentRow = ref<CallPerson | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<CallPersonFormData>({
  person_code: '',
  person_name: '',
  group_id: null,
  rank: null,
  mobile_phone: '',
  office_phone: null,
  contact_address: null,
  event_level: null,
  organization_id: null,
  description: null,
  status: 1,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  person_code: [
    { required: true, message: '请输入人员编码', trigger: 'blur' },
  ],
  person_name: [
    { required: true, message: '请输入人员姓名', trigger: 'blur' },
  ],
  mobile_phone: [
    { required: true, message: '请输入手机号码', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' },
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

// 获取分组列表
const fetchGroups = async () => {
  try {
    const response = await callGroupApi.getList({ page_size: 1000, status: 1 })
    groupOptions.value = response.results.map((g: CallGroup) => ({ id: g.id, group_name: g.group_name }))
  } catch (error: any) {
    console.error('获取分组列表失败:', error)
  }
}

// 获取列表数据
const fetchData = async () => {
  loading.value = true
  try {
    const params: CallPersonListParams = {
      page: pagination.page,
      page_size: pagination.pageSize,
      ...searchForm,
    }
    const response = await callPersonApi.getList(params)
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
    group_id: undefined,
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
  dialogTitle.value = '新增叫应人员'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: CallPerson) => {
  isEdit.value = true
  dialogTitle.value = '编辑叫应人员'
  currentRow.value = row
  Object.assign(formData, {
    person_code: row.person_code,
    person_name: row.person_name,
    group_id: row.group_id,
    rank: row.rank,
    mobile_phone: row.mobile_phone,
    office_phone: row.office_phone,
    contact_address: row.contact_address,
    event_level: row.event_level,
    organization_id: row.organization_id,
    description: row.description,
    status: row.status,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: CallPerson) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: CallPerson) => {
  try {
    await ElMessageBox.confirm('确定要删除该叫应人员吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await callPersonApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 更新状态
const handleUpdateStatus = async (row: CallPerson) => {
  try {
    const newStatus: 0 | 1 = row.status === 1 ? 0 : 1
    await callPersonApi.partialUpdate(row.id, { status: newStatus })
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
      await callPersonApi.update(currentRow.value.id, formData)
      ElMessage.success('更新成功')
    } else {
      await callPersonApi.create(formData)
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
    person_code: '',
    person_name: '',
    group_id: null,
    rank: null,
    mobile_phone: '',
    office_phone: null,
    contact_address: null,
    event_level: null,
    organization_id: null,
    description: null,
    status: 1,
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
  fetchGroups()
  fetchData()
})
</script>

<style scoped lang="scss">
.person-list {
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
