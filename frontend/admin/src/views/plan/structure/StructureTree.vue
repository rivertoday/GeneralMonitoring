<template>
  <div class="structure-tree">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h2>预案结构</h2>
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
          新增根节点
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
        class="structure-tree-content"
      >
        <template #default="{ node, data }">
          <div class="tree-node">
            <div class="node-content">
              <span class="node-name">{{ data.node_name }}</span>
              <span class="node-code">({{ data.node_code }})</span>
              <el-tag v-if="data.is_key_info === 1" type="warning" size="small" style="margin-left: 10px">
                重点
              </el-tag>
              <el-tag :type="getNodeTypeTagType(data.node_type)" size="small" style="margin-left: 10px">
                {{ data.node_type_display }}
              </el-tag>
            </div>
            <div class="node-actions">
              <el-button type="primary" link size="small" @click.stop="handleAddChild(data)">
                添加子节点
              </el-button>
              <el-button type="primary" link size="small" @click.stop="handleEdit(data)">
                编辑
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
      width="700px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="120px"
      >
        <el-form-item label="节点编码" prop="node_code">
          <el-input v-model="formData.node_code" placeholder="请输入节点编码" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="节点名称" prop="node_name">
          <el-input v-model="formData.node_name" placeholder="请输入节点名称" />
        </el-form-item>
        <el-form-item label="节点类型" prop="node_type">
          <el-select v-model="formData.node_type" placeholder="请选择" style="width: 100%">
            <el-option label="章节" :value="1" />
            <el-option label="条款" :value="2" />
            <el-option label="子条款" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="父节点">
          <el-input
            v-model="parentNodeName"
            placeholder="根节点"
            disabled
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="节点索引">
          <el-input-number
            v-model="formData.node_index"
            :min="0"
            placeholder="用于排序"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="是否重点信息">
          <el-radio-group v-model="formData.is_key_info">
            <el-radio :label="0">否</el-radio>
            <el-radio :label="1">是</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="节点内容">
          <el-input
            v-model="formData.node_content"
            type="textarea"
            :rows="6"
            placeholder="请输入节点内容"
          />
        </el-form-item>
        <el-form-item label="节点描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入节点描述"
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import type { ElTree } from 'element-plus'
import { emergencyPlanApi, planStructureApi } from '@/api/modules/plan'
import type { EmergencyPlan, PlanStructure, PlanStructureFormData } from '@/types/modules/plan'

const route = useRoute()

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 预案列表
const planList = ref<EmergencyPlan[]>([])
const selectedPlanId = ref<number | null>(null)

// 树形数据
const treeRef = ref<InstanceType<typeof ElTree>>()
const treeData = ref<PlanStructure[]>([])
const treeProps = {
  children: 'children',
  label: 'node_name',
}

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('新增节点')
const currentNode = ref<PlanStructure | null>(null)
const parentNode = ref<PlanStructure | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<PlanStructureFormData>({
  plan_id: 0,
  node_code: '',
  node_name: '',
  parent_id: 0,
  node_type: 1,
  node_content: null,
  node_index: 0,
  is_key_info: 0,
  description: null,
  remark: null,
})

const parentNodeName = computed(() => {
  return parentNode.value ? `${parentNode.value.node_name} (${parentNode.value.node_code})` : '根节点'
})

// 表单验证规则
const formRules: FormRules = {
  node_code: [
    { required: true, message: '请输入节点编码', trigger: 'blur' },
  ],
  node_name: [
    { required: true, message: '请输入节点名称', trigger: 'blur' },
  ],
  node_type: [
    { required: true, message: '请选择节点类型', trigger: 'change' },
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
    const response = await planStructureApi.getTree(selectedPlanId.value)
    treeData.value = response
  } catch (error: any) {
    ElMessage.error(error.message || '获取结构数据失败')
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

// 新增根节点
const handleAddRoot = () => {
  isEdit.value = false
  dialogTitle.value = '新增根节点'
  parentNode.value = null
  resetForm()
  formData.parent_id = 0
  dialogVisible.value = true
}

// 新增子节点
const handleAddChild = (data: PlanStructure) => {
  isEdit.value = false
  dialogTitle.value = '新增子节点'
  parentNode.value = data
  resetForm()
  formData.parent_id = data.id
  dialogVisible.value = true
}

// 编辑
const handleEdit = (data: PlanStructure) => {
  isEdit.value = true
  dialogTitle.value = '编辑节点'
  currentNode.value = data
  parentNode.value = data.parent_id ? { id: data.parent_id, node_name: data.parent_name || '', node_code: '' } as PlanStructure : null
  
  Object.assign(formData, {
    plan_id: selectedPlanId.value!,
    node_code: data.node_code,
    node_name: data.node_name,
    parent_id: data.parent_id,
    node_type: data.node_type,
    node_content: data.node_content,
    node_index: data.node_index,
    is_key_info: data.is_key_info,
    description: data.description,
    remark: data.remark,
  })
  dialogVisible.value = true
}

// 删除
const handleDelete = async (data: PlanStructure) => {
  if (!selectedPlanId.value) return

  try {
    await ElMessageBox.confirm('确定要删除该节点吗？删除后其子节点也将被删除。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await planStructureApi.delete(selectedPlanId.value, data.id)
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
      const data: PlanStructureFormData = {
        plan_id: selectedPlanId.value,
        node_name: formData.node_name,
        parent_id: formData.parent_id,
        node_type: formData.node_type,
        node_content: formData.node_content,
        node_index: formData.node_index,
        is_key_info: formData.is_key_info,
        description: formData.description,
        remark: formData.remark,
      }
      if (isEdit.value && currentNode.value) {
        data.node_code = formData.node_code
        await planStructureApi.update(selectedPlanId.value!, currentNode.value.id, data)
        ElMessage.success('更新成功')
      } else {
        data.node_code = formData.node_code
        await planStructureApi.create(selectedPlanId.value!, data)
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
    node_code: '',
    node_name: '',
    parent_id: 0,
    node_type: 1,
    node_content: null,
    node_index: 0,
    is_key_info: 0,
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

// 获取节点类型标签类型
const getNodeTypeTagType = (nodeType: number) => {
  const typeMap: Record<number, string> = {
    1: 'info',
    2: 'success',
    3: 'warning',
  }
  return typeMap[nodeType] || 'info'
}

// 初始化
onMounted(() => {
  fetchPlanList()
  
  // 从路由参数获取预案ID
  const planId = route.query.plan_id
  if (planId) {
    selectedPlanId.value = Number(planId)
    fetchTreeData()
  }
})
</script>

<style scoped lang="scss">
.structure-tree {
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
    .structure-tree-content {
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
