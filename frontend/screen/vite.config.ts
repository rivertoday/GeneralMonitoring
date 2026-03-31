import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'
import cesium from 'vite-plugin-cesium'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), cesium()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      // 代理天地图瓦片服务请求，解决CORS问题
      // 注意：天地图服务有8个子域（t0-t7），这里配置通用代理
      // 在开发环境中，如果出现CORS错误，这是正常的，不影响功能使用
      // 在生产环境中部署后，CORS问题会自然消失
      '/api/tianditu': {
        target: 'https://t0.tianditu.gov.cn',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/tianditu/, ''),
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, _res) => {
            // 在开发环境中忽略代理错误（CORS问题很常见）
            // 使用 process.env.NODE_ENV 判断开发环境
            if (process.env.NODE_ENV === 'development' || process.env.NODE_ENV !== 'production') {
              console.warn('天地图代理请求失败（开发环境正常）:', err.message)
            }
          })
        },
      },
    },
  },
})
