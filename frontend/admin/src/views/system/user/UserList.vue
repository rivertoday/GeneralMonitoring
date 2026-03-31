<template>
  <div class="user-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <h2>用户管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新增用户
      </el-button>
    </div>

    <!-- 搜索筛选区域 -->
    <el-card class="search-card">
      <el-form :model="searchForm" :inline="true">
        <el-form-item label="用户名">
          <el-input
            v-model="searchForm.username"
            placeholder="请输入用户名"
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
        <el-form-item label="所属组织">
          <el-select
            v-model="searchForm.organization_id"
            placeholder="请选择组织"
            clearable
            filterable
            style="width: 200px"
          >
            <el-option
              v-for="org in organizationList"
              :key="org.id"
              :label="org.org_name"
              :value="org.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="关键词">
          <el-input
            v-model="searchForm.search"
            placeholder="请输入用户名/姓名/邮箱/手机"
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
        <el-table-column prop="username" label="用户名" width="120" />
        <el-table-column prop="real_name" label="真实姓名" width="120" />
        <el-table-column prop="email" label="邮箱" width="180" show-overflow-tooltip />
        <el-table-column prop="phone" label="手机号" width="120" />
        <el-table-column label="性别" width="80">
          <template #default="{ row }">
            {{ row.gender_display || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="organization_name" label="所属组织" width="150" show-overflow-tooltip />
        <el-table-column label="角色" width="150">
          <template #default="{ row }">
            <el-tag
              v-for="role in row.roles"
              :key="role.id"
              size="small"
              style="margin-right: 5px"
            >
              {{ role.role_name }}
            </el-tag>
            <span v-if="!row.roles || row.roles.length === 0">-</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_login_at" label="最后登录时间" width="160" />
        <el-table-column prop="last_login_ip" label="最后登录IP" width="120" />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="handleView(row)">
              查看
            </el-button>
            <el-button type="primary" link size="small" @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="primary" link size="small" @click="handleAssignRoles(row)">
              分配角色
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
            <el-form-item label="用户名" prop="username">
              <el-input v-model="formData.username" placeholder="请输入用户名" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="真实姓名" prop="real_name">
              <el-input v-model="formData.real_name" placeholder="请输入真实姓名" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="formData.email" placeholder="请输入邮箱地址" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="formData.phone" placeholder="请输入手机号" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="formData.gender" placeholder="请选择性别" style="width: 100%">
                <el-option label="未知" :value="0" />
                <el-option label="男" :value="1" />
                <el-option label="女" :value="2" />
              </el-select>
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
            <el-form-item label="所属组织" prop="organization_id">
              <el-select
                v-model="formData.organization_id"
                placeholder="请选择所属组织"
                filterable
                clearable
                style="width: 100%"
              >
                <el-option
                  v-for="org in organizationList"
                  :key="org.id"
                  :label="org.org_name"
                  :value="org.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="是否为员工">
              <el-switch v-model="formData.is_staff" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item v-if="!isEdit" label="密码" prop="password">
              <el-input
                v-model="formData.password"
                type="password"
                placeholder="请输入密码"
                show-password
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="超级用户">
              <el-switch v-model="formData.is_superuser" />
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
    <el-dialog v-model="detailVisible" title="用户详情" width="900px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户名">{{ currentRow?.username }}</el-descriptions-item>
        <el-descriptions-item label="真实姓名">{{ currentRow?.real_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ currentRow?.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ currentRow?.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ currentRow?.gender_display || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentRow?.status === 1 ? 'success' : 'danger'">
            {{ currentRow?.status === 1 ? '启用' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="所属组织">{{ currentRow?.organization_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="是否为员工">
          <el-tag :type="currentUser?.is_staff ? 'success' : 'info'">
            {{ currentUser?.is_staff ? '是' : '否' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="是否为超级用户">
          <el-tag :type="currentUser?.is_superuser ? 'warning' : 'info'">
            {{ currentUser?.is_superuser ? '是' : '否' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="角色">
          <el-tag
            v-for="role in currentRow?.roles"
            :key="role.id"
            size="small"
            style="margin-right: 5px"
          >
            {{ role.role_name }}
          </el-tag>
          <span v-if="!currentRow?.roles || currentRow.roles.length === 0">-</span>
        </el-descriptions-item>
        <el-descriptions-item label="最后登录时间">{{ currentRow?.last_login_at || '-' }}</el-descriptions-item>
        <el-descriptions-item label="最后登录IP">{{ currentRow?.last_login_ip || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentUser?.remark || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentRow?.created_at }}</el-descriptions-item>
        <el-descriptions-item label="更新时间">{{ currentRow?.updated_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <!-- 分配角色对话框 -->
    <el-dialog
      v-model="roleDialogVisible"
      title="分配角色"
      width="600px"
      @close="handleRoleDialogClose"
    >
      <el-form label-width="100px">
        <el-form-item label="用户名">
          <el-input v-if="currentUser" v-model="currentUser.username" disabled />
        </el-form-item>
        <el-form-item label="选择角色">
          <el-checkbox-group v-model="selectedRoleIds">
            <el-checkbox
              v-for="role in roleList"
              :key="role.id"
              :label="role.id"
              :disabled="role.status === 0"
            >
              {{ role.role_name }}
              <el-tag v-if="role.status === 0" size="small" type="danger" style="margin-left: 5px">
                已禁用
              </el-tag>
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="roleSubmitLoading" @click="handleRoleSubmit">
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
import { userApi, organizationApi, roleApi } from '@/api/modules/system'
import type { User, UserDetail, UserFormData, Organization, Role, Status, Gender } from '@/types/modules/system'
import type { PaginatedResponse } from '@/api/types'

// 加载状态
const loading = ref(false)
const submitLoading = ref(false)
const roleSubmitLoading = ref(false)

// 表格数据
const tableData = ref<User[]>([])
const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0,
})

// 搜索表单
const searchForm = reactive({
  username: undefined as string | undefined,
  status: undefined as Status | undefined,
  organization_id: undefined as number | undefined,
  search: undefined as string | undefined,
})

// 对话框
const dialogVisible = ref(false)
const detailVisible = ref(false)
const roleDialogVisible = ref(false)
const dialogTitle = ref('新增用户')
const currentRow = ref<User | null>(null)
const currentUser = ref<UserDetail | null>(null)
const isEdit = ref(false)

// 表单
const formRef = ref<FormInstance>()
const formData = reactive<UserFormData>({
  username: '',
  password: '',
  real_name: null,
  email: null,
  phone: null,
  avatar: null,
  gender: 0,
  status: 1,
  organization_id: null,
  role_ids: [],
  is_staff: false,
  is_superuser: false,
  remark: null,
})

// 组织列表和角色列表
const organizationList = ref<Organization[]>([])
const roleList = ref<Role[]>([])
const selectedRoleIds = ref<number[]>([])

// 表单验证规则
const formRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在3到50个字符之间', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6个字符', trigger: 'blur' },
  ],
  email: [
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' },
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' },
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' },
  ],
}

// 获取组织列表（扁平化）
const fetchOrganizations = async () => {
  try {
    const response = await organizationApi.getTree()
    // 扁平化组织树，以便在el-select中使用
    const flattenOrganizations = (orgs: Organization[], result: Organization[] = []): Organization[] => {
      orgs.forEach((org) => {
        result.push(org)
        if (org.children) {
          flattenOrganizations(org.children, result)
        }
      })
      return result
    }
    organizationList.value = flattenOrganizations(response)
  } catch (error: any) {
    console.error('获取组织列表失败:', error)
  }
}

// 获取角色列表
const fetchRoles = async () => {
  try {
    const response = await roleApi.getList({ page_size: 1000 })
    roleList.value = response.results
  } catch (error: any) {
    console.error('获取角色列表失败:', error)
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
    const response = await userApi.getList(params)
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
    username: undefined,
    status: undefined,
    organization_id: undefined,
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
  dialogTitle.value = '新增用户'
  resetForm()
  dialogVisible.value = true
}

// 编辑
const handleEdit = async (row: User) => {
  isEdit.value = true
  dialogTitle.value = '编辑用户'
  currentRow.value = row
  
  try {
    const detail = await userApi.getDetail(row.id)
    Object.assign(formData, {
      username: detail.username,
      real_name: detail.real_name,
      email: detail.email,
      phone: detail.phone,
      avatar: detail.avatar,
      gender: detail.gender || 0,
      status: detail.status,
      organization_id: detail.organization_id,
      role_ids: detail.role_ids || [],
      is_staff: detail.is_staff || false,
      is_superuser: detail.is_superuser || false,
      remark: detail.remark,
    })
    dialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取用户详情失败')
  }
}

// 查看
const handleView = async (row: User) => {
  try {
    const detail = await userApi.getDetail(row.id)
    currentUser.value = detail as UserDetail
    currentRow.value = detail as User
    detailVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取用户详情失败')
  }
}

// 删除
const handleDelete = async (row: User) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await userApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '删除失败')
    }
  }
}

// 分配角色
const handleAssignRoles = async (row: User) => {
  try {
    const detail = await userApi.getDetail(row.id)
    currentUser.value = detail
    selectedRoleIds.value = detail.role_ids || []
    roleDialogVisible.value = true
  } catch (error: any) {
    ElMessage.error(error.message || '获取用户详情失败')
  }
}

// 提交角色分配
const handleRoleSubmit = async () => {
  if (!currentUser.value) return

  roleSubmitLoading.value = true
  try {
    await userApi.update(currentUser.value.id, {
      role_ids: selectedRoleIds.value,
    })
    ElMessage.success('角色分配成功')
    roleDialogVisible.value = false
    fetchData()
  } catch (error: any) {
    ElMessage.error(error.message || '角色分配失败')
  } finally {
    roleSubmitLoading.value = false
  }
}

// 角色对话框关闭
const handleRoleDialogClose = () => {
  currentUser.value = null
  selectedRoleIds.value = []
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const data: UserFormData = {
        username: formData.username,
        real_name: formData.real_name,
        email: formData.email,
        phone: formData.phone,
        avatar: formData.avatar,
        gender: formData.gender,
        status: formData.status,
        organization_id: formData.organization_id,
        role_ids: formData.role_ids,
        is_staff: formData.is_staff,
        is_superuser: formData.is_superuser,
        remark: formData.remark,
      }

      if (isEdit.value && currentRow.value) {
        // 编辑时不传密码，除非用户明确修改
        await userApi.update(currentRow.value.id, data)
        ElMessage.success('更新成功')
      } else {
        // 新增时必须传密码
        if (!formData.password) {
          ElMessage.error('请输入密码')
          submitLoading.value = false
          return
        }
        await userApi.create({
          ...data,
          password: formData.password,
        })
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
    username: '',
    password: '',
    real_name: null,
    email: null,
    phone: null,
    avatar: null,
    gender: 0,
    status: 1,
    organization_id: null,
    role_ids: [],
    is_staff: false,
    is_superuser: false,
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

// 初始化
onMounted(() => {
  fetchData()
  fetchOrganizations()
  fetchRoles()
})
</script>

<style scoped lang="scss">
.user-list {
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
