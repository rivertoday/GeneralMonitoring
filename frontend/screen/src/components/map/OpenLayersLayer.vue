<template>
  <div ref="olContainer" class="openlayers-layer"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick, inject } from 'vue'
// @ts-ignore - OpenLayers 类型定义未安装
import Map from 'ol/Map'
// @ts-ignore - OpenLayers 类型定义未安装
import View from 'ol/View'
// @ts-ignore - OpenLayers 类型定义未安装
import VectorLayer from 'ol/layer/Vector'
// @ts-ignore - OpenLayers 类型定义未安装
import VectorSource from 'ol/source/Vector'
// @ts-ignore - OpenLayers 类型定义未安装
import Feature from 'ol/Feature'
// @ts-ignore - OpenLayers 类型定义未安装
import OLPoint from 'ol/geom/Point'
// @ts-ignore - OpenLayers 类型定义未安装
import OLPolygon from 'ol/geom/Polygon'
// @ts-ignore - OpenLayers 类型定义未安装
import OLCircle from 'ol/geom/Circle'
// @ts-ignore - OpenLayers 类型定义未安装
import { Style, Icon, Stroke, Fill, Circle as CircleStyle, Text } from 'ol/style'
import type { Point, MapMarker, MapPolygon } from '@/types/map'
import { bd09ToMercator, mercatorToBd09 } from '@/utils/coordinate'

interface Props {
  /**
   * 百度地图实例（用于同步中心点和缩放级别）
   */
  baiduMap: any
  /**
   * 标记点数据
   */
  markers?: MapMarker[]
  /**
   * 多边形数据
   */
  polygons?: MapPolygon[]
  /**
   * 是否显示标记点
   */
  showMarkers?: boolean
  /**
   * 是否显示多边形
   */
  showPolygons?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  markers: () => [],
  polygons: () => [],
  showMarkers: true,
  showPolygons: true,
})

const emit = defineEmits<{
  markerClick: [marker: MapMarker, event: any]
  polygonClick: [polygon: MapPolygon, event: any]
  polygonHover: [polygon: MapPolygon | null, event: any]
  ready: [map: Map]
}>()

const olContainer = ref<HTMLDivElement | null>(null)
const olMapInstance = ref<Map | null>(null)
const vectorSource = ref<VectorSource | null>(null)
const vectorLayer = ref<VectorLayer | null>(null)
const hoverTipRef = ref<HTMLDivElement | null>(null) // 悬停提示元素

/**
 * 初始化OpenLayers地图
 */
const initOpenLayersMap = async () => {
  if (!olContainer.value || !props.baiduMap) {
    return
  }

  await nextTick()

  try {
    // 创建VectorSource用于存储要素
    const source = new VectorSource()
    vectorSource.value = source

          // 创建VectorLayer
          const layer = new VectorLayer({
            source: source,
            visible: true, // 确保图层可见
            opacity: 1.0, // 确保不透明
            zIndex: 1000, // 确保在最上层
          })
          vectorLayer.value = layer
          
          console.log('VectorLayer创建完成:', {
            visible: layer.getVisible(),
            opacity: layer.getOpacity(),
            zIndex: layer.getZIndex(),
          })

    // 创建OpenLayers Map
    // 注意：这里不设置view，因为我们需要与百度地图同步
    const map = new Map({
      target: olContainer.value,
      layers: [layer],
      view: new View({
        // 初始值会在后续与百度地图同步时设置
        center: [0, 0],
        zoom: 2,
        projection: 'EPSG:3857', // Web Mercator
      }),
      controls: [], // 不显示OpenLayers的控件，使用百度地图的控件
      interactions: [], // 禁用所有交互，让百度地图处理拖拽、缩放等操作
    })

    // 确保不拦截鼠标事件，让百度地图可以正常拖拽和缩放
    // OpenLayers只用于渲染和检测标记点/多边形的点击

    olMapInstance.value = map

    // 同步百度地图的视图状态
    syncWithBaiduMap()

    // 监听百度地图的缩放和移动事件，同步到OpenLayers
    props.baiduMap.addEventListener('zoomend', syncWithBaiduMap)
    props.baiduMap.addEventListener('moveend', syncWithBaiduMap)
    props.baiduMap.addEventListener('resize', () => {
      if (map) {
        map.updateSize()
      }
    })

    // 监听百度地图的点击事件，检测是否点击到了OpenLayers要素
    props.baiduMap.addEventListener('click', handleBaiduMapClick)

    // 监听百度地图的鼠标移动事件，用于显示悬停提示
    props.baiduMap.addEventListener('mousemove', handleBaiduMapMouseMove)

    // 初始化时立即渲染标记点和多边形
    // 延迟渲染，确保地图视图完全同步
    setTimeout(() => {
      // 先同步视图
      syncWithBaiduMap()
      
      // 添加测试点（固定位置：慈湖站）
      addTestPoint()
      
      // 等待视图同步后再渲染要素
      setTimeout(() => {
        console.log('准备渲染要素:', {
          showMarkers: props.showMarkers,
          markersCount: props.markers.length,
          showPolygons: props.showPolygons,
          polygonsCount: props.polygons.length,
        })
        
        if (props.showMarkers && props.markers.length > 0) {
          console.log('开始渲染标记点，数量:', props.markers.length)
          updateMarkers()
        }
        if (props.showPolygons && props.polygons.length > 0) {
          console.log('初始化时渲染多边形，数量:', props.polygons.length)
          updatePolygons()
          
          // 渲染后再次同步视图，确保多边形在视图范围内
          setTimeout(() => {
            syncWithBaiduMap()
            if (olMapInstance.value && vectorSource.value) {
              // 确保地图尺寸正确
              olMapInstance.value.updateSize()
              
              // 打印当前视图状态和要素信息
              const view = olMapInstance.value.getView()
              const features = vectorSource.value.getFeatures()
              console.log('OpenLayers视图状态:', {
                center: view.getCenter(),
                zoom: view.getZoom(),
                extent: view.calculateExtent(olMapInstance.value.getSize()),
                featureCount: features.length,
              })
              
              // 打印所有要素的边界范围
              features.forEach((feature: any, index: number) => {
                const geom = feature.getGeometry()
                if (geom) {
                  const extent = geom.getExtent()
                  console.log(`要素 ${index} (${feature.get('type')}):`, {
                    extent,
                    area: geom.getType() === 'Polygon' ? geom.getArea() : null,
                  })
                }
              })
              
              // 检查图层是否被遮挡
              checkLayerVisibility()
            }
          }, 100)
        }
      }, 300)
    }, 500)

    // 触发ready事件
    emit('ready', map)
    
    // 延迟检查图层可见性
    setTimeout(() => {
      checkLayerVisibility()
    }, 1000)
  } catch (error) {
    console.error('初始化OpenLayers图层失败:', error)
  }
}

/**
 * 处理百度地图的点击事件，检测是否点击到了OpenLayers要素
 */
const handleBaiduMapClick = (baiduEvent: any) => {
  if (!olMapInstance.value || !vectorSource.value) {
    return
  }

  try {
    // 获取点击的百度坐标
    const baiduPoint: Point = {
      lng: baiduEvent.point.lng,
      lat: baiduEvent.point.lat,
    }

    // 转换为Web Mercator坐标
    const [mercX, mercY] = bd09ToMercator(baiduPoint)

    // 获取OpenLayers地图的像素坐标
    const view = olMapInstance.value.getView()
    const pixel = olMapInstance.value.getPixelFromCoordinate([mercX, mercY])

    if (!pixel) {
      return
    }

    // 检测点击位置是否有要素
    olMapInstance.value.forEachFeatureAtPixel(
      pixel,
      (feature: any) => {
        const type = feature.get('type')
        const markerId = feature.get('markerId')
        const polygonId = feature.get('polygonId')

        if (type === 'marker' && markerId !== undefined) {
          const marker = props.markers.find((m) => m.id === markerId)
          if (marker) {
            // 触发标记点点击事件
            emit('markerClick', marker, baiduEvent)
            // 阻止事件继续传播（可选，如果需要阻止百度地图的默认行为）
            if (baiduEvent.stopPropagation) {
              baiduEvent.stopPropagation()
            }
          }
        } else if (type === 'polygon' && polygonId !== undefined) {
          const polygon = props.polygons.find((p) => p.id === polygonId)
          if (polygon) {
            // 触发多边形点击事件
            emit('polygonClick', polygon, baiduEvent)
            // 阻止事件继续传播（可选）
            if (baiduEvent.stopPropagation) {
              baiduEvent.stopPropagation()
            }
          }
        }
        return true // 只处理第一个要素
      },
      {
        hitTolerance: 10, // 点击容差（像素），考虑到坐标转换可能有误差
      }
    )
  } catch (error) {
    console.warn('检测OpenLayers要素点击失败:', error)
  }
}

/**
 * 处理百度地图的鼠标移动事件，检测是否悬停在OpenLayers要素上
 */
const handleBaiduMapMouseMove = (baiduEvent: any) => {
  if (!olMapInstance.value || !vectorSource.value) {
    emit('polygonHover', null, baiduEvent)
    return
  }

  try {
    // 获取鼠标位置的百度坐标
    const baiduPoint: Point = {
      lng: baiduEvent.point.lng,
      lat: baiduEvent.point.lat,
    }

    // 转换为Web Mercator坐标
    const [mercX, mercY] = bd09ToMercator(baiduPoint)

    // 获取OpenLayers地图的像素坐标
    const pixel = olMapInstance.value.getPixelFromCoordinate([mercX, mercY])

    if (!pixel) {
      emit('polygonHover', null, baiduEvent)
      return
    }

    let hoveredPolygon: MapPolygon | null = null

    // 检测鼠标位置是否有多边形要素
    olMapInstance.value.forEachFeatureAtPixel(
      pixel,
      (feature: any) => {
        const type = feature.get('type')
        const polygonId = feature.get('polygonId')

        if (type === 'polygon' && polygonId !== undefined) {
          const polygon = props.polygons.find((p) => p.id === polygonId)
          if (polygon) {
            hoveredPolygon = polygon
          }
        }
        return true // 只处理第一个要素
      },
      {
        hitTolerance: 5, // 悬停容差（像素）
      }
    )

    // 触发悬停事件
    emit('polygonHover', hoveredPolygon, baiduEvent)
  } catch (error) {
    console.warn('检测OpenLayers要素悬停失败:', error)
    emit('polygonHover', null, baiduEvent)
  }
}

/**
 * 检查图层可见性和是否被遮挡
 */
const checkLayerVisibility = () => {
  if (!olContainer.value || !olMapInstance.value) {
    return
  }
  
  try {
    const container = olContainer.value
    const containerStyle = window.getComputedStyle(container)
    const containerRect = container.getBoundingClientRect()
    
    // 检查OpenLayers容器
    const containerInfo = {
      zIndex: containerStyle.zIndex,
      position: containerStyle.position,
      width: containerRect.width,
      height: containerRect.height,
      top: containerRect.top,
      left: containerRect.left,
      display: containerStyle.display,
      visibility: containerStyle.visibility,
      opacity: containerStyle.opacity,
    }
    
    // 检查canvas元素
    const canvas = container.querySelector('canvas')
    let canvasInfo = null
    if (canvas) {
      const canvasStyle = window.getComputedStyle(canvas)
      const canvasRect = canvas.getBoundingClientRect()
      canvasInfo = {
        zIndex: canvasStyle.zIndex,
        width: canvasRect.width,
        height: canvasRect.height,
        top: canvasRect.top,
        left: canvasRect.left,
        display: canvasStyle.display,
        visibility: canvasStyle.visibility,
        opacity: canvasStyle.opacity,
      }
    }
    
    // 检查百度地图容器（父元素）
    const baiduMapContainer = container.parentElement
    let baiduMapInfo = null
    if (baiduMapContainer) {
      const baiduStyle = window.getComputedStyle(baiduMapContainer)
      const baiduRect = baiduMapContainer.getBoundingClientRect()
      baiduMapInfo = {
        zIndex: baiduStyle.zIndex,
        width: baiduRect.width,
        height: baiduRect.height,
        top: baiduRect.top,
        left: baiduRect.left,
        className: baiduMapContainer.className,
      }
    }
    
    console.log('图层可见性检查:', {
      openLayersContainer: containerInfo,
      openLayersCanvas: canvasInfo,
      baiduMapContainer: baiduMapInfo,
      layerVisible: vectorLayer.value?.getVisible(),
      layerOpacity: vectorLayer.value?.getOpacity(),
    })
    
    // 检查是否被遮挡
    if (canvas && containerRect.width > 0 && containerRect.height > 0) {
      const canvasRect = canvas.getBoundingClientRect()
      if (canvasRect.width === 0 || canvasRect.height === 0) {
        console.warn('⚠️ OpenLayers canvas尺寸为0，可能没有正确渲染')
      }
      
      if (parseFloat(containerStyle.opacity) === 0) {
        console.warn('⚠️ OpenLayers容器透明度为0，图层不可见')
      }
      
      if (containerStyle.display === 'none') {
        console.warn('⚠️ OpenLayers容器display为none，图层被隐藏')
      }
    }
  } catch (error) {
    console.error('检查图层可见性失败:', error)
  }
}

/**
 * 同步OpenLayers视图与百度地图
 */
const syncWithBaiduMap = () => {
  if (!olMapInstance.value || !props.baiduMap) {
    return
  }

  try {
    const baiduMap = props.baiduMap
    const olMap = olMapInstance.value

    // 获取百度地图的中心点和缩放级别
    const baiduCenter = baiduMap.getCenter()
    const baiduZoom = baiduMap.getZoom()

    // 转换百度坐标到Web Mercator
    const bdPoint: Point = { lng: baiduCenter.lng, lat: baiduCenter.lat }
    const [mercX, mercY] = bd09ToMercator(bdPoint)

    // 更新OpenLayers视图
    const view = olMap.getView()
    view.setCenter([mercX, mercY])
    view.setZoom(baiduZoom)
  } catch (error) {
    console.warn('同步百度地图视图失败:', error)
  }
}

/**
 * 添加测试点（用于调试）
 */
const addTestPoint = () => {
  if (!vectorSource.value) return
  
  try {
    // 固定位置：慈湖站 [118.521577, 31.742368]
    const testPosition = { lng: 118.521577, lat: 31.742368 }
    const [mercX, mercY] = bd09ToMercator(testPosition)
    
    console.log('🔍 测试点坐标转换:', {
      bd09: testPosition,
      mercator: [mercX, mercY],
    })
    
    // 创建点几何
    const geometry = new OLPoint([mercX, mercY])
    
    // 创建要素
    const feature = new Feature({
      geometry: geometry,
      data: { type: 'test', name: '测试点-慈湖站' },
      markerId: 'test-point',
      type: 'marker',
    })
    
    // 设置样式 - 使用大红色圆圈，非常明显
    const style = new Style({
      image: new CircleStyle({
        radius: 20, // 很大的半径，确保可见
        fill: new Fill({
          color: 'rgba(255, 0, 0, 0.8)', // 红色，高不透明度
        }),
        stroke: new Stroke({
          color: '#fff',
          width: 4,
        }),
      }),
      text: new Text({
        text: '测试点',
        offsetY: -30,
        font: 'bold 16px Arial',
        fill: new Fill({
          color: '#fff',
        }),
        stroke: new Stroke({
          color: '#000',
          width: 3,
        }),
      }),
    })
    
    feature.setStyle(style)
    vectorSource.value.addFeature(feature)
    
    // 打印测试点的详细信息
    const extent = geometry.getExtent()
    console.log('✅ 测试点已添加:', {
      id: 'test-point',
      bd09: testPosition,
      mercator: [mercX, mercY],
      extent,
      geometryType: geometry.getType(),
    })
    
    // 强制刷新
    if (vectorLayer.value && olMapInstance.value) {
      vectorLayer.value.changed()
      olMapInstance.value.renderSync()
      
      // 打印视图信息
      const view = olMapInstance.value.getView()
      const viewCenter = view.getCenter()
      const viewZoom = view.getZoom()
      const viewExtent = view.calculateExtent(olMapInstance.value.getSize())
      
      console.log('📊 OpenLayers视图信息:', {
        center: viewCenter,
        zoom: viewZoom,
        extent: viewExtent,
        testPointInExtent: extent[0] >= viewExtent[0] && extent[2] <= viewExtent[2] && 
                          extent[1] >= viewExtent[1] && extent[3] <= viewExtent[3],
        testPointDistance: Math.sqrt(
          Math.pow((viewCenter?.[0] || 0) - mercX, 2) + 
          Math.pow((viewCenter?.[1] || 0) - mercY, 2)
        ),
      })
      
      // 打印容器信息
      if (olContainer.value) {
        const containerRect = olContainer.value.getBoundingClientRect()
        console.log('📦 OpenLayers容器信息:', {
          width: containerRect.width,
          height: containerRect.height,
          top: containerRect.top,
          left: containerRect.left,
          zIndex: window.getComputedStyle(olContainer.value).zIndex,
        })
      }
    }
  } catch (error) {
    console.error('❌ 添加测试点失败:', error)
  }
}

/**
 * 创建标记点要素
 */
const createMarkerFeature = (marker: MapMarker): Feature | null => {
  try {
    // 转换坐标
    const [mercX, mercY] = bd09ToMercator(marker.position)
    
    // 调试：打印坐标转换信息（仅对测试点）
    if (marker.id === 'test-point' || marker.data?.type === 'test') {
      console.log('🔍 标记点坐标转换:', {
        id: marker.id,
        bd09: marker.position,
        mercator: [mercX, mercY],
      })
    }
    
    // 调试：打印坐标转换信息
    if (marker.id === 'test-point' || marker.data?.type === 'test') {
      console.log('标记点坐标转换:', {
        id: marker.id,
        bd09: marker.position,
        mercator: [mercX, mercY],
      })
    }

    // 创建点几何
    const geometry = new OLPoint([mercX, mercY])

    // 创建要素
    const feature = new Feature({
      geometry: geometry,
      data: marker.data,
      markerId: marker.id,
      type: 'marker',
    })

    // 根据资源类型确定颜色
    let markerColor = '#409eff' // 默认蓝色
    let markerRadius = 12 // 默认半径
    if (marker.data) {
      if (marker.data.type === 'warning') {
        // 预警事件：根据预警级别设置颜色
        const levelId = marker.data.warning_level_id
        if (levelId === 1) {
          markerColor = '#ff4d4f' // 红色I级
          markerRadius = 16 // 更重要的预警，标记点更大
        } else if (levelId === 2) {
          markerColor = '#ffa940' // 橙色Ⅱ级
          markerRadius = 14
        } else if (levelId === 3) {
          markerColor = '#ffd666' // 黄色Ⅲ级
          markerRadius = 12
        } else if (levelId === 4) {
          markerColor = '#1890ff' // 蓝色Ⅳ级
          markerRadius = 10
        }
      } else if (marker.data.type === 'resource') {
        // 安全资源：根据资源类型设置颜色
        if (marker.data.resource_type === 1) markerColor = '#ff4d4f' // 红色 - 救援队伍
        else if (marker.data.resource_type === 2) markerColor = '#1890ff' // 蓝色 - 应急专家
        else if (marker.data.resource_type === 3) markerColor = '#52c41a' // 绿色 - 物资装备
      } else if (marker.data.type === 'target') {
        // 防护目标：根据目标类型设置颜色
        if (marker.data.target_type === 1) markerColor = '#faad14' // 橙色 - 学校
        else if (marker.data.target_type === 2) markerColor = '#722ed1' // 紫色 - 居民区
        else if (marker.data.target_type === 3) markerColor = '#eb2f96' // 粉色 - 医院
        else if (marker.data.target_type === 4) markerColor = '#13c2c2' // 青色 - 商场
        else markerColor = '#fa8c16' // 橙红色 - 其他
      } else if (marker.data.type === 'shelter') {
        // 避难场所：根据场所类型设置颜色
        if (marker.data.shelter_type === 1) markerColor = '#52c41a' // 绿色 - 公园
        else if (marker.data.shelter_type === 2) markerColor = '#1890ff' // 蓝色 - 广场
        else if (marker.data.shelter_type === 3) markerColor = '#faad14' // 橙色 - 体育场
        else if (marker.data.shelter_type === 4) markerColor = '#722ed1' // 紫色 - 学校
        else markerColor = '#13c2c2' // 青色 - 其他
      } else if (marker.data.type === 'video') {
        // 视频监控：根据在线状态设置颜色
        if (marker.data.online_status === 1) {
          markerColor = '#52c41a' // 绿色 - 在线
          markerRadius = 10
        } else {
          markerColor = '#ff4d4f' // 红色 - 离线
          markerRadius = 10
        }
      }
    }

    // 设置样式 - 增大标记点半径，使其更明显
    const style = new Style({
      image: marker.icon
        ? new Icon({
            src: typeof marker.icon === 'string' ? marker.icon : '',
            scale: 1,
            anchor: marker.offset
              ? [marker.offset.x || 0.5, marker.offset.y || 1]
              : [0.5, 1],
          })
        : new CircleStyle({
            radius: markerRadius, // 根据类型动态设置半径
            fill: new Fill({
              color: markerColor,
            }),
            stroke: new Stroke({
              color: '#fff',
              width: 3, // 增大边框宽度从2到3
            }),
          }),
      text: marker.label
        ? new Text({
            text: marker.label,
            offsetY: -35, // 调整文字位置
            font: 'bold 14px Arial', // 设置字体
            fill: new Fill({
              color: '#fff',
            }),
            stroke: new Stroke({
              color: '#000',
              width: 3,
            }),
          })
        : undefined,
    })

    feature.setStyle(style)

    // 调试信息
    console.log('创建标记点:', marker.id, {
      position: marker.position,
      mercator: [mercX, mercY],
      color: markerColor,
      label: marker.label,
    })

    return feature
  } catch (error) {
    console.warn('创建标记点失败:', marker.id, error)
    return null
  }
}

/**
 * 创建多边形要素
 */
const createPolygonFeature = (polygon: MapPolygon): Feature | null => {
  try {
    if (!polygon.path || polygon.path.length < 3) {
      console.warn('多边形路径点不足:', polygon.id, polygon.path?.length)
      return null
    }

    // 转换坐标点数组
    const coordinates = polygon.path.map((point) => {
      const [x, y] = bd09ToMercator(point)
      return [x, y] as [number, number]
    })

    // 检查坐标转换后的情况
    if (coordinates.length > 10) {
      console.log('多边形坐标转换后 - 第一个:', coordinates[0], '第10个:', coordinates[10], '中间:', coordinates[Math.floor(coordinates.length / 2)])
    }

    // 确保多边形闭合（最后一个点等于第一个点）
    if (coordinates.length > 0) {
      const first = coordinates[0]
      const last = coordinates[coordinates.length - 1]
      if (first && last && (first[0] !== last[0] || first[1] !== last[1])) {
        coordinates.push([first[0], first[1]])
      }
    }

    console.log('多边形坐标转换:', polygon.id, '坐标点数:', coordinates.length, '第一个坐标:', coordinates[0], '最后一个坐标:', coordinates[coordinates.length - 1])

    // 创建多边形几何（OpenLayers需要坐标环格式，外层数组是一个环）
    // 如果coordinates已经是闭合的，就直接用；否则需要确保闭合
    const geometry = new OLPolygon([coordinates])
    
    // 验证几何对象是否有效
    if (!geometry) {
      console.error('多边形几何创建失败:', polygon.id)
      return null
    }
    
    // 获取多边形的边界范围，用于调试
    const extent = geometry.getExtent()
    console.log('多边形边界范围:', polygon.id, 'extent:', extent, '坐标范围:', {
      minX: extent[0],
      minY: extent[1],
      maxX: extent[2],
      maxY: extent[3],
    })

    // 创建要素
    const feature = new Feature({
      geometry: geometry,
      data: polygon.data,
      polygonId: polygon.id,
      type: 'polygon',
    })

    // 设置样式
    const strokeColor = polygon.strokeColor || 'rgba(0, 102, 255, 1)'
    const fillColor = polygon.fillColor
      ? polygon.fillColor.startsWith('rgba')
        ? polygon.fillColor
        : `rgba(${hexToRgb(polygon.fillColor)}, ${polygon.fillOpacity || 0.3})`
      : 'rgba(0, 102, 255, 0.4)'
    
    console.log('多边形样式:', polygon.id, {
      strokeColor,
      fillColor,
      strokeWeight: polygon.strokeWeight || 5,
    })
    
    const style = new Style({
      stroke: new Stroke({
        color: strokeColor,
        width: polygon.strokeWeight || 5,
        lineDash: undefined,
      }),
      fill: new Fill({
        color: fillColor,
      }),
    })

    feature.setStyle(style)
    
    // 验证样式是否设置成功
    const actualStyle = feature.getStyle()
    console.log('多边形样式验证:', polygon.id, {
      hasStyle: !!actualStyle,
      strokeColor,
      fillColor,
      strokeWeight: polygon.strokeWeight || 5,
    })

    console.log('多边形要素创建成功:', polygon.id, '坐标点数:', coordinates.length)
    
    // 验证几何对象是否有效
    const geometryExtent = geometry.getExtent()
    const geometryArea = geometry.getArea()
    console.log('多边形几何验证:', polygon.id, {
      hasExtent: !!geometryExtent,
      extent: geometryExtent,
      area: geometryArea,
      isValid: geometryArea > 0,
    })
    
    // 强制将要素标记为已更改，触发重新渲染
    feature.changed()
    
    return feature
  } catch (error) {
    console.error('创建多边形失败:', polygon.id, error)
    return null
  }
}

/**
 * 颜色转换：HEX转RGB
 */
function hexToRgb(hex: string): string {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  if (result && result[1] && result[2] && result[3]) {
    return `${parseInt(result[1], 16)}, ${parseInt(result[2], 16)}, ${parseInt(result[3], 16)}`
  }
  return '64, 158, 255'
}

/**
 * 更新标记点
 */
const updateMarkers = () => {
  if (!vectorSource.value || !props.showMarkers) {
    console.log('跳过更新标记点:', { hasSource: !!vectorSource.value, showMarkers: props.showMarkers })
    return
  }

  console.log('开始更新标记点，数量:', props.markers.length)

  // 清除现有标记点
  const features = vectorSource.value.getFeatures()
  const markerFeatures = features.filter((feature: any) => feature.get('type') === 'marker')
  console.log('清除现有标记点数量:', markerFeatures.length)
  markerFeatures.forEach((feature: any) => {
    vectorSource.value?.removeFeature(feature)
  })

  // 添加新标记点
  let successCount = 0
  props.markers.forEach((marker) => {
    const feature = createMarkerFeature(marker)
    if (feature) {
      vectorSource.value?.addFeature(feature)
      successCount++
    } else {
      console.warn('创建标记点失败:', marker.id)
    }
  })

  console.log('标记点更新完成:', {
    total: props.markers.length,
    success: successCount,
    currentFeatures: vectorSource.value.getFeatures().length,
  })

  // 强制刷新图层和地图
  if (vectorLayer.value && olMapInstance.value) {
    vectorLayer.value.changed()
    
    // 确保视图同步
    syncWithBaiduMap()
    
    // 强制重新渲染
    setTimeout(() => {
      if (olMapInstance.value && vectorLayer.value) {
        olMapInstance.value.renderSync()
        olMapInstance.value.updateSize()
        
        // 打印最终状态
        const features = vectorSource.value.getFeatures()
        const markerFeatures = features.filter((f: any) => f.get('type') === 'marker')
        console.log('标记点渲染后状态:', {
          totalFeatures: features.length,
          markerFeatures: markerFeatures.length,
          layerVisible: vectorLayer.value.getVisible(),
          layerOpacity: vectorLayer.value.getOpacity(),
        })
        
        // 打印标记点的坐标信息
        markerFeatures.forEach((feature: any, index: number) => {
          const geom = feature.getGeometry()
          if (geom) {
            const coords = (geom as OLPoint).getCoordinates()
            console.log(`标记点 ${index + 1}:`, {
              id: feature.get('markerId'),
              label: feature.get('data')?.resource_name || feature.get('data')?.target_name || feature.get('data')?.shelter_name,
              coords,
              extent: geom.getExtent(),
            })
          }
        })
      }
    }, 100)
  }
}

/**
 * 更新多边形
 */
const updatePolygons = () => {
  if (!vectorSource.value || !props.showPolygons) {
    return
  }

  // 清除现有多边形
  const features = vectorSource.value.getFeatures()
  features.forEach((feature: any) => {
    const type = feature.get('type')
    if (type === 'polygon') {
      vectorSource.value?.removeFeature(feature)
    }
  })

  // 添加新多边形
  console.log('开始更新多边形，数量:', props.polygons.length)
  props.polygons.forEach((polygon) => {
    console.log('处理多边形:', polygon.id, '路径点数:', polygon.path?.length || 0)
    const feature = createPolygonFeature(polygon)
    if (feature) {
      vectorSource.value?.addFeature(feature)
      console.log('✓ 已添加多边形要素:', polygon.id)
    } else {
      console.error('✗ 创建多边形要素失败:', polygon.id)
    }
  })
  
  // 强制刷新图层和地图
  if (vectorLayer.value) {
    vectorLayer.value.changed()
    // 强制重新渲染
    setTimeout(() => {
      if (vectorLayer.value && olMapInstance.value) {
        vectorLayer.value.changed()
        olMapInstance.value.renderSync()
        // 再次更新尺寸，确保正确渲染
        olMapInstance.value.updateSize()
        
        // 打印图层状态
        console.log('图层刷新后状态:', {
          layerVisible: vectorLayer.value.getVisible(),
          layerOpacity: vectorLayer.value.getOpacity(),
          featureCount: vectorSource.value?.getFeatures().length || 0,
        })
      }
    }, 100)
  }
  
  console.log('多边形更新完成，当前要素数:', vectorSource.value?.getFeatures().length || 0)
}

// 监听标记点变化
watch(
  () => props.markers,
  () => {
    if (olMapInstance.value) {
      updateMarkers()
    }
  },
  { deep: true }
)

// 监听多边形变化
watch(
  () => props.polygons,
  () => {
    if (olMapInstance.value) {
      updatePolygons()
    }
  },
  { deep: true }
)

// 监听显示标记点开关
watch(
  () => props.showMarkers,
  () => {
    if (olMapInstance.value) {
      updateMarkers()
    }
  }
)

// 监听显示多边形开关
watch(
  () => props.showPolygons,
  () => {
    if (olMapInstance.value) {
      updatePolygons()
    }
  }
)

// 暴露方法和实例
defineExpose({
  getMap: () => olMapInstance.value,
  getVectorSource: () => vectorSource.value,
  syncView: syncWithBaiduMap,
  updateMarkers,
  updatePolygons,
  // 提供检测点击的方法，供外部调用
  detectFeatureAtPoint: (point: Point) => {
    if (!olMapInstance.value) {
      return null
    }
    const [mercX, mercY] = bd09ToMercator(point)
    const pixel = olMapInstance.value.getPixelFromCoordinate([mercX, mercY])
    if (!pixel) {
      return null
    }
    let result: { type: string; id: string | number; feature: Feature } | null = null
    olMapInstance.value.forEachFeatureAtPixel(pixel, (feature: any) => {
      const type = feature.get('type')
      const markerId = feature.get('markerId')
      const polygonId = feature.get('polygonId')
      if (type === 'marker' && markerId !== undefined) {
        result = { type: 'marker', id: markerId, feature }
      } else if (type === 'polygon' && polygonId !== undefined) {
        result = { type: 'polygon', id: polygonId, feature }
      }
      return true
    })
    return result
  },
})

onMounted(() => {
  if (props.baiduMap) {
    // 等待百度地图完全加载后再初始化OpenLayers
    setTimeout(() => {
      initOpenLayersMap()
    }, 500)
  }
})

onUnmounted(() => {
  if (olMapInstance.value) {
    // 移除事件监听
    if (props.baiduMap) {
      props.baiduMap.removeEventListener('zoomend', syncWithBaiduMap)
      props.baiduMap.removeEventListener('moveend', syncWithBaiduMap)
      props.baiduMap.removeEventListener('click', handleBaiduMapClick)
      props.baiduMap.removeEventListener('mousemove', handleBaiduMapMouseMove)
    }
    // 销毁OpenLayers地图实例
    olMapInstance.value.setTarget(undefined)
    olMapInstance.value = null
  }
  vectorSource.value = null
  vectorLayer.value = null
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;

.openlayers-layer {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000; // 确保在百度地图上方
  pointer-events: none !important; // 完全不拦截事件，让百度地图处理所有交互（拖拽、缩放、点击等）

  // OpenLayers只用于可视化显示，所有交互都由百度地图处理
  // 标记点和多边形的点击通过百度地图的点击事件来检测
  
  // 调试：添加背景色以检查容器是否渲染（临时调试用）
  // background: rgba(0, 255, 0, 0.1); // 绿色半透明，确认容器可见后可以注释掉

  // 隐藏OpenLayers的控件
  :deep(.ol-control) {
    display: none;
    pointer-events: none !important;
  }
  
  // 调试：检查canvas容器（临时调试用）
  :deep(.ol-layer-container) {
    // background: rgba(0, 255, 0, 0.1); // 绿色半透明，确认容器可见后可以注释掉
    pointer-events: none !important;
  }

  // 确保OpenLayers的canvas覆盖整个容器，但不拦截事件
  :deep(.ol-viewport) {
    width: 100%;
    height: 100%;
    pointer-events: none !important;
    
    canvas {
      pointer-events: none !important;
    }
  }

  // 隐藏OpenLayers的logo
  :deep(.ol-attribution) {
    display: none;
    pointer-events: none !important;
  }
}
</style>
