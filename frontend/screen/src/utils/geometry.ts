/**
 * 几何图形工具函数
 */

import type { Point } from '@/types/map'

/**
 * 计算圆形路径点（用于绘制圆形多边形）
 * 使用Haversine公式在地球表面生成准确的圆形
 * @param center 圆心坐标（WGS84经纬度）
 * @param radiusMeters 半径（米）
 * @param segments 分段数（默认64，越大越圆滑但性能越低）
 * @returns 圆形路径点数组（WGS84经纬度）
 */
export function createCirclePoints(
  center: Point,
  radiusMeters: number,
  segments: number = 64
): Point[] {
  const points: Point[] = []
  const R = 6371000 // 地球半径（米）

  // 将中心点转换为弧度
  const centerLatRad = (center.lat * Math.PI) / 180
  const centerLngRad = (center.lng * Math.PI) / 180

  // 计算角距离（半径对应的角度，单位：弧度）
  const angularRadius = radiusMeters / R

  // 生成圆形路径点
  for (let i = 0; i <= segments; i++) {
    const angle = (i * 2 * Math.PI) / segments

    // 使用球面三角函数计算圆形上的点
    // 参考：https://en.wikipedia.org/wiki/Great-circle_distance
    const latRad = Math.asin(
      Math.sin(centerLatRad) * Math.cos(angularRadius) +
        Math.cos(centerLatRad) * Math.sin(angularRadius) * Math.cos(angle)
    )
    const lngRad =
      centerLngRad +
      Math.atan2(
        Math.sin(angle) * Math.sin(angularRadius) * Math.cos(centerLatRad),
        Math.cos(angularRadius) - Math.sin(centerLatRad) * Math.sin(latRad)
      )

    // 转换回度数
    const lat = (latRad * 180) / Math.PI
    const lng = (lngRad * 180) / Math.PI

    points.push({ lng, lat })
  }

  // 确保圆形闭合（最后一个点等于第一个点）
  if (points.length > 0) {
    const first = points[0]
    const last = points[points.length - 1]
    // 使用较小的阈值判断是否已经闭合
    if (first && last && (Math.abs(first.lng - last.lng) > 1e-10 || Math.abs(first.lat - last.lat) > 1e-10)) {
      points[points.length - 1] = { lng: first.lng, lat: first.lat }
    }
  }

  return points
}

/**
 * 判断点是否在圆形内（使用平面距离计算）
 * @param point 待判断的点
 * @param center 圆心
 * @param radiusMeters 半径（米）
 * @returns 是否在圆内
 */
export function isPointInCircle(
  point: Point,
  center: Point,
  radiusMeters: number
): boolean {
  // 使用Haversine公式计算两点间距离
  const R = 6371000 // 地球半径（米）
  const dLat = ((point.lat - center.lat) * Math.PI) / 180
  const dLng = ((point.lng - center.lng) * Math.PI) / 180
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos((center.lat * Math.PI) / 180) *
      Math.cos((point.lat * Math.PI) / 180) *
      Math.sin(dLng / 2) *
      Math.sin(dLng / 2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
  const distance = R * c

  return distance <= radiusMeters
}

