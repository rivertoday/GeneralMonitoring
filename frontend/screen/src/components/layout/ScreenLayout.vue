<template>
  <div class="screen-layout">
    <!-- 头部 -->
    <header class="screen-header">
      <div class="header-left">
        <h1 class="screen-title">{{ title }}</h1>
      </div>
      <div class="header-center">
        <div class="header-info">
          <span class="info-item">慈湖高新区风险监测预警系统</span>
        </div>
      </div>
      <div class="header-right">
        <div class="screen-time">{{ currentTime }}</div>
        <button
          v-if="showHomeButton"
          class="home-button"
          @click="handleGoHome"
          title="返回首页"
        >
          <span class="home-icon">🏠</span>
        </button>
      </div>
    </header>

    <!-- 内容区 -->
    <main class="screen-content">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'

interface Props {
  title?: string
  showHomeButton?: boolean // 是否显示返回首页按钮
}

const props = withDefaults(defineProps<Props>(), {
  title: '风险监测预警系统',
  showHomeButton: false,
})

const router = useRouter()

const currentTime = ref('')

let timeTimer: ReturnType<typeof setInterval> | null = null

const updateTime = () => {
  currentTime.value = dayjs().format('YYYY年MM月DD日 HH:mm:ss')
}

onMounted(() => {
  updateTime()
  timeTimer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  if (timeTimer) {
    clearInterval(timeTimer)
  }
})

// 返回首页
const handleGoHome = () => {
  router.push('/overview')
}
</script>

<style scoped lang="scss">
@use '@/styles/variables.scss' as *;
@use '@/styles/mixins.scss' as *;

.screen-layout {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  background: $bg-primary;
}

.screen-header {
  width: 100%;
  height: 8vh;
  min-height: 60px;
  padding: 0 2vw;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(180deg, rgba(20, 27, 45, 0.9) 0%, rgba(10, 14, 39, 0.5) 100%);
  border-bottom: 1px solid $border-color;
  position: relative;
  z-index: 100;

  &::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, $color-primary, transparent);
  }
}

.header-left,
.header-center,
.header-right {
  flex: 1;
  display: flex;
  align-items: center;
}

.header-left {
  justify-content: flex-start;
}

.header-center {
  justify-content: center;
}

.header-right {
  justify-content: flex-end;
}

.screen-title {
  @include title(1);
  @include gradient-text;
  text-shadow: 0 0 20px rgba(64, 158, 255, 0.5);
}

.header-info {
  .info-item {
    @include font-size($font-size-lg);
    color: $text-secondary;
    padding: 0 1vw;
  }
}

.screen-time {
  @include font-size($font-size-base);
  color: $text-secondary;
  font-family: 'Courier New', monospace;
  padding: 0.5vh 1vw;
  background: rgba(64, 158, 255, 0.1);
  border-radius: $radius-sm;
  margin-right: 1vw;
}

.home-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  padding: 0;
  background: rgba(64, 158, 255, 0.1);
  border: 1px solid rgba(64, 158, 255, 0.3);
  border-radius: $radius-md;
  color: $text-primary;
  cursor: pointer;
  transition: all $transition-base;
  font-size: 24px;
  
  &:hover {
    background: rgba(64, 158, 255, 0.2);
    border-color: rgba(64, 158, 255, 0.6);
    transform: scale(1.1);
    box-shadow: 0 0 15px rgba(64, 158, 255, 0.5);
  }
  
  &:active {
    transform: scale(0.95);
  }
}

.home-icon {
  display: block;
  line-height: 1;
}

.screen-content {
  width: 100%;
  height: calc(100vh - 8vh);
  overflow: hidden;
  position: relative;
}
</style>

