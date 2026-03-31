# 在2D Cesium上叠加天地图矢量地图和矢量注记的可行性分析

## 一、背景

当前项目在2D模式下使用天地图影像图层（`img_w` + `ibo_w`）作为底图。用户希望在2D模式下使用天地图矢量地图（`vec_w`）和矢量注记（`cva_w`）作为底图，以获得更好的视觉效果和性能。

## 二、技术可行性分析

### 2.1 Cesium 2D模式支持

✅ **可行性：完全支持**

- Cesium支持多种视图模式：2D、3D、哥伦布视图（2.5D）
- 在2D模式下，Cesium仍然可以加载和显示各种影像图层
- 2D模式实际上是将3D场景投影到平面，支持所有3D模式下的图层功能

### 2.2 天地图矢量图层服务

根据 `TIANDITU_OFFICIAL.md`，天地图提供以下矢量图层：

| 图层类型 | WMTS服务地址 | DataServer服务 | 投影方式 |
|---------|-------------|---------------|---------|
| 矢量底图 | `vec_w/wmts` | `DataServer?T=vec_w` | 球面墨卡托 |
| 矢量注记 | `cva_w/wmts` | `DataServer?T=cva_w` | 球面墨卡托 |

**当前实现**：
- ✅ 已使用 `UrlTemplateImageryProvider` 加载影像图层（`img_w`、`ibo_w`）
- ✅ 支持 `DataServer` 服务方式

**结论**：可以沿用相同的技术方案加载矢量图层

### 2.3 技术实现方案

#### 方案一：使用 UrlTemplateImageryProvider（推荐）

与当前影像图层实现方式一致，使用 `DataServer` 服务：

```typescript
// 矢量底图
const vecLayer = new Cesium.UrlTemplateImageryProvider({
  url: 'https://t{s}.tianditu.gov.cn/DataServer?T=vec_w&x={x}&y={y}&l={z}&tk=' + APP_KEY,
  subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'],
  tilingScheme: new Cesium.WebMercatorTilingScheme(),
  maximumLevel: 18,
})

// 矢量注记
const cvaLayer = new Cesium.UrlTemplateImageryProvider({
  url: 'https://t{s}.tianditu.gov.cn/DataServer?T=cva_w&x={x}&y={y}&l={z}&tk=' + APP_KEY,
  subdomains: ['0', '1', '2', '3', '4', '5', '6', '7'],
  tilingScheme: new Cesium.WebMercatorTilingScheme(),
  maximumLevel: 18,
})
```

**优点**：
- ✅ 与现有代码实现方式一致，易于维护
- ✅ 不需要修改现有架构
- ✅ 简单直接，易于理解

**缺点**：
- ⚠️ 需要验证 `DataServer?T=vec_w` 和 `T=cva_w` 的实际可用性

#### 方案二：使用 WebMapTileServiceImageryProvider

使用标准的 WMTS 服务协议：

```typescript
// 矢量底图
const vecLayer = new Cesium.WebMapTileServiceImageryProvider({
  url: 'http://t0.tianditu.gov.cn/vec_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=vec&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=' + APP_KEY,
  layer: 'vec',
  style: 'default',
  format: 'tiles',
  tileMatrixSetID: 'w',
  subdomains: ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7'],
  maximumLevel: 18,
})

// 矢量注记
const cvaLayer = new Cesium.WebMapTileServiceImageryProvider({
  url: 'http://t0.tianditu.gov.cn/cva_w/wmts?service=wmts&request=GetTile&version=1.0.0&LAYER=cva&tileMatrixSet=w&TileMatrix={TileMatrix}&TileRow={TileRow}&TileCol={TileCol}&style=default&format=tiles&tk=' + APP_KEY,
  layer: 'cva',
  style: 'default',
  format: 'tiles',
  tileMatrixSetID: 'w',
  subdomains: ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7'],
  maximumLevel: 18,
})
```

**优点**：
- ✅ 符合OGC标准，更规范
- ✅ 支持更多WMTS特性（如样式切换）
- ✅ 官方文档明确支持

**缺点**：
- ⚠️ 实现稍复杂，需要配置更多参数
- ⚠️ 需要验证WMTS服务的可用性

### 2.4 图层叠加顺序

在Cesium中，后添加的图层会显示在上层。正确的叠加顺序应为：

1. **底层**：矢量底图（`vec_w`）
2. **上层**：矢量注记（`cva_w`）

这样可以确保注记显示在底图之上。

## 三、性能分析

### 3.1 矢量图层 vs 影像图层

| 特性 | 矢量图层 | 影像图层 |
|------|---------|---------|
| 文件大小 | 较小（矢量数据） | 较大（栅格图片） |
| 缩放性能 | 优秀（可无限缩放不失真） | 一般（固定分辨率） |
| 渲染性能 | 优秀（浏览器矢量渲染） | 良好（图片解码） |
| 加载速度 | 较快 | 较慢 |
| 视觉效果 | 清晰、可定制 | 真实、直观 |

**结论**：矢量图层在2D模式下通常性能更好，特别是在大范围缩放时。

### 3.2 2D模式下的优势

- ✅ 2D模式不需要3D渲染管道，性能开销更小
- ✅ 矢量图层在2D模式下渲染更高效
- ✅ 不需要加载三维地形和地名服务，减少网络请求

## 四、实现建议

### 4.1 推荐方案

**优先使用方案一（UrlTemplateImageryProvider）**，原因：
1. 与现有代码实现方式一致
2. 代码更简洁，易于维护
3. 如果 `DataServer` 不支持矢量图层，再考虑方案二

### 4.2 实现步骤

1. **添加矢量图层创建函数**
   ```typescript
   // 在 utils/tianditu.ts 中添加
   export function createTiandituVectorLayer() {
     // 矢量底图
   }
   
   export function createTiandituVectorAnnoLayer() {
     // 矢量注记
   }
   
   export function createTiandituVectorLayers() {
     return [
       createTiandituVectorLayer(),
       createTiandituVectorAnnoLayer(),
     ]
   }
   ```

2. **修改地图样式切换逻辑**
   ```typescript
   // 在 CesiumMap.vue 中
   case 'normal':
     // 标准地图：使用矢量图层
     const vectorLayers = createTiandituVectorLayers()
     vectorLayers.forEach((layer) => {
       viewer.value.imageryLayers.addImageryProvider(layer)
     })
     break
   ```

3. **测试验证**
   - 验证图层加载是否正常
   - 验证图层叠加顺序是否正确
   - 验证缩放和交互是否正常

### 4.3 兼容性考虑

- 保留现有的影像图层实现，作为备选方案
- 如果矢量图层加载失败，自动降级到影像图层
- 提供地图样式切换功能，让用户选择

## 五、风险与挑战

### 5.1 技术风险

| 风险 | 可能性 | 影响 | 应对措施 |
|------|--------|------|---------|
| DataServer不支持矢量图层 | 中 | 高 | 使用WMTS方案 |
| WMTS服务不稳定 | 低 | 中 | 实现自动重试和降级 |
| 图层叠加顺序错误 | 低 | 低 | 严格按照顺序添加 |
| 性能问题 | 低 | 中 | 优化图层加载策略 |

### 5.2 需要验证的问题

1. ✅ **天地图 DataServer 是否支持矢量图层**
   - 需要测试：`DataServer?T=vec_w` 和 `T=cva_w` 是否可用
   
2. ✅ **WMTS 服务的 URL 格式是否正确**
   - 需要验证 WMTS 参数格式与天地图服务是否匹配

3. ✅ **图层叠加顺序是否正确**
   - 需要测试注记是否正常显示在底图之上

## 六、结论

### 6.1 可行性结论

✅ **完全可行**

在2D Cesium上叠加天地图矢量地图和矢量注记在技术上完全可行，理由：

1. ✅ Cesium 2D模式完全支持影像图层叠加
2. ✅ 天地图提供标准的矢量图层服务（WMTS 和 DataServer）
3. ✅ 现有代码架构支持扩展新的图层类型
4. ✅ 与当前实现方式兼容，易于集成

### 6.2 推荐实施计划

1. **第一阶段：验证服务可用性**
   - 测试 `DataServer?T=vec_w` 和 `T=cva_w` 是否可用
   - 如果不可用，测试 WMTS 服务

2. **第二阶段：实现矢量图层加载**
   - 添加矢量图层创建函数
   - 实现图层叠加逻辑

3. **第三阶段：集成到地图组件**
   - 修改地图样式切换逻辑
   - 添加错误处理和降级方案

4. **第四阶段：测试和优化**
   - 功能测试
   - 性能测试
   - 兼容性测试

### 6.3 预期效果

- ✅ 在2D模式下显示清晰的矢量地图
- ✅ 矢量注记正确叠加在底图之上
- ✅ 性能和用户体验优于影像图层
- ✅ 支持缩放、平移等所有交互功能

## 七、参考资料

1. [Cesium官方文档 - Imagery Layers](https://cesium.com/learn/cesiumjs/ref-doc/ImageryLayerCollection.html)
2. [天地图开放平台 - WMTS服务](http://lbs.tianditu.gov.cn/server/MapService.html)
3. 项目文档：`TIANDITU_OFFICIAL.md`
4. 当前实现：`frontend/screen/src/utils/tianditu.ts`

---

**分析日期**：2024年
**分析人员**：AI Assistant
**状态**：✅ 建议实施

