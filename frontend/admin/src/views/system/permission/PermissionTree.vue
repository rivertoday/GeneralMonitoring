<template>
  <div class="permission-tree">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>权限管理</h2>
      <div class="header-right">
        <el-button type="primary" @click="handleAddRoot">
          <el-icon><Plus /></el-icon>
          新增根权限
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
        class="permission-tree-content"
      >
        <template #default="{ node, data }">
          <div class="tree-node">
            <div class="node-content">
              <span class="node-name">{{ data.permission_name }}</span>
              <span class="node-code">({{ data.permission_code }})</span>
              <el-tag
                :type="getPermissionTypeTagType(data.permission_type)"
                size="small"
                style="margin-left: 10px"
              >
                {{ data.permission_type_display || getPermissionTypeDisplay(data.permission_type) }}
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
                添加子权限
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
        <el-form-item label="权限编码" prop="permission_code">
          <el-input v-model="formData.permission_code" placeholder="请输入权限编码" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="权限名称" prop="permission_name">
          <el-input v-model="formData.permission_name" placeholder="请输入权限名称" />
        </el-form-item>
        <el-form-item label="权限类型" prop="permission_type">
          <el-select v-model="formData.permission_type" placeholder="请选择" style="width: 100%" @change="handlePermissionTypeChange">
            <el-option label="菜单" :value="1" />
            <el-option label="按钮" :value="2" />
            <el-option label="接口" :value="3" />
          </el-select>
        </el-form-item>
        <el-form-item label="父权限">
          <el-input
            v-model="parentPermissionName"
            placeholder="根权限"
            disabled
            style="width: 100%"
          />
        </el-form-item>
        <!-- 菜单类型字段 -->
        <template v-if="formData.permission_type === 1">
          <el-form-item label="路由路径">
            <el-input v-model="formData.path" placeholder="请输入路由路径，如：/system/user" />
          </el-form-item>
          <el-form-item label="组件路径">
            <el-input v-model="formData.component" placeholder="请输入组件路径，如：system/user/UserList" />
          </el-form-item>
          <el-form-item label="图标">
            <el-input v-model="formData.icon" placeholder="请输入图标名称，如：User" />
          </el-form-item>
        </template>
        <!-- 接口类型字段 -->
        <template v-if="formData.permission_type === 3">
          <el-form-item label="API路径" prop="api_path">
            <el-input v-model="formData.api_path" placeholder="请输入API路径，如：/api/users/" />
          </el-form-item>
          <el-form-item label="HTTP方法" prop="http_method">
            <el-select v-model="formData.http_method" placeholder="请选择" style="width: 100%">
              <el-option label="GET" value="GET" />
              <el-option label="POST" value="POST" />
              <el-option label="PUT" value="PUT" />
              <el-option label="PATCH" value="PATCH" />
              <el-option label="DELETE" value="DELETE" />
            </el-select>
          </el-form-item>
        </template>
        <!-- 按钮类型字段 -->
        <template v-if="formData.permission_type === 2">
          <el-form-item label="API路径">
            <el-input v-model="formData.api_path" placeholder="请输入API路径（可选）" />
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
          <el-col :span="12">
            <el-form-item label="排序">
              <el-input-number v-model="formData.sort_order" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="权限描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入权限描述"
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
    <el-dialog v-model="detailVisible" title="权限详情" width="800px">
      <el-descriptions :column="2" border v-if="currentRow">
        <el-descriptions-item label="权限编码">{{ currentRow.permission_code }}</el-descriptions-item>
        <el-descriptions-item label="权限名称">{{ currentRow.permission_name }}</el-descriptions-item>
        <el-descriptions-item label="权限类型">
          <el-tag :type="getPermissionTypeTagType(currentRow.permission_type)">
            {{ currentRow.permission_type_display || getPermissionTypeDisplay(currentRow.permission_type) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="父权限">
          {{ currentRow.parent_name || '根权限' }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRow.path" label="路由路径">{{ currentRow.path }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRow.component" label="组件路径">{{ currentRow.component }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRow.icon" label="图标">{{ currentRow.icon }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRow.api_path" label="API路径">{{ currentRow.api_path }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRow.http_method" label="HTTP方法">
          <el-tag type="info">{{ currentRow.http_method }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow.status === 1 ? 'success' : 'danger'">
            {{ currentRow.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="排序">{{ currentRow.sort_order || 0 }}</el-descriptions-item>
        <el-descriptions-item label="权限描述" :span="2">{{ currentRow.description || '-' }}</el-descriptions-item>
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
import { permissionApi } from '@/api/modules/system'
import type { Permission, PermissionFormData, PermissionType, Status } from '@/types/modules/system'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)

// 树形数据
const treeRef = ref<InstanceType<typeof ElTree>>()
const treeData = ref<Permission[]>([])
const treeProps = {
  children: 'children',
  label: 'permission_name',
}

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const dialogTitle = ref('新增权限')
const currentNode = ref<Permission | null>(null)
const currentRow = ref<Permission | null>(null)
const parentNode = ref<Permission | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<PermissionFormData>({
  permission_code: '',
  permission_name: '',
  permission_type: 1,
  parent_id: 0,
  path: null,
  component: null,
  icon: null,
  api_path: null,
  http_method: null,
  description: null,
  status: 1,
  sort_order: 0,
  remark: null,
})

const parentPermissionName = computed(() => {
  return parentNode.value ? `${parentNode.value.permission_name} (${parentNode.value.permission_code})` : '根权限'
})

// 表单验证规则
const formRules: FormRules = {
  permission_code: [
    { required: true, message: '请输入权限编码', trigger: 'blur' },
    { min: 2, max: 100, message: '权限编码长度在2到100个字符之间', trigger: 'blur' },
  ],
  permission_name: [
    { required: true, message: '请输入权限名称', trigger: 'blur' },
    { min: 2, max: 100, message: '权限名称长度在2到100个字符之间', trigger: 'blur' },
  ],
  permission_type: [
    { required: true, message: '请选择权限类型', trigger: 'change' },
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' },
  ],
}

// 获取树形数据
const fetchTreeData = async () => {
  loading.value = true
  try {
    const response = await permissionApi.getTree()
    treeData.value = response
  } catch (error: any) {
    ElMessage.error(error.message || '获取权限数据失败')
  } finally {
    loading.value = false
  }
}

// 刷新
const handleRefresh = () => {
  fetchTreeData()
}

// 新增根权限
const handleAddRoot = () => {
  isEdit.value = false
  dialogTitle.value = '新增根权限'
  parentNode.value = null
  resetForm()
  formData.parent_id = 0
  dialogVisible.value = true
}

// 新增子权限
const handleAddChild = (data: Permission) => {
  isEdit.value = false
  dialogTitle.value = '新增子权限'
  parentNode.value = data
  resetForm()
  formData.parent_id = data.id
  // 子权限默认继承父权限的类型，但可以修改
  formData.permission_type = data.permission_type
  handlePermissionTypeChange()
  dialogVisible.value = true
}

// 编辑
const handleEdit = async (data: Permission) => {
  try {
    const detail = await permissionApi.getDetail(data.id)
    isEdit.value = true
    dialogTitle.value = '编辑权限'
    currentNode.value = detail
    parentNode.value = detail.parent_id && detail.parent_id > 0
      ? { id: detail.parent_id, permission_name: detail.parent_name || '', permission_code: '' } as Permission
      : null
    
    Object.assign(formData, {
      permission_code: detail.permission_code,
      permission_name: detail.permission_name,
      permission_type: detail.permission_type,
      parent_id: detail.parent_id,
      path: detail.path,
      component: detail.component,
      icon: detail.icon,
      api_path: detail.api_path,
      http_method: detail.http_method,
      description: detail.description,
      status: detail.status,
      sort_order: detail.sort_order,
      remark: detail.remark,
    })
    dialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取权限详情失败')
  }
}

// 查看
const handleView = async (data: Permission) => {
  try {
    const detail = await permissionApi.getDetail(data.id)
    currentRow.value = detail
    detailVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取权限详情失败')
  }
}

// 删除
const handleDelete = async (data: Permission) => {
  try {
    await ElMessageBox.confirm('确定要删除该权限吗？删除后其子权限也将被删除。', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await permissionApi.delete(data.id)
    ElMessage.success('删除成功')
    fetchTreeData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 权限类型变化
const handlePermissionTypeChange = () => {
  // 切换权限类型时，清空相关的字段
  if (formData.permission_type === 1) {
    // 菜单类型：清空接口相关字段
    formData.api_path = null
    formData.http_method = null
  } else if (formData.permission_type === 3) {
    // 接口类型：清空菜单相关字段
    formData.path = null
    formData.component = null
    formData.icon = null
  } else if (formData.permission_type === 2) {
    // 按钮类型：清空菜单相关字段，保留API路径（可选）
    formData.path = null
    formData.component = null
    formData.icon = null
    formData.http_method = null
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const data: PermissionFormData = {
        permission_code: formData.permission_code,
        permission_name: formData.permission_name,
        permission_type: formData.permission_type,
        parent_id: formData.parent_id,
        path: formData.path,
        component: formData.component,
        icon: formData.icon,
        api_path: formData.api_path,
        http_method: formData.http_method,
        description: formData.description,
        status: formData.status,
        sort_order: formData.sort_order,
        remark: formData.remark,
      }
      
      if (isEdit.value && currentNode.value) {
        await permissionApi.update(currentNode.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await permissionApi.create(data)
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
    permission_code: '',
    permission_name: '',
    permission_type: 1,
    parent_id: 0,
    path: null,
    component: null,
    icon: null,
    api_path: null,
    http_method: null,
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

// 获取权限类型标签类型
const getPermissionTypeTagType = (type: PermissionType) => {
  const typeMap: Record<PermissionType, string> = {
    1: 'primary', // 菜单
    2: 'success', // 按钮
    3: 'warning', // 接口
  }
  return typeMap[type] || 'info'
}

// 获取权限类型显示
const getPermissionTypeDisplay = (type: PermissionType) => {
  const typeMap: Record<PermissionType, string> = {
    1: '菜单',
    2: '按钮',
    3: '接口',
  }
  return typeMap[type] || '-'
}

// 初始化
onMounted(() => {
  fetchTreeData()
})
</script>

<style scoped lang="scss">
.permission-tree {
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
    .permission-tree-content {
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
