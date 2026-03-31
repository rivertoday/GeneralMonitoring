<template>
  <div class="alarm-record-list">
    <div class="list-header">
      <h3 class="list-title">报警记录列表</h3>
      <div class="list-subtitle">共 {{ recordList.length }} 条报警</div>
    </div>
    <div class="list-content">
      <div
        v-for="record in recordList"
        :key="record.id"
        class="record-item"
        :class="getRecordClass(record)"
        @click="handleRecordClick(record)"
      >
        <div class="record-status" :style="{ backgroundColor: getStatusColor(record.alarm_status) }">
          {{ getStatusLabel(record.alarm_status) }}
        </div>
        <div class="record-info">
          <div class="record-title">{{ record.alarm_type }}</div>
          <div class="record-meta">
            <span class="record-type">{{ record.industry_type_display }}</span>
            <span class="record-time">{{ formatTime(record.alarm_time) }}</span>
          </div>
          <div class="record-detail" v-if="record.monitor_detail">
            <span class="monitor-name">{{ record.monitor_detail.monitor_name }}</span>
          </div>
          <div class="record-value" v-if="record.alarm_value !== null && record.alarm_value !== undefined">
            <span class="value-label">报警值:</span>
            <span class="value-number">{{ record.alarm_value }}</span>
            <span class="value-unit" v-if="record.monitor_detail?.monitor_unit">{{ record.monitor_detail.monitor_unit }}</span>
          </div>
        </div>
      </div>
      <div v-if="recordList.length === 0" class="empty-state">
        暂无报警记录
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { AlarmRecord } from '@/api/modules/risk'

interface Props {
  records: AlarmRecord[]
}

interface Emits {
  (e: 'record-click', record: AlarmRecord): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// 计算属性：按时间排序的记录列表
const recordList = computed(() => {
  return [...props.records].sort((a, b) => {
    return new Date(b.alarm_time).getTime() - new Date(a.alarm_time).getTime()
  })
})

// 获取报警状态颜色
const getStatusColor = (status: number): string => {
  const colors: Record<number, string> = {
    0: '#ff4d4f', // 未处理 - 红色
    1: '#ffa940', // 处理中 - 橙色
    2: '#52c41a', // 已处理 - 绿色
    3: '#999999', // 已忽略 - 灰色
  }
  return colors[status] || '#999'
}

// 获取报警状态标签
const getStatusLabel = (status: number): string => {
  const labels: Record<number, string> = {
    0: '未处理',
    1: '处理中',
    2: '已处理',
    3: '已忽略',
  }
  return labels[status] || '未知'
}

// 获取记录样式类
const getRecordClass = (record: AlarmRecord): string => {
  return `status-${record.alarm_status}`
}

// 格式化时间
const formatTime = (timeStr: string): string => {
  if (!timeStr) return '-'
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' })
}

// 处理记录点击
const handleRecordClick = (record: AlarmRecord) => {
  emit('record-click', record)
}
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;
@use '@/styles/mixins.scss' as *;

.alarm-record-list {
  padding: 1.5vh 1.5vw;
  height: 100%;
  overflow-y: auto;
}

.list-header {
  margin-bottom: 1.5vh;
  border-bottom: 1px solid $border-color;
  padding-bottom: 1vh;
}

.list-title {
  @include title(3);
  margin: 0 0 0.5vh 0;
  color: $text-primary;
}

.list-subtitle {
  @include font-size($font-size-sm);
  color: $text-secondary;
}

.list-content {
  display: flex;
  flex-direction: column;
  gap: 1.2vh;
}

.record-item {
  display: flex;
  gap: 1vw;
  padding: 1.2vh 1vw;
  background: rgba(64, 158, 255, 0.1);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-left: 4px solid #409eff;
  border-radius: $radius-md;
  cursor: pointer;
  transition: all $transition-base;

  &:hover {
    background: rgba(64, 158, 255, 0.15);
    border-color: rgba(64, 158, 255, 0.5);
    transform: translateX(-5px);
  }

  &.status-0 {
    border-left-color: #ff4d4f; // 未处理 - 红色
  }

  &.status-1 {
    border-left-color: #ffa940; // 处理中 - 橙色
  }

  &.status-2 {
    border-left-color: #52c41a; // 已处理 - 绿色
  }

  &.status-3 {
    border-left-color: #999999; // 已忽略 - 灰色
  }
}

.record-status {
  min-width: 50px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: $radius-sm;
  color: #fff;
  font-weight: bold;
  font-size: 11px;
  flex-shrink: 0;
}

.record-info {
  flex: 1;
  min-width: 0;
}

.record-title {
  @include font-size($font-size-base);
  color: $text-primary;
  font-weight: 600;
  margin-bottom: 0.5vh;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.record-meta {
  display: flex;
  gap: 1vw;
  margin-bottom: 0.5vh;
  @include font-size($font-size-xs);
  color: $text-secondary;
}

.record-type {
  padding: 2px 8px;
  background: rgba(64, 158, 255, 0.2);
  border-radius: $radius-sm;
}

.record-time {
  color: $text-muted;
}

.record-detail {
  margin-top: 0.3vh;
  @include font-size($font-size-xs);
  color: $text-secondary;
}

.monitor-name {
  padding: 2px 8px;
  background: rgba(255, 193, 7, 0.2);
  border-radius: $radius-sm;
  color: #ffc107;
}

.record-value {
  margin-top: 0.3vh;
  @include font-size($font-size-xs);
  color: $text-secondary;
  display: flex;
  align-items: center;
  gap: 4px;
}

.value-label {
  color: $text-muted;
}

.value-number {
  color: #ff4d4f;
  font-weight: 600;
}

.value-unit {
  color: $text-muted;
}

.empty-state {
  text-align: center;
  padding: 4vh 2vw;
  color: $text-muted;
  @include font-size($font-size-sm);
}
</style>

