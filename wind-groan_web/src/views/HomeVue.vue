<template>
    <el-container>
        <el-header>
            <div class="logo">
                <img src="../assets/logo.png" alt="logo" />
                <div class="title">风吟运维管理平台</div>
                <i
                    :class="isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'"
                    @click="isCollapse = !isCollapse"
                ></i>
            </div>
            <div class="info">
                <el-button type="primary" @click="logout">退出</el-button>
            </div>
        </el-header>
        <el-container>
            <el-aside :width="isCollapse ? '64px' : '200px'">
                <el-menu
                    router
                    class="el-menu-vertical-demo"
                    background-color="#ffffff"
                    text-color="#123"
                    active-text-color="#ffd04b"
                    :collapse="isCollapse"
                >
                    <template v-for="item in menuList">
                        <template v-if="item.children.length">
                            <el-submenu :index="item.id + ''" :key="item.id">
                                <template slot="title">
                                    <i class="el-icon-location"></i>
                                    <span>{{ item.name }}</span>
                                </template>
                                <el-menu-item
                                    :index="sub.path"
                                    v-for="sub in item.children"
                                    :key="sub.id"
                                >
                                    {{ sub.name }}
                                </el-menu-item>
                            </el-submenu>
                        </template>
                        <template v-else>
                            <el-menu-item :index="item.path" :key="item.id">
                                <i class="el-icon-s-home"></i>
                                <span slot="title">{{ item.name }}</span>
                            </el-menu-item>
                        </template>
                    </template>
                    <el-menu-item index="2">
                        <i class="el-icon-menu"></i>
                        <span slot="title">导航二</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main>
                <router-view></router-view>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
export default {
    created() {
        // 生命周期钩子函数 该组件js内存中的实例对象被创建出来
        this.getMenuList()
    },
    data() {
        return {
            menuList: [
                // { id: 1, name: 'test1', children: [
                //     { id: 101, name: 'test101' },
                //     { id: 102, name: 'test102' },
                // ] },
                // { id: 2, name: 'test2', children: [] }
            ],
            isCollapse: false,
        }
    },
    methods: {
        logout() {
            window.localStorage.removeItem('token') || this.$router.push('/login')
        },
        async getMenuList() {
            const { data: response } = await this.$http.get('/users/menulist/')
            this.menuList = response
        },
    },
}
</script>

<style lang="less" scoped>
.el-container {
    height: 100%;
}
.el-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: #dddddd 0 5px 10px 5px;
    .logo {
        display: flex;
        align-items: center;
        img {
            height: 40px;
        }
        .title {
            font-size: 24px;
            margin-left: 5px;
        }
        i {
            font-size: 30px;
            margin-left: 5px;
        }
    }
}
.el-aside {
    background-color: #ffffff;
    margin-top: 2px;
}
.el-main {
    margin-top: 2px;
    background-color: #f0f2f4;
}
.el-menu {
    border-right: none;
}
</style>
