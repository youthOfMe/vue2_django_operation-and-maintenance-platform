import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wind_groan_back.settings')
django.setup(set_prefix=False)
### 以上四句是固定的 用于获取项目中的django配置资源

from Jumpserver.models import Host
from asgiref.sync import sync_to_async
import asyncio # 引入异步库
import websockets
import json
from rest_framework_simplejwt.authentication import JWTAuthentication
import paramiko
from django.conf import settings
from paramiko.client import SSHClient

# from sesame.utils import get_user
from websockets.frames import CloseCode


@sync_to_async # get_user = sync_to_async(get_user) sync_to_async包装玩后的get_user签名和原函数应该是一样的
def get_user(jwtauth, validated_token):
    return jwtauth.get_user(validated_token)

@sync_to_async
def get_host(id):
    return Host.objects.filter(is_deleted=False).get(pk=id)

async def handler(websocket, path):
    print(websocket, type(websocket))
    print(path, type(path)) # 可以用path来路由道不同的函数
    try:
        # 第一次等道浏览器发过来的数据
        # token给我 token验证成功后 获得userid 有了userid就等于有了user对象 user对象有了就可以进行判断权限了
        firstdata = await websocket.recv()
        print(firstdata, type(firstdata)) # 第一次发过来的数据
        payload = json.loads(firstdata) # 返回数据是字典

        raw_token = payload['token']
        # 进行验证是否被篡改了
        jwtauth = JWTAuthentication()
        validated_token = jwtauth.get_validated_token(raw_token)
        # user = await get_user(jwtauth, validated_token)
        # user = jwtauth.get_user(validated_token) # 从校验后的token里面拿到了user_id
        # user = await sync_to_async(jwtauth.get_user)((validated_token))
        user = await asyncio.to_thread(jwtauth.get_user, validated_token) # 异步化并且传应该参数 主要使用创建新线程 将这个函数扔到一个线程中进行执行
        # 可补充权限 user.has_perms user.has_perm进行检验权限
        print(type(user), user)
        # if True:
        #     await websocket.close(reason='认证失败')

        # 获取主机信息包括密码或者密钥
        host_id = payload['id']

        host = await get_host(host_id)
        name = host.name
        ip = host.ip
        username = host.username
        password = host.password

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        if password:
            # 利用密码访问
            client.connect(ip, 22, username, password)
        else:
            pkey_filename = settings.JUMPSERVER_UPLOADS_BASE / host.ssh_pkey_path # ssh_pkey_path 相对路径
            # 利用密钥进行登录
            client.connect(ip, 22, username, key_filename=pkey_filename)

        # 上下文管理
        with client:
            while True:
                data = await websocket.recv()
                # user = await asyncio.to_thread(get_user, sesame)
                # if user is None:
                #     await websocket.close(CloseCode.INTERNAL_ERROR, "authentication failed")
                #     return
                #
                # await websocket.send(f"Hello {user}!")
                _, stdout, stdarr = client.exec_command(data)
                o1 = stdout.read().decode()
                o2 = stdarr.read().decode()

                await websocket.send(json.dumps([o1, o2]))
        await websocket.close()
    except Exception as e:
        print(e)
        await  websocket.close(reason=str(e))



async def main(): # 异步协程
    async with websockets.serve(handler, "localhost", 10800):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main()) # 大循环 单线程