<template>
    <div class="console">
        <div v-for="(results, index) in resultList" :key="index">
            <template v-if="results instanceof Array === true">
                <p v-for="(result, index) in results" :key="index">{{ result }}</p>
            </template>
            <p v-else>{{ results }}</p>
        </div>
        <div>
            <el-input
                placeholder="请输入肖学长认可的指令"
                v-model="command"
                @keyup.enter.native="handleCommand"
                class="key-input"
            ></el-input>
        </div>
    </div>
</template>

<script>
export default {
    created() {
        this.getHost()
    },
    data() {
        return {
            resultList: [],
            command: '',
        }
    },
    methods: {
        async getHost() {
            const { hostid: id } = this.$route.params
            console.log(id)
            // 我是张富康的爸爸
            const { data: response } = await this.$http.get(`jumpserver/hosts/${id}/`)
            if (response.code) return this.$message.error(response.message)
            console.log(response)
            const { name, ip, username } = response

            // 服务器建立websocket
            if ('WebSocket' in window) {
                // 创建连接
                const remoteWsServer = 'localhost'
                const remoteWsServerPort = 10800
                const ws = new WebSocket(`ws://${remoteWsServer}:${remoteWsServerPort}/abc/xyz/123`)

                // Connection opened
                ws.addEventListener('open', (event) => {
                    this.resultList.push(`正在连接到:${name}, ip为${ip}, 用户为${username}的服务器`)
                    ws.send(
                        JSON.stringify({
                            token: window.localStorage.getItem('token'),
                            id,
                        }),
                    )
                })

                ws.onclose = (event) => {
                    console.log('关闭', event.reason)
                    this.resultList.push(
                        `${this.command} 与${name}, ip为${ip}, 用户为${username}的服务器连接断开, 原因是:${event.reason}`,
                    )
                }

                ws.onerror = (event) => {
                    console.log('错误', event.data)
                    this.resultList.push(this.command + ' ' + event.data)
                }

                ws.onmessage = (event) => {
                    const k = Array(event.data)[0]
                    const messageArr = k
                        .substring(2, k.length - 6)
                        .replace(/\\n/g, ',')
                        .split(',')
                    messageArr.unshift('输入命令: ' + this.command)
                    this.command = ''
                    this.resultList.push(messageArr)
                }

                this.ws = ws
            } else return this.$message.error('该浏览器不支持WebSocket, 请更新浏览器到最新版本')
        },
        // 处理命令
        handleCommand() {
            this.ws.send(this.command)
        },
    },
}
</script>

<style lang="less" scoped>
.console {
    background-color: #000;
    height: 100%;
    min-height: 300px;
    color: #fff;
    padding: 5px;
}

/deep/ .el-input__inner {
    background-color: #000;
    color: #fff;
    border: none;
    padding-left: 0;
}
</style>
