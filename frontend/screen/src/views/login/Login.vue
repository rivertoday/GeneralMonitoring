<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>风险监测预警系统</h2>
        <p>Risk Monitoring and Early Warning System</p>
        <p class="subtitle">大屏展示系统</p>
      </div>

      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-item">
          <input
            v-model="loginForm.username"
            type="text"
            placeholder="请输入用户名"
            class="form-input"
            required
          />
        </div>

        <div class="form-item">
          <input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            class="form-input"
            required
            @keyup.enter="handleLogin"
          />
        </div>

        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div class="form-item">
          <button
            type="submit"
            class="login-button"
            :disabled="loading"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/store/modules/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const loading = ref(false)
const errorMessage = ref('')

const loginForm = reactive({
  username: '',
  password: '',
})

// 登录处理
const handleLogin = async () => {
  if (!loginForm.username || !loginForm.password) {
    errorMessage.value = '请输入用户名和密码'
    return
  }

  if (loginForm.password.length < 6) {
    errorMessage.value = '密码长度不能少于6位'
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    await authStore.login(loginForm)
    
    // 跳转到重定向页面或首页
    const redirect = (route.query.redirect as string) || '/overview'
    router.push(redirect)
  } catch (error: any) {
    errorMessage.value = error.message || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
}

.login-box {
  width: 420px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;

  h2 {
    margin: 0 0 10px 0;
    font-size: 28px;
    font-weight: 600;
    color: #303133;
  }

  p {
    margin: 5px 0;
    font-size: 14px;
    color: #909399;
  }

  .subtitle {
    font-size: 16px;
    color: #409eff;
    font-weight: 500;
  }
}

.login-form {
  .form-item {
    margin-bottom: 20px;
  }

  .form-input {
    width: 100%;
    padding: 12px 16px;
    font-size: 14px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    outline: none;
    transition: border-color 0.3s;

    &:focus {
      border-color: #409eff;
    }

    &::placeholder {
      color: #c0c4cc;
    }
  }

  .error-message {
    margin-bottom: 15px;
    padding: 10px;
    background-color: #fef0f0;
    color: #f56c6c;
    border-radius: 4px;
    font-size: 14px;
  }

  .login-button {
    width: 100%;
    padding: 12px;
    font-size: 16px;
    color: #fff;
    background-color: #409eff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s;

    &:hover:not(:disabled) {
      background-color: #66b1ff;
    }

    &:disabled {
      background-color: #a0cfff;
      cursor: not-allowed;
    }
  }
}
</style>

