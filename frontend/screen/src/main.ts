import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './styles/screen.scss'
import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

// 注册Pinia和路由
app.use(pinia)
app.use(router)

// 在Pinia注册之后设置路由守卫
import { setupRouterGuard } from './router/guards'
setupRouterGuard(router)

app.mount('#app')
