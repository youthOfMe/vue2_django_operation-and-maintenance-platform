<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>用户管理</el-breadcrumb-item>
            <el-breadcrumb-item>权限列表</el-breadcrumb-item>
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
                    <!-- <el-button type="primary" @click="addDialogVisible = true">添加用户</el-button> -->
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
                <el-table-column prop="content_type.app_label" label="应用"></el-table-column>
                <el-table-column prop="codename" label="codename"></el-table-column>
            </el-table>

            <el-pagination
                @current-change="getList"
                :current-page="pagination.page"
                :page-size="pagination.size"
                layout="total, prev, pager, next, jumper"
                :total="pagination.total"
            ></el-pagination>
        </el-card>
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
            username: '',
            pagination: { total: 0, page: 1, size: 20 },
            loading: false,
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
                const { data: response } = await this.$http.get('users/perms/', {
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
    },
}
</script>

<style lang="scss" scoped></style>
