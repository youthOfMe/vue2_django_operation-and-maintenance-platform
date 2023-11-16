import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '@/views/LoginVue'
import Welcome from '@/views/WelcomeVue'
import Home from '@/views/HomeVue.vue'

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
    {
        path: '/home',
        component: Home,
    },
]

const router = new VueRouter({
    routes,
})

router.beforeEach((to, from, next) => {
    to.path === '/login'
        ? next()
        : (() => {
              const token = window.localStorage.getItem('token')
              token ? next() : next('/login')
          })()
})

export default router
