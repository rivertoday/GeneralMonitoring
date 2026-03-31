/**
 * API类型定义
 */

/**
 * API响应基础结构
 */
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  errors?: Record<string, string[]>
}

/**
 * 分页响应结构
 */
export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

/**
 * 分页请求参数
 */
export interface PaginationParams {
  page?: number
  page_size?: number
}

/**
 * 排序参数
 */
export interface OrderingParams {
  ordering?: string
}

/**
 * 搜索参数
 */
export interface SearchParams {
  search?: string
}

/**
 * 列表请求参数（包含分页、排序、搜索）
 */
export interface ListParams extends PaginationParams, OrderingParams, SearchParams {
  [key: string]: any
}

/**
 * 登录请求参数
 */
export interface LoginParams {
  username: string
  password: string
}

/**
 * 登录响应数据
 */
export interface LoginResponse {
  access: string
  refresh: string
  user: {
    id: number
    username: string
    real_name: string
    email: string
    phone: string
    organization_id: number | null
  }
}

/**
 * 刷新Token请求参数
 */
export interface RefreshTokenParams {
  refresh: string
}

/**
 * 刷新Token响应数据
 */
export interface RefreshTokenResponse {
  access: string
  refresh: string
}

