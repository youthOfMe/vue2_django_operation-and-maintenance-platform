<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>用户管理</el-breadcrumb-item>
            <el-breadcrumb-item>角色列表</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row :gutter="20">
                <el-col :span="18">
                    <el-input placeholder="请输入内容" v-model="name">
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
                <el-table-column type="index"></el-table-column>
                <el-table-column prop="id" label="用户ID"></el-table-column>
                <el-table-column prop="name" label="名称"></el-table-column>
                <el-table-column label="操作" fixed="right">
                    <template #default="{ row }">
                        <el-tooltip content="编辑" placement="bottom" effect="light">
                            <el-button size="small" icon="el-icon-edit"></el-button>
                        </el-tooltip>
                        <el-tooltip content="分配权限" placement="bottom" effect="light">
                            <el-button
                                size="small"
                                icon="el-icon-suitcase"
                                @click="handleSetPerm(row)"
                            ></el-button>
                        </el-tooltip>
                        <el-tooltip content="删除" placement="bottom" effect="light">
                            <el-button type="danger" size="small" icon="el-icon-delete"></el-button>
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
            title="新增角色"
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
                <el-form-item label="权限组名称" prop="name">
                    <el-input v-model="addForm.name"></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button @click="resetForm()">重置</el-button>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addHandleClose">取 消</el-button>
                <el-button type="primary" @click="addDialogVisible = false || add()">
                    确 定
                </el-button>
            </span>
        </el-dialog>
        <!-- 分配权限 -->
        <el-dialog
            :title="`[${currentRole.name}]分配权限`"
            :visible.sync="addPermDialogVisible"
            width="50%"
            :before-close="addPermHandleClose"
        >
            <el-tree
                :data="permList"
                :props="defaultProps"
                show-checkbox
                ref="tree"
                node-key="id"
                default-expand-all
                :default-checked-keys="selectedIds"
            ></el-tree>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addPermHandleClose">取 消</el-button>
                <el-button type="primary" @click="addPerm()">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
export default {
    created() {
        this.getList()
    },
    data() {
        return {
            name: '',
            serach: '',
            // 数据显示
            dataList: [],
            pagination: { total: 0, page: 1, size: 20 },
            loading: false,
            // 新增
            addDialogVisible: false,
            addForm: {
                name: '',
            },
            addRules: {
                name: [
                    { required: true, message: '请输入权限组名称', trigger: 'blur' },
                    { min: 4, max: 16, message: '用户名长度在 2 到 16 个字符', trigger: 'blur' },
                ],
            },
            // 分配权限
            addPermDialogVisible: false, // 放一个对象{} 下一级需要使用children label是说对象的什么属性显示节点文字
            permList: [
                { id: 100, name: 'node1' },
                { id: 101, name: 'node2' },
                { id: 102, name: 'node3' },
            ],
            defaultProps: {
                children: 'children',
                label: 'name',
            },
            currentRole: '',
            selectedIds: [],
        }
    },
    methods: {
        // 获取用户列表数据
        async getList(page = 1) {
            this.loading = true
            if (typeof page !== 'number' || page <= 0) {
                page = 1
            }
            try {
                const { data: response } = await this.$http.get('users/roles/', {
                    params: {
                        page,
                        // username: this.username,
                        search: this.username,
                    },
                })
                if (response.code) return this.$message.error(response.message)
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
        // 关闭输入框前提示
        addHandleClose() {
            this.$msgbox
                .alert('取消后会导致当前填写的数据消失', '提示', {
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
        // 添加用户数据
        add() {
            this.$refs['add'].validate(async (valid, obj) => {
                console.log(valid, obj)
                if (valid) {
                    const { data: response } = await this.$http.post('users/mgr/', this.addForm)
                    if (response.code) return this.$message.error(response.message)
                }
                // 成功
                this.addDialogVisible = false
                // 拿回数据
                this.getList()
            })
        },
        // 分配用户
        async handleSetPerm(row) {
            const { id } = row
            const { data: response } = await this.$http.get(`users/roles/${id}/perms/`)
            if (response.code) return this.$message.error(response.message)
            this.permList = response.allPerms
            this.selectedIds = response.permissions
            this.addPermDialogVisible = true
            this.currentRole = row
        },
        // 提交添加权限
        async addPerm() {
            const name = 'tree'
            const selectedIds = this.$refs[name].getCheckedKeys()
            const { id } = this.currentRole
            // 将权限的Id数据传到服务端就可以进行设置权限
            await this.$http.patch(`users/roles/${id}/`, {
                permissions: selectedIds,
            })
            this.addPermDialogVisible = false
            this.$message.success(`${this.currentRole.name}修改权限成功`)
        },
        // 关闭输入框前提示
        addPermHandleClose() {
            this.$msgbox
                .alert('取消后会导致当前填写的数据消失', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                })
                .then(() => {
                    // console.log(666)
                    // this.resetForm('add')
                    this.addPermDialogVisible = false
                    this.$message({
                        type: 'info',
                        message: '已取消',
                    })
                })
                .catch(() => {})
        },
        // 重置数据
        resetTree() {
            this.currentRole = {}
            this.selectedIds = []
            this.permList = []
        },
    },
}
</script>

<style lang="scss" scoped></style>
