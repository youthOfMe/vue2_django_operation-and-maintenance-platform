<template>
    <div class="login_container">
        <div class="login_box">
            <div class="avatar_box">
                <img src="../assets/logo.png" alt="logo" />
            </div>
            <el-form
                class="login_form"
                :model="loginForm"
                :rules="loginRules"
                ref="loginFormRef"
            >
                <el-form-item label="用户名" prop="username">
                    <el-input
                        ref="inputUsername"
                        v-model="loginForm.username"
                        placeholder="请输入用户名"
                        prefix-icon="el-icon-user"
                        @keyup.enter.native="jump"
                    ></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input
                        ref="inputPassword"
                        @keyup.enter.native="login"
                        v-model="loginForm.password"
                        placeholder="请输入密码"
                        type="password"
                        prefix-icon="el-icon-lock"
                    ></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button
                        type="primary"
                        @click="login()"
                        icon="el-icon-user"
                    >
                        登录
                    </el-button>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="resetForm">
                        联系小王同学
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
import { Message } from 'element-ui'
export default {
    // data () { retun { xxx:yyy } }
    data() {
        return {
            // 提交数据
            loginForm: {
                username: '',
                password: '',
            },
            // 验证规则
            loginRules: {
                username: [
                    {
                        required: true,
                        message: '用户名必须进行填写',
                        trigger: 'blur',
                    },
                    {
                        min: 3,
                        max: 18,
                        message: '用户名长度在3到18个字符',
                        trigger: 'blur',
                    },
                ],
                password: [
                    {
                        required: true,
                        message: '用户密码必须进行填写',
                        trigger: 'blur',
                    },
                    {
                        min: 4,
                        max: 18,
                        message: '用户名长度在4到18个字符',
                        trigger: 'blur',
                    },
                ],
            },
        }
    },
    methods: {
        // 重置表单
        resetForm() {
            this.$refs.loginFormRef.resetFields()
        },
        login() {
            console.log('Niubi')
            // 发送数据到后台去, 要进行指定数据校验
            this.$refs.loginFormRef.validate(async (valid, obj) => {
                console.log(valid) // 返回布尔值 表示成功与否
                console.log(obj) // 失败是返回失败规则
                if (valid) {
                    // 成功是怎么办 将数据发送到后端
                    // 在这里this指向vue组件
                    // this.$http.get() // axios
                    const response = await this.$http
                        .post('', this.loginForm)
                        .then()
                        .catch() // axios.post返回一个promise
                    console.log(response, '______________')
                } else {
                    // 报错
                    let err = ''
                    err += obj.username[0].message
                    err += ', ' + obj.password[0].message
                    Message({
                        message: err,
                        type: 'error',
                    })
                }
            })
        },
        jump() {
            this.$refs.inputPassword.focus()
        },
    },
}
</script>

<style lang="less" scoped>
button {
    width: 100%;
}
.login_container {
    background-color: #2b4b6b;
    height: 100%;
}
.login_box {
    width: 450px;
    height: 380px;
    background-color: #fff;
    border-radius: 5px;
    position: absolute;
    // position: relative;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);

    .avatar_box {
        height: 130px;
        width: 130px;
        padding: 10px;
        position: absolute;
        left: 50%;
        transform: translate(-50%, -50%);
        img {
            width: 100%;
            height: 100%;
            border-radius: 35%;
        }
    }

    .login_form {
        position: absolute;
        bottom: 0;
        width: 100%;
        padding: 0 20px;
        box-sizing: border-box;
    }
}
</style>
