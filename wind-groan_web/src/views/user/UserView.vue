<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>用户管理</el-breadcrumb-item>
            <el-breadcrumb-item>用户列表</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row :gutter="20">
                <el-col :span="18">
                    <el-input placeholder="请输入内容" v-model="username">
                        <!-- 在模板中会传入时间对象event -->
                        <el-button
                            slot="append"
                            icon="el-icon-search"
                            @click="getList(1)"
                        ></el-button>
                    </el-input>
                </el-col>
                <el-col :span="6">
                    <el-button type="primary" @click="addDialogVisible = true">添加用户</el-button>
                </el-col>
            </el-row>
            <el-table :data="dataList" style="width: 100%" :border="true" stripe>
                <el-table-column prop="id" label="用户ID"></el-table-column>
                <el-table-column prop="username" label="用户名"></el-table-column>
                <el-table-column prop="email" label="邮箱"></el-table-column>
                <el-table-column prop="phone" label="联系电话"></el-table-column>
                <el-table-column prop="is_active" label="是否激活">
                    <template #default="{ row }">
                        <el-switch
                            v-model="row.is_active"
                            active-color="#409EFF"
                            inactive-color="#ff4949"
                            @change="handleIsactiveChange(row.id, row.is_active)"
                        ></el-switch>
                    </template>
                </el-table-column>
                <el-table-column prop="is_superuser" label="是否为超管">
                    <template #default="{ row }">
                        <el-switch
                            v-model="row.is_superuser"
                            active-color="#409EFF"
                            inactive-color="#ff4949"
                        ></el-switch>
                    </template>
                </el-table-column>
                <el-table-column label="操作" fixed="right">
                    <template>
                        <el-button size="small" icon="el-icon-edit"></el-button>
                        <el-button type="danger" size="small" icon="el-icon-delete"></el-button>
                    </template>
                </el-table-column>
            </el-table>

            <el-pagination
                @current-change="getList"
                :current-page="pagination.page"
                :page-size="pagination.size"
                layout="total, prev, pager, next, jumper"
                :total="pagination.total"
            ></el-pagination>
        </el-card>
        <el-dialog
            title="创建肖学长"
            :visible.sync="addDialogVisible"
            width="50%"
            :before-close="handleClose"
        >
            <el-form
                :model="addForm"
                :rules="addRules"
                ref="add"
                labal-width="100px"
                class="demo-ruleForm"
            >
                <el-form-item label="用户名称" prop="username">
                    <el-input v-model="addForm.username"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="addForm.password"></el-input>
                </el-form-item>
                <el-form-item label="确认密码" prop="checkPass">
                    <el-input v-model="addForm.checkPass"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="addForm.email"></el-input>
                </el-form-item>
                <el-form-item label="联系电话" prop="phone">
                    <el-input v-model="addForm.phone"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button @click="resetForm()">重置</el-button>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="handleClose">取 消</el-button>
                <el-button type="primary" @click="addDialogVisible = false || add()">
                    确 定
                </el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
import { MessageBox } from 'element-ui'
export default {
    created() {
        this.getList ? this.getList() : ''
    },
    data() {
        var validatePass = (rule, value, callback) => {
            value !== this.addForm.password ? callback(new Error('两次密码输入不一致')) : callback()
        }

        return {
            // 搜索框绑定数据
            username: '',
            dataList: [
                {
                    date: '2016-05-02',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1518 弄',
                },
                {
                    date: '2016-05-04',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1517 弄',
                },
                {
                    date: '2016-05-01',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1519 弄',
                },
                {
                    date: '2016-05-03',
                    name: '王小虎',
                    address: '上海市普陀区金沙江路 1516 弄',
                },
            ],
            // 新增
            addDialogVisible: false,
            addForm: {
                username: '',
                password: '',
                checkPass: '',
                email: '',
                phone: '',
            },
            addRules: {
                username: [
                    { required: true, message: '请输入用户名称', trigger: 'blur' },
                    { min: 4, max: 16, message: '用户名长度在 4 到 16 个字符', trigger: 'blur' },
                ],
                password: [
                    { required: true, message: '请输入用户密码', trigger: 'blur' },
                    { min: 4, max: 16, message: '密码长度在 4 到 16 个字符', trigger: 'blur' },
                ],
                checkPass: [
                    { required: true, message: '请再次输入用户密码', trigger: 'blur' },
                    { min: 4, max: 16, message: '密码长度在 4 到 16 个字符', trigger: 'blur' },
                    { validator: validatePass, trigger: 'blur' },
                ],
            },

            // 分页的数据
            pagination: {
                total: 0,
                page: 1,
                size: 20,
            },
        }
    },
    methods: {
        // 重置表单数据
        resetForm() {
            this.$refs['add'].resetFields()
        },
        // 关闭输入框前提示
        handleClose() {
            MessageBox.alert('取消后会导致当前填写的数据消失', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            })
                .then(() => {
                    this.resetForm()
                    this.addDialogVisible = false
                    this.$message({
                        type: 'info',
                        message: '已取消',
                    })
                })
                .catch(() => {})
        },
        // 添加用户数据
        add() {
            this.$refs['add'].validate(async (valid, obj) => {
                console.log(valid, obj)
                if (valid) {
                    const { data: response } = await this.$http.post('users/', this.addForm)
                    if (response.code) return this.$message.error(response.message)
                }
                // 成功
                this.addDialogVisible = false
                // 拿回数据
                this.getList()
            })
        },
        // 获取用户列表数据
        async getList(page = 1) {
            if (typeof page !== 'number' || page <= 0) {
                page = 1
            }
            try {
                const { data: response } = await this.$http.get('users/', {
                    params: {
                        page,
                        // username: this.username,
                        search: this.username,
                    },
                })
                if (response.code) return this.$message.error(response.message)
                console.log(response)
                this.dataList = response.results
                this.pagination = response.pagination
            } catch (error) {
                this.$message({
                    type: 'error',
                    message: '用户未激活',
                })
            }
        },
        // 调整用户激活状态
        async handleIsactiveChange(id, is_active) {
            // 激活/禁用某一个具体的用户 最划算的方式是提交一个值 要通过序列化器的校验就必须使用patch
            console.log(id, is_active)
            const { data: response } = await this.$http.patch(`users/${id}/`, {
                is_active,
            })
            if (response.code) return this.$message.error(response.message)
            this.getList(this.pagination.page)
        },
        async handleSearch(page = 1) {},
    },
}
</script>

<style lang="scss" scoped></style>
