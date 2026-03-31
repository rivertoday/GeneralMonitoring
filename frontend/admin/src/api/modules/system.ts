/**
 * 系统管理模块API
 */
import { get, post, put, patch, del, getList } from '../request'
import type {
  User,
  UserDetail,
  UserListParams,
  UserFormData,
  Role,
  RoleListParams,
  RoleFormData,
  Permission,
  PermissionListParams,
  PermissionFormData,
  Organization,
  OrganizationListParams,
  OrganizationFormData,
  DataSource,
  DataSourceListParams,
  DataSourceFormData,
  MessageTemplate,
  MessageTemplateListParams,
  MessageTemplateFormData,
} from '@/types/modules/system'

/**
 * 用户API
 */
export const userApi = {
  // 获取用户列表
  getList: (params?: UserListParams) => {
    return getList<User>('/users/users/', params)
  },

  // 获取用户详情
  getDetail: (id: number) => {
    return get<UserDetail>(`/users/users/${id}/`)
  },

  // 获取当前用户信息
  getMe: () => {
    return get<UserDetail>('/users/users/me/')
  },

  // 创建用户
  create: (data: UserFormData) => {
    return post<UserDetail>('/users/users/', data)
  },

  // 更新用户
  update: (id: number, data: Partial<UserFormData>) => {
    return put<UserDetail>(`/users/users/${id}/`, data)
  },

  // 部分更新用户
  partialUpdate: (id: number, data: Partial<UserFormData>) => {
    return patch<UserDetail>(`/users/users/${id}/`, data)
  },

  // 更新当前用户信息
  updateMe: (data: Partial<UserFormData>) => {
    return patch<UserDetail>('/users/users/update_me/', data)
  },

  // 删除用户
  delete: (id: number) => {
    return del(`/users/users/${id}/`)
  },

  // 修改密码
  changePassword: (id: number, data: { old_password: string; new_password: string; confirm_password: string }) => {
    return post(`/users/users/${id}/change_password/`, data)
  },
}

/**
 * 角色API
 */
export const roleApi = {
  // 获取角色列表
  getList: (params?: RoleListParams) => {
    return getList<Role>('/users/roles/', params)
  },

  // 获取角色详情
  getDetail: (id: number) => {
    return get<Role>(`/users/roles/${id}/`)
  },

  // 创建角色
  create: (data: RoleFormData) => {
    return post<Role>('/users/roles/', data)
  },

  // 更新角色
  update: (id: number, data: Partial<RoleFormData>) => {
    return put<Role>(`/users/roles/${id}/`, data)
  },

  // 部分更新角色
  partialUpdate: (id: number, data: Partial<RoleFormData>) => {
    return patch<Role>(`/users/roles/${id}/`, data)
  },

  // 删除角色
  delete: (id: number) => {
    return del(`/users/roles/${id}/`)
  },
}

/**
 * 权限API
 */
export const permissionApi = {
  // 获取权限列表
  getList: (params?: PermissionListParams) => {
    return getList<Permission>('/users/permissions/', params)
  },

  // 获取权限树
  getTree: () => {
    return get<Permission[]>('/users/permissions/tree/')
  },

  // 获取权限详情
  getDetail: (id: number) => {
    return get<Permission>(`/users/permissions/${id}/`)
  },

  // 创建权限
  create: (data: PermissionFormData) => {
    return post<Permission>('/users/permissions/', data)
  },

  // 更新权限
  update: (id: number, data: Partial<PermissionFormData>) => {
    return put<Permission>(`/users/permissions/${id}/`, data)
  },

  // 部分更新权限
  partialUpdate: (id: number, data: Partial<PermissionFormData>) => {
    return patch<Permission>(`/users/permissions/${id}/`, data)
  },

  // 删除权限
  delete: (id: number) => {
    return del(`/users/permissions/${id}/`)
  },
}

/**
 * 组织API
 */
export const organizationApi = {
  // 获取组织列表
  getList: (params?: OrganizationListParams) => {
    return getList<Organization>('/users/organizations/', params)
  },

  // 获取组织树
  getTree: () => {
    return get<Organization[]>('/users/organizations/tree/')
  },

  // 获取组织详情
  getDetail: (id: number) => {
    return get<Organization>(`/users/organizations/${id}/`)
  },

  // 创建组织
  create: (data: OrganizationFormData) => {
    return post<Organization>('/users/organizations/', data)
  },

  // 更新组织
  update: (id: number, data: Partial<OrganizationFormData>) => {
    return put<Organization>(`/users/organizations/${id}/`, data)
  },

  // 部分更新组织
  partialUpdate: (id: number, data: Partial<OrganizationFormData>) => {
    return patch<Organization>(`/users/organizations/${id}/`, data)
  },

  // 删除组织
  delete: (id: number) => {
    return del(`/users/organizations/${id}/`)
  },
}

/**
 * 数据源API
 */
export const datasourceApi = {
  // 获取数据源列表
  getList: (params?: DataSourceListParams) => {
    return getList<DataSource>('/system/data-sources/', params)
  },

  // 获取数据源详情
  getDetail: (id: number) => {
    return get<DataSource>(`/system/data-sources/${id}/`)
  },

  // 创建数据源
  create: (data: DataSourceFormData) => {
    return post<DataSource>('/system/data-sources/', data)
  },

  // 更新数据源
  update: (id: number, data: Partial<DataSourceFormData>) => {
    return put<DataSource>(`/system/data-sources/${id}/`, data)
  },

  // 部分更新数据源
  partialUpdate: (id: number, data: Partial<DataSourceFormData>) => {
    return patch<DataSource>(`/system/data-sources/${id}/`, data)
  },

  // 删除数据源
  delete: (id: number) => {
    return del(`/system/data-sources/${id}/`)
  },

  // 同步数据源
  sync: (id: number) => {
    return post<DataSource>(`/system/data-sources/${id}/sync/`)
  },

  // 获取数据源统计
  getStatistics: () => {
    return get('/system/data-sources/statistics/')
  },
}

/**
 * 消息模板API
 */
export const messageTemplateApi = {
  // 获取消息模板列表
  getList: (params?: MessageTemplateListParams) => {
    return getList<MessageTemplate>('/system/message-templates/', params)
  },

  // 获取消息模板详情
  getDetail: (id: number) => {
    return get<MessageTemplate>(`/system/message-templates/${id}/`)
  },

  // 创建消息模板
  create: (data: MessageTemplateFormData) => {
    return post<MessageTemplate>('/system/message-templates/', data)
  },

  // 更新消息模板
  update: (id: number, data: Partial<MessageTemplateFormData>) => {
    return put<MessageTemplate>(`/system/message-templates/${id}/`, data)
  },

  // 部分更新消息模板
  partialUpdate: (id: number, data: Partial<MessageTemplateFormData>) => {
    return patch<MessageTemplate>(`/system/message-templates/${id}/`, data)
  },

  // 删除消息模板
  delete: (id: number) => {
    return del(`/system/message-templates/${id}/`)
  },
}

