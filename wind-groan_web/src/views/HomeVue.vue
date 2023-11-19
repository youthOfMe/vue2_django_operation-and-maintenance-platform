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
                <el-dropdown @command="handleCommand">
                    <span class="el-dropdown-link">
                        {{ user.username }}
                        <i class="el-icon-arrow-down el-icon--right"></i>
                    </span>
                    <el-dropdown-menu slot="dropdown">
                        <el-dropdown-item icon="el-icon-check" command="chpwd">
                            修改密码
                        </el-dropdown-item>
                        <el-dropdown-item icon="el-icon-circle-check" divided command="logout">
                            退出
                        </el-dropdown-item>
                    </el-dropdown-menu>
                </el-dropdown>
            </div>
            <!-- 修改密码 -->
            <el-dialog
                :title="`修改${user.username}密码`"
                :visible.sync="chpwDialogVisible"
                width="50%"
                :before-close="chpwHandleClose"
            >
                <el-form
                    :model="chpwForm"
                    :rules="chpwRules"
                    ref="chpw"
                    labal-width="100px"
                    class="demo-ruleForm"
                >
                    <el-form-item label="原始密码" prop="oldPassword">
                        <el-input type="password" v-model="chpwForm.oldPassword"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input type="password" v-model="chpwForm.password"></el-input>
                    </el-form-item>
                    <el-form-item label="确认密码" prop="checkPass">
                        <el-input v-model="chpwForm.checkPass"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button @click="resetForm()">重置</el-button>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="chpwHandleClose">取 消</el-button>
                    <el-button type="primary" @click="chpwDialogVisible = false || edit()">
                        确 定
                    </el-button>
                </span>
            </el-dialog>
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
        <el-footer>Footer</el-footer>
    </el-container>
</template>

<script>
export default {
    created() {
        // 生命周期钩子函数 该组件js内存中的实例对象被创建出来
        this.getMenuList()
        this.getUserInfo()
    },
    data() {
        const validatePass = (rule, value, callback) => {
            value !== this.addForm.password ? callback(new Error('两次密码输入不一致')) : callback()
        }

        return {
            // 导航栏数据
            menuList: [],
            isCollapse: false,
            // 显示用户
            user: {},
            // 修改密码
            chpwDialogVisible: false,
            chpwForm: {
                oldPassword: '',
                password: '',
                checkPass: '',
            },
            chpwRules: {
                oldPassword: [
                    { required: true, message: '请输入用户密码', trigger: 'blur' },
                    { min: 4, max: 16, message: '密码长度在 4 到 16 个字符', trigger: 'blur' },
                ],
                password: [
                    { required: true, message: '请输入用户新密码', trigger: 'blur' },
                    { min: 4, max: 16, message: '密码长度在 4 到 16 个字符', trigger: 'blur' },
                ],
                checkPass: [
                    { required: true, message: '请再次输入用户新密码', trigger: 'blur' },
                    { min: 4, max: 16, message: '密码长度在 4 到 16 个字符', trigger: 'blur' },
                    { validator: validatePass, trigger: 'blur' },
                ],
            },
        }
    },
    methods: {
        // 重置表单数据
        resetForm(name) {
            this.$refs[name].resetFields()
        },
        // 退出登录
        logout() {
            window.localStorage.removeItem('token') || this.$router.push('/login')
        },
        // 获取导航栏数据
        async getMenuList() {
            const { data: response } = await this.$http.get('/users/menulist/')
            this.menuList = response
        },
        // 获取用户信息
        async getUserInfo() {
            const { data: response } = await this.$http.get('users/whoami/')
            if (response.code) return this.$message.error(response.message)
            this.user = response
        },
        // 下拉菜单
        handleCommand(command) {
            console.log(command, typeof command)
            if (command === 'logout') this.logout()
            if (command === 'chpwd') this.chpwDialogVisible = true
        },
        // 修改密码
        chpw() {},
        // 关闭输入框前提示
        chpwHandleClose() {
            this.$msgbox
                .alert('取消后会导致当前填写的数据消失', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                })
                .then(() => {
                    this.resetForm('chpw')
                    this.chpwDialogVisible = false
                    this.$message({
                        type: 'info',
                        message: '已取消',
                    })
                })
                .catch(() => {})
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
.el-dropdown {
    cursor: pointer;
}
</style>
