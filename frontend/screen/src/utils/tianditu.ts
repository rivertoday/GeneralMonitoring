/**
 * 天地图工具函数和配置
 * 参考官方文档：http://lbs.tianditu.gov.cn/docs/#/sanwei/
 * 
 * 注意：
 * 1. Cesium必须挂载在window对象上
 * 2. 需要加载天地图扩展插件（Cesium_ext_min.js等）
 * 3. 三维地名服务使用GeoWTFS类，不是UrlTemplateImageryProvider
 */
import * as Cesium from 'cesium'

/**
 * 天地图 app_key（tk）
 * 从环境变量获取，如果没有则使用默认值（需要替换为实际的 app_key）
 */
export const TIANDITU_APP_KEY = import.meta.env.VITE_TIANDITU_APP_KEY || 'your-tianditu-app-key'

/**
 * 天地图服务域名模板
 */
export const TIANDITU_URL_TEMPLATE = 'https://t{s}.tianditu.gov.cn/'

/**
 * 天地图服务负载子域
 */
export const TIANDITU_SUBDOMAINS = ['0', '1', '2', '3', '4', '5', '6', '7']

/**
 * 确保Cesium挂载在window对象上（天地图扩展插件需要）
 */
export function ensureCesiumOnWindow() {
  if (typeof window !== 'undefined' && !(window as any).Cesium) {
    ;(window as any).Cesium = Cesium
    console.log('Cesium已挂载到window对象上')
  }
}

/**
 * 加载天地图扩展插件
 * 参考官方文档：http://lbs.tianditu.gov.cn/docs/#/sanwei/
 * 
 * 注意：扩展插件可能会产生 "Cannot redefine property: primitiveAdded" 错误，
 * 这是一个可以安全忽略的警告，不影响功能使用。
 */
export function loadTiandituPlugins(): Promise<void> {
  return new Promise((resolve, reject) => {
    // 检查是否已经加载
    if (
      typeof (window as any).Cesium !== 'undefined' &&
      (window as any).Cesium.GeoWTFS
    ) {
      console.log('天地图扩展插件已加载')
      resolve()
      return
    }

    // 确保Cesium已挂载到window
    if (typeof (window as any).Cesium === 'undefined') {
      console.error('❌ Cesium未加载到window对象，无法加载扩展插件')
      reject(new Error('Cesium未加载到window对象'))
      return
    }

    console.log('✓ Cesium已在window对象上，开始加载扩展插件...')

    // 设置错误处理器，忽略扩展插件可能产生的重定义属性警告
    const originalErrorHandler = window.onerror
    
    window.onerror = (message, source, lineno, colno, error) => {
      // 忽略 "Cannot redefine property: primitiveAdded" 错误
      if (
        typeof message === 'string' &&
        message.includes('Cannot redefine property') &&
        message.includes('primitiveAdded')
      ) {
        console.warn('⚠️ 扩展插件重定义属性警告（可忽略）:', message)
        return true // 阻止默认错误处理
      }
      
      // 其他错误正常处理
      if (originalErrorHandler) {
        return originalErrorHandler(message, source, lineno, colno, error)
      }
      return false
    }

    // 扩展插件CDN地址 - 注意加载顺序很重要
    // 官方文档中的顺序：先加载依赖库，最后加载核心扩展
    const plugins = [
      'https://api.tianditu.gov.cn/cdn/plugins/cesium/long.min.js',
      'https://api.tianditu.gov.cn/cdn/plugins/cesium/bytebuffer.min.js',
      'https://api.tianditu.gov.cn/cdn/plugins/cesium/protobuf.min.js',
      'https://api.tianditu.gov.cn/cdn/plugins/cesium/Cesium_ext_min.js', // 核心扩展放在最后
    ]

    let loadedCount = 0
    const totalCount = plugins.length

    // 顺序加载脚本（一个接一个，确保依赖关系）
    const loadScriptSequentially = async (index: number): Promise<void> => {
      if (index >= totalCount) {
        // 恢复原始错误处理器
        window.onerror = originalErrorHandler
        
        // 所有脚本加载完成，等待扩展插件初始化
        await new Promise(resolve => setTimeout(resolve, 500))
        
        // 验证GeoWTFS是否可用
        let retryCount = 0
        const maxRetries = 10
        
        const checkGeoWTFS = (): void => {
          if (
            typeof (window as any).Cesium !== 'undefined' &&
            (window as any).Cesium.GeoWTFS
          ) {
            console.log('✓ 所有天地图扩展插件加载完成，GeoWTFS可用')
            resolve()
          } else if (retryCount < maxRetries) {
            retryCount++
            console.log(`等待GeoWTFS初始化... (${retryCount}/${maxRetries})`)
            setTimeout(checkGeoWTFS, 500)
          } else {
            console.warn('⚠️ 扩展插件加载完成，但GeoWTFS仍不可用')
            console.warn('   这可能是因为：')
            console.warn('   1. 扩展插件与当前Cesium版本不兼容')
            console.warn('   2. 扩展插件加载顺序有问题')
            console.warn('   3. 网络问题导致扩展插件未完全加载')
            console.warn('   三维地名服务将不可用，但不影响其他功能')
            // 即使GeoWTFS不可用，也不阻止继续，只是三维地名服务不可用
            resolve()
          }
        }
        
        checkGeoWTFS()
        return
      }

      const url = plugins[index]
      if (!url) {
        return
      }
      const fileName = url.split('/').pop() || ''
      
      return new Promise<void>((scriptResolve, scriptReject) => {
        // 检查脚本是否已经加载
        const existingScript = document.querySelector(`script[src="${url}"]`)
        if (existingScript) {
          console.log(`天地图扩展插件 ${index + 1}/${totalCount} 已存在: ${fileName}`)
          loadedCount++
          scriptResolve()
          loadScriptSequentially(index + 1)
          return
        }

        const script = document.createElement('script')
        script.type = 'text/javascript'
        script.src = url || ''

        script.onload = () => {
          loadedCount++
          console.log(`天地图扩展插件 ${loadedCount}/${totalCount} 加载完成: ${fileName}`)
          
          // 等待当前脚本完全执行后再加载下一个
          setTimeout(() => {
            scriptResolve()
            loadScriptSequentially(index + 1)
          }, 100)
        }

        script.onerror = () => {
          // 恢复原始错误处理器
          window.onerror = originalErrorHandler
          console.error(`天地图扩展插件加载失败: ${url}`)
          scriptReject(new Error(`无法加载扩展插件: ${url}`))
        }

        document.head.appendChild(script)
      })
    }

    // 开始顺序加载
    loadScriptSequentially(0).then(() => {
      // 加载完成后恢复错误处理器
      window.onerror = originalErrorHandler
    }).catch((error) => {
      // 加载失败后恢复错误处理器
      window.onerror = originalErrorHandler
      reject(error)
    })
  })
}

/**
 * 检查天地图扩展插件是否已加载
 */
export function isTiandituPluginsLoaded(): boolean {
  return (
    typeof (window as any).Cesium !== 'undefined' &&
    typeof (window as any).Cesium.GeoWTFS !== 'undefined'
  )
}

/**
 * 创建天地图影像底图图层
 * 参考官方文档：使用UrlTemplateImageryProvider加载影像服务
 * URL格式：DataServer?T=img_w&x={x}&y={y}&l={z}&tk=token
 */
export function createTiandituImageLayer() {
  ensureCesiumOnWindow()
  
  if (!TIANDITU_APP_KEY || TIANDITU_APP_KEY === 'your-tianditu-app-key') {
    console.warn('⚠️ 天地图密钥未配置！请在 .env 文件中设置 VITE_TIANDITU_APP_KEY')
  }
  
  const url = TIANDITU_URL_TEMPLATE + 'DataServer?T=img_w&x={x}&y={y}&l={z}&tk=' + TIANDITU_APP_KEY
  
  console.log('天地图影像图层配置:')
  console.log('  URL模板:', url)
  console.log('  App Key (tk):', TIANDITU_APP_KEY || '(未配置)')
  
  return new Cesium.UrlTemplateImageryProvider({
    url: url,
    subdomains: TIANDITU_SUBDOMAINS,
    tilingScheme: new Cesium.WebMercatorTilingScheme(),
    maximumLevel: 18,
    credit: new Cesium.Credit('天地图'),
  })
}

/**
 * 创建天地图国界图层
 * URL格式：DataServer?T=ibo_w&x={x}&y={y}&l={z}&tk=token
 */
export function createTiandituBoundaryLayer() {
  ensureCesiumOnWindow()
  
  const url = TIANDITU_URL_TEMPLATE + 'DataServer?T=ibo_w&x={x}&y={y}&l={z}&tk=' + TIANDITU_APP_KEY
  
  return new Cesium.UrlTemplateImageryProvider({
    url: url,
    subdomains: TIANDITU_SUBDOMAINS,
    tilingScheme: new Cesium.WebMercatorTilingScheme(),
    maximumLevel: 10,
    credit: new Cesium.Credit('天地图'),
  })
}

/**
 * 创建天地图矢量底图图层（球面墨卡托投影）
 * URL格式：DataServer?T=vec_w&x={x}&y={y}&l={z}&tk=token
 * 投影方式：球面墨卡托投影（Web Mercator，EPSG:3857）
 * 服务类型：vec_w（_w表示球面墨卡托投影，Web Mercator）
 * 用于2D模式的标准地图显示
 */
export function createTiandituVectorLayer() {
  ensureCesiumOnWindow()
  
  if (!TIANDITU_APP_KEY || TIANDITU_APP_KEY === 'your-tianditu-app-key') {
    console.warn('⚠️ 天地图密钥未配置！请在 .env 文件中设置 VITE_TIANDITU_APP_KEY')
  }
  
  const url = TIANDITU_URL_TEMPLATE + 'DataServer?T=vec_w&x={x}&y={y}&l={z}&tk=' + TIANDITU_APP_KEY
  
  console.log('天地图矢量底图图层配置（球面墨卡托投影）:')
  console.log('  URL模板:', url)
  console.log('  投影方式: 球面墨卡托投影 (Web Mercator, EPSG:3857)')
  console.log('  服务类型: vec_w（球面墨卡托投影）')
  console.log('  App Key (tk):', TIANDITU_APP_KEY || '(未配置)')
  
  return new Cesium.UrlTemplateImageryProvider({
    url: url,
    subdomains: TIANDITU_SUBDOMAINS,
    tilingScheme: new Cesium.WebMercatorTilingScheme(), // 球面墨卡托投影（Web Mercator）
    maximumLevel: 18,
    credit: new Cesium.Credit('天地图'),
  })
}

/**
 * 创建天地图矢量注记图层（球面墨卡托投影）
 * URL格式：DataServer?T=cva_w&x={x}&y={y}&l={z}&tk=token
 * 投影方式：球面墨卡托投影（Web Mercator，EPSG:3857）
 * 服务类型：cva_w（_w表示球面墨卡托投影，Web Mercator）
 * 用于2D模式的地名标注显示
 */
export function createTiandituVectorAnnoLayer() {
  ensureCesiumOnWindow()
  
  const url = TIANDITU_URL_TEMPLATE + 'DataServer?T=cva_w&x={x}&y={y}&l={z}&tk=' + TIANDITU_APP_KEY
  
  console.log('天地图矢量注记图层配置（球面墨卡托投影）:')
  console.log('  URL模板:', url)
  console.log('  投影方式: 球面墨卡托投影 (Web Mercator, EPSG:3857)')
  console.log('  服务类型: cva_w（球面墨卡托投影）')
  
  return new Cesium.UrlTemplateImageryProvider({
    url: url,
    subdomains: TIANDITU_SUBDOMAINS,
    tilingScheme: new Cesium.WebMercatorTilingScheme(), // 球面墨卡托投影（Web Mercator）
    maximumLevel: 18,
    credit: new Cesium.Credit('天地图'),
  })
}

/**
 * 创建天地图地形服务提供者
 * 参考官方文档：使用GeoTerrainProvider加载地形服务
 * URL格式：mapservice/swdx?T=elv_c&tk=token
 */
export function createTiandituTerrainProvider() {
  ensureCesiumOnWindow()
  
  if (!TIANDITU_APP_KEY || TIANDITU_APP_KEY === 'your-tianditu-app-key') {
    console.warn('⚠️ 天地图密钥未配置！请在 .env 文件中设置 VITE_TIANDITU_APP_KEY')
  }
  
  const terrainUrls: string[] = []
  
  for (let i = 0; i < TIANDITU_SUBDOMAINS.length; i++) {
    const url = TIANDITU_URL_TEMPLATE.replace('{s}', TIANDITU_SUBDOMAINS[i] || '0') + 'mapservice/swdx?T=elv_c&tk=' + TIANDITU_APP_KEY
    terrainUrls.push(url)
  }
  
  console.log('天地图地形服务配置:')
  console.log('  URL数量:', terrainUrls.length)
  console.log('  示例URL:', terrainUrls[0])
  console.log('  App Key (tk):', TIANDITU_APP_KEY || '(未配置)')
  
  // 检查GeoWTFS是否可用（需要加载扩展插件）
  if (!(window as any).Cesium || !(window as any).Cesium.GeoTerrainProvider) {
    console.warn('⚠️ GeoTerrainProvider不可用，可能需要加载天地图扩展插件')
    console.warn('   请在index.html中加载天地图扩展插件脚本')
    // 返回椭球地形作为降级方案
    return new Cesium.EllipsoidTerrainProvider()
  }
  
  return new (window as any).Cesium.GeoTerrainProvider({
    urls: terrainUrls,
  })
}

/**
 * 创建天地图三维地名服务
 * 参考官方文档：使用GeoWTFS类加载三维地名服务
 * URL格式：mapservice/GetTiles?lxys={z},{x},{y}&VERSION=1.0.0&tk=token
 * 
 * 注意：这需要加载天地图扩展插件（Cesium_ext_min.js等）
 */
export function createTianditu3DNameService(viewer: any) {
  ensureCesiumOnWindow()
  
  if (!TIANDITU_APP_KEY || TIANDITU_APP_KEY === 'your-tianditu-app-key') {
    console.warn('⚠️ 天地图密钥未配置！请在 .env 文件中设置 VITE_TIANDITU_APP_KEY')
  }
  
  // 检查GeoWTFS是否可用（需要加载扩展插件）
  const CesiumWindow = (window as any).Cesium
  if (!CesiumWindow || !CesiumWindow.GeoWTFS) {
    console.error('❌ GeoWTFS不可用！请加载天地图扩展插件：')
    console.error('   1. Cesium_ext_min.js')
    console.error('   2. long.min.js')
    console.error('   3. bytebuffer.min.js')
    console.error('   4. protobuf.min.js')
    console.error('   参考：frontend/screen/TIANDITU_OFFICIAL.md')
    return null
  }
  
  const tdtUrl = TIANDITU_URL_TEMPLATE
  
  // 创建GeoWTFS实例
  const wtfs = new CesiumWindow.GeoWTFS({
    viewer,
    subdomains: TIANDITU_SUBDOMAINS,
    metadata: {
      boundBox: {
        minX: -180,
        minY: -90,
        maxX: 180,
        maxY: 90,
      },
      minLevel: 1,
      maxLevel: 20,
    },
    depthTestOptimization: true,
    dTOElevation: 15000,
    dTOPitch: CesiumWindow.Math.toRadians(-70),
    aotuCollide: true, // 是否开启避让
    collisionPadding: [5, 10, 8, 5], // 开启避让时，标注碰撞增加内边距，上、右、下、左
    serverFirstStyle: true, // 服务端样式优先
    labelGraphics: {
      font: '28px sans-serif',
      fontSize: 28,
      fillColor: CesiumWindow.Color.WHITE,
      scale: 0.5,
      outlineColor: CesiumWindow.Color.BLACK,
      outlineWidth: 2,
      style: CesiumWindow.LabelStyle.FILL_AND_OUTLINE,
      showBackground: false,
      backgroundColor: CesiumWindow.Color.RED,
      backgroundPadding: new CesiumWindow.Cartesian2(10, 10),
      horizontalOrigin: CesiumWindow.HorizontalOrigin.LEFT,
      verticalOrigin: CesiumWindow.VerticalOrigin.TOP,
      eyeOffset: CesiumWindow.Cartesian3.ZERO,
      pixelOffset: new CesiumWindow.Cartesian2(5, 5),
      disableDepthTestDistance: undefined,
    },
    billboardGraphics: {
      horizontalOrigin: CesiumWindow.HorizontalOrigin.CENTER,
      verticalOrigin: CesiumWindow.VerticalOrigin.CENTER,
      eyeOffset: CesiumWindow.Cartesian3.ZERO,
      pixelOffset: CesiumWindow.Cartesian2.ZERO,
      alignedAxis: CesiumWindow.Cartesian3.ZERO,
      color: CesiumWindow.Color.WHITE,
      rotation: 0,
      scale: 1,
      width: 18,
      height: 18,
      disableDepthTestDistance: undefined,
    },
  })
  
  // 设置三维地名服务URL
  wtfs.getTileUrl = function() {
    return tdtUrl + 'mapservice/GetTiles?lxys={z},{x},{y}&VERSION=1.0.0&tk=' + TIANDITU_APP_KEY
  }
  
  // 设置三维图标服务URL
  wtfs.getIcoUrl = function() {
    return tdtUrl + 'mapservice/GetIcon?id={id}&tk=' + TIANDITU_APP_KEY
  }
  
  // 初始化（使用官方文档中的边界框数据）
  const initData = [
    { x: 6, y: 1, level: 2, boundBox: { minX: 90, minY: 0, maxX: 135, maxY: 45 } },
    { x: 7, y: 1, level: 2, boundBox: { minX: 135, minY: 0, maxX: 180, maxY: 45 } },
    { x: 6, y: 0, level: 2, boundBox: { minX: 90, minY: 45, maxX: 135, maxY: 90 } },
    { x: 7, y: 0, level: 2, boundBox: { minX: 135, minY: 45, maxX: 180, maxY: 90 } },
    { x: 5, y: 1, level: 2, boundBox: { minX: 45, minY: 0, maxX: 90, maxY: 45 } },
    { x: 4, y: 1, level: 2, boundBox: { minX: 0, minY: 0, maxX: 45, maxY: 45 } },
    { x: 5, y: 0, level: 2, boundBox: { minX: 45, minY: 45, maxX: 90, maxY: 90 } },
    { x: 4, y: 0, level: 2, boundBox: { minX: 0, minY: 45, maxX: 45, maxY: 90 } },
    { x: 6, y: 2, level: 2, boundBox: { minX: 90, minY: -45, maxX: 135, maxY: 0 } },
    { x: 6, y: 3, level: 2, boundBox: { minX: 90, minY: -90, maxX: 135, maxY: -45 } },
    { x: 7, y: 2, level: 2, boundBox: { minX: 135, minY: -45, maxX: 180, maxY: 0 } },
    { x: 5, y: 2, level: 2, boundBox: { minX: 45, minY: -45, maxX: 90, maxY: 0 } },
    { x: 4, y: 2, level: 2, boundBox: { minX: 0, minY: -45, maxX: 45, maxY: 0 } },
    { x: 3, y: 1, level: 2, boundBox: { minX: -45, minY: 0, maxX: 0, maxY: 45 } },
    { x: 3, y: 0, level: 2, boundBox: { minX: -45, minY: 45, maxX: 0, maxY: 90 } },
    { x: 2, y: 0, level: 2, boundBox: { minX: -90, minY: 45, maxX: -45, maxY: 90 } },
    { x: 0, y: 1, level: 2, boundBox: { minX: -180, minY: 0, maxX: -135, maxY: 45 } },
    { x: 1, y: 0, level: 2, boundBox: { minX: -135, minY: 45, maxX: -90, maxY: 90 } },
    { x: 0, y: 0, level: 2, boundBox: { minX: -180, minY: 45, maxX: -135, maxY: 90 } },
  ]
  
  wtfs.initTDT(initData)
  
  console.log('天地图三维地名服务配置完成')
  
  return wtfs
}

/**
 * 创建天地图矢量图层（标准地图 - 矢量底图 + 矢量注记）
 * 投影方式：球面墨卡托投影（Web Mercator，EPSG:3857）
 * 用于2D模式的标准地图显示
 * 
 * 返回图层数组：
 * - 矢量底图（vec_w）：球面墨卡托投影
 * - 矢量注记（cva_w）：球面墨卡托投影
 */
export function createTiandituVectorLayers() {
  return [
    createTiandituVectorLayer(), // 矢量底图（球面墨卡托投影）
    createTiandituVectorAnnoLayer(), // 矢量注记（球面墨卡托投影）
  ]
}

/**
 * 创建天地图底图图层（标准地图 - 矢量地图 + 注记）
 * 注意：标准地图需要加载矢量底图和注记层
 * @deprecated 建议使用 createTiandituVectorLayers()
 */
export function createTiandituBaseLayer() {
  return createTiandituVectorLayers()
}

/**
 * 创建天地图影像图层（影像地图 + 国界）
 */
export function createTiandituImageLayers() {
  return [
    createTiandituImageLayer(), // 影像底图
    createTiandituBoundaryLayer(), // 国界图层
  ]
}

/**
 * 创建天地图地形图层配置
 * 返回地形提供者（需要设置到viewer.terrainProvider）
 */
export function createTiandituTerrainLayer() {
  return createTiandituTerrainProvider()
}
