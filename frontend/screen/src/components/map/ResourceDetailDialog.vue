<template>
  <Teleport to="body">
    <Transition name="dialog-fade">
      <div v-if="visible" class="dialog-overlay" @click.self="handleClose">
        <div class="dialog-container">
          <div class="dialog-header">
            <h3 class="dialog-title">{{ resourceData?.resource_name || '安全资源详情' }}</h3>
            <button class="dialog-close" @click="handleClose">×</button>
          </div>
          <div class="dialog-body">
            <div v-if="resourceData" class="resource-info">
              <div class="info-item">
                <span class="info-label">资源编码：</span>
                <span class="info-value">{{ resourceData.resource_code }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">资源名称：</span>
                <span class="info-value">{{ resourceData.resource_name }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">资源类型：</span>
                <span class="info-value">{{ resourceData.resource_type_display }}</span>
              </div>
              <div v-if="resourceData.sub_type" class="info-item">
                <span class="info-label">子类型：</span>
                <span class="info-value">{{ resourceData.sub_type }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">所在位置：</span>
                <span class="info-value">{{ resourceData.street || '未知' }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">详细地址：</span>
                <span class="info-value">{{ resourceData.address || '未知' }}</span>
              </div>
              <div v-if="resourceData.organization_name" class="info-item">
                <span class="info-label">所属组织：</span>
                <span class="info-value">{{ resourceData.organization_name }}</span>
              </div>
              <div v-if="resourceData.contact_person" class="info-item">
                <span class="info-label">联系人：</span>
                <span class="info-value">{{ resourceData.contact_person }}</span>
              </div>
              <div v-if="resourceData.contact_phone" class="info-item">
                <span class="info-label">联系电话：</span>
                <span class="info-value phone">{{ resourceData.contact_phone }}</span>
              </div>
              <div v-if="resourceData.capacity" class="info-item">
                <span class="info-label">队伍人数：</span>
                <span class="info-value">{{ resourceData.capacity }}人</span>
              </div>
              <div v-if="resourceData.expert_field" class="info-item">
                <span class="info-label">专业领域：</span>
                <span class="info-value">{{ resourceData.expert_field }}</span>
              </div>
              <div v-if="resourceData.expert_level" class="info-item">
                <span class="info-label">技术等级：</span>
                <span class="info-value">{{ resourceData.expert_level }}</span>
              </div>
              <div v-if="resourceData.quantity" class="info-item">
                <span class="info-label">数量：</span>
                <span class="info-value">{{ resourceData.quantity }} {{ resourceData.unit || '件' }}</span>
              </div>
              <div v-if="resourceData.description" class="info-item full-width">
                <span class="info-label">描述：</span>
                <div class="info-value">{{ resourceData.description }}</div>
              </div>
            </div>
          </div>
          <div class="dialog-footer">
            <button v-if="resourceData?.contact_phone" class="call-btn" @click="handleCall">
              <span class="icon">📞</span>
              <span>呼叫</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import type { SafetyResource } from '@/api/modules/safety'

interface Props {
  visible: boolean
  resourceData?: SafetyResource | null
}

const props = withDefaults(defineProps<Props>(), {
  visible: false,
  resourceData: null,
})

const emit = defineEmits<{
  'update:visible': [value: boolean]
  close: []
  call: [phone: string]
}>()

const handleClose = () => {
  emit('update:visible', false)
  emit('close')
}

const handleCall = () => {
  if (props.resourceData?.contact_phone) {
    emit('call', props.resourceData.contact_phone)
  }
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

.resource-info {
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

  &.phone {
    color: #409eff;
    font-weight: bold;
  }
}

.dialog-footer {
  padding: 16px 24px;
  border-top: 1px solid #2d4a7a;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.call-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 24px;
  background: linear-gradient(135deg, #409eff 0%, #1890ff 100%);
  border: none;
  border-radius: 6px;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.4);

  &:hover {
    background: linear-gradient(135deg, #1890ff 0%, #409eff 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(64, 158, 255, 0.6);
  }

  &:active {
    transform: translateY(0);
  }

  .icon {
    font-size: 20px;
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

