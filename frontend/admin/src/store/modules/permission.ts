/**
 * 权限状态管理
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { RouteRecordRaw } from 'vue-router'

export const usePermissionStore = defineStore('permission', () => {
  // 状态
  const routes = ref<RouteRecordRaw[]>([])
  const permissions = ref<string[]>([])
  const roles = ref<string[]>([])

  // 设置路由
  function setRoutes(newRoutes: RouteRecordRaw[]) {
    routes.value = newRoutes
  }

  // 添加路由
  function addRoutes(newRoutes: RouteRecordRaw[]) {
    routes.value.push(...newRoutes)
  }

  // 设置权限
  function setPermissions(newPermissions: string[]) {
    permissions.value = newPermissions
  }

  // 添加权限
  function addPermissions(newPermissions: string[]) {
    permissions.value = [...new Set([...permissions.value, ...newPermissions])]
  }

  // 设置角色
  function setRoles(newRoles: string[]) {
    roles.value = newRoles
  }

  // 添加角色
  function addRoles(newRoles: string[]) {
    roles.value = [...new Set([...roles.value, ...newRoles])]
  }

  // 检查权限
  function hasPermission(permission: string): boolean {
    return permissions.value.includes(permission)
  }

  // 检查角色
  function hasRole(role: string): boolean {
    return roles.value.includes(role)
  }

  // 检查多个权限（需要全部满足）
  function hasAllPermissions(perms: string[]): boolean {
    return perms.every((perm) => permissions.value.includes(perm))
  }

  // 检查多个权限（满足任意一个即可）
  function hasAnyPermission(perms: string[]): boolean {
    return perms.some((perm) => permissions.value.includes(perm))
  }

  // 检查多个角色（需要全部满足）
  function hasAllRoles(roleList: string[]): boolean {
    return roleList.every((role) => roles.value.includes(role))
  }

  // 检查多个角色（满足任意一个即可）
  function hasAnyRole(roleList: string[]): boolean {
    return roleList.some((role) => roles.value.includes(role))
  }

  // 清除所有权限和角色
  function clear() {
    routes.value = []
    permissions.value = []
    roles.value = []
  }

  return {
    // 状态
    routes,
    permissions,
    roles,
    // 方法
    setRoutes,
    addRoutes,
    setPermissions,
    addPermissions,
    setRoles,
    addRoles,
    hasPermission,
    hasRole,
    hasAllPermissions,
    hasAnyPermission,
    hasAllRoles,
    hasAnyRole,
    clear,
  }
})

