/**
 * 系统管理模块类型定义
 */

/**
 * 性别类型
 */
export type Gender = 0 | 1 | 2 // 0-未知，1-男，2-女

/**
 * 状态类型
 */
export type Status = 0 | 1 // 0-禁用，1-启用

/**
 * 组织类型
 */
export type OrgType = 1 | 2 | 3 // 1-政府部门，2-企业单位，3-事业单位

/**
 * 权限类型
 */
export type PermissionType = 1 | 2 | 3 // 1-菜单，2-按钮，3-接口

/**
 * 用户信息（列表）
 */
export interface User {
  id: number
  username: string
  real_name?: string | null
  email?: string | null
  phone?: string | null
  avatar?: string | null
  gender?: Gender
  gender_display?: string
  status: Status
  organization?: number | null
  organization_name?: string | null
  roles?: Array<{ id: number; role_name: string }>
  last_login_at?: string | null
  last_login_ip?: string | null
  created_at: string
  updated_at: string
}

/**
 * 用户详情
 */
export interface UserDetail extends Omit<User, 'organization'> {
  organization?: Organization | null
  organization_id?: number | null
  roles?: Role[]
  role_ids?: number[]
  permissions?: Permission[]
  is_staff?: boolean
  is_superuser?: boolean
  remark?: string | null
}

/**
 * 用户列表查询参数
 */
export interface UserListParams {
  page?: number
  page_size?: number
  username?: string
  status?: Status
  organization_id?: number
  search?: string
}

/**
 * 用户表单数据
 */
export interface UserFormData {
  username: string
  password?: string
  real_name?: string | null
  email?: string | null
  phone?: string | null
  avatar?: string | null
  gender?: Gender
  status?: Status
  organization_id?: number | null
  role_ids?: number[]
  is_staff?: boolean
  is_superuser?: boolean
  remark?: string | null
}

/**
 * 角色信息
 */
export interface Role {
  id: number
  role_code: string
  role_name: string
  description?: string | null
  status: Status
  sort_order: number
  remark?: string | null
  permissions?: Permission[]
  permission_ids?: number[]
  created_at: string
  updated_at: string
}

/**
 * 角色列表查询参数
 */
export interface RoleListParams {
  page?: number
  page_size?: number
  role_code?: string
  role_name?: string
  status?: Status
  search?: string
}

/**
 * 角色表单数据
 */
export interface RoleFormData {
  role_code: string
  role_name: string
  description?: string | null
  status?: Status
  sort_order?: number
  permission_ids?: number[]
  remark?: string | null
}

/**
 * 权限信息
 */
export interface Permission {
  id: number
  permission_code: string
  permission_name: string
  permission_type: PermissionType
  permission_type_display?: string
  parent_id: number
  parent_name?: string | null
  path?: string | null
  component?: string | null
  icon?: string | null
  api_path?: string | null
  http_method?: string | null
  description?: string | null
  status: Status
  sort_order: number
  remark?: string | null
  children?: Permission[]
  created_at: string
  updated_at: string
}

/**
 * 权限列表查询参数
 */
export interface PermissionListParams {
  page?: number
  page_size?: number
  permission_code?: string
  permission_name?: string
  permission_type?: PermissionType
  parent_id?: number
  status?: Status
  search?: string
}

/**
 * 权限表单数据
 */
export interface PermissionFormData {
  permission_code: string
  permission_name: string
  permission_type: PermissionType
  parent_id?: number
  path?: string | null
  component?: string | null
  icon?: string | null
  api_path?: string | null
  http_method?: string | null
  description?: string | null
  status?: Status
  sort_order?: number
  remark?: string | null
}

/**
 * 组织信息
 */
export interface Organization {
  id: number
  org_code: string
  org_name: string
  parent_id: number
  parent_name?: string | null
  org_type: OrgType
  org_type_display?: string
  level: number
  leader?: string | null
  phone?: string | null
  address?: string | null
  description?: string | null
  status: Status
  sort_order: number
  remark?: string | null
  children?: Organization[]
  created_at: string
  updated_at: string
}

/**
 * 组织列表查询参数
 */
export interface OrganizationListParams {
  page?: number
  page_size?: number
  org_code?: string
  org_name?: string
  parent_id?: number
  org_type?: OrgType
  status?: Status
  search?: string
}

/**
 * 组织表单数据
 */
export interface OrganizationFormData {
  org_code: string
  org_name: string
  parent_id?: number
  org_type?: OrgType
  level?: number
  leader?: string | null
  phone?: string | null
  address?: string | null
  description?: string | null
  status?: Status
  sort_order?: number
  remark?: string | null
}

/**
 * 数据源类型
 */
export type SourceType = 1 | 2 | 3 // 1-API接口，2-数据库，3-文件

/**
 * 行业类型
 */
export type IndustryType = 1 | 2 | 3 | 4 | 5 // 1-气象，2-危化，3-防汛，4-交通运输，5-森林火灾

/**
 * 数据源信息
 */
export interface DataSource {
  id: number
  source_code: string
  source_name: string
  source_type: SourceType
  source_type_display?: string
  industry_type: IndustryType
  industry_type_display?: string
  api_url?: string | null
  api_method?: string | null
  api_params?: string | null
  api_params_dict?: Record<string, any> | null
  db_host?: string | null
  db_port?: number | null
  db_name?: string | null
  db_user?: string | null
  db_password?: string | null
  db_table?: string | null
  sync_interval?: number | null
  last_sync_at?: string | null
  status: Status
  description?: string | null
  remark?: string | null
  created_at: string
  updated_at: string
}

/**
 * 数据源列表查询参数
 */
export interface DataSourceListParams {
  page?: number
  page_size?: number
  source_type?: SourceType
  industry_type?: IndustryType
  status?: Status
  search?: string
}

/**
 * 数据源表单数据
 */
export interface DataSourceFormData {
  source_code?: string
  source_name: string
  source_type: SourceType
  industry_type: IndustryType
  api_url?: string | null
  api_method?: string | null
  api_params?: string | null
  db_host?: string | null
  db_port?: number | null
  db_name?: string | null
  db_user?: string | null
  db_password?: string | null
  db_table?: string | null
  sync_interval?: number | null
  status?: Status
  description?: string | null
  remark?: string | null
}

/**
 * 消息模板类型
 */
export type TemplateType = 1 | 2 | 3 // 1-系统消息，2-短信，3-邮件

/**
 * 消息类型
 */
export type MessageType = 1 | 2 | 3 | 4 | 5 // 1-预警通知，2-报警通知，3-简报推送，4-叫应通知，5-其他

/**
 * 消息模板信息
 */
export interface MessageTemplate {
  id: number
  template_code: string
  template_name: string
  template_type: TemplateType
  template_type_display?: string
  message_type: MessageType
  message_type_display?: string
  subject?: string | null
  content: string
  variables?: string | null
  variables_dict?: Record<string, any> | null
  status: Status
  description?: string | null
  remark?: string | null
  created_at: string
  updated_at: string
}

/**
 * 消息模板列表查询参数
 */
export interface MessageTemplateListParams {
  page?: number
  page_size?: number
  template_type?: TemplateType
  message_type?: MessageType
  status?: Status
  search?: string
}

/**
 * 消息模板表单数据
 */
export interface MessageTemplateFormData {
  template_code?: string
  template_name: string
  template_type: TemplateType
  message_type: MessageType
  subject?: string | null
  content: string
  variables?: string | null
  status?: Status
  description?: string | null
  remark?: string | null
}

