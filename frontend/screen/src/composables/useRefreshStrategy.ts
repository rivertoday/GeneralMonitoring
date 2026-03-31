/**
 * 刷新策略管理 Composable
 * 提供智能刷新、错误重试、页面可见性检测等功能
 */
import { ref, onMounted, onUnmounted, watch } from 'vue'

export interface RefreshOptions {
  /** 刷新间隔（毫秒） */
  interval: number
  /** 是否立即执行（默认true） */
  immediate?: boolean
  /** 错误重试配置 */
  retry?: {
    /** 最大重试次数（默认3） */
    maxRetries?: number
    /** 重试延迟（毫秒，默认1000） */
    retryDelay?: number
    /** 是否指数退避（默认true） */
    exponentialBackoff?: boolean
  }
  /** 是否启用页面可见性检测（默认true） */
  enableVisibilityCheck?: boolean
}

export interface RefreshResult {
  /** 是否成功 */
  success: boolean
  /** 错误信息 */
  error?: Error
  /** 重试次数 */
  retryCount?: number
}

/**
 * 使用刷新策略
 * @param refreshFn 刷新函数，返回 Promise
 * @param options 刷新选项
 */
export function useRefreshStrategy(
  refreshFn: () => Promise<void>,
  options: RefreshOptions
) {
  const {
    interval,
    immediate = true,
    retry = {
      maxRetries: 3,
      retryDelay: 1000,
      exponentialBackoff: true,
    },
    enableVisibilityCheck = true,
  } = options

  const isRefreshing = ref(false)
  const lastUpdateTime = ref<Date | null>(null)
  const errorCount = ref(0)
  const retryCount = ref(0)
  const isPageVisible = ref(!document.hidden)

  let refreshTimer: ReturnType<typeof setInterval> | null = null
  let retryTimer: ReturnType<typeof setTimeout> | null = null

  /**
   * 执行刷新（带重试机制）
   */
  const executeRefresh = async (): Promise<RefreshResult> => {
    // 如果页面不可见且启用了可见性检测，跳过刷新
    if (enableVisibilityCheck && !isPageVisible.value) {
      console.log('页面不可见，跳过刷新')
      return { success: false, error: new Error('页面不可见') }
    }

    isRefreshing.value = true
    let currentRetryCount = 0
    const maxRetries = retry.maxRetries || 3
    const retryDelay = retry.retryDelay || 1000
    const exponentialBackoff = retry.exponentialBackoff !== false

    while (currentRetryCount <= maxRetries) {
      try {
        await refreshFn()
        // 成功
        lastUpdateTime.value = new Date()
        errorCount.value = 0
        retryCount.value = 0
        isRefreshing.value = false
        return { success: true, retryCount: currentRetryCount }
      } catch (error) {
        currentRetryCount++
        retryCount.value = currentRetryCount

        if (currentRetryCount > maxRetries) {
          // 达到最大重试次数
          errorCount.value++
          isRefreshing.value = false
          console.error(`刷新失败，已重试 ${maxRetries} 次:`, error)
          return {
            success: false,
            error: error as Error,
            retryCount: currentRetryCount - 1,
          }
        }

        // 计算重试延迟（指数退避）
        const delay = exponentialBackoff
          ? retryDelay * Math.pow(2, currentRetryCount - 1)
          : retryDelay

        console.warn(
          `刷新失败，${delay}ms 后进行第 ${currentRetryCount} 次重试:`,
          error
        )

        // 等待后重试
        await new Promise((resolve) => setTimeout(resolve, delay))
      }
    }

    isRefreshing.value = false
    return { success: false, error: new Error('未知错误'), retryCount: maxRetries }
  }

  /**
   * 启动定时刷新
   */
  const startRefresh = () => {
    // 清除现有定时器
    stopRefresh()

    // 立即执行一次（如果启用）
    if (immediate) {
      executeRefresh()
    }

    // 设置定时刷新
    refreshTimer = setInterval(() => {
      executeRefresh()
    }, interval)
  }

  /**
   * 停止定时刷新
   */
  const stopRefresh = () => {
    if (refreshTimer) {
      clearInterval(refreshTimer)
      refreshTimer = null
    }
    if (retryTimer) {
      clearTimeout(retryTimer)
      retryTimer = null
    }
  }

  /**
   * 手动刷新
   */
  const manualRefresh = async () => {
    return await executeRefresh()
  }

  /**
   * 页面可见性变化处理
   */
  const handleVisibilityChange = () => {
    const visible = !document.hidden
    isPageVisible.value = visible

    if (visible) {
      // 页面变为可见，立即刷新一次
      console.log('页面变为可见，立即刷新数据')
      executeRefresh()
      // 重新启动定时刷新
      if (!refreshTimer) {
        startRefresh()
      }
    } else {
      // 页面变为不可见，停止刷新（但不清除定时器，只是暂停执行）
      console.log('页面变为不可见，暂停刷新')
    }
  }

  // 监听页面可见性变化
  if (enableVisibilityCheck) {
    onMounted(() => {
      document.addEventListener('visibilitychange', handleVisibilityChange)
      // 初始化页面可见性状态
      isPageVisible.value = !document.hidden
    })

    onUnmounted(() => {
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    })
  }

  // 组件卸载时清理
  onUnmounted(() => {
    stopRefresh()
  })

  return {
    isRefreshing,
    lastUpdateTime,
    errorCount,
    retryCount,
    isPageVisible,
    startRefresh,
    stopRefresh,
    manualRefresh,
    executeRefresh,
  }
}

