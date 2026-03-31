/**
 * 路由守卫
 */
import type { Router } from 'vue-router'
import { TOKEN_KEY } from '@/api/constants'
import { useAuthStore } from '@/store/modules/auth'
import { usePermissionStore } from '@/store/modules/permission'

/**
 * 白名单路由（不需要登录即可访问）
 */
const whiteList = ['/login']

/**
 * 路由前置守卫
 */
export function setupRouterGuard(router: Router) {
  router.beforeEach(async (to, _from, next) => {
    // 获取token
    const token = localStorage.getItem(TOKEN_KEY)

    // 如果在白名单中，直接放行
    if (whiteList.includes(to.path)) {
      // 如果已登录，访问登录页时重定向到首页
      if (token && to.path === '/login') {
        next('/dashboard')
        return
      }
      next()
      return
    }

    // 如果没有token，跳转到登录页
    if (!token) {
      next({
        path: '/login',
        query: { redirect: to.fullPath },
      })
      return
    }

    // 有token，继续访问（用户信息可以异步获取，不阻塞路由）
    const authStore = useAuthStore()
    const permissionStore = usePermissionStore()

    // 如果用户信息不存在，尝试异步获取（不阻塞路由）
    if (!authStore.user) {
      authStore.fetchUserInfo().catch((error) => {
        console.warn('获取用户信息失败:', error)
        // 如果是401错误，说明token无效，清除token
        if (error.message?.includes('401') || error.message?.includes('未授权')) {
          authStore.logout()
        }
      })
    }

    // 检查路由权限
    if (to.meta.requiresAuth !== false) {
      // 如果路由需要特定权限
      if (to.meta.permission) {
        const permission = Array.isArray(to.meta.permission)
          ? to.meta.permission
          : [to.meta.permission]
        
        const hasPermission = permission.some((perm) =>
          authStore.hasPermission(perm) || permissionStore.hasPermission(perm)
        )
        
        if (!hasPermission) {
          next({
            path: '/403',
            replace: true,
          })
          return
        }
      }

      // 如果路由需要特定角色
      if (to.meta.role) {
        const role = Array.isArray(to.meta.role)
          ? to.meta.role
          : [to.meta.role]
        
        const hasRole = role.some((r) =>
          authStore.hasRole(r) || permissionStore.hasRole(r)
        )
        
        if (!hasRole) {
          next({
            path: '/403',
            replace: true,
          })
          return
        }
      }
    }

    // 继续访问
    next()
  })

  // 路由后置守卫 - 设置页面标题
  router.afterEach((to) => {
    // 设置页面标题
    document.title = to.meta.title
      ? `${to.meta.title} - 风险监测预警系统`
      : '风险监测预警系统'
  })
}

