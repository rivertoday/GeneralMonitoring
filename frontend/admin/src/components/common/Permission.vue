<template>
  <slot v-if="hasAccess" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/store/modules/auth'
import { usePermissionStore } from '@/store/modules/permission'

interface Props {
  permission?: string | string[]
  role?: string | string[]
  requireAll?: boolean // 如果为true，需要满足所有权限/角色；如果为false，满足任意一个即可
}

const props = withDefaults(defineProps<Props>(), {
  requireAll: false,
})

const authStore = useAuthStore()
const permissionStore = usePermissionStore()

const hasAccess = computed(() => {
  // 如果既没有指定权限也没有指定角色，默认显示
  if (!props.permission && !props.role) {
    return true
  }

  // 检查权限
  if (props.permission) {
    const permissions = Array.isArray(props.permission)
      ? props.permission
      : [props.permission]

    const hasPermission = props.requireAll
      ? permissions.every(
          (perm) =>
            authStore.hasPermission(perm) || permissionStore.hasPermission(perm)
        )
      : permissions.some(
          (perm) =>
            authStore.hasPermission(perm) || permissionStore.hasPermission(perm)
        )

    if (!hasPermission) {
      return false
    }
  }

  // 检查角色
  if (props.role) {
    const roles = Array.isArray(props.role) ? props.role : [props.role]

    const hasRole = props.requireAll
      ? roles.every(
          (role) =>
            authStore.hasRole(role) || permissionStore.hasRole(role)
        )
      : roles.some(
          (role) =>
            authStore.hasRole(role) || permissionStore.hasRole(role)
        )

    if (!hasRole) {
      return false
    }
  }

  return true
})
</script>

