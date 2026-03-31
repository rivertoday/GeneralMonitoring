# 风险监测预警系统 - 大屏展示系统

## 项目概述

大屏展示系统是基于 Vue 3 + TypeScript + Cesium + 天地图开发的三个一张图大屏可视化系统，提供安全运行、安全态势、监测预警的可视化展示。

## 技术栈

- **框架**: Vue 3.0 (Composition API)
- **语言**: TypeScript
- **3D地图引擎**: Cesium 1.108.0
- **地图服务**: 天地图（Tianditu）
- **可视化**: ECharts
- **大屏组件**: DataV
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **构建工具**: Vite
- **Node版本**: Node.js 22.12

## 项目结构

```
screen/
├── src/
│   ├── api/                 # API接口封装
│   ├── assets/              # 静态资源
│   ├── components/          # 公共组件
│   │   ├── charts/         # 图表组件
│   │   ├── map/            # 地图组件
│   │   └── widgets/        # 大屏组件
│   ├── views/              # 页面组件
│   │   ├── overview/       # 大屏总览
│   │   ├── safety-run/     # 安全运行一张图
│   │   ├── safety-status/  # 安全态势一张图
│   │   └── monitor-warn/   # 监测预警一张图
│   ├── router/             # 路由配置
│   ├── store/              # 状态管理
│   ├── utils/              # 工具函数
│   │   └── tianditu.ts    # 天地图工具（扩展插件加载）
│   ├── config/             # 配置文件
│   ├── types/              # TypeScript类型定义
│   └── styles/             # 样式文件
├── public/
├── package.json
└── vite.config.ts
```

## 安装和配置

### 1. 安装依赖

```bash
cd frontend/screen
npm install
```

### 2. 配置天地图 app_key

#### 2.1 获取天地图密钥

1. 访问 [天地图开放平台](http://lbs.tianditu.gov.cn/)
2. 注册/登录账号
3. 创建应用，获取 app_key（也称为 tk）
4. **重要**：将访问域名添加到白名单（开发环境：`localhost`、`127.0.0.1` 等）

#### 2.2 配置环境变量

在项目根目录（`frontend/screen/`）创建 `.env` 或 `.env.local` 文件：

```env
VITE_TIANDITU_APP_KEY=您的天地图密钥
```

**注意**：
- 环境变量名必须以 `VITE_` 开头
- `.env.local` 文件不会提交到版本控制，更安全
- 配置后需要重启开发服务器

#### 2.3 验证配置

启动开发服务器后，打开浏览器控制台，应该能看到：

```
开始加载天地图扩展插件...
天地图扩展插件 1/4 加载完成: Cesium_ext_min.js
天地图扩展插件 2/4 加载完成: long.min.js
天地图扩展插件 3/4 加载完成: bytebuffer.min.js
天地图扩展插件 4/4 加载完成: protobuf.min.js
✓ 所有天地图扩展插件加载完成，GeoWTFS可用
```

### 3. 启动开发服务器

```bash
npm run dev
```

## Cesium + 天地图集成

### 技术架构

```
Cesium Viewer (3D/2D GIS引擎)
  └── 天地图底图图层
      ├── 影像底图 (img_w)
      ├── 国界图层 (ibo_w)
      ├── 三维地形服务 (swdx)
      └── 三维地名服务 (GetTiles)
  └── 业务图层 (Entity/Primitive API)
      ├── 标记点 (Billboard/Point/Label)
      ├── 多边形 (Polygon)
      └── 其他业务要素
```

### 核心组件

#### CesiumMap.vue

Cesium 地图组件，提供基础的地图展示功能。

**Props**:
- `center`: 地图中心点（经纬度）`{ lng: number, lat: number }`
- `zoom`: 缩放级别 `number`
- `mapStyle`: 地图样式 `'normal' | 'satellite' | 'terrain'`
- `sceneMode`: 场景模式 `'2D' | '3D' | 'COLUMBUS_VIEW'`

**Events**:
- `ready`: 地图初始化完成
- `click`: 地图点击事件
- `dblclick`: 地图双击事件

**使用示例**:

```vue
<template>
  <CesiumMap
    ref="cesiumMapRef"
    :center="{ lng: 118.521577, lat: 31.742368 }"
    :zoom="12"
    map-style="normal"
    @ready="onMapReady"
  />
</template>

<script setup lang="ts">
import CesiumMap from '@/components/map/CesiumMap.vue'

const onMapReady = (viewer: any) => {
  console.log('Cesium 地图初始化完成', viewer)
}
</script>
```

## JavaScript 文件加载说明

### 加载流程

```
1. 应用启动
   └─> main.ts 执行
       └─> Vue 应用初始化

2. CesiumMap 组件挂载
   └─> onMounted() 触发
       └─> initCesiumMap() 执行
           │
           ├─> ensureCesiumOnWindow()
           │   └─> 将 Cesium 挂载到 window.Cesium
           │
           ├─> new Cesium.Viewer()
           │   └─> 创建 Cesium Viewer（使用 npm 包的 Cesium）
           │
           ├─> loadTiandituPlugins()
           │   ├─> 动态加载 long.min.js
           │   ├─> 动态加载 bytebuffer.min.js
           │   ├─> 动态加载 protobuf.min.js
           │   └─> 动态加载 Cesium_ext_min.js
           │
           └─> updateMapStyle()
               └─> 添加天地图图层和三维地名服务
```

### 文件加载位置

| JavaScript 文件 | 加载位置 | 加载方式 |
|----------------|---------|---------|
| **Cesium.js** | `CesiumMap.vue` 第 7 行 | npm 包导入 (`cesium@1.108.0`) |
| **Cesium_ext_min.js** | `utils/tianditu.ts` | 动态加载（CDN） |
| **long.min.js** | `utils/tianditu.ts` | 动态加载（CDN） |
| **bytebuffer.min.js** | `utils/tianditu.ts` | 动态加载（CDN） |
| **protobuf.min.js** | `utils/tianditu.ts` | 动态加载（CDN） |

**为什么使用 npm 包而不是 CDN？**
- ✅ 更好的 TypeScript 类型支持
- ✅ 可以配合 Vite 进行打包优化
- ✅ 版本管理更清晰
- ✅ 离线开发更方便

**为什么扩展插件动态加载？**
- ✅ 只在需要时加载，减少初始页面加载时间
- ✅ 可以控制加载顺序和时机
- ✅ 可以在 Viewer 创建后加载，避免初始化冲突
- ✅ 更好的错误处理

### 关键代码位置

**Cesium 导入和挂载** (`CesiumMap.vue`):
```typescript
import * as Cesium from 'cesium'
ensureCesiumOnWindow() // 将 Cesium 挂载到 window.Cesium
```

**扩展插件加载** (`utils/tianditu.ts`):
```typescript
export function loadTiandituPlugins(): Promise<void> {
  // 按顺序动态加载扩展插件
  const plugins = [
    'https://api.tianditu.gov.cn/cdn/plugins/cesium/long.min.js',
    'https://api.tianditu.gov.cn/cdn/plugins/cesium/bytebuffer.min.js',
    'https://api.tianditu.gov.cn/cdn/plugins/cesium/protobuf.min.js',
    'https://api.tianditu.gov.cn/cdn/plugins/cesium/Cesium_ext_min.js',
  ]
  // ...加载逻辑
}
```

## 图层说明

### 影像底图图层

- **服务类型**: `UrlTemplateImageryProvider`
- **URL格式**: `DataServer?T=img_w&x={x}&y={y}&l={z}&tk=token`
- **用途**: 显示卫星影像地图

### 国界图层

- **服务类型**: `UrlTemplateImageryProvider`
- **URL格式**: `DataServer?T=ibo_w&x={x}&y={y}&l={z}&tk=token`
- **用途**: 显示国界标注

### 三维地形服务

- **服务类型**: `GeoTerrainProvider`（需要扩展插件）
- **URL格式**: `mapservice/swdx?T=elv_c&tk=token`
- **用途**: 显示三维地形数据
- **加载方式**: 设置为 `viewer.terrainProvider`

### 三维地名服务

- **服务类型**: `GeoWTFS`（需要扩展插件）
- **URL格式**: `mapservice/GetTiles?lxys={z},{x},{y}&VERSION=1.0.0&tk=token`
- **用途**: 显示三维地名标注
- **加载方式**: 通过 `createTianditu3DNameService(viewer)` 创建

## 常见问题

### 1. 403 Forbidden 错误

**原因**：API Key 未绑定域名或无效

**解决方案**：
1. 登录 [天地图开放平台](http://lbs.tianditu.gov.cn/)
2. 进入"控制台" -> "应用管理"
3. 找到您的应用，点击"编辑"
4. 在"白名单"中添加您的访问域名（开发环境：`localhost`、`127.0.0.1` 等）
5. 保存配置

### 2. GeoWTFS 不可用

**原因**：扩展插件未加载或加载失败

**解决方案**：
- 查看浏览器控制台是否有扩展插件加载错误
- 确认网络可以访问天地图CDN
- 检查 Cesium 是否已挂载到 `window.Cesium`

### 3. 地图显示空白

**解决方案**：
- 检查网络连接
- 检查浏览器控制台是否有错误信息
- 确认 Cesium 是否正确加载
- 确认天地图服务是否可访问
- 检查 app_key 是否正确配置

### 4. 环境变量不生效

**解决方案**：
- 确认环境变量名称以 `VITE_` 开头
- 重启开发服务器
- 清除浏览器缓存

### 调试方法

1. **查看浏览器控制台**
   - 查看是否有具体的错误信息
   - 检查URL是否正确生成

2. **检查扩展插件状态**
   ```javascript
   // 在浏览器控制台执行
   console.log('Cesium:', window.Cesium)
   console.log('GeoWTFS:', window.Cesium?.GeoWTFS)
   console.log('GeoTerrainProvider:', window.Cesium?.GeoTerrainProvider)
   ```

3. **检查网络请求**
   - 打开浏览器开发者工具的Network标签
   - 查看天地图服务的请求是否成功
   - 检查响应状态码和内容

## 坐标系说明

- **天地图**: 使用 GCJ-02（火星坐标系）或 WGS84
- **Cesium**: 默认使用 WGS84（EPSG:4326）
- **数据存储**: MySQL 使用 WGS84 存储空间数据

如果天地图使用 GCJ-02，需要进行坐标转换。建议后端统一转换为 WGS84 后返回前端。

## 性能优化建议

1. **大量要素渲染**: 使用 Entity 聚合功能，减少渲染要素数量
2. **LOD控制**: 根据缩放级别显示不同详细程度
3. **视锥剔除**: 只渲染视野内的要素
4. **数据分页**: 避免一次性加载大量数据
5. **场景优化**: 合理设置相机参数，避免不必要的渲染

## 注意事项

1. **Cesium 版本**: 当前使用 `cesium@1.108.0`，天地图扩展插件支持此版本
2. **Cesium 加载**: 确保 Cesium 在组件挂载前已加载
3. **天地图 app_key**: 必须配置有效的天地图 app_key 并绑定域名
4. **浏览器兼容性**: Cesium 需要 WebGL 支持，建议使用现代浏览器
5. **包体积**: Cesium 包体积较大，注意按需加载

## 参考文档

- [Cesium 官方文档](https://cesium.com/learn/cesiumjs/)
- [天地图开放平台](http://lbs.tianditu.gov.cn/)
- [天地图三维服务文档](http://lbs.tianditu.gov.cn/docs/#/sanwei/)
- 项目中的 `TIANDITU_OFFICIAL.md` 文件（包含官方示例代码）

## 开发规范

### 代码规范

- 使用 TypeScript 进行开发
- 使用 Composition API
- 组件命名使用 PascalCase
- 文件命名：组件使用 PascalCase，工具文件使用 camelCase

### 构建和部署

```bash
# 开发
npm run dev

# 构建
npm run build

# 预览构建结果
npm run preview
```
