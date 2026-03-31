<template>
  <div class="rectification-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>隐患整改</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增整改
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="隐患">
          <el-select
            v-model="searchForm.danger_id"
            placeholder="请选择隐患"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="danger in hiddenDangers"
              :key="danger.id"
              :label="danger.danger_name"
              :value="danger.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="整改状态">
          <el-select v-model="searchForm.rectification_status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="待开始" :value="0" />
            <el-option label="进行中" :value="1" />
            <el-option label="已完成" :value="2" />
            <el-option label="已延期" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="验收状态">
          <el-select v-model="searchForm.verification_status" placeholder="请选择" clearable style="width: 120px">
            <el-option label="待验收" :value="0" />
            <el-option label="验收通过" :value="1" />
            <el-option label="验收不通过" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="计划完成时间">
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
            placeholder="请输入整改编码/方案/措施"
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
        <el-table-column prop="rectification_code" label="整改编码" width="150" />
        <el-table-column label="隐患" width="150">
          <template #default="{ row }">
            <span v-if="row.danger_detail">{{ row.danger_detail.danger_name }}</span>
            <span v-else>隐患ID: {{ row.danger_id }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="rectification_plan" label="整改方案" min-width="200" show-overflow-tooltip />
        <el-table-column label="责任人" width="120">
          <template #default="{ row }">
            <span v-if="row.responsible_user_name">{{ row.responsible_user_name }}</span>
            <span v-else>用户ID: {{ row.responsible_user_id }}</span>
          </template>
        </el-table-column>
        <el-table-column label="责任组织" width="150">
          <template #default="{ row }">
            <span v-if="row.responsible_org_name">{{ row.responsible_org_name }}</span>
            <span v-else>组织ID: {{ row.responsible_org_id }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="plan_start_time" label="计划开始时间" width="160" />
        <el-table-column prop="plan_end_time" label="计划完成时间" width="160" />
        <el-table-column prop="actual_start_time" label="实际开始时间" width="160">
          <template #default="{ row }">
            <span v-if="row.actual_start_time">{{ row.actual_start_time }}</span>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="actual_end_time" label="实际完成时间" width="160">
          <template #default="{ row }">
            <span v-if="row.actual_end_time">{{ row.actual_end_time }}</span>
            <span v-else class="text-muted">-</span>
          </template>
        </el-table-column>
        <el-table-column label="整改状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getRectificationStatusTagType(row.rectification_status)">
              {{ row.rectification_status_display || getRectificationStatusDisplay(row.rectification_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="验收状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getVerificationStatusTagType(row.verification_status)">
              {{ row.verification_status_display || getVerificationStatusDisplay(row.verification_status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button
              v-if="row.rectification_status === 2 && row.verification_status === 0"
              type="success"
              link
              size="small"
              @click="handleVerify(row)"
            >
              验收
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
            <el-form-item label="整改编码" prop="rectification_code">
              <el-input v-model="formData.rectification_code" placeholder="请输入整改编码" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="关联隐患" prop="danger_id">
              <el-select
                v-model="formData.danger_id"
                placeholder="请选择隐患"
                filterable
                style="width: 100%"
              >
                <el-option
                  v-for="danger in hiddenDangers"
                  :key="danger.id"
                  :label="danger.danger_name"
                  :value="danger.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="整改方案" prop="rectification_plan">
          <el-input
            v-model="formData.rectification_plan"
            type="textarea"
            :rows="4"
            placeholder="请输入整改方案"
          />
        </el-form-item>
        <el-form-item label="整改措施" prop="rectification_measures">
          <el-input
            v-model="formData.rectification_measures"
            type="textarea"
            :rows="4"
            placeholder="请输入整改措施"
          />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="责任人ID" prop="responsible_user_id">
              <el-input-number
                v-model="formData.responsible_user_id"
                :min="1"
                placeholder="请输入责任人ID"
                style="width: 100%"
              />
              <div class="form-tip">注意：需要先选择对应的责任人</div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="责任组织ID" prop="responsible_org_id">
              <el-input-number
                v-model="formData.responsible_org_id"
                :min="1"
                placeholder="请输入责任组织ID"
                style="width: 100%"
              />
              <div class="form-tip">注意：需要先选择对应的责任组织</div>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="计划开始时间" prop="plan_start_time">
              <el-date-picker
                v-model="formData.plan_start_time"
                type="datetime"
                placeholder="请选择计划开始时间"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="计划完成时间" prop="plan_end_time">
              <el-date-picker
                v-model="formData.plan_end_time"
                type="datetime"
                placeholder="请选择计划完成时间"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="实际开始时间">
              <el-date-picker
                v-model="formData.actual_start_time"
                type="datetime"
                placeholder="请选择实际开始时间（可选）"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="实际完成时间">
              <el-date-picker
                v-model="formData.actual_end_time"
                type="datetime"
                placeholder="请选择实际完成时间（可选）"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="整改状态">
          <el-select v-model="formData.rectification_status" placeholder="请选择" style="width: 100%">
            <el-option label="待开始" :value="0" />
            <el-option label="进行中" :value="1" />
            <el-option label="已完成" :value="2" />
            <el-option label="已延期" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="整改结果">
          <el-input
            v-model="formData.rectification_result"
            type="textarea"
            :rows="3"
            placeholder="请输入整改结果（可选）"
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
    <el-dialog v-model="detailVisible" title="整改详情" width="1000px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="整改编码">{{ currentRow?.rectification_code }}</el-descriptions-item>
        <el-descriptions-item label="关联隐患">
          {{ currentRow?.danger_detail?.danger_name || `隐患ID: ${currentRow?.danger_id}` }}
        </el-descriptions-item>
        <el-descriptions-item label="责任人">
          {{ currentRow?.responsible_user_name || `用户ID: ${currentRow?.responsible_user_id}` }}
        </el-descriptions-item>
        <el-descriptions-item label="责任组织">
          {{ currentRow?.responsible_org_name || `组织ID: ${currentRow?.responsible_org_id}` }}
        </el-descriptions-item>
        <el-descriptions-item label="计划开始时间">{{ currentRow?.plan_start_time }}</el-descriptions-item>
        <el-descriptions-item label="计划完成时间">{{ currentRow?.plan_end_time }}</el-descriptions-item>
        <el-descriptions-item label="实际开始时间">
          {{ currentRow?.actual_start_time || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="实际完成时间">
          {{ currentRow?.actual_end_time || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="整改状态">
          <el-tag :type="getRectificationStatusTagType(currentRow?.rectification_status)">
            {{ currentRow?.rectification_status_display || getRectificationStatusDisplay(currentRow?.rectification_status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="验收状态">
          <el-tag :type="getVerificationStatusTagType(currentRow?.verification_status)">
            {{ currentRow?.verification_status_display || getVerificationStatusDisplay(currentRow?.verification_status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="验收时间">
          {{ currentRow?.verification_time || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="验收人">
          {{ currentRow?.verification_user_name || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="整改方案" :span="2">
          {{ currentRow?.rectification_plan }}
        </el-descriptions-item>
        <el-descriptions-item label="整改措施" :span="2">
          {{ currentRow?.rectification_measures }}
        </el-descriptions-item>
        <el-descriptions-item label="整改结果" :span="2">
          {{ currentRow?.rectification_result || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="验收意见" :span="2">
          {{ currentRow?.verification_opinion || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 验收对话框 -->
    <el-dialog v-model="verifyVisible" title="验收整改" width="600px">
      <el-form ref="verifyFormRef" :model="verifyForm" :rules="verifyFormRules" label-width="100px">
        <el-form-item label="验收状态" prop="verification_status">
          <el-select v-model="verifyForm.verification_status" placeholder="请选择" style="width: 100%">
            <el-option label="验收通过" :value="1" />
            <el-option label="验收不通过" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="验收意见" prop="verification_opinion">
          <el-input
            v-model="verifyForm.verification_opinion"
            type="textarea"
            :rows="5"
            placeholder="请输入验收意见"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="verifyVisible = false">取消</el-button>
        <el-button type="primary" :loading="verifyLoading" @click="handleVerifySubmit">
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
import { riskRectificationApi, riskHiddenDangerApi } from '@/api/modules/risk'
import type {
  RiskRectification,
  RiskRectificationFormData,
  RiskHiddenDanger,
} from '@/types/modules/risk'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)
const verifyLoading = ref(false)

// 表格数据
const tableData = ref<RiskRectification[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 隐患列表
const hiddenDangers = ref<RiskHiddenDanger[]>([])

// 搜索表单
const searchForm = reactive({
  danger_id: undefined as number | undefined,
  rectification_status: undefined as 0 | 1 | 2 | 3 | undefined,
  verification_status: undefined as 0 | 1 | 2 | undefined,
  search: undefined as string | undefined,
})

// 时间范围
const timeRange = ref<[string, string] | null>(null)

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const verifyVisible = ref(false)
const dialogTitle = ref('新增整改')
const currentRow = ref<RiskRectification | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const verifyFormRef = ref<FormInstance>()
const formData = reactive<RiskRectificationFormData>({
  rectification_code: '',
  danger_id: 0,
  rectification_plan: '',
  rectification_measures: '',
  responsible_user_id: 0,
  responsible_org_id: 0,
  plan_start_time: '',
  plan_end_time: '',
  actual_start_time: null,
  actual_end_time: null,
  rectification_status: 0,
  rectification_result: null,
  verification_status: 0,
  verification_time: null,
  verification_user_id: null,
  verification_opinion: null,
  remark: null,
})

// 验收表单
const verifyForm = reactive({
  verification_status: 1 as 1 | 2,
  verification_opinion: '',
})

// 表单验证规则
const formRules: FormRules = {
  rectification_code: [
    { required: true, message: '请输入整改编码', trigger: 'blur' },
  ],
  danger_id: [
    { required: true, message: '请选择关联隐患', trigger: 'change' },
  ],
  rectification_plan: [
    { required: true, message: '请输入整改方案', trigger: 'blur' },
  ],
  rectification_measures: [
    { required: true, message: '请输入整改措施', trigger: 'blur' },
  ],
  responsible_user_id: [
    { required: true, message: '请输入责任人ID', trigger: 'blur' },
    { type: 'number', min: 1, message: '责任人ID必须大于0', trigger: 'blur' },
  ],
  responsible_org_id: [
    { required: true, message: '请输入责任组织ID', trigger: 'blur' },
    { type: 'number', min: 1, message: '责任组织ID必须大于0', trigger: 'blur' },
  ],
  plan_start_time: [
    { required: true, message: '请选择计划开始时间', trigger: 'change' },
  ],
  plan_end_time: [
    { required: true, message: '请选择计划完成时间', trigger: 'change' },
  ],
}

// 验收表单验证规则
const verifyFormRules: FormRules = {
  verification_status: [
    { required: true, message: '请选择验收状态', trigger: 'change' },
  ],
  verification_opinion: [
    { required: true, message: '请输入验收意见', trigger: 'blur' },
  ],
}

// 获取隐患列表
const fetchHiddenDangers = async () => {
  try {
    const response = await riskHiddenDangerApi.getList({
      page_size: 100,
      status: 0, // 待整改和整改中的隐患
    })
    hiddenDangers.value = response.results.filter((d) => d.status === 0 || d.status === 1)
  } catch (error: any) {
    console.error('获取隐患列表失败:', error)
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
    const response = await riskRectificationApi.getList(params)
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
    danger_id: undefined,
    rectification_status: undefined,
    verification_status: undefined,
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
  dialogTitle.value = '新增整改'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = (row: RiskRectification) => {
  isEdit.value = true
  dialogTitle.value = '编辑整改'
  currentRow.value = row
  Object.assign(formData, {
    rectification_code: row.rectification_code,
    danger_id: row.danger_id,
    rectification_plan: row.rectification_plan,
    rectification_measures: row.rectification_measures,
    responsible_user_id: row.responsible_user_id,
    responsible_org_id: row.responsible_org_id,
    plan_start_time: row.plan_start_time,
    plan_end_time: row.plan_end_time,
    actual_start_time: row.actual_start_time,
    actual_end_time: row.actual_end_time,
    rectification_status: row.rectification_status,
    rectification_result: row.rectification_result,
    verification_status: row.verification_status,
    verification_time: row.verification_time,
    verification_user_id: row.verification_user_id,
    verification_opinion: row.verification_opinion,
    remark: row.remark,
  })
  dialogVisible.value = true
}

// 查看
const handleView = (row: RiskRectification) => {
  currentRow.value = row
  detailVisible.value = true
}

// 验收
const handleVerify = (row: RiskRectification) => {
  currentRow.value = row
  verifyForm.verification_status = 1
  verifyForm.verification_opinion = ''
  verifyVisible.value = true
}

// 验收提交
const handleVerifySubmit = async () => {
  if (!verifyFormRef.value || !currentRow.value) return

  await verifyFormRef.value.validate(async (valid) => {
    if (!valid) return

    if (!currentRow.value) {
      ElMessage.warning('请选择要验收的整改记录')
      return
    }
    
    verifyLoading.value = true
    try {
      await riskRectificationApi.verify(currentRow.value.id, {
        verification_status: verifyForm.verification_status,
        verification_opinion: verifyForm.verification_opinion,
      })
      ElMessage.success('验收成功')
      verifyVisible.value = false
      fetchData()
    } catch (error: any) {
      ElMessage.error(error.message || '验收失败')
    } finally {
      verifyLoading.value = false
    }
  })
}

// 删除
const handleDelete = async (row: RiskRectification) => {
  try {
    await ElMessageBox.confirm('确定要删除该整改记录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await riskRectificationApi.delete(row.id)
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
      const data: RiskRectificationFormData = {
        rectification_code: formData.rectification_code,
        danger_id: formData.danger_id,
        rectification_plan: formData.rectification_plan,
        rectification_measures: formData.rectification_measures,
        responsible_user_id: formData.responsible_user_id,
        responsible_org_id: formData.responsible_org_id,
        plan_start_time: formData.plan_start_time,
        plan_end_time: formData.plan_end_time,
        actual_start_time: formData.actual_start_time,
        actual_end_time: formData.actual_end_time,
        rectification_status: formData.rectification_status,
        rectification_result: formData.rectification_result,
        verification_status: formData.verification_status,
        verification_time: formData.verification_time,
        verification_user_id: formData.verification_user_id,
        verification_opinion: formData.verification_opinion,
        remark: formData.remark,
      }
      if (isEdit.value && currentRow.value) {
        await riskRectificationApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await riskRectificationApi.create(data)
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
    rectification_code: '',
    danger_id: 0,
    rectification_plan: '',
    rectification_measures: '',
    responsible_user_id: 0,
    responsible_org_id: 0,
    plan_start_time: '',
    plan_end_time: '',
    actual_start_time: null,
    actual_end_time: null,
    rectification_status: 0,
    rectification_result: null,
    verification_status: 0,
    verification_time: null,
    verification_user_id: null,
    verification_opinion: null,
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

// 获取整改状态标签类型
const getRectificationStatusTagType = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: 'info', // 待开始
    1: 'warning', // 进行中
    2: 'success', // 已完成
    3: 'danger', // 已延期
  }
  return statusMap[status ?? 0] || 'info'
}

// 获取整改状态显示
const getRectificationStatusDisplay = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: '待开始',
    1: '进行中',
    2: '已完成',
    3: '已延期',
  }
  return statusMap[status ?? 0] || '-'
}

// 获取验收状态标签类型
const getVerificationStatusTagType = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: 'info', // 待验收
    1: 'success', // 验收通过
    2: 'danger', // 验收不通过
  }
  return statusMap[status ?? 0] || 'info'
}

// 获取验收状态显示
const getVerificationStatusDisplay = (status?: number) => {
  const statusMap: Record<number, string> = {
    0: '待验收',
    1: '验收通过',
    2: '验收不通过',
  }
  return statusMap[status ?? 0] || '-'
}

// 初始化
onMounted(() => {
  fetchHiddenDangers()
  fetchData()
})
</script>

<style scoped lang="scss">
.rectification-list {
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

  .text-muted {
    color: #909399;
  }

  .form-tip {
    font-size: 12px;
    color: #909399;
    margin-top: 5px;
  }
}
</style>
