<template>
  <el-breadcrumb class="app-breadcrumb" separator="/">
    <el-breadcrumb-item
      v-for="(item, index) in breadcrumbList"
      :key="item.path"
      :to="index < breadcrumbList.length - 1 ? item.path : undefined"
    >
      {{ item.title }}
    </el-breadcrumb-item>
  </el-breadcrumb>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 路由标题映射
const routeTitleMap: Record<string, string> = {
  '/dashboard': '仪表盘',
  '/risk': '风险监测预警',
  '/risk/monitor': '风险监测',
  '/risk/warning': '风险预警',
  '/risk/alarm': '报警管理',
  '/risk/rule': '预警规则',
  '/risk/level': '预警级别',
  '/risk/danger': '隐患排查',
  '/risk/rectification': '隐患整改',
  '/risk/statistics': '统计分析',
  '/brief': '平急两用简报',
  '/brief/template': '简报模板',
  '/brief/strategy': '简报策略',
  '/brief/data': '简报数据',
  '/brief/push': '简报推送',
  '/call': '平急两用叫应',
  '/call/target': '叫应对象',
  '/call/person': '叫应人员',
  '/call/group': '叫应分组',
  '/call/policy': '政策文件',
  '/call/distribution': '政策下发',
  '/call/record': '叫应记录',
  '/call/emergency': '一键叫应',
  '/plan': '应急预案数智化',
  '/plan/plan': '应急预案',
  '/plan/structure': '预案结构',
  '/plan/flow': '预案流程',
  '/plan/task': '预案任务',
  '/plan/execution': '预案执行',
  '/safety': '安全态势',
  '/safety/resource': '安全资源',
  '/safety/target': '防护目标',
  '/safety/shelter': '避难场所',
  '/safety/hazard': '危险源',
  '/safety/video': '视频监控',
  '/drill': '应急演练监督',
  '/drill/event': '演练事件',
  '/drill/evaluation': '演练评价',
  '/drill/summary': '演练总结',
  '/drill/analysis': '演练分析',
  '/system': '系统管理',
  '/system/user': '用户管理',
  '/system/role': '角色管理',
  '/system/permission': '权限管理',
  '/system/organization': '组织管理',
  '/system/datasource': '数据源管理',
  '/system/template': '消息模板',
  '/screen': '大屏展示',
  '/screen/overview': '大屏总览',
}

// 生成面包屑列表
const breadcrumbList = computed(() => {
  const matched = route.matched.filter((item) => item.meta && item.meta.title)
  const list: Array<{ path: string; title: string }> = []

  // 添加首页
  list.push({ path: '/dashboard', title: '首页' })

  // 添加匹配的路由
  matched.forEach((item) => {
    const path = item.path
    const title = (item.meta?.title as string) || routeTitleMap[path] || path
    if (path !== '/dashboard') {
      list.push({ path, title })
    }
  })

  return list
})
</script>

<style scoped lang="scss">
.app-breadcrumb {
  padding: 16px 20px;
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  width: 100%;
  flex-shrink: 0;
  box-sizing: border-box;
}
</style>

