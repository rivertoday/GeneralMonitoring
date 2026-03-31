/**
 * 坐标系转换工具
 * 用于百度地图（BD09）和OpenLayers（Web Mercator）之间的坐标转换
 */

import type { Point } from '@/types/map'

// 百度坐标系常量
const X_PI = (3.14159265358979324 * 3000.0) / 180.0
const PI = 3.1415926535897932384626
const A = 6378245.0
const EE = 0.00669342162296594323

/**
 * 判断是否在中国境内（用于坐标转换）
 */
function outOfChina(lng: number, lat: number): boolean {
  return lng < 72.004 || lng > 137.8347 || lat < 0.8293 || lat > 55.8271
}

/**
 * 百度坐标（BD09）转火星坐标（GCJ02）
 */
function bd09ToGcj02(lng: number, lat: number): [number, number] {
  const x = lng - 0.0065
  const y = lat - 0.006
  const z = Math.sqrt(x * x + y * y) - 0.00002 * Math.sin(y * X_PI)
  const theta = Math.atan2(y, x) - 0.000003 * Math.cos(x * X_PI)
  const ggLng = z * Math.cos(theta)
  const ggLat = z * Math.sin(theta)
  return [ggLng, ggLat]
}

/**
 * 火星坐标（GCJ02）转百度坐标（BD09）
 */
function gcj02ToBd09(lng: number, lat: number): [number, number] {
  const z = Math.sqrt(lng * lng + lat * lat) + 0.00002 * Math.sin(lat * X_PI)
  const theta = Math.atan2(lat, lng) + 0.000003 * Math.cos(lng * X_PI)
  const bdLng = z * Math.cos(theta) + 0.0065
  const bdLat = z * Math.sin(theta) + 0.006
  return [bdLng, bdLat]
}

/**
 * 火星坐标（GCJ02）转WGS84
 */
function gcj02ToWgs84(lng: number, lat: number): [number, number] {
  if (outOfChina(lng, lat)) {
    return [lng, lat]
  }
  let dLat = transformLat(lng - 105.0, lat - 35.0)
  let dLng = transformLng(lng - 105.0, lat - 35.0)
  const radLat = (lat / 180.0) * PI
  let magic = Math.sin(radLat)
  magic = 1 - EE * magic * magic
  const sqrtMagic = Math.sqrt(magic)
  dLat = (dLat * 180.0) / (((A * (1 - EE)) / (magic * sqrtMagic)) * PI)
  dLng = (dLng * 180.0) / ((A / sqrtMagic) * Math.cos(radLat) * PI)
  const mgLat = lat + dLat
  const mgLng = lng + dLng
  return [lng * 2 - mgLng, lat * 2 - mgLat]
}

/**
 * WGS84转火星坐标（GCJ02）
 */
function wgs84ToGcj02(lng: number, lat: number): [number, number] {
  if (outOfChina(lng, lat)) {
    return [lng, lat]
  }
  let dLat = transformLat(lng - 105.0, lat - 35.0)
  let dLng = transformLng(lng - 105.0, lat - 35.0)
  const radLat = (lat / 180.0) * PI
  let magic = Math.sin(radLat)
  magic = 1 - EE * magic * magic
  const sqrtMagic = Math.sqrt(magic)
  dLat = (dLat * 180.0) / (((A * (1 - EE)) / (magic * sqrtMagic)) * PI)
  dLng = (dLng * 180.0) / ((A / sqrtMagic) * Math.cos(radLat) * PI)
  const mgLat = lat + dLat
  const mgLng = lng + dLng
  return [mgLng, mgLat]
}

function transformLat(lng: number, lat: number): number {
  let ret =
    -100.0 +
    2.0 * lng +
    3.0 * lat +
    0.2 * lat * lat +
    0.1 * lng * lat +
    0.2 * Math.sqrt(Math.abs(lng))
  ret +=
    ((20.0 * Math.sin(6.0 * lng * PI) + 20.0 * Math.sin(2.0 * lng * PI)) *
      2.0) /
    3.0
  ret +=
    ((20.0 * Math.sin(lat * PI) + 40.0 * Math.sin((lat / 3.0) * PI)) * 2.0) /
    3.0
  ret +=
    ((160.0 * Math.sin((lat / 12.0) * PI) +
      320 * Math.sin((lat * PI) / 30.0)) *
      2.0) /
    3.0
  return ret
}

function transformLng(lng: number, lat: number): number {
  let ret =
    300.0 +
    lng +
    2.0 * lat +
    0.1 * lng * lng +
    0.1 * lng * lat +
    0.1 * Math.sqrt(Math.abs(lng))
  ret +=
    ((20.0 * Math.sin(6.0 * lng * PI) + 20.0 * Math.sin(2.0 * lng * PI)) *
      2.0) /
    3.0
  ret +=
    ((20.0 * Math.sin(lng * PI) + 40.0 * Math.sin((lng / 3.0) * PI)) * 2.0) /
    3.0
  ret +=
    ((150.0 * Math.sin((lng / 12.0) * PI) +
      300.0 * Math.sin((lng / 30.0) * PI)) *
      2.0) /
    3.0
  return ret
}

/**
 * Web Mercator转WGS84
 */
function mercatorToWgs84(x: number, y: number): [number, number] {
  const lng = (x / 20037508.34) * 180.0
  let lat = (y / 20037508.34) * 180.0
  lat =
    (180.0 / PI) *
    (2 * Math.atan(Math.exp((lat * PI) / 180.0)) - PI / 2.0)
  return [lng, lat]
}

/**
 * WGS84转Web Mercator
 */
function wgs84ToMercator(lng: number, lat: number): [number, number] {
  const x = lng * 20037508.34
  let y = Math.log(Math.tan(((90.0 + lat) * PI) / 360.0)) / (PI / 180.0)
  y = (y * 20037508.34) / 180.0
  return [x, y]
}

/**
 * 百度坐标（BD09）转Web Mercator（用于OpenLayers）
 */
export function bd09ToMercator(point: Point): [number, number] {
  // BD09 -> GCJ02 -> WGS84 -> Mercator
  const [gcjLng, gcjLat] = bd09ToGcj02(point.lng, point.lat)
  const [wgsLng, wgsLat] = gcj02ToWgs84(gcjLng, gcjLat)
  const [mercX, mercY] = wgs84ToMercator(wgsLng, wgsLat)
  return [mercX, mercY]
}

/**
 * Web Mercator转百度坐标（BD09）
 */
export function mercatorToBd09(x: number, y: number): Point {
  // Mercator -> WGS84 -> GCJ02 -> BD09
  const [wgsLng, wgsLat] = mercatorToWgs84(x, y)
  const [gcjLng, gcjLat] = wgs84ToGcj02(wgsLng, wgsLat)
  const [bdLng, bdLat] = gcj02ToBd09(gcjLng, gcjLat)
  return { lng: bdLng, lat: bdLat }
}

/**
 * 批量转换：BD09转Web Mercator
 */
export function bd09PointsToMercator(points: Point[]): [number, number][] {
  return points.map((point) => bd09ToMercator(point))
}

/**
 * 批量转换：Web Mercator转BD09
 */
export function mercatorPointsToBd09(mercatorPoints: [number, number][]): Point[] {
  return mercatorPoints.map(([x, y]) => mercatorToBd09(x, y))
}

