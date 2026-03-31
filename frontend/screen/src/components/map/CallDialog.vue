<template>
  <Teleport to="body">
    <Transition name="dialog-fade">
      <div v-if="visible" class="dialog-overlay" @click.self="handleClose">
        <div class="dialog-container">
          <div class="dialog-header">
            <h3 class="dialog-title">呼叫中...</h3>
            <button class="dialog-close" @click="handleClose">×</button>
          </div>
          <div class="dialog-body">
            <div class="call-info">
              <div class="call-icon">
                <div class="phone-ring" :class="{ 'ringing': isRinging }">
                  📞
                </div>
              </div>
              <div class="call-phone">{{ phone }}</div>
              <div class="call-status">{{ callStatus }}</div>
            </div>
          </div>
          <div class="dialog-footer">
            <button class="call-btn hangup" @click="handleHangup">
              <span class="icon">📴</span>
              <span>挂断</span>
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'

interface Props {
  visible: boolean
  phone: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  close: []
}>()

const isRinging = ref(true)
const callStatus = ref('正在呼叫...')

let callTimer: ReturnType<typeof setInterval> | null = null
let statusTimer: ReturnType<typeof setInterval> | null = null

watch(() => props.visible, (newVal) => {
  if (newVal) {
    startCall()
  } else {
    stopCall()
  }
})

const startCall = () => {
  isRinging.value = true
  callStatus.value = '正在呼叫...'
  
  // 模拟呼叫过程
  statusTimer = setTimeout(() => {
    callStatus.value = '正在接通...'
  }, 2000)
  
  callTimer = setTimeout(() => {
    isRinging.value = false
    callStatus.value = '通话中'
  }, 4000)
}

const stopCall = () => {
  if (callTimer) {
    clearTimeout(callTimer)
    callTimer = null
  }
  if (statusTimer) {
    clearTimeout(statusTimer)
    statusTimer = null
  }
  isRinging.value = false
}

const handleClose = () => {
  stopCall()
  emit('update:visible', false)
  emit('close')
}

const handleHangup = () => {
  stopCall()
  callStatus.value = '已挂断'
  setTimeout(() => {
    handleClose()
  }, 500)
}

onMounted(() => {
  if (props.visible) {
    startCall()
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
  z-index: 10000;
  backdrop-filter: blur(4px);
}

.dialog-container {
  background: linear-gradient(135deg, #1a2b4a 0%, #0d1b2d 100%);
  border: 2px solid #2d4a7a;
  border-radius: 8px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5), 0 0 20px rgba(26, 43, 74, 0.8);
  width: 90%;
  max-width: 400px;
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
  padding: 40px 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.call-info {
  text-align: center;
  width: 100%;
}

.call-icon {
  margin-bottom: 24px;
}

.phone-ring {
  font-size: 80px;
  display: inline-block;
  transition: transform 0.3s;

  &.ringing {
    animation: ring 1s ease-in-out infinite;
  }
}

@keyframes ring {
  0%, 100% {
    transform: rotate(0deg) scale(1);
  }
  25% {
    transform: rotate(-10deg) scale(1.1);
  }
  75% {
    transform: rotate(10deg) scale(1.1);
  }
}

.call-phone {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 16px;
  text-shadow: 0 0 10px rgba(64, 158, 255, 0.5);
}

.call-status {
  font-size: 18px;
  color: #7aa4d4;
}

.dialog-footer {
  padding: 16px 24px;
  border-top: 1px solid #2d4a7a;
  display: flex;
  justify-content: center;
}

.call-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 32px;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;

  &.hangup {
    background: linear-gradient(135deg, #ff4d4f 0%, #cf1322 100%);
    color: #fff;
    box-shadow: 0 4px 12px rgba(255, 77, 79, 0.4);

    &:hover {
      background: linear-gradient(135deg, #cf1322 0%, #ff4d4f 100%);
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(255, 77, 79, 0.6);
    }
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
</style>

