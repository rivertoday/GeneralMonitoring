<template>
  <div class="warning-event-list">
    <div class="list-header">
      <h3 class="list-title">预警事件列表</h3>
      <div class="list-subtitle">共 {{ eventList.length }} 条预警</div>
    </div>
    <div class="list-content">
      <div
        v-for="event in eventList"
        :key="event.id"
        class="event-item"
        :class="getEventClass(event)"
        @click="handleEventClick(event)"
      >
        <div class="event-level" :style="{ backgroundColor: getLevelColor(event.warning_level_id) }">
          {{ getLevelLabel(event.warning_level_id) }}
        </div>
        <div class="event-info">
          <div class="event-title">{{ event.warning_title }}</div>
          <div class="event-meta">
            <span class="event-type">{{ event.industry_type_display }}</span>
            <span class="event-time">{{ formatTime(event.warning_time) }}</span>
          </div>
          <div class="event-status">
            <span class="status-badge" :class="getStatusClass(event.warning_status)">
              {{ event.warning_status_display }}
            </span>
          </div>
        </div>
      </div>
      <div v-if="eventList.length === 0" class="empty-state">
        暂无预警事件
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { WarningEvent } from '@/api/modules/safety'

interface Props {
  events: WarningEvent[]
}

interface Emits {
  (e: 'event-click', event: WarningEvent): void
}

const props = defineProps<Props>()
const emit = defineEmits<Emits>()

// 计算属性：按时间排序的事件列表
const eventList = computed(() => {
  return [...props.events].sort((a, b) => {
    return new Date(b.warning_time).getTime() - new Date(a.warning_time).getTime()
  })
})

// 获取预警级别颜色
const getLevelColor = (levelId: number): string => {
  const colors: Record<number, string> = {
    1: '#ff4d4f', // 红色I级
    2: '#ffa940', // 橙色Ⅱ级
    3: '#ffd666', // 黄色Ⅲ级
    4: '#1890ff', // 蓝色Ⅳ级
  }
  return colors[levelId] || '#999'
}

// 获取预警级别标签
const getLevelLabel = (levelId: number): string => {
  const labels: Record<number, string> = {
    1: 'I级',
    2: 'Ⅱ级',
    3: 'Ⅲ级',
    4: 'Ⅳ级',
  }
  return labels[levelId] || '未知'
}

// 获取事件样式类
const getEventClass = (event: WarningEvent): string => {
  return `level-${event.warning_level_id} status-${event.warning_status}`
}

// 获取状态样式类
const getStatusClass = (status: number): string => {
  const classes: Record<number, string> = {
    0: 'status-draft', // 未发布
    1: 'status-published', // 已发布
    2: 'status-processing', // 处理中
    3: 'status-resolved', // 已处置
    4: 'status-closed', // 已关闭
  }
  return classes[status] || ''
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

// 处理事件点击
const handleEventClick = (event: WarningEvent) => {
  emit('event-click', event)
}
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;
@use '@/styles/mixins.scss' as *;

.warning-event-list {
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

.event-item {
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

  &.level-1 {
    border-left-color: #ff4d4f;
  }

  &.level-2 {
    border-left-color: #ffa940;
  }

  &.level-3 {
    border-left-color: #ffd666;
  }

  &.level-4 {
    border-left-color: #1890ff;
  }
}

.event-level {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: $radius-sm;
  color: #fff;
  font-weight: bold;
  font-size: 12px;
  flex-shrink: 0;
}

.event-info {
  flex: 1;
  min-width: 0;
}

.event-title {
  @include font-size($font-size-base);
  color: $text-primary;
  font-weight: 600;
  margin-bottom: 0.5vh;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.event-meta {
  display: flex;
  gap: 1vw;
  margin-bottom: 0.5vh;
  @include font-size($font-size-xs);
  color: $text-secondary;
}

.event-type {
  padding: 2px 8px;
  background: rgba(64, 158, 255, 0.2);
  border-radius: $radius-sm;
}

.event-time {
  color: $text-muted;
}

.event-status {
  margin-top: 0.3vh;
}

.status-badge {
  display: inline-block;
  padding: 2px 8px;
  border-radius: $radius-sm;
  font-size: 11px;
  font-weight: 500;

  &.status-draft {
    background: rgba(153, 153, 153, 0.2);
    color: #999;
  }

  &.status-published {
    background: rgba(24, 144, 255, 0.2);
    color: #1890ff;
  }

  &.status-processing {
    background: rgba(255, 165, 0, 0.2);
    color: #ffa940;
  }

  &.status-resolved {
    background: rgba(82, 196, 26, 0.2);
    color: #52c41a;
  }

  &.status-closed {
    background: rgba(140, 140, 140, 0.2);
    color: #8c8c8c;
  }
}

.empty-state {
  text-align: center;
  padding: 4vh 2vw;
  color: $text-muted;
  @include font-size($font-size-sm);
}
</style>

