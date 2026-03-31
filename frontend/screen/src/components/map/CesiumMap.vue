<template>
  <div ref="mapContainer" class="cesium-map-container"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as Cesium from 'cesium'
import type { Point } from '@/types/map'
import {
  ensureCesiumOnWindow,
  createTiandituImageLayers,
  createTiandituVectorLayers,
  createTiandituTerrainProvider,
  createTianditu3DNameService,
  loadTiandituPlugins,
  isTiandituPluginsLoaded,
} from '@/utils/tianditu'

interface Props {
  center?: Point // 地图中心点（经纬度）
  zoom?: number // 缩放级别（对应 Cesium 的相机高度）
  minZoom?: number // 最小缩放级别
  maxZoom?: number // 最大缩放级别
  mapStyle?: 'normal' | 'satellite' | 'terrain' // 地图样式
  enableScrollWheelZoom?: boolean // 启用滚轮缩放
  enableDragging?: boolean // 启用拖拽
  enableDoubleClickZoom?: boolean // 启用双击缩放
  enableKeyboard?: boolean // 启用键盘操作
  sceneMode?: '2D' | '3D' | 'COLUMBUS_VIEW' // 场景模式
}

const props = withDefaults(defineProps<Props>(), {
  center: () => ({ lng: 118.521577, lat: 31.742368 }), // 默认中心点：慈湖站位置
  zoom: 12,
  minZoom: 3,
  maxZoom: 19,
  enableScrollWheelZoom: true,
  enableDragging: true,
  enableDoubleClickZoom: true,
  enableKeyboard: true,
  mapStyle: 'normal',
  sceneMode: '2D',
})

const emit = defineEmits<{
  ready: [viewer: any]
  click: [event: any]
  dblclick: [event: any]
  mousemove: [event: any]
  zoomend: [event: any]
  moveend: [event: any]
}>()

const mapContainer = ref<HTMLDivElement | null>(null)
const viewer = ref<any>(null)
const isMapReady = ref(false)
const wtfsService = ref<any>(null) // 三维地名服务实例

/**
 * 初始化 Cesium 地图
 */
const initCesiumMap = async () => {
  if (!mapContainer.value) {
    return
  }

  await nextTick()

  try {
    // 确保Cesium挂载在window对象上（天地图扩展插件需要）
    ensureCesiumOnWindow()

    // 创建 Cesium Viewer（先创建Viewer，再加载扩展插件）
    console.log('创建 Cesium Viewer...')
    viewer.value = new Cesium.Viewer(mapContainer.value, {
      // 不显示默认的底图（使用天地图）
      baseLayerPicker: false,
      // 使用椭球地形作为初始地形（后续会根据地图样式切换）
      terrainProvider: new Cesium.EllipsoidTerrainProvider(),
      // 不显示默认的动画控件
      animation: false,
      // 不显示默认的时间轴控件
      timeline: false,
      // 不显示默认的全屏控件
      fullscreenButton: false,
      // 不显示默认的VR控件
      vrButton: false,
      // 不显示默认的地理编码搜索框
      geocoder: false,
      // 不显示默认的Home按钮
      homeButton: false,
      // 不显示默认的信息框
      infoBox: false,
      // 不显示默认的选择指示器
      selectionIndicator: false,
      // 不显示默认的导航帮助
      navigationHelpButton: false,
      // 不显示默认的导航指令提示
      navigationInstructionsInitiallyVisible: false,
      // 场景模式
      sceneMode: getSceneMode(props.sceneMode),
      // 请求渲染模式
      requestRenderMode: true,
      // 最大渲染时间
      maximumRenderTimeChange: Infinity,
    })

    // Viewer创建后，等待一下确保完全初始化
    await new Promise(resolve => setTimeout(resolve, 200))
    
    // Viewer创建后，加载天地图扩展插件
    console.log('开始加载天地图扩展插件（在Viewer创建之后）...')
    try {
      if (!isTiandituPluginsLoaded()) {
        await loadTiandituPlugins()
      }
      console.log('✓ 天地图扩展插件已就绪')
    } catch (error) {
      console.warn('⚠️ 天地图扩展插件加载失败，三维地名服务可能不可用:', error)
      // 即使加载失败，也继续设置底图
    }

    // 设置天地图底图（包括三维地名服务）
    updateMapStyle(props.mapStyle)

    // 设置初始视图
    updateCenterAndZoom()
    
    // 抑制天地图瓦片加载错误（CORS和418错误在开发环境中很常见，不影响功能）
    // 这些错误会在生产环境中消失（如果部署在正确的域名下）
    // 添加安全检查，确保对象存在后再添加事件监听器
    if (viewer.value && viewer.value.scene && viewer.value.scene.globe && viewer.value.scene.globe.tileLoadErrorEvent) {
      viewer.value.scene.globe.tileLoadErrorEvent.addEventListener((error: any) => {
        // 只在开发环境中抑制错误日志
        if (import.meta.env.DEV) {
          // 检查是否是CORS或418错误（天地图服务限制）
          if (error && (error.message?.includes('CORS') || error.message?.includes('418'))) {
            // 静默处理，不输出错误
            return
          }
        }
        // 其他错误正常处理
        console.error('地图瓦片加载错误:', error)
      })
    }
    
    // 调试：检查图层状态
    setTimeout(() => {
      console.log('天地图图层状态:', {
        layerCount: viewer.value.imageryLayers.length,
        layers: viewer.value.imageryLayers._layers.map((layer: any) => ({
          ready: layer._imageryProvider?.ready,
          errorEvent: layer._imageryProvider?.errorEvent,
        })),
      })
      
      // 检查相机位置
      const camera = viewer.value.camera
      const position = camera.positionCartographic
      console.log('相机位置:', {
        longitude: Cesium.Math.toDegrees(position.longitude),
        latitude: Cesium.Math.toDegrees(position.latitude),
        height: position.height,
      })
    }, 1000)

    // 设置相机限制
    if (props.minZoom !== undefined || props.maxZoom !== undefined) {
      const camera = viewer.value.camera
      
      // 监听相机高度变化
      camera.moveEnd.addEventListener(() => {
        const height = camera.positionCartographic.height
        const currentZoom = getZoomFromHeight(height)
        
        if (props.minZoom !== undefined && currentZoom < props.minZoom) {
          const targetHeight = getHeightFromZoom(props.minZoom)
          camera.setView({
            destination: Cesium.Cartesian3.fromDegrees(
              props.center.lng,
              props.center.lat,
              targetHeight
            ),
          })
        } else if (props.maxZoom !== undefined && currentZoom > props.maxZoom) {
          const targetHeight = getHeightFromZoom(props.maxZoom)
          camera.setView({
            destination: Cesium.Cartesian3.fromDegrees(
              props.center.lng,
              props.center.lat,
              targetHeight
            ),
          })
        }
      })
    }

    // 禁用/启用滚轮缩放
    if (!props.enableScrollWheelZoom) {
      viewer.value.scene.screenSpaceCameraController.enableZoom = false
    }

    // 禁用/启用拖拽
    if (!props.enableDragging) {
      viewer.value.scene.screenSpaceCameraController.enableTranslate = false
    }

    // 禁用/启用双击缩放
    if (!props.enableDoubleClickZoom) {
      viewer.value.scene.screenSpaceCameraController.enableLook = false
    }

    // 禁用/启用键盘操作
    if (!props.enableKeyboard) {
      viewer.value.scene.screenSpaceCameraController.enableKeyboardEvent = false
    }

    // 绑定事件
    bindEvents()
    
    // 延迟设置就绪状态，确保所有初始化都完成
    await new Promise(resolve => setTimeout(resolve, 100))

    isMapReady.value = true
    emit('ready', viewer.value)

    console.log('Cesium 地图初始化完成')
  } catch (error) {
    console.error('Cesium 地图初始化失败:', error)
    // 即使初始化失败，也要设置就绪状态，避免阻塞后续操作
    isMapReady.value = false
  }
}

/**
 * 获取场景模式
 */
function getSceneMode(mode: string): any {
  switch (mode) {
    case '2D':
      return Cesium.SceneMode.SCENE2D
    case '3D':
      return Cesium.SceneMode.SCENE3D
    case 'COLUMBUS_VIEW':
      return Cesium.SceneMode.COLUMBUS_VIEW
    default:
      return Cesium.SceneMode.SCENE2D
  }
}

/**
 * 更新地图样式
 */
function updateMapStyle(style: 'normal' | 'satellite' | 'terrain') {
  if (!viewer.value) return

  // 清除现有图层
  viewer.value.imageryLayers.removeAll()
  
  // 清除三维地名服务
  if (wtfsService.value) {
    try {
      wtfsService.value.destroy?.()
    } catch (e) {
      console.warn('清除三维地名服务时出错:', e)
    }
    wtfsService.value = null
  }

  try {
    // 根据当前场景模式决定图层类型
    const currentSceneMode = viewer.value.scene.mode
    const is2DMode = currentSceneMode === Cesium.SceneMode.SCENE2D || currentSceneMode === Cesium.SceneMode.COLUMBUS_VIEW
    
    switch (style) {
      case 'normal':
        // 标准地图：2D模式使用矢量图层，3D模式使用影像图层
        {
          if (is2DMode) {
            // 2D模式：使用矢量图层（球面墨卡托投影，更清晰、性能更好）
            console.log('2D模式：使用天地图矢量图层（球面墨卡托投影）')
            const layers = createTiandituVectorLayers()
            layers.forEach((layer, index) => {
              viewer.value.imageryLayers.addImageryProvider(layer)
              console.log(`  天地图矢量图层 ${index} 已添加 (${index === 0 ? '矢量底图 vec_w（球面墨卡托投影）' : '矢量注记 cva_w（球面墨卡托投影）'})`)
            })
          } else {
            // 3D模式：使用影像图层（更真实）
            console.log('3D模式：使用天地图影像图层')
            const layers = createTiandituImageLayers()
            layers.forEach((layer, index) => {
              viewer.value.imageryLayers.addImageryProvider(layer)
              console.log(`  天地图影像图层 ${index} 已添加`)
            })
          }
        }
        break
        
      case 'satellite':
        // 影像地图：使用影像图层 + 国界
        {
          const layers = createTiandituImageLayers()
          layers.forEach((layer, index) => {
            viewer.value.imageryLayers.addImageryProvider(layer)
            console.log(`天地图影像图层 ${index} 已添加`)
          })
        }
        break
        
      case 'terrain':
        // 地形地图：设置地形提供者
        {
          const terrainProvider = createTiandituTerrainProvider()
          viewer.value.terrainProvider = terrainProvider
          console.log('天地图地形服务已设置')
          
          // 添加影像图层作为底图
          const imageLayer = createTiandituImageLayers()[0]
          viewer.value.imageryLayers.addImageryProvider(imageLayer)
        }
        break
    }
    
    // 添加三维地名服务（如果扩展插件已加载）
    if (isTiandituPluginsLoaded() && viewer.value) {
      try {
        const wtfs = createTianditu3DNameService(viewer.value)
        if (wtfs) {
          wtfsService.value = wtfs
          console.log('✓ 天地图三维地名服务已添加')
        }
      } catch (error) {
        console.warn('⚠️ 添加三维地名服务失败:', error)
      }
    } else {
      console.warn('⚠️ 三维地名服务不可用（扩展插件未加载）')
    }
    
    // 强制渲染
    viewer.value.scene.requestRender()
  } catch (error) {
    console.error('创建天地图图层失败:', error)
  }
}

/**
 * 更新中心点和缩放级别
 */
function updateCenterAndZoom() {
  if (!viewer.value) return

  const height = getHeightFromZoom(props.zoom || 12)
  viewer.value.camera.setView({
    destination: Cesium.Cartesian3.fromDegrees(props.center.lng, props.center.lat, height),
  })
}

/**
 * 从缩放级别计算相机高度
 */
function getHeightFromZoom(zoom: number): number {
  // Cesium 的相机高度与缩放级别的关系（近似）
  // 缩放级别越大，高度越小
  const baseHeight = 40075017 // 地球周长的一半（米）
  return baseHeight / Math.pow(2, zoom)
}

/**
 * 从相机高度计算缩放级别
 */
function getZoomFromHeight(height: number): number {
  const baseHeight = 40075017
  return Math.log2(baseHeight / Math.max(height, 1))
}

/**
 * 绑定地图事件
 */
function bindEvents() {
  if (!viewer.value) return

  // 点击事件
  viewer.value.cesiumWidget.canvas.addEventListener('click', (event: MouseEvent) => {
    const clickPosition = new Cesium.Cartesian2(event.clientX, event.clientY)
    
    // 优先检测Billboard（图标），然后检测其他Entity
    // 使用drillPick获取所有被点击的Entity，优先返回Billboard
    const pickedObjects = viewer.value.scene.drillPick(clickPosition)
    
    let pickedObject = null
    let pickedEntity = null
    
    if (pickedObjects && pickedObjects.length > 0) {
      // 优先选择Billboard（图标）
      const billboard = pickedObjects.find((obj: any) => {
        // 检查是否有billboard属性或者是Billboard实例
        if (obj.id && obj.id.billboard) {
          return true
        }
        if (obj.primitive instanceof Cesium.Billboard) {
          return true
        }
        // 检查primitive是否有billboard属性
        if (obj.primitive && obj.primitive.id && obj.primitive.id.billboard) {
          return true
        }
        return false
      })
      
      if (billboard) {
        pickedObject = billboard
        // 获取Entity对象
        pickedEntity = billboard.id || (billboard.primitive && billboard.primitive.id) || null
      } else {
        // 如果没有Billboard，选择第一个有id的Entity
        const entityObj = pickedObjects.find((obj: any) => {
          return obj.id || (obj.primitive && obj.primitive.id)
        })
        if (entityObj) {
          pickedObject = entityObj
          pickedEntity = entityObj.id || (entityObj.primitive && entityObj.primitive.id) || null
        } else {
          pickedObject = pickedObjects[0]
          pickedEntity = pickedObjects[0]?.id || null
        }
      }
    } else {
      // 如果没有drillPick到，使用pick（单点检测）
      const picked = viewer.value.scene.pick(clickPosition)
      if (picked) {
        pickedObject = picked
        pickedEntity = picked.id || (picked.primitive && picked.primitive.id) || null
      }
    }
    
    // 如果仍然没有找到Entity，尝试通过坐标查找最近的Entity
    if (!pickedEntity && viewer.value) {
      const cartesian = viewer.value.camera.pickEllipsoid(clickPosition, viewer.value.scene.globe.ellipsoid)
      if (cartesian) {
        // 查找距离点击位置最近的Entity
        const allEntities = viewer.value.entities.values
        let minDistance = Infinity
        let nearestEntity: any = null
        
        for (let i = 0; i < allEntities.length; i++) {
          const entity = allEntities[i]
          if (entity.position && entity.billboard) {
            const entityPosition = entity.position.getValue(viewer.value.clock.currentTime)
            if (entityPosition) {
              const distance = Cesium.Cartesian3.distance(cartesian, entityPosition)
              // 如果距离在合理范围内（例如500米内），认为是点击了该Entity
              if (distance < minDistance && distance < 500) {
                minDistance = distance
                nearestEntity = entity
              }
            }
          }
        }
        
        if (nearestEntity) {
          pickedEntity = nearestEntity
          console.log('通过坐标查找找到最近的Entity:', nearestEntity.id, '距离:', minDistance.toFixed(2), '米')
        }
      }
    }
    
    emit('click', {
      event,
      pickedObject,
      pickedEntity, // 添加pickedEntity字段，方便父组件使用
      position: viewer.value.camera.pickEllipsoid(
        clickPosition,
        viewer.value.scene.globe.ellipsoid
      ),
    })
  })

  // 双击事件
  viewer.value.cesiumWidget.canvas.addEventListener('dblclick', (event: MouseEvent) => {
    emit('dblclick', { event })
  })

  // 鼠标移动事件
  viewer.value.cesiumWidget.canvas.addEventListener('mousemove', (event: MouseEvent) => {
    const pickPosition = new Cesium.Cartesian2(event.clientX, event.clientY)
    
    // 尝试pick Entity
    let pickedObject = null
    let pickedEntity = null
    
    try {
      const picked = viewer.value.scene.pick(pickPosition)
      if (picked) {
        pickedObject = picked
        pickedEntity = picked.id || (picked.primitive && picked.primitive.id) || null
      }
      
      // 如果pick没找到，尝试drillPick
      if (!pickedEntity) {
        const pickedObjects = viewer.value.scene.drillPick(pickPosition)
        if (pickedObjects && pickedObjects.length > 0) {
          // 优先选择Billboard（图标），然后选择其他Entity
          const billboard = pickedObjects.find((obj: any) => {
            if (obj.id && obj.id.billboard) return true
            if (obj.primitive && obj.primitive.id && obj.primitive.id.billboard) return true
            return false
          })
          
          if (billboard) {
            pickedObject = billboard
            pickedEntity = billboard.id || (billboard.primitive && billboard.primitive.id) || null
          } else {
            pickedObject = pickedObjects[0]
            pickedEntity = pickedObjects[0].id || (pickedObjects[0].primitive && pickedObjects[0].primitive.id) || null
          }
        }
      }
    } catch (error) {
      // 忽略pick错误
    }
    
    emit('mousemove', {
      event,
      pickedObject,
      pickedEntity,
    })
  })

  // 相机移动结束事件
  viewer.value.camera.moveEnd.addEventListener(() => {
    emit('moveend', {
      center: getCenter(),
      zoom: getZoom(),
    })
  })
}

/**
 * 获取当前中心点
 */
function getCenter(): Point {
  if (!viewer.value) {
    return { lng: 0, lat: 0 }
  }

  const camera = viewer.value.camera
  const cartographic = camera.positionCartographic
  return {
    lng: Cesium.Math.toDegrees(cartographic.longitude),
    lat: Cesium.Math.toDegrees(cartographic.latitude),
  }
}

/**
 * 获取当前缩放级别
 */
function getZoom(): number {
  if (!viewer.value) {
    return 12
  }

  const height = viewer.value.camera.positionCartographic.height
  return getZoomFromHeight(height)
}

// 监听属性变化
watch(
  () => props.center,
  () => {
    if (isMapReady.value) {
      updateCenterAndZoom()
    }
  },
  { deep: true }
)

watch(
  () => props.zoom,
  () => {
    if (isMapReady.value) {
      updateCenterAndZoom()
    }
  }
)

watch(
  () => props.mapStyle,
  (newStyle) => {
    if (isMapReady.value) {
      updateMapStyle(newStyle)
    }
  }
)

watch(
  () => props.sceneMode,
  (newMode) => {
    if (isMapReady.value && viewer.value) {
      viewer.value.scene.mode = getSceneMode(newMode)
      // 场景模式改变后，如果地图样式是 normal，需要重新加载图层
      // 因为 2D 模式使用矢量图层，3D 模式使用影像图层
      if (props.mapStyle === 'normal') {
        // 等待场景模式切换完成后再更新图层
        setTimeout(() => {
          updateMapStyle(props.mapStyle)
        }, 100)
      }
    }
  }
)

// 生命周期
onMounted(() => {
  initCesiumMap()
})

onUnmounted(() => {
  // 清理三维地名服务
  if (wtfsService.value) {
    try {
      wtfsService.value.destroy?.()
    } catch (e) {
      console.warn('清理三维地名服务时出错:', e)
    }
    wtfsService.value = null
  }
  
  // 销毁Cesium Viewer
  if (viewer.value) {
    viewer.value.destroy()
    viewer.value = null
  }
})

// 暴露方法
defineExpose({
  getViewer: () => viewer.value,
  getCenter,
  getZoom,
  setCenter: (center: Point) => {
    if (viewer.value) {
      const height = viewer.value.camera.positionCartographic.height
      viewer.value.camera.setView({
        destination: Cesium.Cartesian3.fromDegrees(center.lng, center.lat, height),
      })
    }
  },
  setZoom: (zoom: number) => {
    if (viewer.value) {
      const center = getCenter()
      const height = getHeightFromZoom(zoom)
      viewer.value.camera.setView({
        destination: Cesium.Cartesian3.fromDegrees(center.lng, center.lat, height),
      })
    }
  },
  setMapStyle: (style: 'normal' | 'satellite' | 'terrain') => {
    updateMapStyle(style)
  },
  panTo: (point: Point) => {
    if (viewer.value) {
      const height = viewer.value.camera.positionCartographic.height
      viewer.value.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(point.lng, point.lat, height),
      })
    }
  },
  setSceneMode: (mode: '2D' | '3D' | 'COLUMBUS_VIEW') => {
    if (viewer.value) {
      viewer.value.scene.mode = getSceneMode(mode)
      // 场景模式改变后，如果地图样式是 normal，需要重新加载图层
      if (props.mapStyle === 'normal') {
        setTimeout(() => {
          updateMapStyle(props.mapStyle)
        }, 100)
      }
    }
  },
  fitBounds: (points: Point[]) => {
    if (viewer.value && points.length > 0) {
      const boundingSphere = Cesium.BoundingSphere.fromPoints(
        points.map((p) =>
          Cesium.Cartesian3.fromDegrees(p.lng, p.lat)
        )
      )
      viewer.value.camera.flyTo({
        destination: boundingSphere.center,
        orientation: {
          heading: Cesium.Math.toRadians(0),
          pitch: Cesium.Math.toRadians(-90),
          roll: 0.0,
        },
      })
    }
  },
})
</script>

<style scoped lang="scss">
.cesium-map-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}
</style>

