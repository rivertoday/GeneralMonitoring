<template>
  <div class="organization-tree">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>组织管理</h2>
      <div class="header-right">
        <el-button type="primary" @click="handleAddRoot">
          <el-icon><Plus /></el-icon>
          新增根组织
        </el-button>
        <el-button type="primary" @click="handleRefresh">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 树形结构 -->
    <el-card class="tree-card">
      <el-tree
        ref="treeRef"
        v-loading="loading"
        :data="treeData"
        :props="treeProps"
        node-key="id"
        default-expand-all
        :expand-on-click-node="false"
        :highlight-current="true"
        class="organization-tree-content"
      >
        <template #default="{ node, data }">
          <div class="tree-node">
            <div class="node-content">
              <span class="node-name">{{ data.org_name }}</span>
              <span class="node-code">({{ data.org_code }})</span>
              <el-tag
                :type="getOrgTypeTagType(data.org_type)"
                size="small"
                style="margin-left: 10px"
              >
                {{ data.org_type_display || getOrgTypeDisplay(data.org_type) }}
              </el-tag>
              <el-tag
                :type="data.status === 1 ? 'success' : 'danger'"
                size="small"
                style="margin-left: 10px"
              >
                {{ data.status === 1 ? '启用' : '禁用' }}
              </el-tag>
            </div>
            <div class="node-actions">
              <el-button type="primary" link size="small" @click.stop="handleView(data)">
                查看
              </el-button>
              <el-button type="primary" link size="small" @click.stop="handleAddChild(data)">
                添加子组织
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
        <el-form-item label="组织编码" prop="org_code">
          <el-input v-model="formData.org_code" placeholder="请输入组织编码" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="组织名称" prop="org_name">
          <el-input v-model="formData.org_name" placeholder="请输入组织名称" />
        </el-form-item>
        <el-form-item label="组织类型" prop="org_type">
          <el-select v-model="formData.org_type" placeholder="请选择" style="width: 100%">
            <el-option label="政府部门" :value="1" />
            <el-option label="企业单位" :value="2" />
            <el-option label="事业单位" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="父组织">
          <el-input
            v-model="parentOrganizationName"
            placeholder="根组织"
            disabled
            style="width: 100%"
          />
        </el-form-item>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="组织层级">
              <el-input-number v-model="formData.level" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="formData.status" placeholder="请选择状态" style="width: 100%">
                <el-option label="启用" :value="1" />
                <el-option label="禁用" :value="0" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="负责人">
              <el-input v-model="formData.leader" placeholder="请输入负责人姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话">
              <el-input v-model="formData.phone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="地址">
          <el-input v-model="formData.address" placeholder="请输入地址" />
        </el-form-item>
        <el-form-item label="组织描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入组织描述"
          />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="formData.sort_order" :min="0" style="width: 100%" />
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
    <el-dialog v-model="detailVisible" title="组织详情" width="800px">
      <el-descriptions :column="2" border v-if="currentRow">
        <el-descriptions-item label="组织编码">{{ currentRow.org_code }}</el-descriptions-item>
        <el-descriptions-item label="组织名称">{{ currentRow.org_name }}</el-descriptions-item>
        <el-descriptions-item label="组织类型">
          <el-tag :type="getOrgTypeTagType(currentRow.org_type)">
            {{ currentRow.org_type_display || getOrgTypeDisplay(currentRow.org_type) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="父组织">
          {{ currentRow.parent_name || '根组织' }}
        </el-descriptions-item>
        <el-descriptions-item label="组织层级">{{ currentRow.level || 1 }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow.status === 1 ? 'success' : 'danger'">
            {{ currentRow.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="负责人">{{ currentRow.leader || '-' }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentRow.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="地址" :span="2">{{ currentRow.address || '-' }}</el-descriptions-item>
        <el-descriptions-item label="组织描述" :span="2">{{ currentRow.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="排序">{{ currentRow.sort_order || 0 }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus, Refresh } from '@element-plus/icons-vue'
import type { ElTree } from 'element-plus'
import { organizationApi } from '@/api/modules/system'
import type { Organization, OrganizationFormData, OrgType, Status } from '@/types/modules/system'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 树形数据
const treeRef = ref<InstanceType<typeof ElTree>>()
const treeData = ref<Organization[]>([])
const treeProps = {
  children: 'children',
  label: 'org_name',
}

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增组织')
const currentNode = ref<Organization | null>(null)
const currentRow = ref<Organization | null>(null)
const parentNode = ref<Organization | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<OrganizationFormData>({
  org_code: '',
  org_name: '',
  parent_id: 0,
  org_type: 1,
  level: 1,
  leader: null,
  phone: null,
  address: null,
  description: null,
  status: 1,
  sort_order: 0,
  remark: null,
})

const parentOrganizationName = computed(() => {
  return parentNode.value ? `${parentNode.value.org_name} (${parentNode.value.org_code})` : '根组织'
})

// 表单验证规则
const formRules: FormRules = {
  org_code: [
    { required: true, message: '请输入组织编码', trigger: 'blur' },
    { min: 2, max: 50, message: '组织编码长度在2到50个字符之间', trigger: 'blur' },
  ],
  org_name: [
    { required: true, message: '请输入组织名称', trigger: 'blur' },
    { min: 2, max: 100, message: '组织名称长度在2到100个字符之间', trigger: 'blur' },
  ],
  org_type: [
    { required: true, message: '请选择组织类型', trigger: 'change' },
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' },
  ],
}

// 获取树形数据
const fetchTreeData = async () => {
  loading.value = true
  try {
    const response = await organizationApi.getTree()
    treeData.value = response
  } catch (error: any) {
    ElMessage.error(error.message || '获取组织数据失败')
  } finally {
    loading.value = false
  }
}

// 刷新
const handleRefresh = () => {
  fetchTreeData()
}

// 新增根组织
const handleAddRoot = () => {
  isEdit.value = false
  dialogTitle.value = '新增根组织'
  parentNode.value = null
  resetForm()
  formData.parent_id = 0
  formData.level = 1
  dialogVisible.value = true
}

// 新增子组织
const handleAddChild = (data: Organization) => {
  isEdit.value = false
  dialogTitle.value = '新增子组织'
  parentNode.value = data
  resetForm()
  formData.parent_id = data.id
  formData.level = (data.level || 1) + 1
  dialogVisible.value = true
}

// 编辑
const handleEdit = async (data: Organization) => {
  try {
    const detail = await organizationApi.getDetail(data.id)
    isEdit.value = true
    dialogTitle.value = '编辑组织'
    currentNode.value = detail
    parentNode.value = detail.parent_id && detail.parent_id > 0
      ? { id: detail.parent_id, org_name: detail.parent_name || '', org_code: '' } as Organization
      : null
    
    Object.assign(formData, {
      org_code: detail.org_code,
      org_name: detail.org_name,
      parent_id: detail.parent_id,
      org_type: detail.org_type,
      level: detail.level,
      leader: detail.leader,
      phone: detail.phone,
      address: detail.address,
      description: detail.description,
      status: detail.status,
      sort_order: detail.sort_order,
      remark: detail.remark,
    })
    dialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取组织详情失败')
  }
}

// 查看
const handleView = async (data: Organization) => {
  try {
    const detail = await organizationApi.getDetail(data.id)
    currentRow.value = detail
    detailVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取组织详情失败')
  }
}

// 删除
const handleDelete = async (data: Organization) => {
  try {
    await ElMessageBox.confirm('确定要删除该组织吗？删除后其子组织也将被删除。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await organizationApi.delete(data.id)
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
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const data: OrganizationFormData = {
        org_code: formData.org_code,
        org_name: formData.org_name,
        parent_id: formData.parent_id,
        org_type: formData.org_type,
        level: formData.level,
        leader: formData.leader,
        phone: formData.phone,
        address: formData.address,
        description: formData.description,
        status: formData.status,
        sort_order: formData.sort_order,
        remark: formData.remark,
      }
      
      if (isEdit.value && currentNode.value) {
        await organizationApi.update(currentNode.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await organizationApi.create(data)
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
    org_code: '',
    org_name: '',
    parent_id: 0,
    org_type: 1,
    level: 1,
    leader: null,
    phone: null,
    address: null,
    description: null,
    status: 1,
    sort_order: 0,
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

// 获取组织类型标签类型
const getOrgTypeTagType = (type: OrgType) => {
  const typeMap: Record<OrgType, string> = {
    1: 'primary', // 政府部门
    2: 'success', // 企业单位
    3: 'warning', // 事业单位
  }
  return typeMap[type] || 'info'
}

// 获取组织类型显示
const getOrgTypeDisplay = (type: OrgType) => {
  const typeMap: Record<OrgType, string> = {
    1: '政府部门',
    2: '企业单位',
    3: '事业单位',
  }
  return typeMap[type] || '-'
}

// 初始化
onMounted(() => {
  fetchTreeData()
})
</script>

<style scoped lang="scss">
.organization-tree {
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

    .header-right {
      display: flex;
      gap: 10px;
    }
  }

  .tree-card {
    .organization-tree-content {
      min-height: 400px;

      .tree-node {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 14px;
        padding-right: 8px;

        .node-content {
          flex: 1;
          display: flex;
          align-items: center;

          .node-name {
            font-weight: 500;
            margin-right: 8px;
          }

          .node-code {
            color: #909399;
            font-size: 12px;
            margin-right: 8px;
          }
        }

        .node-actions {
          display: flex;
          gap: 5px;
        }
      }
    }
  }
}
</style>
