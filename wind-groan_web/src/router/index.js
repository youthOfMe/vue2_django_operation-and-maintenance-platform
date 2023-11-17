import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/login',
        component:() => import('@/views/WelcomeVue')
    },
    {
        path: '/',
        redirect: '/login',
    },
    {
        path: '/home',
        component: () => import('@/views/HomeVue.vue'),
        redirect: '/welcome',
        children: [
            {
                path: '/welcome', component:() => import('@/views/WelcomeVue')
            },
            {
                path: '/users', component:() => import('@/views/user/UserView.vue')
            },
        ]
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
