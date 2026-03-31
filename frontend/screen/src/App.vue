<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'

const route = useRoute()

// 使用路由路径作为key，确保路由变化时组件重新渲染
const routeKey = computed(() => route.fullPath)
</script>

<template>
  <RouterView :key="routeKey" />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
</style>
