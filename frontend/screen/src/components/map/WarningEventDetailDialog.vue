<template>
  <div v-if="visible" class="dialog-overlay" @click="handleOverlayClick">
    <div class="dialog-container" @click.stop>
      <div class="dialog-header">
        <h3 class="dialog-title">预警事件详情</h3>
        <button class="close-btn" @click="handleClose">×</button>
      </div>
      <div class="dialog-content" v-if="eventData">
        <div class="info-section">
          <div class="info-item">
            <span class="info-label">预警编码：</span>
            <span class="info-value">{{ eventData.warning_code }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">预警标题：</span>
            <span class="info-value">{{ eventData.warning_title }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">预警级别：</span>
            <span class="info-value" :class="getLevelClass(eventData.warning_level_id)">
              {{ getLevelLabel(eventData.warning_level_id) }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">行业类型：</span>
            <span class="info-value">{{ eventData.industry_type_display }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">预警类型：</span>
            <span class="info-value">{{ eventData.warning_type }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">预警状态：</span>
            <span class="info-value" :class="getStatusClass(eventData.warning_status)">
              {{ eventData.warning_status_display }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">预警时间：</span>
            <span class="info-value">{{ formatDateTime(eventData.warning_time) }}</span>
          </div>
          <div class="info-item" v-if="eventData.street">
            <span class="info-label">所属街道：</span>
            <span class="info-value">{{ eventData.street }}</span>
          </div>
          <div class="info-item" v-if="eventData.address">
            <span class="info-label">详细地址：</span>
            <span class="info-value">{{ eventData.address }}</span>
          </div>
        </div>

        <div class="stats-section" v-if="eventData.nearby_monitor_count || eventData.nearby_risk_count || eventData.nearby_resource_count">
          <h4 class="section-title">周边资源</h4>
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-label">附近监测点</div>
              <div class="stat-value">{{ eventData.nearby_monitor_count || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">附近危险源</div>
              <div class="stat-value">{{ eventData.nearby_risk_count || 0 }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">附近应急资源</div>
              <div class="stat-value">{{ eventData.nearby_resource_count || 0 }}</div>
            </div>
          </div>
        </div>

        <div class="description-section" v-if="eventData.description">
          <h4 class="section-title">事件描述</h4>
          <div class="description-content">{{ eventData.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { WarningEvent } from '@/api/modules/safety'

interface Props {
  visible: boolean
  eventData: WarningEvent | null
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
}>()

const handleClose = () => {
  emit('update:visible', false)
}

const handleOverlayClick = () => {
  emit('update:visible', false)
}

const getLevelLabel = (levelId: number): string => {
  const labels: Record<number, string> = {
    1: '红色I级',
    2: '橙色Ⅱ级',
    3: '黄色Ⅲ级',
    4: '蓝色Ⅳ级',
  }
  return labels[levelId] || '未知'
}

const getLevelClass = (levelId: number): string => {
  return `level-${levelId}`
}

const getStatusClass = (status: number): string => {
  return `status-${status}`
}

const formatDateTime = (timeStr: string): string => {
  if (!timeStr) return '-'
  const date = new Date(timeStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}
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
  background: rgba(0, 20, 40, 0.95);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: 12px;
  width: 90%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
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
}

.info-section {
  margin-bottom: 24px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  font-size: 14px;

  &:last-child {
    margin-bottom: 0;
  }
}

.info-label {
  color: #999;
  min-width: 100px;
}

.info-value {
  color: #e0e0e0;
  font-weight: 500;

  &.level-1 {
    color: #ff4d4f;
  }

  &.level-2 {
    color: #ffa940;
  }

  &.level-3 {
    color: #ffd666;
  }

  &.level-4 {
    color: #1890ff;
  }

  &.status-0 {
    color: #999;
  }

  &.status-1 {
    color: #1890ff;
  }

  &.status-2 {
    color: #ffa940;
  }

  &.status-3 {
    color: #52c41a;
  }

  &.status-4 {
    color: #8c8c8c;
  }
}

.stats-section,
.description-section {
  margin-bottom: 24px;

  &:last-child {
    margin-bottom: 0;
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-item {
  background: rgba(64, 158, 255, 0.1);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: 8px;
  padding: 16px;
  text-align: center;
}

.stat-label {
  font-size: 13px;
  color: #999;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
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
</style>

