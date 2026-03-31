/**
 * 应用状态管理
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAppStore = defineStore('app', () => {
  // 状态
  const theme = ref<'light' | 'dark'>('light')
  const sidebarCollapsed = ref(false)
  const screenSize = ref<'desktop' | 'tablet' | 'mobile'>('desktop')

  // 计算属性
  const isMobile = computed(() => screenSize.value === 'mobile')
  const isTablet = computed(() => screenSize.value === 'tablet')
  const isDesktop = computed(() => screenSize.value === 'desktop')

  // 切换主题
  function toggleTheme() {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    // 可以在这里添加主题切换的逻辑，比如更新CSS变量
    document.documentElement.setAttribute('data-theme', theme.value)
  }

  // 设置主题
  function setTheme(newTheme: 'light' | 'dark') {
    theme.value = newTheme
    document.documentElement.setAttribute('data-theme', newTheme)
  }

  // 切换侧边栏
  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  // 设置侧边栏状态
  function setSidebarCollapsed(collapsed: boolean) {
    sidebarCollapsed.value = collapsed
  }

  // 设置屏幕尺寸
  function setScreenSize(size: 'desktop' | 'tablet' | 'mobile') {
    screenSize.value = size
  }

  // 初始化屏幕尺寸监听
  function initScreenSize() {
    const updateScreenSize = () => {
      const width = window.innerWidth
      if (width < 768) {
        setScreenSize('mobile')
      } else if (width < 1024) {
        setScreenSize('tablet')
      } else {
        setScreenSize('desktop')
      }
    }

    updateScreenSize()
    window.addEventListener('resize', updateScreenSize)
  }

  return {
    // 状态
    theme,
    sidebarCollapsed,
    screenSize,
    // 计算属性
    isMobile,
    isTablet,
    isDesktop,
    // 方法
    toggleTheme,
    setTheme,
    toggleSidebar,
    setSidebarCollapsed,
    setScreenSize,
    initScreenSize,
  }
})

