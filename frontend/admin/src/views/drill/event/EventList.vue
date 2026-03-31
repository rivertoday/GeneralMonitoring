<template>
  <div class="event-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>演练事件</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增事件
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="事件类型">
          <el-select v-model="searchForm.event_type" placeholder="请选择" clearable style="width: 150px">
            <el-option label="火灾" :value="1" />
            <el-option label="爆炸" :value="2" />
            <el-option label="泄漏" :value="3" />
            <el-option label="坍塌" :value="4" />
            <el-option label="其他" :value="5" />
          </el-select>
        </el-form-item>
        <el-form-item label="演练状态">
          <el-select v-model="searchForm.drill_status" placeholder="请选择" clearable style="width: 150px">
            <el-option label="未开始" :value="0" />
            <el-option label="进行中" :value="1" />
            <el-option label="已完成" :value="2" />
            <el-option label="已取消" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="数据来源">
          <el-select v-model="searchForm.data_source" placeholder="请选择" clearable style="width: 150px">
            <el-option label="企业安全在线服务" :value="1" />
            <el-option label="化工园区安全智能化管控平台" :value="2" />
            <el-option label="手动录入" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入事件编码/名称"
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
        <el-table-column prop="event_code" label="事件编码" width="150" />
        <el-table-column prop="event_name" label="演练事件名称" min-width="200" show-overflow-tooltip />
        <el-table-column prop="organization_name" label="事发单位" width="150" show-overflow-tooltip />
        <el-table-column prop="event_type_display" label="事件类型" width="100" />
        <el-table-column prop="accident_type" label="事故类型" width="120" />
        <el-table-column label="演练状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusTagType(row.drill_status)">
              {{ row.drill_status_display }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="event_time" label="事发时间" width="160" />
        <el-table-column label="伤亡情况" width="120">
          <template #default="{ row }">
            <span v-if="row.death_count > 0 || row.injured_count > 0">
              死亡: {{ row.death_count }} 受伤: {{ row.injured_count }}
            </span>
            <span v-else>无</span>
          </template>
        </el-table-column>
        <el-table-column prop="data_source_display" label="数据来源" width="150" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button
              v-if="row.drill_status === 0"
              type="primary"
              link
              size="small"
              @click="handleEdit(row)"
            >
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
            <el-form-item label="事件编码" prop="event_code">
              <el-input v-model="formData.event_code" placeholder="请输入事件编码" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="演练事件名称" prop="event_name">
              <el-input v-model="formData.event_name" placeholder="请输入演练事件名称" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="事发单位ID" prop="organization_id">
              <el-input v-model="formData.organization_id" placeholder="请输入事发单位ID" type="number" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="事件类型" prop="event_type">
              <el-select v-model="formData.event_type" placeholder="请选择" style="width: 100%">
                <el-option label="火灾" :value="1" />
                <el-option label="爆炸" :value="2" />
                <el-option label="泄漏" :value="3" />
                <el-option label="坍塌" :value="4" />
                <el-option label="其他" :value="5" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="事故类型">
              <el-input v-model="formData.accident_type" placeholder="请输入事故类型（详细分类）" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="事发时间" prop="event_time">
              <el-date-picker
                v-model="formData.event_time"
                type="datetime"
                placeholder="请选择事发时间"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="经度">
              <el-input v-model="formData.longitude" placeholder="请输入经度" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="纬度">
              <el-input v-model="formData.latitude" placeholder="请输入纬度" />
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
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="受伤人数">
              <el-input-number v-model="formData.injured_count" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="死亡人数">
              <el-input-number v-model="formData.death_count" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="演练状态">
              <el-select v-model="formData.drill_status" placeholder="请选择" style="width: 100%">
                <el-option label="未开始" :value="0" />
                <el-option label="进行中" :value="1" />
                <el-option label="已完成" :value="2" />
                <el-option label="已取消" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="数据来源">
              <el-select v-model="formData.data_source" placeholder="请选择" clearable style="width: 100%">
                <el-option label="企业安全在线服务" :value="1" />
                <el-option label="化工园区安全智能化管控平台" :value="2" />
                <el-option label="手动录入" :value="3" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="关联演练计划名称">
          <el-input v-model="formData.drill_plan_name" placeholder="请输入关联演练计划名称" />
        </el-form-item>
        <el-form-item label="事故简介">
          <el-input
            v-model="formData.accident_summary"
            type="textarea"
            :rows="4"
            placeholder="请输入事故简介"
          />
        </el-form-item>
        <el-form-item label="事件描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入事件描述"
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
    <el-dialog v-model="detailVisible" title="演练事件详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="事件编码">{{ currentRow?.event_code }}</el-descriptions-item>
        <el-descriptions-item label="演练事件名称">{{ currentRow?.event_name }}</el-descriptions-item>
        <el-descriptions-item label="事发单位">{{ currentRow?.organization_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="事件类型">{{ currentRow?.event_type_display }}</el-descriptions-item>
        <el-descriptions-item label="事故类型">{{ currentRow?.accident_type || '-' }}</el-descriptions-item>
        <el-descriptions-item label="演练状态">
          <el-tag :type="getStatusTagType(currentRow?.drill_status)">
            {{ currentRow?.drill_status_display }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="事发时间">{{ currentRow?.event_time }}</el-descriptions-item>
        <el-descriptions-item label="所属街道">{{ currentRow?.street || '-' }}</el-descriptions-item>
        <el-descriptions-item label="详细地址" :span="2">{{ currentRow?.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="经度">{{ currentRow?.longitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="纬度">{{ currentRow?.latitude || '-' }}</el-descriptions-item>
        <el-descriptions-item label="受伤人数">{{ currentRow?.injured_count || 0 }}</el-descriptions-item>
        <el-descriptions-item label="死亡人数">{{ currentRow?.death_count || 0 }}</el-descriptions-item>
        <el-descriptions-item label="关联演练计划名称">{{ currentRow?.drill_plan_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="数据来源">{{ currentRow?.data_source_display || '-' }}</el-descriptions-item>
        <el-descriptions-item label="外部系统ID">{{ currentRow?.external_id || '-' }}</el-descriptions-item>
        <el-descriptions-item label="需要启动的预案">{{ currentRow?.related_plan_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="事故简介" :span="2">{{ currentRow?.accident_summary || '-' }}</el-descriptions-item>
        <el-descriptions-item label="事件描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
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
import { drillEventApi } from '@/api/modules/drill'
import type { DrillEvent, DrillEventFormData } from '@/types/modules/drill'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 表格数据
const tableData = ref<DrillEvent[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive({
  event_type: undefined as number | undefined,
  drill_status: undefined as number | undefined,
  data_source: undefined as number | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增演练事件')
const currentRow = ref<DrillEvent | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<DrillEventFormData>({
  event_code: '',
  event_name: '',
  organization_id: 0,
  drill_plan_name: null,
  drill_plan_id: null,
  event_type: 1,
  accident_type: null,
  longitude: null,
  latitude: null,
  street: null,
  address: null,
  event_time: '',
  injured_count: 0,
  death_count: 0,
  accident_summary: null,
  related_plan_id: null,
  drill_status: 0,
  data_source: null,
  external_id: null,
  description: null,
  remark: null,
})

// 表单验证规则
const formRules: FormRules = {
  event_code: [
    { required: true, message: '请输入事件编码', trigger: 'blur' },
  ],
  event_name: [
    { required: true, message: '请输入演练事件名称', trigger: 'blur' },
  ],
  organization_id: [
    { required: true, message: '请输入事发单位ID', trigger: 'blur' },
  ],
  event_type: [
    { required: true, message: '请选择事件类型', trigger: 'change' },
  ],
  event_time: [
    { required: true, message: '请选择事发时间', trigger: 'change' },
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
    const response = await drillEventApi.getList(params)
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
    event_type: undefined,
    drill_status: undefined,
    data_source: undefined,
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
  dialogTitle.value = '新增演练事件'
  resetForm()
  // 生成事件编码（格式：DRILL-YYYYMMDD-XXXX）
  const now = new Date()
  const dateStr = now.getFullYear().toString() +
    (now.getMonth() + 1).toString().padStart(2, '0') +
    now.getDate().toString().padStart(2, '0')
  const randomStr = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
  formData.event_code = `DRILL-${dateStr}-${randomStr}`
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: DrillEvent) => {
  isEdit.value = true
  dialogTitle.value = '编辑演练事件'
  currentRow.value = row
  Object.assign(formData, {
    event_code: row.event_code,
    event_name: row.event_name,
    organization_id: row.organization_id,
    drill_plan_name: row.drill_plan_name,
    drill_plan_id: row.drill_plan_id,
    event_type: row.event_type,
    accident_type: row.accident_type,
    longitude: row.longitude,
    latitude: row.latitude,
    street: row.street,
    address: row.address,
    event_time: row.event_time,
    injured_count: row.injured_count,
    death_count: row.death_count,
    accident_summary: row.accident_summary,
    related_plan_id: row.related_plan_id,
    drill_status: row.drill_status,
    data_source: row.data_source,
    external_id: row.external_id,
    description: row.description,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: DrillEvent) => {
  currentRow.value = row
  detailVisible.value = true
}

// 删除
const handleDelete = async (row: DrillEvent) => {
  try {
    await ElMessageBox.confirm('确定要删除该演练事件吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await drillEventApi.delete(row.id)
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
      const data: DrillEventFormData = {
        event_name: formData.event_name,
        organization_id: formData.organization_id,
        drill_plan_name: formData.drill_plan_name,
        drill_plan_id: formData.drill_plan_id,
        event_type: formData.event_type,
        accident_type: formData.accident_type,
        longitude: formData.longitude,
        latitude: formData.latitude,
        street: formData.street,
        address: formData.address,
        event_time: formData.event_time,
        injured_count: formData.injured_count,
        death_count: formData.death_count,
        accident_summary: formData.accident_summary,
        related_plan_id: formData.related_plan_id,
        drill_status: formData.drill_status,
        data_source: formData.data_source,
        external_id: formData.external_id,
        description: formData.description,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        data.event_code = formData.event_code
        await drillEventApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        data.event_code = formData.event_code
        await drillEventApi.create(data)
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
    event_code: '',
    event_name: '',
    organization_id: 0,
    drill_plan_name: null,
    drill_plan_id: null,
    event_type: 1,
    accident_type: null,
    longitude: null,
    latitude: null,
    street: null,
    address: null,
    event_time: '',
    injured_count: 0,
    death_count: 0,
    accident_summary: null,
    related_plan_id: null,
    drill_status: 0,
    data_source: null,
    external_id: null,
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

// 获取状态标签类型
const getStatusTagType = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: 'info',
    1: 'warning',
    2: 'success',
    3: 'danger',
  }
  return statusMap[status || 0] || 'info'
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped lang="scss">
.event-list {
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

