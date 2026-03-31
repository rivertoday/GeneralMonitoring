<template>
  <div v-if="visible" class="dialog-overlay" @click="handleOverlayClick">
    <div class="dialog-container" @click.stop>
      <div class="dialog-header">
        <h3 class="dialog-title">报警记录详情</h3>
        <button class="close-btn" @click="handleClose">×</button>
      </div>
      <div class="dialog-content" v-if="recordData">
        <div class="info-section">
          <div class="info-item">
            <span class="info-label">报警编码：</span>
            <span class="info-value">{{ recordData.alarm_code }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">报警类型：</span>
            <span class="info-value">{{ recordData.alarm_type }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">报警状态：</span>
            <span class="info-value" :class="getStatusClass(recordData.alarm_status)">
              {{ recordData.alarm_status_display }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">行业类型：</span>
            <span class="info-value">{{ recordData.industry_type_display }}</span>
          </div>
          <div class="info-item" v-if="recordData.monitor_detail">
            <span class="info-label">监测点：</span>
            <span class="info-value">{{ recordData.monitor_detail.monitor_name }}</span>
          </div>
          <div class="info-item" v-if="recordData.alarm_value !== null && recordData.alarm_value !== undefined">
            <span class="info-label">报警数值：</span>
            <span class="info-value">
              {{ recordData.alarm_value }}
              <span v-if="recordData.monitor_detail?.monitor_unit">{{ recordData.monitor_detail.monitor_unit }}</span>
            </span>
          </div>
          <div class="info-item" v-if="recordData.threshold_value !== null && recordData.threshold_value !== undefined">
            <span class="info-label">阈值数值：</span>
            <span class="info-value">
              {{ recordData.threshold_value }}
              <span v-if="recordData.monitor_detail?.monitor_unit">{{ recordData.monitor_detail.monitor_unit }}</span>
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">报警时间：</span>
            <span class="info-value">{{ formatDateTime(recordData.alarm_time) }}</span>
          </div>
          <div class="info-item" v-if="recordData.alarm_duration !== null && recordData.alarm_duration !== undefined">
            <span class="info-label">持续时间：</span>
            <span class="info-value">{{ recordData.alarm_duration }} 分钟</span>
          </div>
          <div class="info-item" v-if="recordData.street">
            <span class="info-label">所属街道：</span>
            <span class="info-value">{{ recordData.street }}</span>
          </div>
          <div class="info-item" v-if="recordData.address">
            <span class="info-label">详细地址：</span>
            <span class="info-value">{{ recordData.address }}</span>
          </div>
          <div class="info-item" v-if="recordData.handle_time">
            <span class="info-label">处理时间：</span>
            <span class="info-value">{{ formatDateTime(recordData.handle_time) }}</span>
          </div>
          <div class="info-item" v-if="recordData.handle_result">
            <span class="info-label">处理结果：</span>
            <span class="info-value">{{ recordData.handle_result }}</span>
          </div>
        </div>

        <div class="description-section" v-if="recordData.description">
          <h4 class="section-title">报警描述</h4>
          <div class="description-content">{{ recordData.description }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { AlarmRecord } from '@/api/modules/risk'

interface Props {
  visible: boolean
  recordData: AlarmRecord | null
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

  &.status-0 {
    color: #ff4d4f; // 未处理 - 红色
  }

  &.status-1 {
    color: #ffa940; // 处理中 - 橙色
  }

  &.status-2 {
    color: #52c41a; // 已处理 - 绿色
  }

  &.status-3 {
    color: #999999; // 已忽略 - 灰色
  }
}

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

