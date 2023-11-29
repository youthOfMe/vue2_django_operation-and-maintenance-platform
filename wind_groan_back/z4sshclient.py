
import paramiko

# 目标主句s1 开着 22端口 ssh
# client 连接目标主句
client = paramiko.SSHClient() # 仅仅初始化一个client对象
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
try:
    # 1. 跳板机使用ip, 用户名, 密码的方式可以登录到目标主句
    # client.connect('43.138.118.145', 22, 'root','20050229zY')
    #  ip\username\密钥
    key_filename = r'D:/id_rsa' # 指定密钥文件 必须给私钥
    # client.connect('43.138.118.145', 22, 'root', key_filename=key_filename) # 使用的是指定的私钥
    # 使用ssh-copy-id -i ~/.ssh/id_rsa.pub 目标主机用户名@目标主机ip 将公钥打入敌军内部
    client.connect('43.138.118.145', 22, 'root') # 使用的是本机用户的私钥
    stdin, stdout, stderr = client.exec_command('id;hostname;id1')
    # print(stdin.read()) 只能写
    print(stdout.read().decode()) # 默认都是utf-8解码
    print(stderr.read().decode())
except Exception as e:
    print(e)
finally:
    client.close()