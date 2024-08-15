import { createApp } from 'vue' // 导入 Vue 的 createApp 函数
import App from './App.vue' // 导入根组件 App
import naive from 'naive-ui' // 导入 Naive UI 组件库
import { setupAssets, setupScrollbarStyle } from './plugins' // 导入插件设置函数
import { setupStore } from './store' // 导入 Vuex 状态管理设置函数
import { setupRouter } from './router' // 导入 Vue Router 设置函数
import { setupI18n } from './locales' // 导入国际化设置函数

// 引导函数，用于初始化应用
async function bootstrap() {
    const app = createApp(App) // 创建 Vue 应用实例
    setupAssets() // 设置静态资源

    setupScrollbarStyle() // 设置滚动条样式

    setupStore(app) // 配置 Vuex 状态管理

    setupI18n(app) // 配置国际化

    await setupRouter(app) // 配置 Vue Router，并等待路由初始化完成

    app.use(naive) // 使用 Naive UI 组件库

    app.mount('#app') // 将应用挂载到 DOM 元素 #app 上
}

bootstrap() // 启动应用