/**
 * 权限指令
 */
import type { DirectiveBinding } from 'vue'
import { useAuthStore } from '@/store/modules/auth'
import { usePermissionStore } from '@/store/modules/permission'

function checkPermission(
  el: HTMLElement,
  binding: DirectiveBinding<string | string[]>
) {
  const { value } = binding
  const authStore = useAuthStore()
  const permissionStore = usePermissionStore()

  if (!value) {
    return
  }

  const permissions = Array.isArray(value) ? value : [value]
  const hasPermission = permissions.some(
    (perm) =>
      authStore.hasPermission(perm) || permissionStore.hasPermission(perm)
  )

  if (!hasPermission) {
    el.style.display = 'none'
    // 或者完全移除元素
    // el.parentNode?.removeChild(el)
  } else {
    el.style.display = ''
  }
}

export default {
  mounted(el: HTMLElement, binding: DirectiveBinding) {
    checkPermission(el, binding)
  },
  updated(el: HTMLElement, binding: DirectiveBinding) {
    checkPermission(el, binding)
  },
}

