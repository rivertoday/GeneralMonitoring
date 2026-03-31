/**
 * 路由配置
 */
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { setupRouterGuard } from './guards'

// 导入模块路由
import riskRoutes from './modules/risk'
import briefRoutes from './modules/brief'
import callRoutes from './modules/call'
import planRoutes from './modules/plan'
import safetyRoutes from './modules/safety'
import drillRoutes from './modules/drill'
import systemRoutes from './modules/system'

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/Login.vue'),
    meta: {
      title: '登录',
      requiresAuth: false,
    },
  },
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/dashboard/Dashboard.vue'),
    meta: {
      title: '仪表盘',
      requiresAuth: true,
    },
  },
  {
    path: '/screen',
    name: 'Screen',
    redirect: '/screen/overview',
    meta: {
      title: '大屏展示',
      icon: 'Monitor',
    },
    children: [
      {
        path: 'overview',
        name: 'ScreenOverview',
        component: () => import('@/views/screen/ScreenOverview.vue'),
        meta: {
          title: '大屏总览',
          requiresAuth: true,
        },
      },
    ],
  },
  // 模块路由
  ...riskRoutes,
  ...briefRoutes,
  ...callRoutes,
  ...planRoutes,
  ...safetyRoutes,
  ...drillRoutes,
  ...systemRoutes,
  // 403页面
  {
    path: '/403',
    name: 'Forbidden',
    component: () => import('@/views/error/Forbidden.vue'),
    meta: {
      title: '无权限访问',
      requiresAuth: false,
    },
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/NotFound.vue'),
    meta: {
      title: '页面不存在',
    },
  },
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

// 设置路由守卫
setupRouterGuard(router)

export default router

