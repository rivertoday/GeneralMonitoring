/**
 * 简报模块路由
 */
import type { RouteRecordRaw } from 'vue-router'

const briefRoutes: RouteRecordRaw[] = [
  {
    path: '/brief',
    name: 'Brief',
    redirect: '/brief/template',
    meta: {
      title: '平急两用简报',
      icon: 'Document',
    },
    children: [
      {
        path: 'template',
        name: 'BriefTemplate',
        component: () => import('@/views/brief/template/TemplateList.vue'),
        meta: {
          title: '简报模板',
          requiresAuth: true,
        },
      },
      {
        path: 'strategy',
        name: 'BriefStrategy',
        component: () => import('@/views/brief/strategy/StrategyList.vue'),
        meta: {
          title: '简报策略',
          requiresAuth: true,
        },
      },
      {
        path: 'data',
        name: 'BriefData',
        component: () => import('@/views/brief/data/DataList.vue'),
        meta: {
          title: '简报数据',
          requiresAuth: true,
        },
      },
      {
        path: 'push',
        name: 'BriefPush',
        component: () => import('@/views/brief/push/PushList.vue'),
        meta: {
          title: '简报推送',
          requiresAuth: true,
        },
      },
    ],
  },
]

export default briefRoutes

