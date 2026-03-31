/**
 * API常量配置
 */

// API基础URL（开发环境）
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

// API版本
export const API_VERSION = 'v1'

// API前缀
export const API_PREFIX = `/api/${API_VERSION}`

// 请求超时时间（毫秒）
export const REQUEST_TIMEOUT = 30000

// Token存储键名
export const TOKEN_KEY = 'access_token'
export const REFRESH_TOKEN_KEY = 'refresh_token'

// 响应状态码
export const HTTP_STATUS = {
  SUCCESS: 200,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  SERVER_ERROR: 500,
} as const

