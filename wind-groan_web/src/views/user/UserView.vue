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
            <el-table
                :data="dataList"
                style="width: 100%"
                :border="true"
                stripe
                v-loading="loading"
                element-loading-text="拼命加载中"
                element-loading-spinner="el-icon-loading"
                element-loading-background="rgba(0, 0, 0, 0.8)"
            >
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
                    <template #default="{ row }">
                        <el-tooltip content="编辑" placement="bottom" effect="light">
                            <el-button
                                size="small"
                                icon="el-icon-edit"
                                @click="handleEdit(row)"
                            ></el-button>
                        </el-tooltip>
                        <el-tooltip content="分配权限" placement="bottom" effect="light">
                            <el-button
                                size="small"
                                icon="el-icon-suitcase"
                                @click="handleAuthorRole(row)"
                            ></el-button>
                        </el-tooltip>
                        <el-tooltip content="删除" placement="bottom" effect="light">
                            <el-button
                                type="danger"
                                size="small"
                                icon="el-icon-delete"
                                @click="handleDelete(row.id)"
                            ></el-button>
                        </el-tooltip>
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
        <!-- 增加用户 -->
        <el-dialog
            title="创建肖学长"
            :visible.sync="addDialogVisible"
            width="50%"
            :before-close="addHandleClose"
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
                <el-button @click="addHandleClose">取 消</el-button>
                <el-button type="primary" @click="add()">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 修改用户 -->
        <el-dialog
            title="修改肖学长"
            :visible.sync="editDialogVisible"
            width="50%"
            :before-close="editHandleClose"
        >
            <el-form
                :model="editForm"
                :rules="editRules"
                ref="edit"
                labal-width="100px"
                class="demo-ruleForm"
            >
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="editForm.email"></el-input>
                </el-form-item>
                <el-form-item label="联系电话" prop="phone">
                    <el-input v-model="editForm.phone"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button @click="resetForm()">重置</el-button>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editHandleClose">取 消</el-button>
                <el-button type="primary" @click="edit()">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 分配角色 -->
        <el-dialog
            :title="`[${currentUser}]分配角色`"
            :visible.sync="addRoleDialogVisible"
            width="50%"
            :before-close="addRoleHandleClose"
        >
            <el-tree
                :data="roleList"
                :props="{ label: 'name' }"
                show-checkbox
                ref="tree"
                node-key="id"
                default-expand-all
                :default-checked-keys="selectedIds"
            ></el-tree>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addRoleHandleClose">取 消</el-button>
                <el-button type="primary" @click="addRole()">确 定</el-button>
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
        const validatePass = (rule, value, callback) => {
            value !== this.addForm.password ? callback(new Error('两次密码输入不一致')) : callback()
        }

        return {
            // 数据加载
            loading: false,
            // 搜索框绑定数据
            username: '',
            dataList: [],
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
            // 编辑
            editDialogVisible: false,
            editForm: {
                id: '',
                email: '',
                phone: '',
            },
            editRules: {
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
            // 分配角色
            addRoleDialogVisible: false,
            roleList: [],
            currentUser: {},
            selectedIds: [],
        }
    },
    methods: {
        // 重置表单数据
        resetForm(name) {
            this.$refs[name].resetFields()
        },
        // 关闭输入框前提示
        addHandleClose() {
            MessageBox.alert('取消后会导致当前填写的数据消失', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            })
                .then(() => {
                    this.resetForm('add')
                    this.addDialogVisible = false
                    this.$message({
                        type: 'info',
                        message: '已取消',
                    })
                })
                .catch(() => {})
        },
        // 关闭输入框前提示
        editHandleClose() {
            MessageBox.alert('取消后会导致当前填写的数据消失', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            })
                .then(() => {
                    this.resetForm('edit')
                    this.editDialogVisible = false
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
                    const { data: response } = await this.$http.post('users/mgr/', this.addForm)
                    if (response.code) return this.$message.error(response.message)
                    // 成功
                    this.addDialogVisible = false
                    // 拿回数据
                    this.getList()
                }
            })
        },
        // 编辑用户数据
        handleEdit(row) {
            console.log(row)
            const { id, username, email, phone } = row
            this.editForm = { id, username, email, phone }
            this.editDialogVisible = true
        },
        edit() {
            const { id } = this.editForm
            this.$refs['edit'].validate(async (valid) => {
                if (valid) {
                    const { data: response } = await this.$http.patch(
                        `users/mgr/${id}/chpw`,
                        this.editForm,
                    )
                    if (response.code) return this.$message.error(response.message)
                    this.editDialogVisible = false
                    this.getList(this.pagination.page)
                }
            })
        },
        // 获取用户列表数据
        async getList(page = 1) {
            this.loading = true
            if (typeof page !== 'number' || page <= 0) {
                page = 1
            }
            try {
                const { data: response } = await this.$http.get('users/mgr/', {
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
            } finally {
                this.loading = false
            }
        },
        // 调整用户激活状态
        async handleIsactiveChange(id, is_active) {
            // 激活/禁用某一个具体的用户 最划算的方式是提交一个值 要通过序列化器的校验就必须使用patch
            console.log(id, is_active)
            const { data: response } = await this.$http.patch(`users/mgr/${id}/`, {
                is_active,
            })
            if (response.code) return this.$message.error(response.message)
            this.getList(this.pagination.page)
        },
        // 删除用户数据
        handleDelete(id) {
            this.$confirm('此操作将永久删除该用户, 是否继续', '警告', {
                distinguishCancelAndClose: true,
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'error',
            })
                .then(async () => {
                    const { data: response } = await this.$http.delete(`users/mgr/${id}/`)
                    if (response.code) return this.$message.error(response.message)
                    this.getList(this.pagination.page)
                    this.$message({
                        type: 'success',
                        message: '删除成功',
                    })
                })
                .catch((action) => {
                    console.log(action)
                    this.$message({
                        type: 'error',
                        message: action,
                    })
                })
        },
        // 清空表单
        resetTree() {
            this.roleList = []
            this.selectedIds = []
            this.currentUser = []
        },
        // 进行分配权限
        async handleAuthorRole(row) {
            const { id } = row
            const { data: response } = await this.$http.get(`users/mgr/${id}/roles/`)
            if (response.code) return this.$message.error(response.message)
            console.log(response)
            this.roleList = response.allRoles
            this.selectedIds = response.roles
            this.currentUser = row
            this.addRoleDialogVisible = true
        },
        async addRole() {
            const name = 'tree'
            const { id } = this.currentUser
            const roles = this.$refs[name].getCheckedKeys()
            const { data: response } = await this.$http.put(`users/mgr/${id}/roles/`, {
                roles,
            })
            if (response.code) return this.$message.error(response.message)
            this.addRoleDialogVisible = false
            this.$message.success(`${this.currentUser.username}权限修改成功`)
        },
        // 关闭输入框前提示
        addRoleHandleClose() {
            this.$msgbox
                .alert('取消后会导致当前填写的数据消失', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                })
                .then(() => {
                    // console.log(666)
                    // this.resetForm('add')
                    this.addRoleDialogVisible = false
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

<style lang="scss" scoped></style>
