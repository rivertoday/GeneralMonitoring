/**
 * 大屏响应式适配工具
 */

// 设计稿基准尺寸
const DESIGN_WIDTH = 1920
const DESIGN_HEIGHT = 1080

/**
 * 根据设计稿尺寸计算vw值
 * @param px 设计稿像素值
 * @returns vw单位值
 */
export function pxToVw(px: number): string {
  return `${(px / DESIGN_WIDTH) * 100}vw`
}

/**
 * 根据设计稿尺寸计算vh值
 * @param px 设计稿像素值
 * @returns vh单位值
 */
export function pxToVh(px: number): string {
  return `${(px / DESIGN_HEIGHT) * 100}vh`
}

/**
 * 计算缩放比例
 * @returns 缩放比例
 */
export function getScale(): number {
  const width = window.innerWidth
  const height = window.innerHeight
  
  const scaleX = width / DESIGN_WIDTH
  const scaleY = height / DESIGN_HEIGHT
  
  // 取较小的缩放比例，保证内容完全显示
  return Math.min(scaleX, scaleY)
}

/**
 * 应用缩放
 * @param element 要应用缩放的元素
 */
export function applyScale(element: HTMLElement): void {
  const scale = getScale()
  element.style.transform = `scale(${scale})`
  element.style.transformOrigin = 'top left'
}

/**
 * 移除缩放
 * @param element 要移除缩放的元素
 */
export function removeScale(element: HTMLElement): void {
  element.style.transform = ''
  element.style.transformOrigin = ''
}

/**
 * 响应式适配类
 */
export class ResponsiveAdapter {
  private container: HTMLElement | null = null
  private resizeHandler: (() => void) | null = null

  /**
   * 初始化适配器
   * @param containerId 容器元素ID
   */
  init(containerId: string = 'app'): void {
    const container = document.getElementById(containerId)
    if (!container) {
      console.warn(`Container with id "${containerId}" not found`)
      return
    }

    this.container = container
    this.updateScale()

    // 监听窗口大小变化
    this.resizeHandler = () => {
      this.updateScale()
    }
    window.addEventListener('resize', this.resizeHandler)
  }

  /**
   * 更新缩放
   */
  updateScale(): void {
    if (!this.container) return

    const scale = getScale()
    this.container.style.transform = `scale(${scale})`
    this.container.style.transformOrigin = 'top left'

    // 计算缩放后的尺寸，避免出现滚动条
    const width = DESIGN_WIDTH * scale
    const height = DESIGN_HEIGHT * scale
    this.container.style.width = `${DESIGN_WIDTH}px`
    this.container.style.height = `${DESIGN_HEIGHT}px`

    // 调整父容器以居中显示
    const parent = this.container.parentElement
    if (parent) {
      parent.style.width = '100vw'
      parent.style.height = '100vh'
      parent.style.overflow = 'hidden'
      parent.style.display = 'flex'
      parent.style.alignItems = 'center'
      parent.style.justifyContent = 'center'
    }
  }

  /**
   * 销毁适配器
   */
  destroy(): void {
    if (this.resizeHandler) {
      window.removeEventListener('resize', this.resizeHandler)
      this.resizeHandler = null
    }
    this.container = null
  }
}

/**
 * 创建响应式适配器实例
 */
export function createResponsiveAdapter(): ResponsiveAdapter {
  return new ResponsiveAdapter()
}

