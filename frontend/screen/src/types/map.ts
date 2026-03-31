/**
 * 地图相关类型定义
 */

/**
 * 坐标点（WGS84经纬度）
 */
export interface Point {
  lng: number
  lat: number
}

/**
 * 地图标记点配置
 */
export interface MarkerConfig {
  position: Point // 标记点位置
  title?: string // 标题
  icon?: string | object // 图标
  label?: string // 标签
  zIndex?: number // 层级
  enableDragging?: boolean // 是否可拖拽
  enableClicking?: boolean // 是否可点击
  offset?: { x: number; y: number } // 偏移量
}

/**
 * 地图标记点
 */
export interface MapMarker extends MarkerConfig {
  id: string | number // 唯一标识
  data?: any // 关联的业务数据
}

/**
 * 地图多边形配置
 */
export interface PolygonConfig {
  path: Point[] // 多边形路径点数组
  strokeColor?: string // 边线颜色
  strokeWeight?: number // 边线宽度
  strokeOpacity?: number // 边线透明度
  fillColor?: string // 填充颜色
  fillOpacity?: number // 填充透明度
}

/**
 * 地图多边形
 */
export interface MapPolygon extends PolygonConfig {
  id: string | number // 唯一标识
  data?: any // 关联的业务数据
}

/**
 * 地图信息窗口配置
 */
export interface InfoWindowConfig {
  content: string | HTMLElement // 内容
  width?: number // 宽度
  height?: number // 高度
  offset?: { x: number; y: number } // 偏移量
  enableAutoPan?: boolean // 是否自动平移
  enableCloseOnClick?: boolean // 是否点击关闭
}

/**
 * 地图事件类型
 */
export type MapEventType =
  | 'click'
  | 'dblclick'
  | 'mousemove'
  | 'mouseover'
  | 'mouseout'
  | 'zoomstart'
  | 'zoomend'
  | 'moveend'
  | 'dragend'

/**
 * 地图事件回调
 */
export type MapEventCallback = (event: any) => void

/**
 * 百度地图配置
 */
export interface BaiduMapConfig {
  center?: Point
  zoom?: number
  minZoom?: number
  maxZoom?: number
  enableScrollWheelZoom?: boolean
  enableDragging?: boolean
  enableDoubleClickZoom?: boolean
  enableKeyboard?: boolean
  mapStyle?: string
}

