<template>
  <div class="flow-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h2>预案流程</h2>
        <el-select
          v-model="selectedPlanId"
          placeholder="请选择预案"
          clearable
          filterable
          style="width: 300px; margin-left: 20px"
          @change="handlePlanChange"
        >
          <el-option
            v-for="plan in planList"
            :key="plan.id"
            :label="`${plan.plan_code} - ${plan.plan_name}`"
            :value="plan.id"
          />
        </el-select>
      </div>
      <div class="header-right">
        <el-button type="primary" :disabled="!selectedPlanId" @click="handleAddRoot">
          <el-icon><Plus /></el-icon>
          新增根流程
        </el-button>
        <el-button type="primary" :disabled="!selectedPlanId" @click="handleRefresh">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 树形结构 -->
    <el-card v-if="selectedPlanId" class="tree-card">
      <el-tree
        ref="treeRef"
        :data="treeData"
        :props="treeProps"
        node-key="id"
        default-expand-all
        :expand-on-click-node="false"
        :highlight-current="true"
        class="flow-tree-content"
      >
        <template #default="{ node, data }">
          <div class="tree-node">
            <div class="node-content">
              <span class="node-name">{{ data.flow_name }}</span>
              <span class="node-code">({{ data.flow_code }})</span>
              <el-tag :type="getFlowTypeTagType(data.flow_type)" size="small" style="margin-left: 10px">
                {{ data.flow_type_display }}
              </el-tag>
            </div>
            <div class="node-actions">
              <el-button type="primary" link size="small" @click.stop="handleAddChild(data)">
                添加子流程
              </el-button>
              <el-button type="primary" link size="small" @click.stop="handleEdit(data)">
                编辑
              </el-button>
              <el-button type="info" link size="small" @click.stop="handleViewConfig(data)">
                查看配置
              </el-button>
              <el-button type="danger" link size="small" @click.stop="handleDelete(data)">
                删除
              </el-button>
            </div>
          </div>
        </template>
      </el-tree>
    </el-card>

    <el-empty v-else description="请先选择预案" />

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
        <el-form-item label="流程编码" prop="flow_code">
          <el-input v-model="formData.flow_code" placeholder="请输入流程编码" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="流程名称" prop="flow_name">
          <el-input v-model="formData.flow_name" placeholder="请输入流程名称" />
        </el-form-item>
        <el-form-item label="流程类型" prop="flow_type">
          <el-select v-model="formData.flow_type" placeholder="请选择" style="width: 100%">
            <el-option label="主流程" :value="1" />
            <el-option label="子流程" :value="2" />
            <el-option label="任务节点" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="父流程">
          <el-input
            v-model="parentFlowName"
            placeholder="根流程"
            disabled
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="排序顺序">
          <el-input-number
            v-model="formData.sort_order"
            :min="0"
            placeholder="用于排序"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="流程描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入流程描述"
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

    <!-- 配置查看对话框 -->
    <el-dialog v-model="configVisible" title="流程配置" width="900px">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="流程配置" name="flow">
          <el-input
            v-model="currentFlowConfig"
            type="textarea"
            :rows="15"
            readonly
            placeholder="流程配置（JSON格式）"
          />
        </el-tab-pane>
        <el-tab-pane label="下一流程" name="next">
          <el-input
            v-model="currentNextFlowIds"
            type="textarea"
            :rows="10"
            readonly
            placeholder="下一流程ID列表（JSON数组）"
          />
        </el-tab-pane>
        <el-tab-pane label="条件配置" name="condition">
          <el-input
            v-model="currentConditionConfig"
            type="textarea"
            :rows="15"
            readonly
            placeholder="条件配置（JSON格式）"
          />
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import type { ElTree } from 'element-plus'
import { emergencyPlanApi, planFlowApi } from '@/api/modules/plan'
import type { EmergencyPlan, PlanFlow, PlanFlowFormData } from '@/types/modules/plan'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 预案列表
const planList = ref<EmergencyPlan[]>([])
const selectedPlanId = ref<number | null>(null)

// 树形数据
const treeRef = ref<InstanceType<typeof ElTree>>()
const treeData = ref<PlanFlow[]>([])
const treeProps = {
  children: 'children',
  label: 'flow_name',
}

// 对话框
const dialogVisible = ref(false)
const configVisible = ref(false)
const dialogTitle = ref('新增流程')
const currentNode = ref<PlanFlow | null>(null)
const parentNode = ref<PlanFlow | null>(null)
const isEdit = ref(false)
const activeTab = ref('flow')
const currentFlowConfig = ref('')
const currentNextFlowIds = ref('')
const currentConditionConfig = ref('')

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<PlanFlowFormData>({
  plan_id: 0,
  flow_code: '',
  flow_name: '',
  parent_id: 0,
  flow_type: 1,
  flow_config: null,
  next_flow_ids: null,
  condition_config: null,
  sort_order: 0,
  description: null,
  remark: null,
})

const parentFlowName = computed(() => {
  return parentNode.value ? `${parentNode.value.flow_name} (${parentNode.value.flow_code})` : '根流程'
})

// 表单验证规则
const formRules: FormRules = {
  flow_code: [
    { required: true, message: '请输入流程编码', trigger: 'blur' },
  ],
  flow_name: [
    { required: true, message: '请输入流程名称', trigger: 'blur' },
  ],
  flow_type: [
    { required: true, message: '请选择流程类型', trigger: 'change' },
  ],
}

// 获取预案列表
const fetchPlanList = async () => {
  try {
    const response = await emergencyPlanApi.getList({ page_size: 1000 })
    planList.value = response.results
  } catch (error: any) {
    ElMessage.error(error.message || '获取预案列表失败')
  }
}

// 获取树形数据
const fetchTreeData = async () => {
  if (!selectedPlanId.value) return

  loading.value = true
  try {
    const response = await planFlowApi.getTree(selectedPlanId.value)
    treeData.value = response
  } catch (error: any) {
    ElMessage.error(error.message || '获取流程数据失败')
  } finally {
    loading.value = false
  }
}

// 预案变化
const handlePlanChange = () => {
  treeData.value = []
  if (selectedPlanId.value) {
    fetchTreeData()
  }
}

// 刷新
const handleRefresh = () => {
  fetchTreeData()
}

// 新增根流程
const handleAddRoot = () => {
  isEdit.value = false
  dialogTitle.value = '新增根流程'
  parentNode.value = null
  resetForm()
  formData.parent_id = 0
  dialogVisible.value = true
}

// 新增子流程
const handleAddChild = (data: PlanFlow) => {
  isEdit.value = false
  dialogTitle.value = '新增子流程'
  parentNode.value = data
  resetForm()
  formData.parent_id = data.id
  dialogVisible.value = true
}

// 编辑
const handleEdit = (data: PlanFlow) => {
  isEdit.value = true
  dialogTitle.value = '编辑流程'
  currentNode.value = data
  parentNode.value = data.parent_id ? { id: data.parent_id, flow_name: data.parent_name || '', flow_code: '' } as PlanFlow : null
  
  Object.assign(formData, {
    plan_id: selectedPlanId.value!,
    flow_code: data.flow_code,
    flow_name: data.flow_name,
    parent_id: data.parent_id,
    flow_type: data.flow_type,
    flow_config: data.flow_config,
    next_flow_ids: data.next_flow_ids,
    condition_config: data.condition_config,
    sort_order: data.sort_order,
    description: data.description,
    remark: data.remark,
  })
  dialogVisible.value = true
}

// 查看配置
const handleViewConfig = (data: PlanFlow) => {
  currentNode.value = data
  currentFlowConfig.value = data.flow_config || '无配置'
  currentNextFlowIds.value = data.next_flow_ids || '[]'
  currentConditionConfig.value = data.condition_config || '无配置'
  activeTab.value = 'flow'
  configVisible.value = true
}

// 删除
const handleDelete = async (data: PlanFlow) => {
  if (!selectedPlanId.value) return

  try {
    await ElMessageBox.confirm('确定要删除该流程吗？删除后其子流程也将被删除。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await planFlowApi.delete(selectedPlanId.value, data.id)
    ElMessage.success('删除成功')
    fetchTreeData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value || !selectedPlanId.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    if (!selectedPlanId.value) {
      ElMessage.warning('请先选择预案')
      return
    }
    
    submitLoading.value = true
    try {
      const data: PlanFlowFormData = {
        plan_id: selectedPlanId.value,
        flow_name: formData.flow_name,
        parent_id: formData.parent_id,
        flow_type: formData.flow_type,
        flow_config: formData.flow_config,
        next_flow_ids: formData.next_flow_ids,
        condition_config: formData.condition_config,
        sort_order: formData.sort_order,
        description: formData.description,
        remark: formData.remark,
      }
      if (isEdit.value && currentNode.value) {
        data.flow_code = formData.flow_code
        await planFlowApi.update(selectedPlanId.value!, currentNode.value.id, data)
        ElMessage.success('更新成功')
      } else {
        data.flow_code = formData.flow_code
        await planFlowApi.create(selectedPlanId.value!, data)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      fetchTreeData()
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
    plan_id: selectedPlanId.value || 0,
    flow_code: '',
    flow_name: '',
    parent_id: 0,
    flow_type: 1,
    flow_config: null,
    next_flow_ids: null,
    condition_config: null,
    sort_order: 0,
    description: null,
    remark: null,
  })
  formRef.value?.clearValidate()
  currentNode.value = null
}

// 对话框关闭
const handleDialogClose = () => {
  resetForm()
  isEdit.value = false
  parentNode.value = null
}

// 获取流程类型标签类型
const getFlowTypeTagType = (flowType: number) => {
  const typeMap: Record<number, string> = {
    1: 'primary',
    2: 'success',
    3: 'warning',
  }
  return typeMap[flowType] || 'info'
}

// 初始化
onMounted(() => {
  fetchPlanList()
})
</script>

<style scoped lang="scss">
.flow-list {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    .header-left {
      display: flex;
      align-items: center;

      h2 {
        margin: 0;
        font-size: 20px;
        font-weight: 500;
      }
    }

    .header-right {
      display: flex;
      gap: 10px;
    }
  }

  .tree-card {
    .flow-tree-content {
      min-height: 400px;
    }

    .tree-node {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex: 1;
      padding-right: 20px;

      .node-content {
        display: flex;
        align-items: center;
        flex: 1;

        .node-name {
          font-weight: 500;
          margin-right: 8px;
        }

        .node-code {
          color: #909399;
          font-size: 12px;
        }
      }

      .node-actions {
        display: flex;
        gap: 10px;
      }
    }
  }
}
</style>
