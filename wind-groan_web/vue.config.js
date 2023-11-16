const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // 配置请求代理
  devServer: {
    proxy: {
        '/api/v1': {
            target: 'http://127.0.0.1:8000',
            ws: true,
            changeOrigin: true,
            pathRewrite: { '^/api/v1': '' }
        }
    }
  }
})
