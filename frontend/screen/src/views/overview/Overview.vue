<template>
  <div class="overview-container">
    <h1>大屏总览</h1>
    <div class="screen-grid">
      <div class="screen-card" @click="goToScreen('safety-run')">
        <div class="card-icon">🏢</div>
        <div class="card-title">安全运行一张图</div>
        <div class="card-desc">展示安全基础数据信息、救援队伍、物资装备等</div>
      </div>
      <div class="screen-card" @click="goToScreen('safety-status')">
        <div class="card-icon">📊</div>
        <div class="card-title">安全态势一张图</div>
        <div class="card-desc">展示区域四色风险图、行业态势、区域态势</div>
      </div>
      <div class="screen-card" @click="goToScreen('monitor-warn')">
        <div class="card-icon">⚠️</div>
        <div class="card-title">监测预警一张图</div>
        <div class="card-desc">展示实时监测数据、预警事件、视频监控</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToScreen = (name: string) => {
  // 使用路径跳转，确保路由正常工作
  const routeMap: Record<string, string> = {
    'safety-run': '/safety-run',
    'safety-status': '/safety-status',
    'monitor-warn': '/monitor-warn',
  }
  const path = routeMap[name]
  if (path) {
    // 直接使用push跳转，RouterView的key属性会确保组件重新渲染
    router.push(path)
  } else {
    console.error(`未知的大屏名称: ${name}`)
  }
}
</script>

<style scoped lang="scss">
.overview-container {
  min-height: 100vh;
  padding: 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;

  h1 {
    text-align: center;
    font-size: 48px;
    margin-bottom: 60px;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  }

  .screen-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 40px;
    max-width: 1400px;
    margin: 0 auto;
  }

  .screen-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 2px solid rgba(255, 255, 255, 0.2);

    &:hover {
      transform: translateY(-10px);
      background: rgba(255, 255, 255, 0.2);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }

    .card-icon {
      font-size: 80px;
      margin-bottom: 20px;
    }

    .card-title {
      font-size: 32px;
      font-weight: bold;
      margin-bottom: 15px;
    }

    .card-desc {
      font-size: 16px;
      opacity: 0.9;
      line-height: 1.6;
    }
  }
}
</style>

