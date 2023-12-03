<template>
    <div>
        <el-row :gutter="20" class="data_notice">
            <el-col :xs="24" :sm="24" :md="24" :lg="18" class="data">
                <el-card>
                    <div slot="header" class="notice">
                        <span>监控数据</span>
                        <el-button style="float: right; padding: 3px 0" type="text">
                            查看更多
                        </el-button>
                    </div>
                    <div class="data_main">
                        <el-row :gutter="10">
                            <el-col :span="6">
                                <el-card>
                                    <el-row :gutter="5">
                                        <el-col :span="18">
                                            <p>新增主机</p>
                                            <p>+888</p>
                                            <p>稳定运行无压力</p>
                                        </el-col>
                                        <el-col :span="6">
                                            <i class="el-icon-s-platform"></i>
                                        </el-col>
                                    </el-row>
                                </el-card>
                            </el-col>
                            <el-col :span="6">
                                <el-card>
                                    <el-row :gutter="5">
                                        <el-col :span="18">
                                            <p>新增主机</p>
                                            <p>+888</p>
                                            <p>稳定运行无压力</p>
                                        </el-col>
                                        <el-col :span="6">
                                            <i class="el-icon-s-platform"></i>
                                        </el-col>
                                    </el-row>
                                </el-card>
                            </el-col>
                            <el-col :span="6">
                                <el-card>
                                    <el-row :gutter="5">
                                        <el-col :span="18">
                                            <p>新增主机</p>
                                            <p>+888</p>
                                            <p>稳定运行无压力</p>
                                        </el-col>
                                        <el-col :span="6">
                                            <i class="el-icon-s-platform"></i>
                                        </el-col>
                                    </el-row>
                                </el-card>
                            </el-col>
                            <el-col :span="6">
                                <el-card>
                                    <el-row :gutter="5">
                                        <el-col :span="18">
                                            <p>新增主机</p>
                                            <p>+888</p>
                                            <p>稳定运行无压力</p>
                                        </el-col>
                                        <el-col :span="6">
                                            <i class="el-icon-s-platform"></i>
                                        </el-col>
                                    </el-row>
                                </el-card>
                            </el-col>
                        </el-row>
                        <el-row :gutter="10" style="margin-top: 10px">
                            <el-col :span="6">
                                <el-card>
                                    <el-row :gutter="5">
                                        <el-col :span="18">
                                            <p>新增主机</p>
                                            <p>+888</p>
                                            <p>稳定运行无压力</p>
                                        </el-col>
                                        <el-col :span="6">
                                            <i class="el-icon-s-platform"></i>
                                        </el-col>
                                    </el-row>
                                </el-card>
                            </el-col>
                            <el-col :span="6">
                                <el-card>
                                    <el-row :gutter="5">
                                        <el-col :span="18">
                                            <p>新增主机</p>
                                            <p>+888</p>
                                            <p>稳定运行无压力</p>
                                        </el-col>
                                        <el-col :span="6">
                                            <i class="el-icon-s-platform"></i>
                                        </el-col>
                                    </el-row>
                                </el-card>
                            </el-col>
                            <el-col :span="6">
                                <el-card>
                                    <el-row :gutter="5">
                                        <el-col :span="18">
                                            <p>新增主机</p>
                                            <p>+888</p>
                                            <p>稳定运行无压力</p>
                                        </el-col>
                                        <el-col :span="6">
                                            <i class="el-icon-s-platform"></i>
                                        </el-col>
                                    </el-row>
                                </el-card>
                            </el-col>
                            <el-col :span="6">
                                <el-card>
                                    <el-row :gutter="5">
                                        <el-col :span="18">
                                            <p>新增主机</p>
                                            <p>+888</p>
                                            <p>稳定运行无压力</p>
                                        </el-col>
                                        <el-col :span="6">
                                            <i class="el-icon-s-platform"></i>
                                        </el-col>
                                    </el-row>
                                </el-card>
                            </el-col>
                        </el-row>
                    </div>
                </el-card>
            </el-col>
            <el-col class="hidden-md-and-down notice" :lg="6">
                <el-card>
                    <div slot="header">
                        <span>高层公告</span>
                        <el-button style="float: right; padding: 3px 0" type="text">
                            查看更多
                        </el-button>
                    </div>
                    <div class="notice_item" v-for="o in 4" :key="o">
                        <p>
                            {{ o }}
                        </p>
                        <el-button size="mini" icon="el-icon-arrow-right"></el-button>
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {}
</script>

<style lang="less" scoped>
.data_notice {
    .data {
        > .el-card {
            min-height: 350px;
            max-height: 350px;
        }
        .data_main {
            &_item {
                color: aqua;
            }
            .el-card {
                min-height: 100px;
                min-height: 100px;
                i {
                    font-size: 80px;
                    color: rgba(0, 0, 0, 0.5);
                }
            }
        }
    }

    .notice {
        .el-card {
            min-height: 350px;
            max-height: 350px;
        }
        span {
            font-weight: bold;
        }
    }
    .notice_item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        /* 不进行换行 */
        white-space: nowrap;
        /* 使用省略号 */
        text-overflow: ellipsis;
        /* 不使用滑动条 */
        overflow: hidden;
        width: 100%;
        padding: 2px 0;
        .el-button {
            border: none;
        }
    }
}
</style>
