<template>
  <div class="role-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>角色管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增角色
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="角色编码">
          <el-input
            v-model="searchForm.role_code"
            placeholder="请输入角色编码"
            clearable
            style="width: 150px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="角色名称">
          <el-input
            v-model="searchForm.role_name"
            placeholder="请输入角色名称"
            clearable
            style="width: 150px"
            @keyup.enter="handleSearch"
          />
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
            placeholder="请输入角色编码/名称"
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
        <el-table-column prop="role_code" label="角色编码" width="150" />
        <el-table-column prop="role_name" label="角色名称" width="150" />
        <el-table-column prop="description" label="角色描述" min-width="200" show-overflow-tooltip />
        <el-table-column label="权限数量" width="100" align="center">
          <template #default="{ row }">
            <span>{{ row.permissions ? row.permissions.length : 0 }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sort_order" label="排序" width="80" align="center" />
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="primary" link size="small" @click="handleAssignPermissions(row)">
              分配权限
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
      width="700px"
      @close="handleDialogClose"
    >
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="120px"
      >
        <el-form-item label="角色编码" prop="role_code">
          <el-input v-model="formData.role_code" placeholder="请输入角色编码" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="角色名称" prop="role_name">
          <el-input v-model="formData.role_name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色描述">
          <el-input
            v-model="formData.description"
            type="textarea"
            :rows="3"
            placeholder="请输入角色描述"
          />
        </el-form-item>
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
    <el-dialog v-model="detailVisible" title="角色详情" width="700px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="角色编码">{{ currentRow?.role_code }}</el-descriptions-item>
        <el-descriptions-item label="角色名称">{{ currentRow?.role_name }}</el-descriptions-item>
        <el-descriptions-item label="角色描述" :span="2">{{ currentRow?.description || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'danger'">
            {{ currentRow?.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="排序">{{ currentRow?.sort_order || 0 }}</el-descriptions-item>
        <el-descriptions-item label="权限数量">
          {{ currentRow?.permissions ? currentRow.permissions.length : 0 }}
        </el-descriptions-item>
        <el-descriptions-item label="权限列表" :span="2">
          <el-tag
            v-for="permission in currentRow?.permissions"
            :key="permission.id"
            size="small"
            style="margin-right: 5px; margin-bottom: 5px"
          >
            {{ permission.permission_name }}
          </el-tag>
          <span v-if="!currentRow?.permissions || currentRow.permissions.length === 0">-</span>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRow?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 分配权限对话框 -->
    <el-dialog
      v-model="permissionDialogVisible"
      title="分配权限"
      width="700px"
      @close="handlePermissionDialogClose"
    >
      <el-form label-width="100px" v-if="currentRole">
        <el-form-item label="角色名称">
          <el-input v-model="currentRole.role_name" disabled />
        </el-form-item>
        <el-form-item label="选择权限">
          <el-tree
            ref="permissionTreeRef"
            :data="permissionTreeData"
            :props="treeProps"
            show-checkbox
            node-key="id"
            :default-expand-all="false"
            :check-strictly="false"
            class="permission-tree"
          >
            <template #default="{ node, data }">
              <span class="tree-node-label">
                {{ data.permission_name }}
                <el-tag
                  v-if="data.permission_type"
                  :type="getPermissionTypeTagType(data.permission_type)"
                  size="small"
                  style="margin-left: 5px"
                >
                  {{ data.permission_type_display || getPermissionTypeDisplay(data.permission_type) }}
                </el-tag>
              </span>
            </template>
          </el-tree>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="permissionDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="permissionSubmitLoading" @click="handlePermissionSubmit">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import type { ElTree } from 'element-plus'
import { Plus, Search, Refresh } from '@element-plus/icons-vue'
import { roleApi, permissionApi } from '@/api/modules/system'
import type { Role, RoleFormData, Permission, Status, PermissionType } from '@/types/modules/system'
import type { PaginatedResponse } from '@/api/types'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)
const permissionSubmitLoading = ref(false)

// 表格数据
const tableData = ref<Role[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive({
  role_code: undefined as string | undefined,
  role_name: undefined as string | undefined,
  status: undefined as Status | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const permissionDialogVisible = ref(false)
const dialogTitle = ref('新增角色')
const currentRow = ref<Role | null>(null)
const currentRole = ref<Role | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<RoleFormData>({
  role_code: '',
  role_name: '',
  description: null,
  status: 1,
  sort_order: 0,
  permission_ids: [],
  remark: null,
})

// 权限树
const permissionTreeRef = ref<InstanceType<typeof ElTree>>()
const permissionTreeData = ref<Permission[]>([])
const treeProps = {
  children: 'children',
  label: 'permission_name',
}

// 表单验证规则
const formRules: FormRules = {
  role_code: [
    { required: true, message: '请输入角色编码', trigger: 'blur' },
    { min: 2, max: 50, message: '角色编码长度在2到50个字符之间', trigger: 'blur' },
  ],
  role_name: [
    { required: true, message: '请输入角色名称', trigger: 'blur' },
    { min: 2, max: 50, message: '角色名称长度在2到50个字符之间', trigger: 'blur' },
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' },
  ],
}

// 获取权限树
const fetchPermissionTree = async () => {
  try {
    const response = await permissionApi.getTree()
    permissionTreeData.value = response
  } catch (error: any) {
    console.error('获取权限树失败:', error)
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
    const response = await roleApi.getList(params)
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
    role_code: undefined,
    role_name: undefined,
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
  dialogTitle.value = '新增角色'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = async (row: Role) => {
  isEdit.value = true
  dialogTitle.value = '编辑角色'
  currentRow.value = row
  
  try {
    const detail = await roleApi.getDetail(row.id)
    Object.assign(formData, {
      role_code: detail.role_code,
      role_name: detail.role_name,
      description: detail.description,
      status: detail.status,
      sort_order: detail.sort_order,
      permission_ids: detail.permission_ids || [],
      remark: detail.remark,
    })
    dialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取角色详情失败')
  }
}

// 查看
const handleView = async (row: Role) => {
  try {
    const detail = await roleApi.getDetail(row.id)
    currentRow.value = detail
    detailVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取角色详情失败')
  }
}

// 删除
const handleDelete = async (row: Role) => {
  try {
    await ElMessageBox.confirm('确定要删除该角色吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await roleApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 分配权限
const handleAssignPermissions = async (row: Role) => {
  try {
    const detail = await roleApi.getDetail(row.id)
    currentRole.value = detail
    
    // 等待权限树加载完成
    await fetchPermissionTree()
    
    // 等待DOM更新
    await new Promise((resolve) => setTimeout(resolve, 100))
    
    // 设置已选中的权限
    if (permissionTreeRef.value && detail.permission_ids) {
      permissionTreeRef.value.setCheckedKeys(detail.permission_ids)
    }
    
    permissionDialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取角色详情失败')
  }
}

// 提交权限分配
const handlePermissionSubmit = async () => {
  if (!currentRole.value || !permissionTreeRef.value) return

  permissionSubmitLoading.value = true
  try {
    const checkedKeys = permissionTreeRef.value.getCheckedKeys() as number[]
    const halfCheckedKeys = permissionTreeRef.value.getHalfCheckedKeys() as number[]
    // 合并完全选中和半选中的节点（半选中的节点表示父节点，应该包含所有子节点）
    const allKeys = [...checkedKeys, ...halfCheckedKeys]
    
    await roleApi.update(currentRole.value.id, {
      permission_ids: allKeys,
    })
    ElMessage.success('权限分配成功')
    permissionDialogVisible.value = false
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '权限分配失败')
  } finally {
    permissionSubmitLoading.value = false
  }
}

// 权限对话框关闭
const handlePermissionDialogClose = () => {
  currentRole.value = null
  if (permissionTreeRef.value) {
    permissionTreeRef.value.setCheckedKeys([])
  }
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const data: RoleFormData = {
        role_code: formData.role_code,
        role_name: formData.role_name,
        description: formData.description,
        status: formData.status,
        sort_order: formData.sort_order,
        permission_ids: formData.permission_ids,
        remark: formData.remark,
      }
      
      if (isEdit.value && currentRow.value) {
        await roleApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        await roleApi.create(data)
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
    role_code: '',
    role_name: '',
    description: null,
    status: 1,
    sort_order: 0,
    permission_ids: [],
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
  fetchData()
  fetchPermissionTree()
})
</script>

<style scoped lang="scss">
.role-list {
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

  .permission-tree {
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    padding: 10px;

    .tree-node-label {
      display: flex;
      align-items: center;
    }
  }
}
</style>
