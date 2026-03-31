/**
 * 风险监测预警模块路由
 */
import type { RouteRecordRaw } from 'vue-router'

const riskRoutes: RouteRecordRaw[] = [
  {
    path: '/risk',
    name: 'Risk',
    redirect: '/risk/monitor',
    meta: {
      title: '风险监测预警',
      icon: 'Warning',
    },
    children: [
      {
        path: 'monitor',
        name: 'RiskMonitor',
        component: () => import('@/views/risk/monitor/MonitorList.vue'),
        meta: {
          title: '风险监测',
          requiresAuth: true,
        },
      },
      {
        path: 'warning',
        name: 'RiskWarning',
        component: () => import('@/views/risk/warning/WarningList.vue'),
        meta: {
          title: '风险预警',
          requiresAuth: true,
        },
      },
      {
        path: 'alarm',
        name: 'RiskAlarm',
        component: () => import('@/views/risk/alarm/AlarmList.vue'),
        meta: {
          title: '报警管理',
          requiresAuth: true,
        },
      },
      {
        path: 'rule',
        name: 'RiskRule',
        component: () => import('@/views/risk/rule/RuleList.vue'),
        meta: {
          title: '预警规则',
          requiresAuth: true,
        },
      },
      {
        path: 'level',
        name: 'RiskLevel',
        component: () => import('@/views/risk/level/LevelList.vue'),
        meta: {
          title: '预警级别',
          requiresAuth: true,
        },
      },
      {
        path: 'danger',
        name: 'RiskDanger',
        component: () => import('@/views/risk/danger/DangerList.vue'),
        meta: {
          title: '隐患排查',
          requiresAuth: true,
        },
      },
      {
        path: 'rectification',
        name: 'RiskRectification',
        component: () => import('@/views/risk/rectification/RectificationList.vue'),
        meta: {
          title: '隐患整改',
          requiresAuth: true,
        },
      },
      {
        path: 'statistics',
        name: 'RiskStatistics',
        component: () => import('@/views/risk/statistics/Statistics.vue'),
        meta: {
          title: '统计分析',
          requiresAuth: true,
        },
      },
    ],
  },
]

export default riskRoutes

