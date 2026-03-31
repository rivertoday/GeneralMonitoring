/**
 * HTTP请求封装
 * 提供常用的请求方法
 */
import service from './index'
import type { AxiosRequestConfig } from 'axios'
import type { ApiResponse, ListParams, PaginatedResponse } from './types'

/**
 * GET请求
 * 注意：响应拦截器已经提取了 data，所以返回的是 T 而不是 AxiosResponse<T>
 */
export function get<T = any>(
  url: string,
  params?: any,
  config?: AxiosRequestConfig
): Promise<T> {
  return service.get<T>(url, { params, ...config }) as Promise<T>
}

/**
 * POST请求
 */
export function post<T = any>(
  url: string,
  data?: any,
  config?: AxiosRequestConfig
): Promise<T> {
  return service.post<T>(url, data, config) as Promise<T>
}

/**
 * PUT请求
 */
export function put<T = any>(
  url: string,
  data?: any,
  config?: AxiosRequestConfig
): Promise<T> {
  return service.put<T>(url, data, config) as Promise<T>
}

/**
 * PATCH请求
 */
export function patch<T = any>(
  url: string,
  data?: any,
  config?: AxiosRequestConfig
): Promise<T> {
  return service.patch<T>(url, data, config) as Promise<T>
}

/**
 * DELETE请求
 */
export function del<T = any>(
  url: string,
  config?: AxiosRequestConfig
): Promise<T> {
  return service.delete<T>(url, config) as Promise<T>
}

/**
 * 获取分页列表
 */
export function getList<T = any>(
  url: string,
  params?: ListParams,
  config?: AxiosRequestConfig
): Promise<PaginatedResponse<T>> {
  return service.get<PaginatedResponse<T>>(url, { params, ...config }) as unknown as Promise<PaginatedResponse<T>>
}

export default service

