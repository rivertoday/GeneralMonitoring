<template>
  <Teleport to="body">
    <Transition name="dialog-fade">
      <div v-if="visible" class="dialog-overlay" @click.self="handleClose">
        <div class="dialog-container">
          <div class="dialog-header">
            <h3 class="dialog-title">重点防护目标详情</h3>
            <button class="dialog-close" @click="handleClose">×</button>
          </div>
          <div class="dialog-body">
            <div v-if="targetData" class="target-info">
              <div class="info-item">
                <span class="info-label">目标名称：</span>
                <span class="info-value">{{ targetData.name }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">目标类型：</span>
                <span class="info-value">{{ targetData.type }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">防护级别：</span>
                <span class="info-value level">{{ targetData.level }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">所在位置：</span>
                <span class="info-value">{{ targetData.location }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">详细地址：</span>
                <span class="info-value">{{ targetData.address }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">防护范围：</span>
                <span class="info-value">{{ targetData.radius }}公里</span>
              </div>
              <div class="info-item">
                <span class="info-label">责任人：</span>
                <span class="info-value">{{ targetData.contactPerson }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">联系电话：</span>
                <span class="info-value">{{ targetData.contactPhone }}</span>
              </div>
              <div class="info-item full-width">
                <span class="info-label">防护措施：</span>
                <div class="info-value">{{ targetData.protectionMeasures }}</div>
              </div>
              <div class="info-item full-width">
                <span class="info-label">应急联系人：</span>
                <div class="info-value">{{ targetData.emergencyContact }}</div>
              </div>
              <div class="info-item full-width">
                <span class="info-label">备注说明：</span>
                <div class="info-value">{{ targetData.remark }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

interface Props {
  visible: boolean
  targetData?: {
    name: string
    type: string
    level: string
    location: string
    address: string
    radius: number
    contactPerson: string
    contactPhone: string
    protectionMeasures: string
    emergencyContact: string
    remark: string
  } | null
}

const props = withDefaults(defineProps<Props>(), {
  visible: false,
  targetData: null,
})

const emit = defineEmits<{
  'update:visible': [value: boolean]
  close: []
}>()

const handleClose = () => {
  emit('update:visible', false)
  emit('close')
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
  z-index: 9999;
  backdrop-filter: blur(4px);
}

.dialog-container {
  background: linear-gradient(135deg, #1a2b4a 0%, #0d1b2d 100%);
  border: 2px solid #2d4a7a;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), 0 0 20px rgba(26, 43, 74, 0.8);
  width: 90%;
  max-width: 600px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  border-bottom: 1px solid #2d4a7a;
  background: rgba(13, 27, 45, 0.8);
}

.dialog-title {
  margin: 0;
  font-size: 20px;
  font-weight: bold;
  color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
}

.dialog-close {
  background: none;
  border: none;
  color: #fff;
  font-size: 32px;
  line-height: 1;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  border-radius: 4px;

  &:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: rotate(90deg);
  }
}

.dialog-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.target-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;

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

  &.level {
    color: #ffaa00;
    font-weight: bold;
  }
}

// 动画效果
.dialog-fade-enter-active,
.dialog-fade-leave-active {
  transition: opacity 0.3s;
}

.dialog-fade-enter-active .dialog-container,
.dialog-fade-leave-active .dialog-container {
  transition: transform 0.3s, opacity 0.3s;
}

.dialog-fade-enter-from,
.dialog-fade-leave-to {
  opacity: 0;

  .dialog-container {
    transform: scale(0.9) translateY(-20px);
    opacity: 0;
  }
}

.dialog-fade-enter-to,
.dialog-fade-leave-from {
  opacity: 1;

  .dialog-container {
    transform: scale(1) translateY(0);
    opacity: 1;
  }
}

// 滚动条样式
.dialog-body::-webkit-scrollbar {
  width: 8px;
}

.dialog-body::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 4px;
}

.dialog-body::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;

  &:hover {
    background: rgba(255, 255, 255, 0.3);
  }
}
</style>

