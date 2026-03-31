/**
 * 预案模块路由
 */
import type { RouteRecordRaw } from 'vue-router'

const planRoutes: RouteRecordRaw[] = [
  {
    path: '/plan',
    name: 'Plan',
    redirect: '/plan/plan',
    meta: {
      title: '应急预案数智化',
      icon: 'Files',
    },
    children: [
      {
        path: 'plan',
        name: 'EmergencyPlan',
        component: () => import('@/views/plan/plan/PlanList.vue'),
        meta: {
          title: '应急预案',
          requiresAuth: true,
        },
      },
      {
        path: 'structure',
        name: 'PlanStructure',
        component: () => import('@/views/plan/structure/StructureTree.vue'),
        meta: {
          title: '预案结构',
          requiresAuth: true,
        },
      },
      {
        path: 'flow',
        name: 'PlanFlow',
        component: () => import('@/views/plan/flow/FlowList.vue'),
        meta: {
          title: '预案流程',
          requiresAuth: true,
        },
      },
      {
        path: 'task',
        name: 'PlanTask',
        component: () => import('@/views/plan/task/TaskList.vue'),
        meta: {
          title: '预案任务',
          requiresAuth: true,
        },
      },
      {
        path: 'execution',
        name: 'PlanExecution',
        component: () => import('@/views/plan/execution/ExecutionList.vue'),
        meta: {
          title: '预案执行',
          requiresAuth: true,
        },
      },
    ],
  },
]

export default planRoutes

