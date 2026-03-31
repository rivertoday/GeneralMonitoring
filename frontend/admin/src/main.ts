import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './style.css'
import App from './App.vue'
import router from './router'
import pinia from './store'
import { useAppStore } from './store/modules/app'
import permissionDirective from './directives/permission'

const app = createApp(App)

// 注册Element Plus
app.use(ElementPlus)

// 注册Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 注册权限指令
app.directive('permission', permissionDirective)

// 注册路由
app.use(router)

// 注册状态管理
app.use(pinia)

// 初始化应用状态
const appStore = useAppStore()
appStore.initScreenSize()

app.mount('#app')
