/**
 * HTTP请求封装
 * 提供常用的请求方法
 */
import service from './index'
import type { AxiosRequestConfig } from 'axios'
import type { ListParams, PaginatedResponse } from './types'

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

/**
 * 上传文件
 */
export function uploadFile<T = any>(
  url: string,
  file: File | FormData,
  onUploadProgress?: (progressEvent: any) => void
): Promise<T> {
  const formData = file instanceof FormData ? file : new FormData()
  if (file instanceof File) {
    formData.append('file', file)
  }

  return service.post<T>(url, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    onUploadProgress,
  }) as Promise<T>
}

/**
 * 下载文件
 */
export function downloadFile(
  url: string,
  params?: any,
  filename?: string
): Promise<void> {
  return service
    .get<Blob>(url, {
      params,
      responseType: 'blob',
    })
    .then((response: any) => {
      // 对于 blob 类型，响应拦截器可能返回的是 Blob 本身，或者需要从 response.data 获取
      const blob = response instanceof Blob ? response : (response.data || response)
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename || 'download'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
    })
}

export default service

