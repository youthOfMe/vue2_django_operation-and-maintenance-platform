import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/login',
        component: () => import('@/views/LoginVue'),
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
                path: '/welcome',
                component: () => import('@/views/WelcomeVue'),
            },
            {
                path: '/users',
                component: () => import('@/views/user/UserView.vue'),
            },
            {
                path: '/users/perms',
                component: () => import('@/views/user/PermView.vue'),
            },
            {
                path: '/users/roles',
                component: () => import('@/views/user/RoleView.vue'),
            },
        ],
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

// 获取原型对象push函数
const originalPush = VueRouter.prototype.push

// 获取原型对象replace函数
const originalReplace = VueRouter.prototype.replace

// 修改原型对象中的push函数
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch((err) => err)
}

// 修改原型对象中的replace函数
VueRouter.prototype.replace = function replace(location) {
    return originalReplace.call(this, location).catch((err) => err)
}

export default router
