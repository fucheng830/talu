import { createApp } from 'vue'
import App from './App.vue'
import naive from 'naive-ui'
import { setupAssets, setupScrollbarStyle } from './plugins'
import { setupStore } from './store'
import { setupRouter } from './router'
import { setupI18n } from './locales';

async function bootstrap() {
    const app = createApp(App)
    setupAssets()

    setupScrollbarStyle()

    setupStore(app)

    setupI18n(app) // 配置国际化

    await setupRouter(app)

    app.use(naive)

    app.mount('#app')
}

bootstrap()