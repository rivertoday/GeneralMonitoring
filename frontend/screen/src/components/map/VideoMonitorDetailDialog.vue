<template>
  <div v-if="visible" class="dialog-overlay" @click="handleOverlayClick">
    <div class="dialog-container" @click.stop>
      <div class="dialog-header">
        <h3 class="dialog-title">视频监控详情</h3>
        <button class="close-btn" @click="handleClose">×</button>
      </div>
      <div class="dialog-content" v-if="monitorData">
        <div class="content-layout">
          <!-- 左侧：视频播放区域 -->
          <div class="video-section">
            <h4 class="section-title">视频监控</h4>
            <div class="video-container">
              <video
                v-if="videoStreamUrl && monitorData.online_status === 1"
                ref="videoPlayer"
                class="video-player"
                controls
                autoplay
                muted
                :src="videoStreamUrl"
                @error="handleVideoError"
                @loadedmetadata="handleVideoLoaded"
                @play="handleVideoPlay"
                @pause="handleVideoPause"
              >
                您的浏览器不支持视频播放
              </video>
              <div v-else-if="monitorData.online_status === 0" class="video-offline">
                <div class="offline-icon">📹</div>
                <div class="offline-text">监控设备离线</div>
              </div>
              <div v-else class="video-unavailable">
                <div class="unavailable-icon">⚠️</div>
                <div class="unavailable-text">视频流不可用</div>
                <div class="unavailable-desc" v-if="monitorData.rtsp_url">
                  RTSP地址: {{ monitorData.rtsp_url }}
                </div>
              </div>
              <div v-if="isSimulated" class="simulated-badge">
                <span class="badge-text">模拟播放</span>
              </div>
            </div>
            <div class="video-controls" v-if="videoStreamUrl && monitorData.online_status === 1">
              <div class="control-info">
                <span class="control-label">播放状态：</span>
                <span class="control-value">{{ videoStatus }}</span>
              </div>
              <div class="control-info" v-if="monitorData.video_url">
                <span class="control-label">视频源：</span>
                <span class="control-value">实际视频流</span>
              </div>
              <div class="control-info" v-else-if="isSimulated">
                <span class="control-label">视频源：</span>
                <span class="control-value">模拟视频流（消防救援演练）</span>
              </div>
            </div>
          </div>

          <!-- 右侧：详情信息 -->
          <div class="info-section">
            <h4 class="section-title">监控详情</h4>
            <div class="info-list">
              <div class="info-item">
                <span class="info-label">监控编码：</span>
                <span class="info-value">{{ monitorData.monitor_code }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">监控名称：</span>
                <span class="info-value">{{ monitorData.monitor_name }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">监控类型：</span>
                <span class="info-value">{{ monitorData.monitor_type_display }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">行业类型：</span>
                <span class="info-value">{{ monitorData.industry_type_display }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">在线状态：</span>
                <span class="info-value" :class="monitorData.online_status === 1 ? 'online' : 'offline'">
                  {{ monitorData.online_status_display }}
                </span>
              </div>
              <div class="info-item" v-if="monitorData.street">
                <span class="info-label">所属街道：</span>
                <span class="info-value">{{ monitorData.street }}</span>
              </div>
              <div class="info-item" v-if="monitorData.address">
                <span class="info-label">详细地址：</span>
                <span class="info-value">{{ monitorData.address }}</span>
              </div>
              <div class="info-item" v-if="monitorData.coverage_radius">
                <span class="info-label">覆盖半径：</span>
                <span class="info-value">{{ monitorData.coverage_radius }} 米</span>
              </div>
              <div class="info-item" v-if="monitorData.camera_angle">
                <span class="info-label">摄像头角度：</span>
                <span class="info-value">{{ monitorData.camera_angle }}°</span>
              </div>
              <div class="info-item" v-if="monitorData.organization_name">
                <span class="info-label">所属组织：</span>
                <span class="info-value">{{ monitorData.organization_name }}</span>
              </div>
              <div class="info-item full-width" v-if="monitorData.description">
                <span class="info-label">监控描述：</span>
                <div class="info-value">{{ monitorData.description }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onUnmounted, onMounted } from 'vue'
import type { VideoMonitor } from '@/api/modules/safety'

interface Props {
  visible: boolean
  monitorData: VideoMonitor | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()

const videoPlayer = ref<HTMLVideoElement | null>(null)
const videoStatus = ref<string>('准备中...')
const isSimulated = ref(false)

// 公开的消防救援测试视频流URL（用于模拟播放）
// 使用国内可访问的公开测试视频流，实际项目中应替换为真实的视频流地址
// 使用一个公开的测试视频（模拟消防救援场景）
// 注意：这是一个通用的测试视频，实际项目中应使用真实的消防救援视频流
const DEMO_FIRE_RESCUE_VIDEO_URL = 'https://lf9-cdn-tos.bytecdntp.com/cdn/expire-1-M/byted-player-videos/1.0.0/xgplayer-demo.mp4'

// 计算视频流URL
const videoStreamUrl = computed(() => {
  if (!props.monitorData || props.monitorData.online_status !== 1) {
    return null
  }
  
  // 如果监控有实际的视频流URL，使用实际URL
  if (props.monitorData.video_url) {
    isSimulated.value = false
    return props.monitorData.video_url
  }
  
  // 如果没有实际URL但监控在线，使用模拟视频流
  isSimulated.value = true
  return DEMO_FIRE_RESCUE_VIDEO_URL
})

const handleClose = () => {
  emit('update:visible', false)
}

const handleOverlayClick = () => {
  emit('update:visible', false)
}

const handleVideoError = (event: Event) => {
  console.error('视频播放失败:', event)
  videoStatus.value = '播放失败'
  
  // 如果是模拟视频流失败，尝试使用备用URL
  if (isSimulated.value && videoPlayer.value) {
    console.warn('模拟视频流播放失败，尝试备用URL')
    // 可以在这里添加备用视频流URL的逻辑
  }
}

const handleVideoLoaded = () => {
  console.log('视频加载完成')
  videoStatus.value = '已加载'
}

const handleVideoPlay = () => {
  console.log('视频开始播放')
  videoStatus.value = '播放中'
}

const handleVideoPause = () => {
  console.log('视频暂停')
  videoStatus.value = '已暂停'
}

// 监听对话框显示/隐藏，控制视频播放
watch(
  () => props.visible,
  (newVal) => {
    if (!newVal && videoPlayer.value) {
      // 对话框关闭时，停止视频播放
      videoPlayer.value.pause()
      videoPlayer.value.src = ''
      videoStatus.value = '已停止'
    } else if (newVal && videoPlayer.value) {
      // 对话框打开时，重置状态
      videoStatus.value = '准备中...'
    }
  }
)

// 监听监控数据变化，重置视频状态
watch(
  () => props.monitorData,
  () => {
    if (videoPlayer.value) {
      videoStatus.value = '准备中...'
    }
  }
)

onMounted(() => {
  // 组件挂载时的初始化
  if (videoPlayer.value) {
    videoStatus.value = '准备中...'
  }
})

onUnmounted(() => {
  // 组件卸载时，停止视频播放
  if (videoPlayer.value) {
    videoPlayer.value.pause()
    videoPlayer.value.src = ''
    videoStatus.value = '已停止'
  }
})
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 3000;
  backdrop-filter: blur(4px);
}

.dialog-container {
  background: linear-gradient(135deg, #1a2b4a 0%, #0d1b2d 100%);
  border: 2px solid #2d4a7a;
  border-radius: 12px;
  width: 90%;
  max-width: 1200px;
  max-height: 90vh;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), 0 0 20px rgba(26, 43, 74, 0.8);
  display: flex;
  flex-direction: column;
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid rgba(64, 158, 255, 0.2);
}

.dialog-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #409eff;
}

.close-btn {
  background: none;
  border: none;
  color: #e0e0e0;
  font-size: 28px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.3s;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #409eff;
  }
}

.dialog-content {
  padding: 24px;
  flex: 1;
  overflow-y: auto;
}

.content-layout {
  display: flex;
  gap: 24px;
  height: 100%;
}

.video-section {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.info-section {
  width: 350px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-size: 14px;

  &.full-width {
    flex-direction: column;
    gap: 8px;
  }
}

.info-label {
  color: #7aa4d4;
  font-weight: 500;
  white-space: nowrap;
  flex-shrink: 0;
  min-width: 100px;
}

.info-value {
  color: #e0e8f0;
  flex: 1;
  word-break: break-all;
  line-height: 1.6;

  &.online {
    color: #52c41a;
    font-weight: bold;
  }

  &.offline {
    color: #ff4d4f;
    font-weight: bold;
  }
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #409eff;
  margin: 0 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(64, 158, 255, 0.2);
}

.video-container {
  flex: 1;
  min-height: 0;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(64, 158, 255, 0.3);
  position: relative;
}

.video-player {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.video-offline,
.video-unavailable {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: #999;
}

.offline-icon,
.unavailable-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.offline-text,
.unavailable-text {
  font-size: 16px;
  color: #e0e0e0;
  margin-bottom: 8px;
}

.unavailable-desc {
  font-size: 12px;
  color: #999;
  word-break: break-all;
  padding: 0 20px;
  text-align: center;
}

.description-content {
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #e0e0e0;
  line-height: 1.6;
  white-space: pre-wrap;
}

.simulated-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 10;
}

.badge-text {
  display: inline-block;
  padding: 4px 12px;
  background: rgba(255, 165, 0, 0.9);
  color: #fff;
  font-size: 12px;
  font-weight: 600;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.video-controls {
  margin-top: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.control-info {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.control-label {
  color: #7aa4d4;
  font-weight: 500;
}

.control-value {
  color: #e0e8f0;
}
</style>

