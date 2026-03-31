/**
 * 叫应模块路由
 */
import type { RouteRecordRaw } from 'vue-router'

const callRoutes: RouteRecordRaw[] = [
  {
    path: '/call',
    name: 'Call',
    redirect: '/call/target',
    meta: {
      title: '平急两用叫应',
      icon: 'Phone',
    },
    children: [
      {
        path: 'target',
        name: 'CallTarget',
        component: () => import('@/views/call/target/TargetList.vue'),
        meta: {
          title: '叫应对象',
          requiresAuth: true,
        },
      },
      {
        path: 'person',
        name: 'CallPerson',
        component: () => import('@/views/call/person/PersonList.vue'),
        meta: {
          title: '叫应人员',
          requiresAuth: true,
        },
      },
      {
        path: 'group',
        name: 'CallGroup',
        component: () => import('@/views/call/group/GroupList.vue'),
        meta: {
          title: '叫应分组',
          requiresAuth: true,
        },
      },
      {
        path: 'policy',
        name: 'CallPolicy',
        component: () => import('@/views/call/policy/PolicyList.vue'),
        meta: {
          title: '政策文件',
          requiresAuth: true,
        },
      },
      {
        path: 'distribution',
        name: 'CallDistribution',
        component: () => import('@/views/call/distribution/DistributionList.vue'),
        meta: {
          title: '政策下发',
          requiresAuth: true,
        },
      },
      {
        path: 'record',
        name: 'CallRecord',
        component: () => import('@/views/call/record/RecordList.vue'),
        meta: {
          title: '叫应记录',
          requiresAuth: true,
        },
      },
      {
        path: 'emergency',
        name: 'CallEmergency',
        component: () => import('@/views/call/emergency/EmergencyCall.vue'),
        meta: {
          title: '一键叫应',
          requiresAuth: true,
        },
      },
    ],
  },
]

export default callRoutes

