/**
 * 演练模块路由
 */
import type { RouteRecordRaw } from 'vue-router'

const drillRoutes: RouteRecordRaw[] = [
  {
    path: '/drill',
    name: 'Drill',
    redirect: '/drill/event',
    meta: {
      title: '应急演练监督',
      icon: 'VideoPlay',
    },
    children: [
      {
        path: 'event',
        name: 'DrillEvent',
        component: () => import('@/views/drill/event/EventList.vue'),
        meta: {
          title: '演练事件',
          requiresAuth: true,
        },
      },
      {
        path: 'evaluation',
        name: 'DrillEvaluation',
        component: () => import('@/views/drill/evaluation/EvaluationList.vue'),
        meta: {
          title: '演练评价',
          requiresAuth: true,
        },
      },
      {
        path: 'summary',
        name: 'DrillSummary',
        component: () => import('@/views/drill/summary/SummaryList.vue'),
        meta: {
          title: '演练总结',
          requiresAuth: true,
        },
      },
      {
        path: 'analysis',
        name: 'DrillAnalysis',
        component: () => import('@/views/drill/analysis/Analysis.vue'),
        meta: {
          title: '演练分析',
          requiresAuth: true,
        },
      },
    ],
  },
]

export default drillRoutes

