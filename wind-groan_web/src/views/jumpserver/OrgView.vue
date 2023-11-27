<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>堡垒机</el-breadcrumb-item>
            <el-breadcrumb-item>资产管理</el-breadcrumb-item>
        </el-breadcrumb>
        <!-- 组织树 -->
        <el-tree
            :data="dataList"
            show-checkbox
            node-key="id"
            default-expand-all
            :expand-on-click-node="false"
            :props="defaultProps"
        >
            <span class="custom-tree-node" slot-scope="{ node, data }">
                <span>{{ node.label }}</span>
                <span>
                    <el-button type="text" size="mini" @click="() => append(data)">
                        Append
                    </el-button>
                    <el-button type="text" size="mini" @click="() => remove(node, data)">
                        Delete
                    </el-button>
                    <el-dropdown @command="handleCommand">
                        <span class="el-dropdown-link">
                            <i class="el-icon-setting el-icon--right"></i>
                            操作
                        </span>
                        <el-dropdown-menu slot="dropdown">
                            <el-dropdown-item :command="['add_group', node, data]">
                                增加子分组
                            </el-dropdown-item>
                            <el-dropdown-item :command="['delete', node, data]">
                                删除分组及其子分组
                            </el-dropdown-item>
                            <el-dropdown-item :command="['add_server', node, data]">
                                增加主机
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </span>
            </span>
        </el-tree>
        <!-- 增加用户 -->
        <el-dialog
            :title="`${addForm.groupname}新增子分组`"
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
                <el-form-item label="分组名称" prop="name">
                    <el-input v-model="addForm.name"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addHandleClose">取 消</el-button>
                <el-button type="primary" @click="add()">确 定</el-button>
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
        const validatePass = (rule, value, callback) => {
            value !== this.addForm.password ? callback(new Error('两次密码输入不一致')) : callback()
        }

        return {
            serach: '',
            // 数据显示
            dataList: [],
            loading: false,
            defaultProps: {
                label: 'name',
            },
            // 新增
            addDialogVisible: false,
            addForm: {
                groupname: '', // 父级
                name: '', // 本名
            },
            addRules: {
                name: [
                    { required: true, message: '请输入分组名称', trigger: 'blur' },
                    { min: 1, max: 16, message: '用户名长度在 4 到 16 个字符', trigger: 'blur' },
                ],
            },
        }
    },
    methods: {
        // 重置表单数据
        resetForm(name) {
            this.$refs[name].resetFields()
        },
        // 获取用户列表数据
        async getList(page = 1) {
            this.loading = true
            if (typeof page !== 'number' || page <= 0) {
                page = 1
            }
            try {
                const { data: response } = await this.$http.get('jumpserver/orgs/tree/', {
                    params: {
                        page,
                        // username: this.username,
                        search: this.serach,
                    },
                })
                // console.log(response)
                if (response.code) return this.$message.error(response.message)
                const vroot = { name: '组织树', parent: null, children: null, id: null }
                vroot.children = response.results
                this.dataList = [vroot]
            } catch (error) {
                this.$message({
                    type: 'error',
                    message: '用户未激活',
                })
            } finally {
                this.loading = false
            }
        },
        // 操作功能
        handleCommand(command) {
            console.log(command)
            // node.data = data
            const [type, node, data] = command
            console.log(type)
            if (type === 'add_group') {
                this.addDialogVisible = true
                this.addForm.groupname = data.name
                this.addForm.parent = data.id
            }
            console.log(this.addForm)
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
        // 关闭输入框前提示
        editHandleClose() {
            this.$msgbox
                .alert('取消后会导致当前填写的数据消失', '提示', {
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
                console.log(this.addForm)
                if (valid) {
                    const { data: response } = await this.$http.post(
                        'jumpserver/orgs/',
                        this.addForm,
                    )
                    if (response.code) return this.$message.error(response.message)
                    // 成功
                    this.addDialogVisible = false
                    // 拿回数据
                    this.getList()
                    this.resetForm('add')
                }
            })
        },
    },
}
</script>

<style scoped lang="less">
.el-tree {
    padding: 10px;
    min-height: 400px;
}

.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
}
</style>
