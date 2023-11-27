<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>堡垒机</el-breadcrumb-item>
            <el-breadcrumb-item>资产类型</el-breadcrumb-item>
        </el-breadcrumb>
        <!-- 组织树 -->
        <el-tree
            :data="dataList"
            show-checkbox
            node-key="id"
            default-expand-all
            :expand-on-click-node="false"
            :props="defaultProps"
        ></el-tree>
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
            defaultProps: {
                label: 'name',
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
                console.log(response)
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
    },
}
</script>

<style lang="scss" scoped></style>
