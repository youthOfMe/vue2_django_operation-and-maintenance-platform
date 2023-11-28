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
                    <el-button
                        type="text"
                        size="mini"
                        @click="() => handleCommand(['add_group', node, data])"
                    >
                        Append
                    </el-button>
                    <el-button
                        type="text"
                        size="mini"
                        @click="() => handleCommand(['delete', node, data])"
                    >
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
                            <el-dropdown-item
                                :command="['add_server', node, data]"
                                :disabled="!data.id"
                            >
                                增加主机
                            </el-dropdown-item>
                        </el-dropdown-menu>
                    </el-dropdown>
                </span>
            </span>
        </el-tree>
        <!-- 增加资产组 -->
        <el-dialog
            :title="`${addForm.groupname}新增子分组`"
            :visible.sync="addDialogVisible"
            width="50%"
            :before-close="() => addHandleClose('add')"
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
                <el-button type="primary" @click="add('add')">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 增加主机 -->
        <el-dialog
            :title="`[${addHostForm.orgName}]组新增主机`"
            :visible.sync="addHostDialogVisible"
            width="50%"
            :before-close="() => addHandleClose('addHost')"
        >
            <el-form
                :model="addHostForm"
                :rules="addHostRules"
                ref="addHost"
                labal-width="100px"
                class="demo-ruleForm"
            >
                <el-form-item label="主机名称" prop="name">
                    <el-input v-model="addHostForm.name"></el-input>
                </el-form-item>
                <el-form-item label="管理IP" prop="ip">
                    <el-input v-model="addHostForm.ip"></el-input>
                </el-form-item>
                <el-form-item label="登录用户名" prop="username">
                    <el-input v-model="addHostForm.username"></el-input>
                </el-form-item>
                <el-form-item label="登录密码" prop="password">
                    <el-input v-model="addHostForm.password"></el-input>
                </el-form-item>
                <el-form-item label="私钥文件上传">
                    <el-upload
                        class="upload-demo"
                        :action="`${this.$http.defaults.baseURL}jumpserver/orgs/`"
                        :on-remove="handleRemove"
                        :before-remove="beforeRemove"
                        :limit="1"
                        :on-exceed="handleExceed"
                        :file-list="fileList"
                    >
                        <el-button size="small" type="primary">点击上传</el-button>
                        <div slot="tip" class="el-upload__tip">
                            只能上传1个私钥文件，且不超过1kb
                        </div>
                    </el-upload>
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
    </div>
</template>

<script>
export default {
    created() {
        this.getList()
    },
    data() {
        const validateIp = (rule, value, callback) => {
            const ipv4 = /^((\d|[1-9]\d|1\d\d|2([0-4]\d|5[0-5]))\.){4}$/
            const ipv6 = /^(([\da-fA-F]{1,4}):){8}$/
            if (ipv4.test(value) || ipv6.test(value)) callback()
            else callback(new Error('IP地址不符合IPV6/IPV4协议'))
        }

        return {
            serach: '',
            // 数据显示
            dataList: [],
            loading: false,
            defaultProps: {
                label: 'name',
            },
            // 新增资产组
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
            // 新增主机
            addHostForm: {
                name: '',
            },
            addHostRules: {
                name: [
                    { required: true, message: '请输入主机名称', trigger: 'blur' },
                    { min: 1, max: 16, message: '用户名长度在 4 到 16 个字符', trigger: 'blur' },
                ],
                ip: [
                    { required: true, message: '请输入背管理主机IP主机', trigger: 'blur' },
                    // 自定义校验器 里面使用IPV4或者V6的正则表达式进行校验
                    { validator: validateIp, trigger: 'blur' },
                ],
                username: [
                    { required: true, message: '请输入用户名称', trigger: 'blur' },
                    { min: 4, max: 16, message: '用户名长度在 4 到 16 个字符', trigger: 'blur' },
                ],
                password: [
                    { required: true, message: '请输入用户密码', trigger: 'blur' },
                    { min: 1, max: 16, message: '用户名长度在 4 到 16 个字符', trigger: 'blur' },
                ],
            },
            addHostDialogVisible: false,
            fileList: [],
        }
    },
    methods: {
        // 重置表单数据
        resetForm(name) {
            console.log(name)
            console.log(this.$refs[name])
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
            } else if (type === 'delete') this.delOrg(data)
            else {
                this.addHostForm.org = data.id
                this.addHostForm.orgName = data.name
                this.addHostDialogVisible = true
            }
        },
        // 关闭输入框前提示 通用
        addHandleClose(funcType) {
            console.log(funcType, 'funcType')
            this.$msgbox
                .alert('取消后会导致当前填写的数据消失', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                })
                .then(() => {
                    this.resetForm(funcType)
                    funcType === 'add'
                        ? (this.addDialogVisible = false)
                        : (this.addHostDialogVisible = false)
                })
                .catch(() => {
                    this.$message({
                        type: 'info',
                        message: '已取消',
                    })
                })
        },
        // 添加用户数据
        add(funcType) {
            this.$refs[funcType].validate(async (valid, obj) => {
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
                    this.$message({
                        type: 'success',
                        message: '添加成功',
                    })
                    // 拿回数据
                    this.getList()
                    this.resetForm(funcType)
                }
            })
        },
        // 删除资产数据
        delOrg(data) {
            const { id, name } = data
            this.$confirm(
                `此操作将永久删除[${name}]组及其子分组, 以及其下所有的主机 </br> 是否继续`,
                '警告',
                {
                    distinguishCancelAndClose: true,
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'error',
                    dangerouslyUseHTMLString: true,
                },
            )
                .then(async () => {
                    const { data: response } = await this.$http.delete(`jumpserver/orgs/${id}/`) // 删除某个id的数据 详情页
                    if (response.code) return this.$message.error(response.message)
                    this.getList()
                    this.$message({
                        type: 'success',
                        message: '删除成功',
                    })
                })
                .catch((action) => {
                    console.log(action)
                    this.$message({
                        type: 'error',
                        message: '取消删除 你是个牛马',
                    })
                })
        },
        handleRemove(file, fileList) {
            console.log(file, fileList)
        },
        handleExceed(files, fileList) {
            this.$message.warning(
                `当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${
                    files.length + fileList.length
                } 个文件`,
            )
            console.log(files) // 本次选择的稳健对象们
            console.log(fileList) // 文件列表对应的
            console.log(this.fileList) // 初始自定义的
        },
        beforeRemove(file, fileList) {
            return this.$confirm(`确定移除 ${file.name}？`)
        },
        // 新增主机
        addHost() {},
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
