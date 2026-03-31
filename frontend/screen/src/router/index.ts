/**
 * 路由配置
 */
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { setupRouterGuard } from './guards'

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
    redirect: '/overview',
  },
  {
    path: '/overview',
    name: 'Overview',
    component: () => import('@/views/overview/Overview.vue'),
    meta: {
      title: '大屏总览',
      requiresAuth: true,
    },
  },
  {
    path: '/safety-run',
    name: 'SafetyRun',
    component: () => import('@/views/safety-run/SafetyRun.vue'),
    meta: {
      title: '安全运行一张图',
      requiresAuth: true,
    },
  },
  {
    path: '/safety-status',
    name: 'SafetyStatus',
    component: () => import('@/views/safety-status/SafetyStatus.vue'),
    meta: {
      title: '安全态势一张图',
      requiresAuth: true,
    },
  },
  {
    path: '/monitor-warn',
    name: 'MonitorWarn',
    component: () => import('@/views/monitor-warn/MonitorWarn.vue'),
    meta: {
      title: '监测预警一张图',
      requiresAuth: true,
    },
  },
  // Cesium 地图测试页面
  {
    path: '/cesium-test',
    name: 'CesiumTest',
    component: () => import('@/views/test/CesiumTest.vue'),
    meta: {
      title: 'Cesium 地图测试',
      requiresAuth: true,
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
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  },
})

// 路由守卫将在main.ts中设置（在Pinia注册之后）

export default router

