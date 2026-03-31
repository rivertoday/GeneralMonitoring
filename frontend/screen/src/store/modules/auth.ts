/**
 * 认证状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { TOKEN_KEY, REFRESH_TOKEN_KEY } from '@/api/constants'
import type { UserInfo, LoginParams } from '../types'
import { post, get } from '@/api/request'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const token = ref<string | null>(localStorage.getItem(TOKEN_KEY))
  const refreshToken = ref<string | null>(localStorage.getItem(REFRESH_TOKEN_KEY))
  const user = ref<UserInfo | null>(null)
  const permissions = ref<string[]>([])
  const roles = ref<string[]>([])

  // 计算属性
  const isAuthenticated = computed(() => !!token.value)
  const hasPermission = computed(() => (permission: string) => {
    return permissions.value.includes(permission)
  })
  const hasRole = computed(() => (role: string) => {
    return roles.value.includes(role)
  })

  // 登录
  async function login(params: LoginParams) {
    try {
      const response = await post<{
        access_token: string
        refresh_token: string
        user: UserInfo
      }>('/auth/login/', params)
      
      // 保存token
      token.value = response.access_token
      refreshToken.value = response.refresh_token
      localStorage.setItem(TOKEN_KEY, response.access_token)
      localStorage.setItem(REFRESH_TOKEN_KEY, response.refresh_token)
      
      // 保存用户信息
      user.value = response.user
      
      // 提取角色代码数组
      if (response.user.roles && Array.isArray(response.user.roles)) {
        roles.value = response.user.roles.map((role) => role.role_code || role.role_name)
      } else {
        roles.value = []
      }
      
      // 提取权限代码数组
      if (response.user.permissions && Array.isArray(response.user.permissions)) {
        permissions.value = response.user.permissions.map((perm) => perm.permission_code || perm.permission_name)
      } else {
        permissions.value = []
      }
      
      return response
    } catch (error) {
      console.error('登录失败:', error)
      throw error
    }
  }

  // 登出
  function logout() {
    token.value = null
    refreshToken.value = null
    user.value = null
    permissions.value = []
    roles.value = []
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
  }

  // 刷新Token
  async function refreshAccessToken() {
    if (!refreshToken.value) {
      throw new Error('没有刷新Token')
    }

    try {
      const response = await post<{ access_token: string }>('/auth/refresh/', {
        refresh: refreshToken.value,
      })
      
      token.value = response.access_token
      localStorage.setItem(TOKEN_KEY, response.access_token)
      
      return response
    } catch (error) {
      console.error('刷新Token失败:', error)
      logout()
      throw error
    }
  }

  // 获取当前用户信息
  async function fetchUserInfo() {
    try {
      const response = await get<UserInfo>('/auth/user-info/')
      user.value = response
      
      // 提取角色代码数组
      if (response.roles && Array.isArray(response.roles)) {
        roles.value = response.roles.map((role) => role.role_code || role.role_name)
      } else {
        roles.value = []
      }
      
      // 提取权限代码数组
      if (response.permissions && Array.isArray(response.permissions)) {
        permissions.value = response.permissions.map((perm) => perm.permission_code || perm.permission_name)
      } else {
        permissions.value = []
      }
      
      return response
    } catch (error) {
      console.error('获取用户信息失败:', error)
      throw error
    }
  }

  // 设置用户信息
  function setUserInfo(userInfo: UserInfo) {
    user.value = userInfo
    
    // 提取角色代码数组
    if (userInfo.roles && Array.isArray(userInfo.roles)) {
      roles.value = userInfo.roles.map((role) => role.role_code || role.role_name)
    } else {
      roles.value = []
    }
    
    // 提取权限代码数组
    if (userInfo.permissions && Array.isArray(userInfo.permissions)) {
      permissions.value = userInfo.permissions.map((perm) => perm.permission_code || perm.permission_name)
    } else {
      permissions.value = []
    }
  }

  // 同步token（用于单点登录）
  function syncToken() {
    const tokenInStorage = localStorage.getItem(TOKEN_KEY)
    const refreshTokenInStorage = localStorage.getItem(REFRESH_TOKEN_KEY)
    if (tokenInStorage !== token.value) {
      token.value = tokenInStorage
    }
    if (refreshTokenInStorage !== refreshToken.value) {
      refreshToken.value = refreshTokenInStorage
    }
  }

  return {
    // 状态
    token,
    refreshToken,
    user,
    permissions,
    roles,
    // 计算属性
    isAuthenticated,
    hasPermission,
    hasRole,
    // 方法
    login,
    logout,
    refreshAccessToken,
    fetchUserInfo,
    setUserInfo,
    syncToken,
  }
})

