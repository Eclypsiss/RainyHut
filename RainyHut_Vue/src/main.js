import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import ElementPlus from 'element-plus' //导入 ElementPlus 组件库的所有模块和功能
import 'element-plus/dist/index.css' //导入 ElementPlus 组件库所需的全局 CSS 样式
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import './theme-chalk.css'

import App from './App.vue'
import router from './router'

import axios from 'axios'

// 创建 Vue 应用
const app = createApp(App)

// 将 Axios 设置为全局属性
app.config.globalProperties.$http = axios;

// 使用 Pinia 和 Router
app.use(createPinia())
app.use(router)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
        app.component(key, component)
    }
app.use(ElementPlus)

// 挂载应用
app.mount('#app')