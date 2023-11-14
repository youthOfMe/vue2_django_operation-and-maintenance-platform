import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/LoginVue'
import Welcome from '@/views/WelcomeVue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/login',
        component: Login,
    },
    {
        path: '/',
        redirect: '/login',
    },
    {
        path: '/welcome',
        component: Welcome,
    },
]

const router = new VueRouter({
    routes,
})

export default router
