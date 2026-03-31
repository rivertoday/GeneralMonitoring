<template>
  <div ref="mapContainer" class="baidu-map-container"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import type { BaiduMapConfig, Point, MapEventType, MapEventCallback } from '@/types/map'
import { waitForBaiduMap, isBaiduMapLoaded } from '@/utils/map'

interface Props {
  center?: Point // 地图中心点
  zoom?: number // 缩放级别
  minZoom?: number // 最小缩放级别
  maxZoom?: number // 最大缩放级别
  enableScrollWheelZoom?: boolean // 启用滚轮缩放
  enableDragging?: boolean // 启用拖拽
  enableDoubleClickZoom?: boolean // 启用双击缩放
  enableKeyboard?: boolean // 启用键盘操作
  mapStyle?: string // 地图样式：normal, satellite, hybrid
}

const props = withDefaults(defineProps<Props>(), {
  center: () => ({ lng: 118.521577, lat: 31.742368 }), // 默认中心点：慈湖站位置
  zoom: 13,
  minZoom: 3,
  maxZoom: 19,
  enableScrollWheelZoom: true,
  enableDragging: true,
  enableDoubleClickZoom: true,
  enableKeyboard: true,
  mapStyle: 'normal',
})

const emit = defineEmits<{
  ready: [map: any]
  click: [event: any]
  dblclick: [event: any]
  mousemove: [event: any]
  zoomend: [event: any]
  moveend: [event: any]
}>()

const mapContainer = ref<HTMLDivElement | null>(null)
const mapInstance = ref<any>(null)
const isMapReady = ref(false)
const controlsAdded = ref(false) // 标记控件是否已添加

/**
 * 初始化百度地图
 */
const initMap = async () => {
  if (!mapContainer.value) {
    console.error('地图容器不存在')
    return
  }

  // 确保容器有尺寸
  if (mapContainer.value.offsetWidth === 0 || mapContainer.value.offsetHeight === 0) {
    console.warn('地图容器尺寸为0，延迟初始化')
    setTimeout(() => {
      initMap()
    }, 100)
    return
  }

  try {
    // 等待百度地图API加载完成
    await waitForBaiduMap()

    if (!isBaiduMapLoaded()) {
      console.error('百度地图API未加载')
      return
    }

    // 如果地图已经初始化，先销毁
    if (mapInstance.value) {
      mapInstance.value = null
    }

    // 创建地图实例
    const BMap = window.BMap
    const map = new BMap.Map(mapContainer.value)

    // 设置地图中心点和缩放级别
    const point = new BMap.Point(props.center.lng, props.center.lat)
    map.centerAndZoom(point, props.zoom)

    // 设置最小和最大缩放级别
    if (props.minZoom) {
      map.setMinZoom(props.minZoom)
    }
    if (props.maxZoom) {
      map.setMaxZoom(props.maxZoom)
    }

    // 启用滚轮缩放
    if (props.enableScrollWheelZoom) {
      map.enableScrollWheelZoom()
    } else {
      map.disableScrollWheelZoom()
    }

    // 启用拖拽
    if (props.enableDragging) {
      map.enableDragging()
    } else {
      map.disableDragging()
    }

    // 启用双击缩放
    if (props.enableDoubleClickZoom) {
      map.enableDoubleClickZoom()
    } else {
      map.disableDoubleClickZoom()
    }

    // 启用键盘操作
    if (props.enableKeyboard) {
      map.enableKeyboard()
    } else {
      map.disableKeyboard()
    }

    // 设置地图样式
    const mapTypes: Record<string, any> = {
      normal: BMap.BMAP_NORMAL_MAP,
      satellite: BMap.BMAP_SATELLITE_MAP,
      hybrid: BMap.BMAP_HYBRID_MAP,
    }
    if (mapTypes[props.mapStyle]) {
      map.setMapType(mapTypes[props.mapStyle])
    }

    // 保存地图实例（先保存，后续再添加控件）
    mapInstance.value = map

    // 监听地图事件
    map.addEventListener('click', (e: any) => {
      emit('click', e)
    })

    map.addEventListener('dblclick', (e: any) => {
      emit('dblclick', e)
    })

    map.addEventListener('mousemove', (e: any) => {
      emit('mousemove', e)
    })

    map.addEventListener('zoomend', (e: any) => {
      emit('zoomend', e)
    })

    map.addEventListener('moveend', (e: any) => {
      emit('moveend', e)
    })

    // 添加单个控件的方法（安全包装）
    const addControlSafely = (controlFactory: () => any, controlName: string) => {
      return new Promise<void>((resolve) => {
        setTimeout(() => {
          try {
            const control = controlFactory()
            if (control && map) {
              map.addControl(control)
            }
            resolve()
          } catch (error) {
            // 静默失败，不输出错误
            resolve()
          }
        }, 300) // 每个控件之间延迟300ms
      })
    }

    // 添加地图控件的方法（逐个添加，确保DOM完全准备好）
    const addMapControls = async () => {
      if (controlsAdded.value || !mapContainer.value) {
        return
      }

      // 使用requestAnimationFrame确保浏览器完成所有渲染
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          // 再次检查DOM是否准备好
          if (!mapContainer.value || controlsAdded.value) {
            return
          }

          // 逐个添加控件，每个控件之间都有延迟
          setTimeout(async () => {
            try {
              // 缩放控件
              await addControlSafely(
                () =>
                  new BMap.NavigationControl({
                    anchor: BMap.BMAP_ANCHOR_TOP_RIGHT,
                    type: BMap.BMAP_NAVIGATION_CONTROL_LARGE,
                  }),
                'NavigationControl'
              )

              // 比例尺控件
              await addControlSafely(
                () =>
                  new BMap.ScaleControl({
                    anchor: BMap.BMAP_ANCHOR_BOTTOM_LEFT,
                  }),
                'ScaleControl'
              )

              // 地图类型控件
              await addControlSafely(
                () =>
                  new BMap.MapTypeControl({
                    anchor: BMap.BMAP_ANCHOR_TOP_RIGHT,
                    mapTypes: [
                      BMap.BMAP_NORMAL_MAP,
                      BMap.BMAP_SATELLITE_MAP,
                      BMap.BMAP_HYBRID_MAP,
                    ],
                  }),
                'MapTypeControl'
              )

              controlsAdded.value = true
            } catch (error) {
              // 静默处理错误
            }
          }, 500) // 初始延迟500ms
        })
      })
    }

    // 等待地图完全加载后再添加控件
    // 使用多个事件确保地图完全准备好
    let controlsTimer: ReturnType<typeof setTimeout> | null = null

    const addControlsOnce = () => {
      if (controlsAdded.value || controlsTimer) {
        return
      }

      // 清除之前可能存在的定时器
      if (controlsTimer) {
        clearTimeout(controlsTimer)
      }

      // 延迟较长时间，确保所有DOM元素都准备好
      // 使用requestAnimationFrame + setTimeout组合，延迟3秒确保地图完全稳定
      controlsTimer = setTimeout(() => {
        requestAnimationFrame(() => {
          requestAnimationFrame(() => {
            requestAnimationFrame(() => {
              addMapControls()
              controlsTimer = null
            })
          })
        })
      }, 3000)
    }

    // 监听多个事件，确保地图完全加载
    map.addEventListener('tilesloaded', () => {
      // 延迟执行，确保瓦片完全加载
      addControlsOnce()
    })

    // 使用load事件作为备用
    map.addEventListener('load', () => {
      addControlsOnce()
    })

    // 设置一个较长的延迟备用，确保万无一失（5秒后）
    setTimeout(addControlsOnce, 5000)

    // 标记地图已准备就绪
    isMapReady.value = true

    // 延迟触发ready事件，确保地图完全渲染
    setTimeout(() => {
      emit('ready', map)
    }, 200)
  } catch (error) {
    console.error('初始化百度地图失败:', error)
    // 如果是容器相关错误，尝试重新初始化
    if (error instanceof Error && error.message.includes('undefined')) {
      setTimeout(() => {
        console.log('尝试重新初始化地图...')
        initMap()
      }, 500)
    }
  }
}

/**
 * 更新地图中心点
 */
const updateCenter = (center: Point) => {
  if (!mapInstance.value || !isBaiduMapLoaded()) return

  const point = new window.BMap.Point(center.lng, center.lat)
  mapInstance.value.panTo(point)
}

/**
 * 更新缩放级别
 */
const updateZoom = (zoom: number) => {
  if (!mapInstance.value) return
  mapInstance.value.setZoom(zoom)
}

// 监听中心点变化
watch(
  () => props.center,
  (newCenter) => {
    if (isMapReady.value && newCenter) {
      updateCenter(newCenter)
    }
  },
  { deep: true }
)

// 监听缩放级别变化
watch(
  () => props.zoom,
  (newZoom) => {
    if (isMapReady.value && newZoom) {
      updateZoom(newZoom)
    }
  }
)

// 监听地图样式变化
watch(
  () => props.mapStyle,
  (newStyle) => {
    if (isMapReady.value && mapInstance.value && newStyle) {
      const BMap = window.BMap
      const mapTypes: Record<string, any> = {
        normal: BMap.BMAP_NORMAL_MAP,
        satellite: BMap.BMAP_SATELLITE_MAP,
        hybrid: BMap.BMAP_HYBRID_MAP,
      }
      if (mapTypes[newStyle]) {
        mapInstance.value.setMapType(mapTypes[newStyle])
      }
    }
  }
)

// 暴露地图实例和方法
defineExpose({
  getMap: () => mapInstance.value,
  getCenter: () => {
    if (!mapInstance.value) return null
    const center = mapInstance.value.getCenter()
    return { lng: center.lng, lat: center.lat }
  },
  getZoom: () => {
    if (!mapInstance.value) return null
    return mapInstance.value.getZoom()
  },
  setCenter: updateCenter,
  setZoom: updateZoom,
  panTo: (point: Point) => {
    if (!mapInstance.value) return
    const bdPoint = new window.BMap.Point(point.lng, point.lat)
    mapInstance.value.panTo(bdPoint)
  },
  fitBounds: (points: Point[]) => {
    if (!mapInstance.value || !points.length) return
    const bdPoints = points.map(
      (p) => new window.BMap.Point(p.lng, p.lat)
    )
    const viewport = mapInstance.value.getViewport(bdPoints)
    mapInstance.value.centerAndZoom(viewport.center, viewport.zoom)
  },
})

onMounted(() => {
  // 使用双重nextTick确保DOM完全渲染
  nextTick(() => {
    nextTick(() => {
      // 额外延迟，确保容器完全准备好
      setTimeout(() => {
        initMap()
      }, 100)
    })
  })
})

onUnmounted(() => {
  if (mapInstance.value) {
    try {
      // 清理地图实例
      mapInstance.value = null
      isMapReady.value = false
      controlsAdded.value = false
    } catch (error) {
      console.warn('清理地图实例时出错:', error)
    }
  }
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;

.baidu-map-container {
  width: 100%;
  height: 100%;
  overflow: hidden;
  background: $bg-secondary;
}
</style>

