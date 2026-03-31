/**
 * Cesium Entity 管理工具
 * 用于在Cesium地图上添加、更新、删除标记点和多边形
 */
import * as Cesium from 'cesium'
import type { Point, MapMarker, MapPolygon } from '@/types/map'

/**
 * 将颜色字符串转换为Cesium颜色对象
 */
function parseColor(colorStr: string, alpha: number = 1.0): Cesium.Color {
  if (typeof colorStr !== 'string') {
    return Cesium.Color.WHITE.withAlpha(alpha)
  }
  
  if (colorStr.startsWith('rgba')) {
    const rgba = colorStr.match(/\d+/g)
    if (rgba && rgba.length >= 3 && rgba[0] && rgba[1] && rgba[2]) {
      return Cesium.Color.fromBytes(
        parseInt(rgba[0]),
        parseInt(rgba[1]),
        parseInt(rgba[2]),
        alpha * 255
      )
    }
  } else if (colorStr.startsWith('#')) {
    const hex = colorStr.replace('#', '')
    const r = parseInt(hex.substring(0, 2), 16)
    const g = parseInt(hex.substring(2, 4), 16)
    const b = parseInt(hex.substring(4, 6), 16)
    return Cesium.Color.fromBytes(r, g, b, alpha * 255)
  }
  return Cesium.Color.WHITE.withAlpha(alpha)
}

/**
 * 创建带 emoji 的圆形标记点图标（SVG Base64）
 * 统一图标样式：圆形背景 + emoji图标 + 白色边框
 */
function createEmojiMarkerIcon(emoji: string, color: string = '#409eff', size: number = 32): string {
  const svg = `
    <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
      <!-- 外圈阴影（可选，增强视觉效果） -->
      <circle cx="${size / 2}" cy="${size / 2}" r="${size / 2}" fill="rgba(0, 0, 0, 0.2)"/>
      <!-- 主圆形背景 -->
      <circle cx="${size / 2}" cy="${size / 2}" r="${size / 2 - 2}" fill="${color}" stroke="#fff" stroke-width="2"/>
      <!-- Emoji图标 -->
      <text x="${size / 2}" y="${size / 2 + size / 6}" font-size="${size * 0.5}" text-anchor="middle" dominant-baseline="middle">${emoji}</text>
    </svg>
  `.trim()

  return `data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))}`
}

/**
 * 创建标记点 Entity
 */
export function createMarkerEntity(
  viewer: any,
  marker: MapMarker
): Cesium.Entity | null {
  if (!viewer) {
    console.error('createMarkerEntity: viewer不存在')
    return null
  }
  
  if (!marker.position) {
    console.error('createMarkerEntity: marker.position不存在', marker)
    return null
  }

  const Cesium = window.Cesium
  if (!Cesium) {
    console.error('createMarkerEntity: Cesium未加载')
    return null
  }

  const position = Cesium.Cartesian3.fromDegrees(
    marker.position.lng,
    marker.position.lat
  )

  // 确保id是唯一且可识别的
  // 如果marker.id是数字，转换为字符串以保持一致
  const entityId = marker.id !== undefined && marker.id !== null ? String(marker.id) : `marker_${Date.now()}_${Math.random()}`
  
  console.log('createMarkerEntity: 创建Entity', {
    markerId: marker.id,
    entityId,
    position: marker.position,
    icon: marker.icon,
  })
  
  // 确保 data 只包含可序列化的基本类型数据，避免 Worker 序列化错误
  const serializableData: any = {}
  if (marker.data) {
    Object.keys(marker.data).forEach((key) => {
      const value = (marker.data as any)[key]
      // 只保留可序列化的基本类型
      if (
        value === null ||
        value === undefined ||
        typeof value === 'string' ||
        typeof value === 'number' ||
        typeof value === 'boolean'
      ) {
        serializableData[key] = value
      }
    })
  }

  const entityOptions: any = {
    id: entityId, // 使用字符串ID确保一致性
    position: position,
    data: serializableData, // 使用清理后的可序列化数据
  }
  
  // 将原始marker数据附加到Entity，方便后续查找
  // 确保 properties 也只包含可序列化的数据
  entityOptions.properties = {
    markerId: typeof marker.id === 'string' || typeof marker.id === 'number' ? marker.id : String(marker.id),
    markerData: serializableData, // 使用已经清理过的可序列化数据
    markerLabel: typeof marker.label === 'string' ? marker.label : (marker.label || ''),
  }

  // 确保所有标记点都使用图标（Billboard），不使用点标记
  // 统一图标大小：普通标记32px，特殊标记40px
  let iconImage: string
  let iconSize = 32 // 默认图标大小
  
  // 特殊类型使用更大的图标
  if (marker.data?.type === 'station') {
    iconSize = 40
  }
  
  if (marker.icon && typeof marker.icon === 'string') {
    // 检查是否是 emoji（简单判断：如果长度 <= 2 且不包含 http 和 data:）
    if (marker.icon.length <= 2 && !marker.icon.startsWith('http') && !marker.icon.startsWith('data:')) {
      // 创建带有 emoji 的圆形 SVG 图标
      const color = marker.data?.color || '#409eff'
      iconImage = createEmojiMarkerIcon(marker.icon, color, iconSize)
    } else {
      // 直接使用提供的图标URL（如果是URL或Base64）
      iconImage = marker.icon
      // 如果是URL，保持原始大小；如果是Base64 SVG，可能需要调整
    }
  } else {
    // 如果没有提供图标，使用默认图标
    const defaultIcon = '📍'
    const color = marker.data?.color || '#409eff'
    iconImage = createEmojiMarkerIcon(defaultIcon, color, iconSize)
  }
  
  // 使用Billboard显示图标，确保图标可点击
  // 设置较大的点击区域，确保点击图标就能触发
  entityOptions.billboard = {
    image: iconImage,
    width: iconSize,
    height: iconSize,
    verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
    scale: 1.0,
    heightReference: Cesium.HeightReference.CLAMP_TO_GROUND,
    disableDepthTestDistance: Number.POSITIVE_INFINITY, // 确保图标始终可点击，不受深度测试影响
    sizeInMeters: false, // 使用像素大小，确保图标大小一致
    // 增大点击区域（通过scale或width/height）
    // 注意：Cesium的点击检测基于Billboard的实际像素大小
  }

  console.log('createMarkerEntity: Billboard配置', {
    imageType: iconImage.substring(0, 50) + (iconImage.length > 50 ? '...' : ''),
    width: iconSize,
    height: iconSize,
  })

  // 添加标签 - 使用更清晰醒目的样式
  if (marker.label) {
    entityOptions.label = {
      text: marker.label,
      font: 'bold 16px "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif', // 增大字体，使用粗体，支持中文
      fillColor: Cesium.Color.YELLOW, // 使用黄色文字，更醒目
      outlineColor: Cesium.Color.BLACK, // 黑色轮廓
      outlineWidth: 3, // 增大轮廓宽度，提高对比度
      style: Cesium.LabelStyle.FILL_AND_OUTLINE, // 填充和轮廓样式
      verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
      pixelOffset: new Cesium.Cartesian2(0, -40),
      heightReference: Cesium.HeightReference.CLAMP_TO_GROUND,
      showBackground: true, // 启用背景以提高可读性
      backgroundColor: Cesium.Color.BLACK.withAlpha(0.7), // 半透明黑色背景
      backgroundPadding: new Cesium.Cartesian2(6, 3), // 背景内边距
      disableDepthTestDistance: Number.POSITIVE_INFINITY, // 确保标签始终可见
    }
    console.log('createMarkerEntity: 添加标签', marker.label)
  }

  const entity = viewer.entities.add(entityOptions)
  
  // 安全地获取 image 信息用于日志
  let imageInfo = 'N/A'
  try {
    const image = entity.billboard?.image
    if (image) {
      if (typeof image === 'string') {
        imageInfo = image.substring(0, 50) + (image.length > 50 ? '...' : '')
      } else if (image._value) {
        // Cesium 的 Resource 对象
        imageInfo = typeof image._value === 'string' ? image._value.substring(0, 50) : 'Resource对象'
      } else {
        imageInfo = typeof image === 'object' ? '对象' : String(image)
      }
    }
  } catch (e) {
    imageInfo = '无法获取'
  }
  
  console.log('createMarkerEntity: Entity已添加到viewer', {
    id: entity.id,
    hasBillboard: !!entity.billboard,
    billboardImage: imageInfo,
    position: entity.position ? '有位置' : '无位置',
  })
  
  return entity
}

/**
 * 创建多边形 Entity
 */
export function createPolygonEntity(
  viewer: any,
  polygon: MapPolygon
): Cesium.Entity | null {
  if (!viewer || !polygon.path || polygon.path.length < 3) {
    return null
  }

  const Cesium = window.Cesium
  if (!Cesium) {
    console.error('Cesium未加载')
    return null
  }

  // 转换路径点为Cesium坐标数组
  // 使用扁平的 number[] 数组，避免可能的序列化问题
  const positions: number[] = []
  polygon.path.forEach((point: Point) => {
    // 确保坐标值是有效的数字
    if (typeof point.lng === 'number' && typeof point.lat === 'number' && 
        !isNaN(point.lng) && !isNaN(point.lat) && 
        isFinite(point.lng) && isFinite(point.lat)) {
      positions.push(point.lng, point.lat)
    }
  })
  
  // 确保至少有3个点（多边形至少需要3个点）
  if (positions.length < 6) {
    console.warn(`多边形 ${polygon.id} 的点数不足（至少需要3个点）`)
    return null
  }

  // 填充颜色和透明度
  let fillColor = Cesium.Color.BLUE.withAlpha(0.3)
  if (polygon.fillColor) {
    fillColor = parseColor(polygon.fillColor, polygon.fillOpacity || 0.5)
  }

  // 边框颜色
  let outlineColor = Cesium.Color.BLUE
  if (polygon.strokeColor) {
    outlineColor = parseColor(polygon.strokeColor, polygon.strokeOpacity || 1.0)
  }

  // 确保id是唯一且可识别的
  const entityId = polygon.id !== undefined && polygon.id !== null ? String(polygon.id) : `polygon_${Date.now()}_${Math.random()}`
  
  // 计算多边形中心点（用于标签位置）
  const center = polygon.path && polygon.path.length > 0 
    ? getPolygonCenter(polygon.path) 
    : null
  
  // 设置Entity的position（标签需要Entity有position才能正确显示）
  const entityPosition = center 
    ? Cesium.Cartesian3.fromDegrees(center.lng, center.lat)
    : null

  // 确保 data 只包含可序列化的基本类型数据，避免 Worker 序列化错误
  // Cesium 会在 Worker 中处理 Entity，需要确保所有数据都可以被序列化
  const serializableData: any = {}
  if (polygon.data) {
    // 只保留可序列化的基本类型字段
    Object.keys(polygon.data).forEach((key) => {
      const value = (polygon.data as any)[key]
      // 处理日期对象：转换为字符串
      if (value instanceof Date) {
        serializableData[key] = value.toISOString()
      }
      // 处理数组：只保留基本类型数组
      else if (Array.isArray(value)) {
        // 检查数组中的元素是否都是基本类型
        const isSerializable = value.every(
          (item) =>
            item === null ||
            item === undefined ||
            typeof item === 'string' ||
            typeof item === 'number' ||
            typeof item === 'boolean'
        )
        if (isSerializable) {
          serializableData[key] = value
        }
        // 如果数组包含不可序列化的元素，跳过
      }
      // 只保留 string, number, boolean, null, undefined
      // 不保留对象、函数等可能包含不可序列化内容的数据
      else if (
        value === null ||
        value === undefined ||
        typeof value === 'string' ||
        typeof value === 'number' ||
        typeof value === 'boolean'
      ) {
        serializableData[key] = value
      }
      // 其他类型（对象、函数等）跳过，避免序列化错误
    })
  }

  // 创建 hierarchy - 直接传递 Cartesian3 数组给 polygon.hierarchy
  // Cesium 的 polygon.hierarchy 可以直接接受 Cartesian3[] 数组
  // 为了避免 Worker 序列化错误，确保所有 Cartesian3 对象都是新创建的
  let hierarchy
  try {
    // 创建一个新的扁平数组副本，确保没有其他引用
    const cleanPositions = positions.slice() // 创建副本，避免可能的引用问题
    
    // 创建 Cartesian3 数组 - 这些对象会被 Cesium 正确处理
    // 注意：虽然 Cartesian3 对象本身可能包含不可序列化的内容，但 Cesium 内部会处理
    hierarchy = Cesium.Cartesian3.fromDegreesArray(cleanPositions)
    
    // 验证 hierarchy 是否创建成功
    if (!hierarchy || !Array.isArray(hierarchy) || hierarchy.length === 0) {
      console.warn(`多边形 ${polygon.id} 的 hierarchy 创建失败`)
      return null
    }
  } catch (error) {
    console.error(`创建多边形 ${polygon.id} 的 hierarchy 时出错:`, error, {
      positionsLength: positions.length,
      polygonId: polygon.id,
    })
    return null
  }

  const entityOptions: any = {
    id: entityId, // 使用字符串ID确保一致性
    polygon: {
      hierarchy: hierarchy,
      material: fillColor,
      outline: true,
      outlineColor: outlineColor,
      outlineWidth: polygon.strokeWeight || 2,
      height: 0,
      extrudedHeight: 0, // 设置为0而不是undefined，确保多边形可以被点击
      heightReference: Cesium.HeightReference.CLAMP_TO_GROUND,
      // 确保多边形可以被点击检测
      perPositionHeight: false,
      // 设置多边形为可点击
      classificationType: Cesium.ClassificationType.BOTH,
    },
    // 同时设置 data 和 properties，确保兼容性
    // 注意：确保数据都是可序列化的基本类型
    data: serializableData,
    properties: serializableData, // 使用 properties 作为备用
  }
  
  // 如果有多边形中心点，设置Entity的position（标签需要这个）
  if (entityPosition) {
    entityOptions.position = entityPosition
  }

  // 如果有标签，添加标签到多边形中心
  if (polygon.data && center) {
    let labelText = ''
    
    // 优先使用 name，如果没有则使用 street（区域风险图使用街道名称）
    // 对于区域风险图，只显示街道名称，不显示风险等级
    if (polygon.data.name) {
      labelText = polygon.data.name
    } else if (polygon.data.street) {
      // 只显示街道名称，不包含风险等级信息
      labelText = polygon.data.street
    }
    
    if (labelText) {
      // 根据风险等级设置标签颜色
      let labelColor = Cesium.Color.YELLOW // 默认黄色
      let labelOutlineColor = Cesium.Color.BLACK // 默认黑色轮廓
      
      if (polygon.data.risk_color) {
        const riskColor = polygon.data.risk_color as string
        switch (riskColor) {
          case 'red':
            labelColor = Cesium.Color.RED
            labelOutlineColor = Cesium.Color.WHITE // 红色配白色轮廓，更清晰
            break
          case 'orange':
            labelColor = Cesium.Color.ORANGE
            labelOutlineColor = Cesium.Color.WHITE // 橙色配白色轮廓
            break
          case 'yellow':
            labelColor = Cesium.Color.YELLOW
            labelOutlineColor = Cesium.Color.BLACK // 黄色配黑色轮廓
            break
          case 'blue':
            labelColor = Cesium.Color.BLUE
            labelOutlineColor = Cesium.Color.WHITE // 蓝色配白色轮廓
            break
          default:
            labelColor = Cesium.Color.YELLOW
            labelOutlineColor = Cesium.Color.BLACK
        }
      }
      
      // 设置标签（使用Entity的position，不需要单独设置label.position）
      // 注意：避免使用可能导致序列化问题的对象，尽量使用简单值
      // 确保所有 Cartesian2 对象都是新创建的，避免共享引用导致序列化问题
      entityOptions.label = {
        text: labelText,
        font: 'bold 18px "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif', // 增大字体，使用粗体，支持中文
        fillColor: labelColor, // 使用风险等级对应的颜色
        outlineColor: labelOutlineColor, // 根据风险等级设置轮廓颜色
        outlineWidth: 3, // 增大轮廓宽度，提高对比度
        style: Cesium.LabelStyle.FILL_AND_OUTLINE,
        verticalOrigin: Cesium.VerticalOrigin.CENTER,
        horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
        heightReference: Cesium.HeightReference.CLAMP_TO_GROUND,
        showBackground: true,
        backgroundColor: Cesium.Color.BLACK.withAlpha(0.8), // 半透明黑色背景，提高可读性
        // 创建新的 Cartesian2 对象，避免共享引用导致序列化问题
        backgroundPadding: new Cesium.Cartesian2(10, 5),
        disableDepthTestDistance: Number.POSITIVE_INFINITY, // 确保标签始终可见
        scale: 1.0, // 确保标签正常显示
        pixelOffset: new Cesium.Cartesian2(0, 0), // 创建新的零向量，避免共享引用
      }
      
      console.log('createPolygonEntity: 添加标签', {
        text: labelText,
        center: { lng: center.lng, lat: center.lat },
        riskColor: polygon.data.risk_color,
        labelColor: labelColor,
        hasEntityPosition: !!entityOptions.position,
        hasLabel: !!entityOptions.label,
      })
    }
  }

  return viewer.entities.add(entityOptions)
}

/**
 * 计算多边形中心点
 */
function getPolygonCenter(path: Point[]): Point {
  if (path.length === 0) {
    return { lng: 0, lat: 0 }
  }

  let sumLng = 0
  let sumLat = 0

  path.forEach((point) => {
    sumLng += point.lng
    sumLat += point.lat
  })

  return {
    lng: sumLng / path.length,
    lat: sumLat / path.length,
  }
}

/**
 * 根据ID查找Entity
 */
export function findEntityById(viewer: any, id: string | number): Cesium.Entity | null {
  if (!viewer) return null
  return viewer.entities.getById(id) || null
}

/**
 * 删除Entity
 */
export function removeEntity(viewer: any, id: string | number): boolean {
  if (!viewer) return false
  const entity = viewer.entities.getById(id)
  if (entity) {
    viewer.entities.remove(entity)
    return true
  }
  return false
}

/**
 * 清除所有Entity
 */
export function clearAllEntities(viewer: any): void {
  if (!viewer) {
    return
  }
  
  // 检查viewer是否已经被销毁
  try {
    if (viewer.entities && typeof viewer.entities.removeAll === 'function') {
      viewer.entities.removeAll()
    }
  } catch (error) {
    // viewer可能已经被销毁，忽略错误
    console.warn('清除Entity时出错（viewer可能已销毁）:', error)
  }
}

/**
 * 批量添加标记点
 */
export function addMarkers(
  viewer: any,
  markers: MapMarker[]
): Cesium.Entity[] {
  const entities: Cesium.Entity[] = []
  console.log('addMarkers: 开始批量添加标记点', { markerCount: markers.length })
  
  markers.forEach((marker, index) => {
    console.log(`addMarkers: 处理标记点 ${index + 1}/${markers.length}`, {
      id: marker.id,
      label: marker.label,
      position: marker.position,
      icon: marker.icon,
    })
    
    const entity = createMarkerEntity(viewer, marker)
    if (entity) {
      console.log(`addMarkers: 成功创建Entity`, {
        id: entity.id,
        hasBillboard: !!entity.billboard,
        hasPosition: !!entity.position,
      })
      entities.push(entity)
    } else {
      console.warn(`addMarkers: 创建Entity失败`, marker)
    }
  })
  
  console.log(`addMarkers: 批量添加完成，成功创建 ${entities.length}/${markers.length} 个Entity`)
  return entities
}

/**
 * 批量添加多边形
 */
export function addPolygons(
  viewer: any,
  polygons: MapPolygon[]
): Cesium.Entity[] {
  const entities: Cesium.Entity[] = []
  polygons.forEach((polygon) => {
    const entity = createPolygonEntity(viewer, polygon)
    if (entity) {
      entities.push(entity)
    }
  })
  return entities
}

