<template>
  <div class="screen-overview">
    <h1>大屏总览</h1>
    <div class="screen-cards">
      <el-card class="screen-card" @click="goToScreen('safety-run')">
        <h3>安全运行一张图</h3>
        <p>展示安全基础数据信息、辖区基础情况、救援队伍、应急专家、物资装备等</p>
      </el-card>
      <el-card class="screen-card" @click="goToScreen('safety-status')">
        <h3>安全态势一张图</h3>
        <p>展示行业态势、区域态势、四色风险图等</p>
      </el-card>
      <el-card class="screen-card" @click="goToScreen('monitor-warn')">
        <h3>监测预警一张图</h3>
        <p>展示实时监测数据、预警事件信息、视频监控设施等</p>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goToScreen = (type: string) => {
  // TODO: 跳转到对应的大屏页面
  // 这里暂时只是提示，后续会创建大屏项目
  alert(`跳转到${type}大屏（大屏项目待创建）`)
}
</script>

<style scoped lang="scss">
.screen-overview {
  padding: 20px;
}

.screen-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 20px;
}

.screen-card {
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  h3 {
    margin: 0 0 10px 0;
    color: #303133;
  }

  p {
    margin: 0;
    color: #909399;
    font-size: 14px;
  }
}
</style>

