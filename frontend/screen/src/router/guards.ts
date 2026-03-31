/**
 * 路由守卫
 */
import type { Router } from 'vue-router'
import { TOKEN_KEY } from '@/api/constants'
import { useAuthStore } from '@/store/modules/auth'

/**
 * 白名单路由（不需要登录即可访问）
 */
const whiteList = ['/login']

/**
 * 设置路由守卫
 */
export function setupRouterGuard(router: Router) {
  const authStore = useAuthStore()

  // 监听localStorage变化（用于不同标签页之间的单点登录/退出）
  // 注意：storage事件只在不同标签页之间触发，同一标签页内的变化不会触发
  window.addEventListener('storage', (e) => {
    // 如果access_token被删除或修改，清除store中的token
    if (e.key === TOKEN_KEY) {
      if (!e.newValue) {
        // token被删除，清除store并跳转到登录页
        authStore.logout()
        if (router.currentRoute.value.path !== '/login') {
          router.push({
            path: '/login',
            query: { redirect: router.currentRoute.value.fullPath },
          })
        }
      } else if (e.newValue !== e.oldValue) {
        // token被修改，同步到store
        authStore.syncToken()
      }
    }
  })

  // 定时检查token（用于检测同一标签页内的token变化，如业务管理后台退出登录）
  // 每2秒检查一次localStorage中的token
  let tokenCheckInterval: ReturnType<typeof setInterval> | null = null
  
  const startTokenCheck = () => {
    if (tokenCheckInterval) {
      clearInterval(tokenCheckInterval)
    }
    tokenCheckInterval = setInterval(() => {
      const tokenInStorage = localStorage.getItem(TOKEN_KEY)
      // 如果localStorage中没有token但store中有，说明在另一个系统退出了
      if (!tokenInStorage && authStore.token) {
        authStore.logout()
        if (router.currentRoute.value.path !== '/login') {
          router.push({
            path: '/login',
            query: { redirect: router.currentRoute.value.fullPath },
          })
        }
      }
    }, 2000) // 每2秒检查一次
  }

  // 启动token检查
  startTokenCheck()

  // 认证守卫
  router.beforeEach(async (to, from, next) => {
    // 设置页面标题
    if (to.meta.title) {
      document.title = `${to.meta.title} - 风险监测预警系统`
    }

    // 每次路由跳转时，都重新从localStorage获取token（确保检测到token被清除）
    // 这是关键：直接从localStorage读取，不依赖store中的token
    const token = localStorage.getItem(TOKEN_KEY)

    // 如果在白名单中，直接放行
    if (whiteList.includes(to.path)) {
      // 如果已登录，访问登录页时重定向到首页
      if (token && to.path === '/login') {
        next('/overview')
        return
      }
      next()
      return
    }

    // 如果没有token，立即跳转到登录页（这是最重要的检查）
    if (!token) {
      // 清除store中的token（如果存在）
      if (authStore.token) {
        authStore.logout()
      }
      next({
        path: '/login',
        query: { redirect: to.fullPath },
      })
      return
    }

    // 有token，同步到store
    authStore.syncToken()
    
    // 验证token有效性：如果store中有token但没有用户信息，尝试获取用户信息
    if (authStore.token && !authStore.user) {
      try {
        await authStore.fetchUserInfo()
      } catch (error: any) {
        console.warn('获取用户信息失败:', error)
        // 如果获取失败（可能是401），清除token并跳转到登录页
        if (error.message?.includes('401') || error.message?.includes('未授权')) {
          authStore.logout()
          next({
            path: '/login',
            query: { redirect: to.fullPath },
          })
          return
        }
      }
    }

    // 继续访问
    next()
  })
}

