<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>资产管理</el-breadcrumb-item>
            <el-breadcrumb-item>资产列表</el-breadcrumb-item>
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
                stripe
                v-loading="loading"
                element-loading-text="拼命加载中"
                element-loading-spinner="el-icon-loading"
                element-loading-background="rgba(0, 0, 0, 0.8)"
            >
                <el-table-column type="index"></el-table-column>
                <el-table-column prop="id" label="资产ID"></el-table-column>
                <el-table-column prop="label" label="资产类型"></el-table-column>
                <el-table-column prop="fields[0]" label="资产名称">
                    <template #default="{ row }">
                        {{ row.fields[0].value }}
                    </template>
                </el-table-column>
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
        <!-- 增加资产 -->
        <el-dialog
            title="新增角色"
            :visible.sync="addDialogVisible"
            width="80%"
            :before-close="addHandleClose"
        >
            <el-form
                :model="addForm"
                :rules="addRules"
                ref="add"
                label-width="100px"
                class="demo-ruleForm"
            >
                <el-form-item label="类型" prop="citype">
                    <el-select
                        v-model="addForm.citype"
                        placeholder="请选择资产类型"
                        @change="handleCiTypeChange"
                    >
                        <!-- 选项很多, 但是一次只能选择一个, 选择后其value覆盖选择的值 -->
                        <el-option
                            v-for="citype in citypes"
                            :key="citype.id"
                            :label="citype.label"
                            :value="citype.id"
                        ></el-option>
                    </el-select>
                </el-form-item>
                <!-- 根据上面选择类型 动态增加表单项 -->
                <el-form-item
                    v-for="(field, cmIndex) in addForm.fields"
                    :label="field.label"
                    :key="field.id"
                    :prop="'fields.' + cmIndex + '.value'"
                    :rules="
                        field.required
                            ? {
                                  required: true,
                                  message: field.label + '不能为空',
                                  trigger: 'blur',
                              }
                            : {}
                    "
                >
                    <el-input v-model="field.value" v-if="field.type === 'str'"></el-input>
                    <div v-else-if="field.type === 'date'">自行完成 使用datepicker</div>
                    <div v-else-if="field.type.startsWith('list:')">
                        list: Network Interface:1 怎么处理 要套娃了
                        <el-button
                            icon="el-icon-plus"
                            plain
                            type="success"
                            size="mini"
                            @click="handleAddChild(field)"
                        ></el-button>
                        <el-card
                            v-for="(networkItem, networkIndex) in field.children"
                            :key="`${field.name}.children.${networkIndex}`"
                        >
                            <el-form-item
                                v-for="(field, addNetIndex) in networkItem.fields"
                                :label="field.label"
                                :key="field.id"
                                :prop="
                                    'fields.' +
                                    cmIndex +
                                    '.children.' +
                                    networkIndex +
                                    '.fields.' +
                                    addNetIndex +
                                    '.value'
                                "
                                :rules="
                                    field.required
                                        ? {
                                              required: true,
                                              message: field.label + '不能为空',
                                              trigger: 'blur',
                                          }
                                        : {}
                                "
                            >
                                <el-input
                                    v-model="field.value"
                                    v-if="field.type === 'str'"
                                ></el-input>
                                <div v-else-if="field.type === 'date'">自行完成 使用datepicker</div>
                            </el-form-item>
                        </el-card>
                    </div>
                </el-form-item>
                <el-form-item>
                    <el-button @click="resetForm('add')">重置</el-button>
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
        this.getCiTypeList()
    },
    data() {
        return {
            serach: '',
            // 数据显示
            dataList: [],
            pagination: { total: 0, page: 1, size: 20 },
            loading: false,
            // 类型信息
            citypes: [],
            // 新增
            addDialogVisible: false,
            addForm: {
                citype: '',
                fields: [],
            },
            addRules: {
                citype: [{ required: true, message: '请选择资产类型', trigger: 'blur' }],
            },
        }
    },
    methods: {
        // 重置表单数据
        resetForm(name) {
            this.$refs[name].resetFields()
            this.addForm.fields = []
        },
        // 获取用户列表数据
        async getList(page = 1) {
            this.loading = true
            if (typeof page !== 'number' || page <= 0) {
                page = 1
            }
            try {
                const { data: response } = await this.$http.get('cmdb/cis/', {
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
        // 查询数据
        async getCiTypeList() {
            // 类型要不要进行分页?不分页 选择框提供搜索功能 将类型在分类变成树 并且树节点懒加载
            const { data: response } = await this.$http.get('cmdb/citypes/all/')
            if (response.code) return this.$message.error(response.message)
            this.citypes = response
        },
        // 资产类型选项变化
        async handleCiTypeChange(id) {
            console.log(this.addForm.citype, '############')
            const { data: response } = await this.$http.get(`cmdb/citypes/${id}/`) // 详情页
            if (response.code) return this.$message.error(response.message)
            this.addForm.name = response.name
            this.addForm.label = response.label
            this.addForm.version = response.version

            console.log(response.fields)
            // 进行响应式给对象绑定数据
            this.$set(this.addForm, 'fields', response.fields)
            // this.addForm.fields = response.fields
        },
        //
        async handleAddChild(currentField) {
            console.log(this.addForm.citype, '############')
            console.log(currentField)
            console.log(currentField.type.split(':'))
            const [, name, version = 1] = currentField.type.split(':')
            const { data: response } = await this.$http.get(`cmdb/citypes/${name}/${version}/`) // 详情页
            if (response.code) return this.$message.error(response.message)
            console.log(response) // 返回了类型信息 这个类型信息可以创建多个网络接口的实例，动态创建该类型的表单项用于填写
            if (!(`children` in currentField)) {
                this.$set(currentField, 'children', [])
            }
            currentField.children.push(response)
            console.log(this.addForm)
        },
        // 添加用户数据
        add() {
            this.$refs['add'].validate(async (valid, obj) => {
                console.log(valid, obj)
                if (valid) {
                    console.log(this.addForm)
                    const { data: response } = await this.$http.post('cmdb/cis/', this.addForm) // 资产列表页进行新增
                    console.log(response)
                    if (response.code) return this.$message.error(response.message)
                    this.addDialogVisible = false
                    this.resetForm('add')
                    this.getList()
                }
            })
        },
    },
}
</script>

<style lang="less" scoped>
.el-form-item .el-form-item {
    margin-bottom: 22px;
}
</style>
