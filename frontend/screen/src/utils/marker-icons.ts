/**
 * 标记点图标工具函数
 * 用于生成不同资源类型的标记点图标（SVG格式）
 */

/**
 * 资源类型颜色映射
 */
export const resourceTypeColors: Record<number, string> = {
  1: '#ff4d4f', // 救援队伍 - 红色
  2: '#1890ff', // 应急专家 - 蓝色
  3: '#52c41a', // 物资装备 - 绿色
}

/**
 * 防护目标类型颜色映射
 */
export const targetTypeColors: Record<number, string> = {
  1: '#faad14', // 学校 - 橙色
  2: '#722ed1', // 居民区 - 紫色
  3: '#eb2f96', // 医院 - 粉色
  4: '#13c2c2', // 商场 - 青色
  5: '#fa8c16', // 其他 - 橙红色
}

/**
 * 避难场所类型颜色映射
 */
export const shelterTypeColors: Record<number, string> = {
  1: '#52c41a', // 公园 - 绿色
  2: '#1890ff', // 广场 - 蓝色
  3: '#faad14', // 体育场 - 橙色
  4: '#722ed1', // 学校 - 紫色
  5: '#13c2c2', // 其他 - 青色
}

/**
 * 创建圆形标记点 SVG 图标（Base64）
 * @param color 标记点颜色（十六进制，如 #ff4d4f）
 * @param size 图标大小（默认 32）
 * @param emoji emoji 图标（可选）
 */
export function createCircleMarkerIcon(
  color: string = '#409eff',
  size: number = 32,
  emoji?: string
): string {
  const svg = `
    <svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
      <circle cx="${size / 2}" cy="${size / 2}" r="${size / 2 - 2}" fill="${color}" stroke="#fff" stroke-width="2"/>
      ${emoji ? `<text x="${size / 2}" y="${size / 2 + size / 6}" font-size="${size * 0.5}" text-anchor="middle" dominant-baseline="middle">${emoji}</text>` : ''}
    </svg>
  `.trim()

  return `data:image/svg+xml;base64,${btoa(unescape(encodeURIComponent(svg)))}`
}

/**
 * 根据资源类型创建标记点图标
 */
export function createResourceMarkerIcon(resourceType: number, emoji?: string): string {
  const color = resourceTypeColors[resourceType] || '#409eff'
  return createCircleMarkerIcon(color, 32, emoji)
}

/**
 * 根据防护目标类型创建标记点图标
 */
export function createTargetMarkerIcon(targetType: number, emoji?: string): string {
  const color = targetTypeColors[targetType] || '#409eff'
  return createCircleMarkerIcon(color, 32, emoji)
}

/**
 * 根据避难场所类型创建标记点图标
 */
export function createShelterMarkerIcon(shelterType: number, emoji?: string): string {
  const color = shelterTypeColors[shelterType] || '#409eff'
  return createCircleMarkerIcon(color, 32, emoji)
}

/**
 * 创建火车站标记点图标
 */
export function createStationMarkerIcon(): string {
  return createCircleMarkerIcon('#FFD700', 40, '🚂')
}

