<template>
  <el-container class="app-layout">
    <!-- 侧边栏 -->
    <AppSidebar />
    
    <!-- 主内容区 -->
    <el-container>
      <!-- 顶部导航 -->
      <AppHeader />
      
      <!-- 面包屑 -->
      <el-main class="app-main">
        <AppBreadcrumb />
        
        <!-- 页面内容 -->
        <div class="app-content">
          <router-view />
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import AppSidebar from './AppSidebar.vue'
import AppHeader from './AppHeader.vue'
import AppBreadcrumb from './AppBreadcrumb.vue'
</script>

<style scoped lang="scss">
.app-layout {
  height: 100vh;
  overflow: hidden;
  
  // 确保内部容器占满高度
  :deep(.el-container) {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
}

.app-main {
  padding: 0 !important;
  background-color: #f5f5f5;
  overflow-y: auto;
  overflow-x: hidden;
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0; // 重要：允许 flex 子元素缩小
}

.app-content {
  padding: 20px;
  flex: 1;
  width: 100%;
  box-sizing: border-box;
  min-height: 0; // 重要：允许 flex 子元素缩小
  overflow-y: auto;
}
</style>

