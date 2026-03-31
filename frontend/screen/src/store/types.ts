/**
 * Store类型定义
 */

/**
 * 角色信息
 */
export interface RoleInfo {
  id: number
  role_code: string
  role_name: string
  description?: string | null
  status: number
  sort_order: number
  remark?: string | null
  created_at: string
  updated_at: string
}

/**
 * 权限信息
 */
export interface PermissionInfo {
  id: number
  permission_code: string
  permission_name: string
  permission_type: number
  permission_type_display: string
  parent_id: number
  parent_name?: string | null
  path?: string | null
  component?: string | null
  icon?: string | null
  api_path?: string | null
  http_method?: string | null
  description?: string | null
  status: number
  sort_order: number
  remark?: string | null
  created_at: string
  updated_at: string
}

/**
 * 用户信息
 */
export interface UserInfo {
  id: number
  username: string
  real_name: string
  email?: string | null
  phone?: string | null
  avatar?: string | null
  gender?: number
  gender_display?: string
  status: number
  organization?: number | null
  organization_id?: number | null
  roles?: RoleInfo[]
  permissions?: PermissionInfo[]
  last_login_at?: string | null
  last_login_ip?: string | null
  remark?: string | null
  created_at?: string
  updated_at?: string
}

/**
 * 登录参数
 */
export interface LoginParams {
  username: string
  password: string
}

/**
 * 登录响应
 */
export interface LoginResponse {
  access: string
  refresh: string
  user: UserInfo
}

