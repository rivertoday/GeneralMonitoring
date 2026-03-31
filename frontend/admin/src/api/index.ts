/**
 * Axios实例配置
 */
import axios from 'axios'
import type { AxiosInstance, AxiosResponse } from 'axios'
import { API_BASE_URL, API_PREFIX, REQUEST_TIMEOUT } from './constants'
import type { ApiResponse } from './types'

// 创建Axios实例
const service: AxiosInstance = axios.create({
  baseURL: API_BASE_URL + API_PREFIX,
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    const res = response.data

    // 如果响应状态码不是200，说明请求失败
    if (res.code !== 200) {
      // Token过期或无效，清除token并跳转到登录页
      if (res.code === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        // 这里可以使用router跳转到登录页，但为了避免循环依赖，先不引入router
        // window.location.href = '/login'
      }

      // 返回错误信息
      return Promise.reject(new Error(res.message || '请求失败'))
    }

    // 直接返回数据部分（res.data）
    return res.data
  },
  (error) => {
    console.error('响应错误:', error)

    // 处理HTTP错误状态码
    if (error.response) {
      const { status, data } = error.response

      // 如果后端返回的是统一格式的错误响应（包含code和message）
      if (data && typeof data === 'object' && 'message' in data) {
        // 对于401错误，如果是登录接口，不清除token（因为还没有token）
        if (status === 401 && !error.config?.url?.includes('/login/')) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
        }
        return Promise.reject(new Error(data.message || '请求失败'))
      }

      // 处理标准HTTP错误
      switch (status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          if (!error.config?.url?.includes('/login/')) {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
          }
          return Promise.reject(new Error(data?.message || '未授权，请重新登录'))
        case 403:
          return Promise.reject(new Error(data?.message || '没有权限访问'))
        case 404:
          return Promise.reject(new Error(data?.message || '请求的资源不存在'))
        case 500:
          return Promise.reject(new Error(data?.message || '服务器错误'))
        default:
          return Promise.reject(new Error(data?.message || `请求失败: ${status}`))
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      return Promise.reject(new Error('网络错误，请检查网络连接'))
    } else {
      // 其他错误
      return Promise.reject(new Error(error.message || '请求失败'))
    }
  }
)

export default service

