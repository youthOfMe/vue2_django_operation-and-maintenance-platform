import Vue from 'vue'
import App from './App.vue' // 引入组件
import router from './router' // 静态路由
import './plugins/element.js' // 按需导入文件 不需要就不要了
import '@/assets/css/main.css'
import axios from 'axios'

Vue.prototype.$http = axios
axios.defaults.baseURL = 'https://api.example.com' // 默认值 默认的url头

Vue.config.productionTip = false

// 这是vue脚手架产生文件的入口
new Vue({
    router, // 静态路由 前端路由
    render: (h) => h(App), // APP就是根组件
}).$mount('#app') // 将vue组件挂载到id为APP的标签上
