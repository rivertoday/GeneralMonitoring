<template>
  <div class="not-found-container">
    <div class="content">
      <h1>404</h1>
      <p>页面不存在</p>
      <button @click="goHome" class="home-button">返回首页</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/overview')
}
</script>

<style scoped lang="scss">
.not-found-container {
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;

  .content {
    text-align: center;

    h1 {
      font-size: 120px;
      margin: 0;
      font-weight: bold;
    }

    p {
      font-size: 24px;
      margin: 20px 0 40px;
    }

    .home-button {
      padding: 12px 32px;
      font-size: 16px;
      background: rgba(255, 255, 255, 0.2);
      border: 2px solid rgba(255, 255, 255, 0.3);
      border-radius: 8px;
      color: #fff;
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
      }
    }
  }
}
</style>

