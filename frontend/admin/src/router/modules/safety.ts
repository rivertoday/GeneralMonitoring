/**
 * 安全态势模块路由
 */
import type { RouteRecordRaw } from 'vue-router'

const safetyRoutes: RouteRecordRaw[] = [
  {
    path: '/safety',
    name: 'Safety',
    redirect: '/safety/resource',
    meta: {
      title: '安全态势',
      icon: 'Location',
    },
    children: [
      {
        path: 'resource',
        name: 'SafetyResource',
        component: () => import('@/views/safety/resource/ResourceList.vue'),
        meta: {
          title: '安全资源',
          requiresAuth: true,
        },
      },
      {
        path: 'target',
        name: 'SafetyTarget',
        component: () => import('@/views/safety/target/TargetList.vue'),
        meta: {
          title: '防护目标',
          requiresAuth: true,
        },
      },
      {
        path: 'shelter',
        name: 'SafetyShelter',
        component: () => import('@/views/safety/shelter/ShelterList.vue'),
        meta: {
          title: '避难场所',
          requiresAuth: true,
        },
      },
      {
        path: 'hazard',
        name: 'SafetyHazard',
        component: () => import('@/views/safety/hazard/HazardList.vue'),
        meta: {
          title: '危险源',
          requiresAuth: true,
        },
      },
      {
        path: 'video',
        name: 'SafetyVideo',
        component: () => import('@/views/safety/video/VideoList.vue'),
        meta: {
          title: '视频监控',
          requiresAuth: true,
        },
      },
    ],
  },
]

export default safetyRoutes

