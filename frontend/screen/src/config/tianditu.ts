/**
 * 天地图服务配置
 */
import * as Cesium from 'cesium'

/**
 * 天地图 app_key
 * 从环境变量获取，如果没有则使用默认值（需要替换为实际的 app_key）
 */
export const TIANDITU_APP_KEY = import.meta.env.VITE_TIANDITU_APP_KEY || 'your-tianditu-app-key'

/**
 * 天地图服务域名
 */
const TIANDITU_DOMAINS = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7']

/**
 * 获取天地图服务域名（负载均衡）
 */
export function getTiandituDomain(): string {
  const index = Math.floor(Math.random() * TIANDITU_DOMAINS.length)
  return TIANDITU_DOMAINS[index] || 't0'
}

/**
 * 天地图图层类型
 */
export const TiandituLayerType = {
  VEC: 'vec', // 矢量地图
  IMG: 'img', // 影像地图
  TER: 'ter', // 地形地图
  CIA: 'cia', // 矢量注记
  CVA: 'cva', // 影像注记
} as const

export type TiandituLayerType = typeof TiandituLayerType[keyof typeof TiandituLayerType]

/**
 * 天地图服务 URL 模板
 * @param layer 图层类型
 * @param subdomain 子域名
 */
export function getTiandituUrl(layer: TiandituLayerType, subdomain?: string): string {
  const domain = subdomain || getTiandituDomain()
  return `https://${domain}.tianditu.gov.cn/${layer}_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=${layer}&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=${TIANDITU_APP_KEY}`
}

/**
 * 创建天地图影像图层配置
 */
export function createTiandituImageryProvider(layer: TiandituLayerType) {
  const url = getTiandituUrl(layer)
  
  // 调试：打印 URL 和 app_key
  console.log(`天地图图层 ${layer} URL:`, url)
  console.log(`天地图 app_key:`, TIANDITU_APP_KEY)
  
  return new Cesium.WebMapTileServiceImageryProvider({
    url: url,
    layer: layer,
    style: 'default',
    format: 'tiles',
    tileMatrixSetID: 'w',
    credit: new Cesium.Credit('天地图'),
    maximumLevel: 18,
  } as any)
}

/**
 * 创建天地图底图图层（矢量地图 + 注记）
 */
export function createTiandituBaseLayer() {
  return [
    createTiandituImageryProvider(TiandituLayerType.VEC), // 矢量底图
    createTiandituImageryProvider(TiandituLayerType.CIA), // 矢量注记
  ]
}

/**
 * 创建天地图影像图层（影像地图 + 注记）
 */
export function createTiandituImageLayer() {
  return [
    createTiandituImageryProvider(TiandituLayerType.IMG), // 影像底图
    createTiandituImageryProvider(TiandituLayerType.CVA), // 影像注记
  ]
}

/**
 * 创建天地图地形图层（地形地图 + 注记）
 */
export function createTiandituTerrainLayer() {
  return [
    createTiandituImageryProvider(TiandituLayerType.TER), // 地形底图
    createTiandituImageryProvider(TiandituLayerType.CIA), // 矢量注记
  ]
}

