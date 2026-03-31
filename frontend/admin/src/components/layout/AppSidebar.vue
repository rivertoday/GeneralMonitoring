<template>
  <el-aside :width="appStore.sidebarCollapsed ? '64px' : '200px'" class="app-sidebar">
    <div class="logo">
      <el-icon v-if="appStore.sidebarCollapsed" class="logo-icon"><Warning /></el-icon>
      <span v-if="!appStore.sidebarCollapsed" class="logo-text">风险监测预警系统</span>
    </div>
    
    <el-menu
      :default-active="activeMenu"
      :collapse="appStore.sidebarCollapsed"
      :collapse-transition="false"
      router
      class="sidebar-menu"
    >
      <!-- 仪表盘 -->
      <el-menu-item index="/dashboard">
        <el-icon><Odometer /></el-icon>
        <template #title>仪表盘</template>
      </el-menu-item>

      <!-- 风险监测预警 -->
      <el-sub-menu index="/risk">
        <template #title>
          <el-icon><Warning /></el-icon>
          <span>风险监测预警</span>
        </template>
        <el-menu-item index="/risk/monitor">风险监测</el-menu-item>
        <el-menu-item index="/risk/warning">风险预警</el-menu-item>
        <el-menu-item index="/risk/alarm">报警管理</el-menu-item>
        <el-menu-item index="/risk/rule">预警规则</el-menu-item>
        <el-menu-item index="/risk/level">预警级别</el-menu-item>
        <el-menu-item index="/risk/danger">隐患排查</el-menu-item>
        <el-menu-item index="/risk/rectification">隐患整改</el-menu-item>
        <el-menu-item index="/risk/statistics">统计分析</el-menu-item>
      </el-sub-menu>

      <!-- 平急两用简报 -->
      <el-sub-menu index="/brief">
        <template #title>
          <el-icon><Document /></el-icon>
          <span>平急两用简报</span>
        </template>
        <el-menu-item index="/brief/template">简报模板</el-menu-item>
        <el-menu-item index="/brief/strategy">简报策略</el-menu-item>
        <el-menu-item index="/brief/data">简报数据</el-menu-item>
        <el-menu-item index="/brief/push">简报推送</el-menu-item>
      </el-sub-menu>

      <!-- 平急两用叫应 -->
      <el-sub-menu index="/call">
        <template #title>
          <el-icon><Phone /></el-icon>
          <span>平急两用叫应</span>
        </template>
        <el-menu-item index="/call/target">叫应对象</el-menu-item>
        <el-menu-item index="/call/person">叫应人员</el-menu-item>
        <el-menu-item index="/call/group">叫应分组</el-menu-item>
        <el-menu-item index="/call/policy">政策文件</el-menu-item>
        <el-menu-item index="/call/distribution">政策下发</el-menu-item>
        <el-menu-item index="/call/record">叫应记录</el-menu-item>
        <el-menu-item index="/call/emergency">一键叫应</el-menu-item>
      </el-sub-menu>

      <!-- 应急预案数智化 -->
      <el-sub-menu index="/plan">
        <template #title>
          <el-icon><Files /></el-icon>
          <span>应急预案数智化</span>
        </template>
        <el-menu-item index="/plan/plan">应急预案</el-menu-item>
        <el-menu-item index="/plan/structure">预案结构</el-menu-item>
        <el-menu-item index="/plan/flow">预案流程</el-menu-item>
        <el-menu-item index="/plan/task">预案任务</el-menu-item>
        <el-menu-item index="/plan/execution">预案执行</el-menu-item>
      </el-sub-menu>

      <!-- 安全态势 -->
      <el-sub-menu index="/safety">
        <template #title>
          <el-icon><Location /></el-icon>
          <span>安全态势</span>
        </template>
        <el-menu-item index="/safety/resource">安全资源</el-menu-item>
        <el-menu-item index="/safety/target">防护目标</el-menu-item>
        <el-menu-item index="/safety/shelter">避难场所</el-menu-item>
        <el-menu-item index="/safety/hazard">危险源</el-menu-item>
        <el-menu-item index="/safety/video">视频监控</el-menu-item>
      </el-sub-menu>

      <!-- 应急演练监督 -->
      <el-sub-menu index="/drill">
        <template #title>
          <el-icon><VideoPlay /></el-icon>
          <span>应急演练监督</span>
        </template>
        <el-menu-item index="/drill/event">演练事件</el-menu-item>
        <el-menu-item index="/drill/evaluation">演练评价</el-menu-item>
        <el-menu-item index="/drill/summary">演练总结</el-menu-item>
        <el-menu-item index="/drill/analysis">演练分析</el-menu-item>
      </el-sub-menu>

      <!-- 系统管理 -->
      <el-sub-menu index="/system">
        <template #title>
          <el-icon><Setting /></el-icon>
          <span>系统管理</span>
        </template>
        <el-menu-item index="/system/user">用户管理</el-menu-item>
        <el-menu-item index="/system/role">角色管理</el-menu-item>
        <el-menu-item index="/system/permission">权限管理</el-menu-item>
        <el-menu-item index="/system/organization">组织管理</el-menu-item>
        <el-menu-item index="/system/datasource">数据源管理</el-menu-item>
        <el-menu-item index="/system/template">消息模板</el-menu-item>
      </el-sub-menu>
    </el-menu>
  </el-aside>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import {
  Odometer,
  Warning,
  Document,
  Phone,
  Files,
  Location,
  VideoPlay,
  Setting,
} from '@element-plus/icons-vue'
import { useAppStore } from '@/store/modules/app'

const route = useRoute()
const appStore = useAppStore()

// 当前激活的菜单
const activeMenu = computed(() => {
  const { path } = route
  return path
})
</script>

<style scoped lang="scss">
.app-sidebar {
  background-color: #001529;
  transition: width 0.3s;
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 64px;
  padding: 0 16px;
  background-color: #002140;
  border-bottom: 1px solid #001529;
  flex-shrink: 0; // 固定logo高度，不收缩

  .logo-icon {
    font-size: 24px;
    color: #fff;
  }

  .logo-text {
    color: #fff;
    font-size: 16px;
    font-weight: 500;
    white-space: nowrap;
  }
}

.sidebar-menu {
  border: none;
  background-color: #001529;
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  height: 0; // 重要：配合 flex: 1 使用，让菜单部分可以正确计算高度
  // 自定义滚动条样式
  &::-webkit-scrollbar {
    width: 6px;
  }
  &::-webkit-scrollbar-track {
    background: #001529;
  }
  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
    &:hover {
      background: rgba(255, 255, 255, 0.5);
    }
  }

  // 一级菜单项（如"仪表盘"）
  :deep(.el-menu-item:not(.el-sub-menu .el-menu-item)) {
    color: rgba(255, 255, 255, 0.65);
    background-color: transparent;

    &:hover {
      background-color: #000c17;
      color: #fff;
    }
  }

  // 子菜单标题（如"风险监测预警"、"平急两用简报"等）
  :deep(.el-sub-menu__title) {
    color: rgba(255, 255, 255, 0.65);
    background-color: transparent;

    &:hover {
      background-color: #000c17;
      color: #fff;
    }
  }

  // 子菜单容器背景
  :deep(.el-sub-menu .el-menu) {
    background-color: #1a1a1a; // 灰色背景
  }

  // 子菜单项（展开后的菜单项，如"风险监测"、"风险预警"等）
  :deep(.el-sub-menu .el-menu-item) {
    color: rgba(255, 255, 255, 0.85);
    background-color: #1a1a1a; // 灰色背景

    &:hover {
      background-color: #1890ff; // 悬停时蓝色背景
      color: #fff;
    }
  }

  // 激活的菜单项（包括一级菜单和子菜单项）
  :deep(.el-menu-item.is-active) {
    background-color: #1890ff; // 激活时蓝色背景
    color: #fff;
  }

  // 激活的子菜单标题
  :deep(.el-sub-menu.is-active .el-sub-menu__title) {
    color: #fff;
  }
}
</style>

