<template>
  <div class="forbidden">
    <div class="forbidden-content">
      <h1>403</h1>
      <p>抱歉，您没有权限访问此页面</p>
      <el-button type="primary" @click="goBack">返回上一页</el-button>
      <el-button @click="goHome">返回首页</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.go(-1)
}

const goHome = () => {
  router.push('/dashboard')
}
</script>

<style scoped lang="scss">
.forbidden {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100vh;
  background-color: #f5f5f5;
}

.forbidden-content {
  text-align: center;

  h1 {
    font-size: 120px;
    margin: 0;
    color: #f56c6c;
  }

  p {
    font-size: 18px;
    color: #909399;
    margin: 20px 0 40px 0;
  }

  .el-button {
    margin: 0 10px;
  }
}
</style>

