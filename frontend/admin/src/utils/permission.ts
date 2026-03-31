/**
 * 权限工具函数
 */
import { useAuthStore } from '@/store/modules/auth'
import { usePermissionStore } from '@/store/modules/permission'

/**
 * 检查是否有权限
 */
export function hasPermission(permission: string): boolean {
  const authStore = useAuthStore()
  const permissionStore = usePermissionStore()
  
  // 先检查Auth Store中的权限
  if (authStore.hasPermission(permission)) {
    return true
  }
  
  // 再检查Permission Store中的权限
  return permissionStore.hasPermission(permission)
}

/**
 * 检查是否有角色
 */
export function hasRole(role: string): boolean {
  const authStore = useAuthStore()
  const permissionStore = usePermissionStore()
  
  // 先检查Auth Store中的角色
  if (authStore.hasRole(role)) {
    return true
  }
  
  // 再检查Permission Store中的角色
  return permissionStore.hasRole(role)
}

/**
 * 检查是否有多个权限（全部满足）
 */
export function hasAllPermissions(permissions: string[]): boolean {
  const authStore = useAuthStore()
  const permissionStore = usePermissionStore()
  
  return (
    permissions.every((perm) => authStore.hasPermission(perm)) ||
    permissions.every((perm) => permissionStore.hasPermission(perm))
  )
}

/**
 * 检查是否有多个权限（满足任意一个）
 */
export function hasAnyPermission(permissions: string[]): boolean {
  const authStore = useAuthStore()
  const permissionStore = usePermissionStore()
  
  return (
    permissions.some((perm) => authStore.hasPermission(perm)) ||
    permissions.some((perm) => permissionStore.hasPermission(perm))
  )
}

/**
 * 检查是否有多个角色（全部满足）
 */
export function hasAllRoles(roles: string[]): boolean {
  const authStore = useAuthStore()
  const permissionStore = usePermissionStore()
  
  return (
    roles.every((role) => authStore.hasRole(role)) ||
    roles.every((role) => permissionStore.hasRole(role))
  )
}

/**
 * 检查是否有多个角色（满足任意一个）
 */
export function hasAnyRole(roles: string[]): boolean {
  const authStore = useAuthStore()
  const permissionStore = usePermissionStore()
  
  return (
    roles.some((role) => authStore.hasRole(role)) ||
    roles.some((role) => permissionStore.hasRole(role))
  )
}

