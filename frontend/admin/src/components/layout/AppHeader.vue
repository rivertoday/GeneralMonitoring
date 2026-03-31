<template>
  <el-header class="app-header">
    <div class="header-left">
      <!-- 折叠按钮 -->
      <el-icon class="collapse-icon" @click="toggleSidebar">
        <Expand v-if="appStore.sidebarCollapsed" />
        <Fold v-else />
      </el-icon>
    </div>
    
    <div class="header-right">
      <!-- 大屏入口 -->
      <el-button type="primary" link @click="goToScreen">
        <el-icon><Monitor /></el-icon>
        大屏展示
      </el-button>
      
      <!-- 用户信息 -->
      <el-dropdown @command="handleCommand">
        <div class="user-info">
          <el-avatar :size="32" :src="authStore.user?.avatar">
            <el-icon><User /></el-icon>
          </el-avatar>
          <span class="username">{{ authStore.user?.real_name || authStore.user?.username }}</span>
          <el-icon class="arrow-down"><ArrowDown /></el-icon>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="profile">
              <el-icon><User /></el-icon>
              个人中心
            </el-dropdown-item>
            <el-dropdown-item command="settings">
              <el-icon><Setting /></el-icon>
              系统设置
            </el-dropdown-item>
            <el-dropdown-item divided command="logout">
              <el-icon><SwitchButton /></el-icon>
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </el-header>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Expand,
  Fold,
  Monitor,
  User,
  ArrowDown,
  Setting,
  SwitchButton,
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/modules/auth'
import { useAppStore } from '@/store/modules/app'

const router = useRouter()
const authStore = useAuthStore()
const appStore = useAppStore()

// 切换侧边栏
const toggleSidebar = () => {
  appStore.toggleSidebar()
}

// 跳转到大屏
const goToScreen = () => {
  // 获取大屏展示系统的URL，优先使用环境变量，否则使用默认值
  const screenBaseUrl = import.meta.env.VITE_SCREEN_BASE_URL || 'http://localhost:5174'
  window.open(`${screenBaseUrl}/overview`, '_blank')
}

// 处理下拉菜单命令
const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      // TODO: 跳转到个人中心
      ElMessage.info('个人中心功能开发中')
      break
    case 'settings':
      // TODO: 跳转到系统设置
      ElMessage.info('系统设置功能开发中')
      break
    case 'logout':
      handleLogout()
      break
  }
}

// 退出登录
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })

    // 调用登出接口
    // await post('/auth/logout/')
    
    // 清除状态
    authStore.logout()
    
    // 跳转到登录页
    router.push('/login')
    ElMessage.success('退出登录成功')
  } catch (error) {
    // 用户取消
  }
}
</script>

<style scoped lang="scss">
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  padding: 0 20px;
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  flex-shrink: 0;
}

.header-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.collapse-icon {
  font-size: 20px;
  cursor: pointer;
  color: #606266;
  transition: color 0.3s;

  &:hover {
    color: #409eff;
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-left: auto;
  flex-shrink: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;

  &:hover {
    background-color: #f5f7fa;
  }

  .username {
    font-size: 14px;
    color: #303133;
  }

  .arrow-down {
    font-size: 12px;
    color: #909399;
  }
}
</style>

