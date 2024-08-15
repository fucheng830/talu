import path from 'path'
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from 'tailwindcss'
import autoprefixer from 'autoprefixer'

// https://vitejs.dev/config/
export default defineConfig(env => {
  // 加载环境变量
  const viteEnv = loadEnv(env.mode, process.cwd()) as unknown as ImportMetaEnv

  return {
    // 插件配置
    plugins: [vue()],
    // 模块解析配置
    resolve: {
      alias: {
        '@': path.resolve(process.cwd(), 'src'), // 路径别名，将 @ 映射到 src 目录
      },
    },
    // CSS 配置
    css: {
      postcss: {
        plugins: [tailwindcss, autoprefixer] // 使用 Tailwind CSS 和 Autoprefixer
      }
    },
    // 服务器配置
    server: {
      host: '0.0.0.0', // 监听所有网络接口
      port: 5173, // 端口号
      open: false, // 启动时不自动打开浏览器
      proxy: {
        '/api': {
          target: viteEnv.VITE_APP_API_BASE_URL, // 目标 API 基础 URL
          changeOrigin: true, // 允许跨域
          rewrite: (path) => path.replace(/^\/api/, '/'), // 重写路径，去掉 /api 前缀
        },
      },
    },
  }
})