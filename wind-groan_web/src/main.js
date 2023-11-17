import Vue from 'vue'
import App from './App.vue' // 引入组件
import router from './router' // 静态路由
import './plugins/element.js' // 按需导入文件 不需要就不要了
import '@/assets/css/main.css'
import axios from 'axios'

Vue.prototype.$http = axios

// 添加请求拦截器
axios.interceptors.request.use((config) => {
    config.headers['Authorization'] = 'Bearer' + ' ' + window.localStorage.getItem('token')
    return config
}, (err) => {
    return Promise.reject(err)
})

// 添加响应拦截器
axios.interceptors.response.use((response) => {
    if(response.data && response.data.code < 100) return router.push('/login')
    return response
 })

// 请求代理
// axios.defaults.baseURL = 'http://127.0.0.1:8080/api/v1/' // 默认值 默认的url头 默认drf会进行 api的处理 接口都会使用这种路径
// 同域无需写服务器地址+端口号
axios.defaults.baseURL = '/api/v1/'

Vue.config.productionTip = false

// 这是vue脚手架产生文件的入口
new Vue({
    router, // 静态路由 前端路由
    render: (h) => h(App), // APP就是根组件
}).$mount('#app') // 将vue组件挂载到id为APP的标签上
