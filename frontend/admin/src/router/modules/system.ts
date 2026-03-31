/**
 * 系统管理模块路由
 */
import type { RouteRecordRaw } from 'vue-router'

const systemRoutes: RouteRecordRaw[] = [
  {
    path: '/system',
    name: 'System',
    redirect: '/system/user',
    meta: {
      title: '系统管理',
      icon: 'Setting',
    },
    children: [
      {
        path: 'user',
        name: 'SystemUser',
        component: () => import('@/views/system/user/UserList.vue'),
        meta: {
          title: '用户管理',
          requiresAuth: true,
        },
      },
      {
        path: 'role',
        name: 'SystemRole',
        component: () => import('@/views/system/role/RoleList.vue'),
        meta: {
          title: '角色管理',
          requiresAuth: true,
        },
      },
      {
        path: 'permission',
        name: 'SystemPermission',
        component: () => import('@/views/system/permission/PermissionTree.vue'),
        meta: {
          title: '权限管理',
          requiresAuth: true,
        },
      },
      {
        path: 'organization',
        name: 'SystemOrganization',
        component: () => import('@/views/system/organization/OrganizationTree.vue'),
        meta: {
          title: '组织管理',
          requiresAuth: true,
        },
      },
      {
        path: 'datasource',
        name: 'SystemDatasource',
        component: () => import('@/views/system/datasource/DatasourceList.vue'),
        meta: {
          title: '数据源管理',
          requiresAuth: true,
        },
      },
      {
        path: 'template',
        name: 'SystemTemplate',
        component: () => import('@/views/system/template/TemplateList.vue'),
        meta: {
          title: '消息模板',
          requiresAuth: true,
        },
      },
    ],
  },
]

export default systemRoutes

