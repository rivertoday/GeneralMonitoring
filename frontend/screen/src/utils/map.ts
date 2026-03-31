/**
 * 地图工具函数
 */

import type { Point } from '@/types/map'

/**
 * 百度地图API全局对象声明
 */
declare global {
  interface Window {
    BMap: any
    BMAP_NORMAL_MAP: any
    BMAP_SATELLITE_MAP: any
    BMAP_HYBRID_MAP: any
  }
}

/**
 * 检查百度地图API是否已加载
 */
export function isBaiduMapLoaded(): boolean {
  return typeof window !== 'undefined' && typeof window.BMap !== 'undefined'
}

/**
 * 等待百度地图API加载完成
 */
export function waitForBaiduMap(): Promise<void> {
  return new Promise((resolve, reject) => {
    if (isBaiduMapLoaded()) {
      resolve()
      return
    }

    const maxAttempts = 50 // 最多尝试50次
    let attempts = 0

    const checkInterval = setInterval(() => {
      attempts++
      if (isBaiduMapLoaded()) {
        clearInterval(checkInterval)
        resolve()
      } else if (attempts >= maxAttempts) {
        clearInterval(checkInterval)
        reject(new Error('百度地图API加载超时'))
      }
    }, 100)
  })
}

/**
 * 坐标转换：WGS84（GPS坐标）转百度坐标（BD09）
 * @param point WGS84坐标点
 * @returns 百度坐标点
 */
export function wgs84ToBd09(point: Point): Point {
  if (!isBaiduMapLoaded()) {
    console.warn('百度地图API未加载，无法进行坐标转换')
    return point
  }

  const converter = new window.BMap.Convertor()
  const pointList = [new window.BMap.Point(point.lng, point.lat)]
  const fromType = 1 // WGS84
  const toType = 5 // BD09

  // 注意：这是一个异步操作，这里只是示例
  // 实际使用时应该使用Promise封装
  return point // 简化处理，实际应该调用转换API
}

/**
 * 坐标转换：百度坐标（BD09）转WGS84（GPS坐标）
 * @param point 百度坐标点
 * @returns WGS84坐标点
 */
export function bd09ToWgs84(point: Point): Point {
  if (!isBaiduMapLoaded()) {
    console.warn('百度地图API未加载，无法进行坐标转换')
    return point
  }

  // 坐标转换逻辑（简化处理）
  return point
}

/**
 * 计算两点之间的距离（米）
 * @param point1 起点
 * @param point2 终点
 * @returns 距离（米）
 */
export function getDistance(point1: Point, point2: Point): number {
  if (!isBaiduMapLoaded()) {
    // 使用Haversine公式计算（WGS84坐标系）
    const R = 6371000 // 地球半径（米）
    const dLat = ((point2.lat - point1.lat) * Math.PI) / 180
    const dLng = ((point2.lng - point1.lng) * Math.PI) / 180
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos((point1.lat * Math.PI) / 180) *
        Math.cos((point2.lat * Math.PI) / 180) *
        Math.sin(dLng / 2) *
        Math.sin(dLng / 2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    return R * c
  }

  // 使用百度地图API计算
  const p1 = new window.BMap.Point(point1.lng, point1.lat)
  const p2 = new window.BMap.Point(point2.lng, point2.lat)
  return window.BMap.Map.prototype.getDistance(p1, p2)
}

/**
 * 创建百度地图图标
 * @param iconUrl 图标URL
 * @param size 图标大小 { width, height }
 * @param anchor 锚点位置 { x, y }，默认居中
 * @returns 百度地图图标对象
 */
export function createBaiduIcon(
  iconUrl: string,
  size: { width: number; height: number },
  anchor?: { x: number; y: number }
) {
  if (!isBaiduMapLoaded()) {
    return null
  }

  const icon = new window.BMap.Icon(
    iconUrl,
    new window.BMap.Size(size.width, size.height),
    {
      anchor: anchor
        ? new window.BMap.Size(anchor.x, anchor.y)
        : new window.BMap.Size(size.width / 2, size.height / 2),
    }
  )

  return icon
}

/**
 * 格式化坐标点
 * @param point 坐标点
 * @param precision 精度（小数位数）
 * @returns 格式化后的坐标点字符串
 */
export function formatPoint(point: Point, precision: number = 6): string {
  return `${point.lng.toFixed(precision)}, ${point.lat.toFixed(precision)}`
}

/**
 * 解析坐标点字符串
 * @param pointStr 坐标点字符串 "lng,lat"
 * @returns 坐标点对象
 */
export function parsePoint(pointStr: string): Point | null {
  const parts = pointStr.split(',').map((s) => parseFloat(s.trim()))
  const lng = parts[0]
  const lat = parts[1]
  if (parts.length === 2 && lng !== undefined && lat !== undefined && !isNaN(lng) && !isNaN(lat)) {
    return { lng, lat }
  }
  return null
}

