<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>资产管理</el-breadcrumb-item>
            <el-breadcrumb-item>资产类型</el-breadcrumb-item>
        </el-breadcrumb>
        <el-card>
            <el-row :gutter="20">
                <el-col :span="18">
                    <el-input placeholder="请输入内容" v-model="serach">
                        <!-- 在模板中会传入时间对象event -->
                        <el-button
                            slot="append"
                            icon="el-icon-search"
                            @click="getList(1)"
                        ></el-button>
                    </el-input>
                </el-col>
                <el-col :span="6">
                    <el-button type="primary" @click="addDialogVisible = true">添加资产</el-button>
                </el-col>
            </el-row>
            <el-table
                :data="dataList"
                style="width: 100%"
                :border="true"
                label-width="100px"
                stripe
                v-loading="loading"
                element-loading-text="拼命加载中"
                element-loading-spinner="el-icon-loading"
                element-loading-background="rgba(0, 0, 0, 0.8)"
            >
                <el-table-column type="index"></el-table-column>
                <el-table-column prop="id" label="终端ID"></el-table-column>
                <el-table-column prop="label" label="名称"></el-table-column>
                <el-table-column label="操作" fixed="right">
                    <template #default="{ row }">
                        <el-tooltip content="编辑" placement="bottom" effect="light">
                            <el-button
                                size="small"
                                icon="el-icon-edit"
                                @click="handleEdit(row.id)"
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
        <!-- 增加资产组 -->
        <el-dialog
            title="新增资产组"
            :visible.sync="addDialogVisible"
            width="50%"
            :before-close="() => handleClose('add')"
        >
            <el-form
                :model="addForm"
                :rules="addRules"
                ref="add"
                labal-width="600px"
                class="demo-ruleForm"
            >
                <el-form-item label="资产组英文名称" prop="name">
                    <el-input v-model="addForm.name"></el-input>
                </el-form-item>
                <el-form-item label="资产组中文名称" prop="label">
                    <el-input v-model="addForm.label"></el-input>
                </el-form-item>
                <el-form-item label="资产组版本号" prop="version">
                    <el-input v-model="addForm.version"></el-input>
                </el-form-item>
                <!-- 根据上面选择类型 动态增加表单项 -->
                <el-form-item label="添加资产字段">
                    <el-button
                        icon="el-icon-plus"
                        plain
                        type="success"
                        size="mini"
                        @click="handleAddField()"
                    ></el-button>
                </el-form-item>
                <el-form-item
                    v-for="(field, cmIndex) in addForm.fields"
                    label="资产组字段"
                    :key="cmIndex"
                    props="fileds"
                >
                    <el-card>
                        <el-form-item label="英文名" prop="name">
                            <el-input v-model="field.name"></el-input>
                        </el-form-item>
                        <el-form-item label="中文名" prop="label">
                            <el-input v-model="field.label"></el-input>
                        </el-form-item>
                        <el-form-item label="字段类型" prop="type">
                            <el-input v-model="field.type"></el-input>
                        </el-form-item>
                        <el-form-item label="是否必填" prop="required">
                            <el-switch v-model="field.required"></el-switch>
                        </el-form-item>
                        <!-- <el-form-item label="是否必须" prop="required">
                            <el-input v-model="field.required"></el-input>
                        </el-form-item> -->
                    </el-card>
                </el-form-item>
                <el-form-item>
                    <el-button @click="resetForm('add')">重置</el-button>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="handleClose('add')">取 消</el-button>
                <el-button type="primary" @click="add()">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 编辑资产组 -->
        <el-dialog
            title="编辑资产组"
            :visible.sync="editDialogVisible"
            width="50%"
            :before-close="() => handleClose('edit')"
        >
            <el-form
                :model="editForm"
                :rules="addRules"
                ref="edit"
                labal-width="600px"
                class="demo-ruleForm"
            >
                <el-form-item label="资产组英文名称" prop="name">
                    <el-input v-model="editForm.name"></el-input>
                </el-form-item>
                <el-form-item label="资产组中文名称" prop="label">
                    <el-input v-model="editForm.label"></el-input>
                </el-form-item>
                <el-form-item label="资产组版本号" prop="version">
                    <el-input v-model="editForm.version"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="handleClose('edit')">取 消</el-button>
                <el-button type="primary" @click="edit(editForm.id)">确 定</el-button>
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
            serach: '',
            // 数据显示
            dataList: [],
            pagination: { total: 0, page: 1, size: 20 },
            loading: false,
            // 新增
            addDialogVisible: false,
            addForm: {
                name: '',
                label: '',
                version: '',
                fields: [],
            },
            addRules: {
                name: [
                    { required: true, message: '请输入英文名称', trigger: 'blur' },
                    { min: 1, max: 26, message: '英文名称长度在 1 到 26个字符', trigger: 'blur' },
                ],
                label: [
                    { required: true, message: '请输入中文名称', trigger: 'blur' },
                    { min: 1, max: 16, message: '中文名称长度在 1 到 16 个字符', trigger: 'blur' },
                ],
                version: [
                    { required: true, message: '请输入版本名', trigger: 'blur' },
                    { min: 1, max: 16, message: '版本必须在1-16版本', trigger: 'blur' },
                ],
                // 记得补充校验规则 字段的
            },
            // 编辑
            editDialogVisible: false,
            editForm: {
                name: '',
                label: '',
                version: '',
            },
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
                const { data: response } = await this.$http.get('cmdb/citypes/', {
                    params: {
                        page,
                        // username: this.username,
                        search: this.serach,
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
        handleClose(type) {
            this.$msgbox
                .alert('取消后会导致当前填写的数据消失', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                })
                .then(() => {
                    this.resetForm(type)
                    switch (type) {
                        case 'add':
                            this.addForm.length = 0
                            this.addDialogVisible = false
                            break
                        case 'edit':
                            this.editForm.length = 0
                            this.editDialogVisible = false
                            break
                        default:
                            break
                    }

                    this.$message({
                        type: 'info',
                        message: '已取消',
                    })
                })
                .catch(() => {})
        },
        // 添加资产组数据
        add() {
            this.$refs['add'].validate(async (valid, obj) => {
                if (valid) {
                    const { data: response } = await this.$http.post('cmdb/citypes/', this.addForm) // 资产列表页进行新增
                    if (response.code) return this.$message.error(response.message)
                    this.addDialogVisible = false
                    this.resetForm('add')
                    this.addForm.length = 0
                    this.getList()
                }
            })
        },
        // 添加资产组字段
        handleAddField() {
            this.addForm.fields.push({
                name: '',
                label: '',
                type: '',
                required: true,
            })
        },
        // 删除资产数据
        async handleDelete(id) {
            this.$confirm('此操作将永久删除该资产类型, 是否继续', '警告', {
                distinguishCancelAndClose: true,
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'error',
            })
                .then(async () => {
                    const { data: response } = await this.$http.delete(`cmdb/citypes/${id}/`)
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
        // 编辑资产组数据
        async handleEdit(id) {
            const { data: response } = await this.$http.get(`cmdb/citypes/${id}/`, {})
            this.editForm = response
            this.editDialogVisible = true
            console.log(this.editForm)
        },

        async edit(id) {
            this.$refs['edit'].validate(async (valid, obj) => {
                if (valid) {
                    const { data: response } = await this.$http.patch(
                        `cmdb/citypes/${id}/`,
                        this.editForm,
                    ) // 资产列表页进行新增
                    if (response.code) return this.$message.error(response.message)
                    this.editDialogVisible = false
                    this.resetForm('edit')
                    this.editForm.length = 0
                    this.getList()
                }
            })
        },
    },
}
</script>

<style lang="scss" scoped></style>
