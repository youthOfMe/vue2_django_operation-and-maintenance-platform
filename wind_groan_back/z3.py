# import pymongo
#
# url = ""
# # client = pymongo.MongoClient(host=url)
# # client = pymongo.MongoClient(url)
# # username, password
# client = pymongo.MongoClient('127.0.0.1', 27017)
# print(client, type(client))
#
# # use db
# # db = client.mytest # database
# db = client['mytest'] # 属性和key访问都可以 背后什么原理
# print(type(db), db)
#
# # col = db.users
# col = db['users']
# print(type(col), col) # collection 表
#
# print(*col.find()) # select * from mytest.users
#
# client.close()

# mongoengine
from mongoengine import connect, Q
# _connections 字典就是和数据库有紧密关联的数据 不保存就没有持久态
connect = connect(db='mytest', host='127.0.0.1', port=27017) # 读取配置文件 字典

# 定义文档 相当于定义Model类
from z1 import User

# 改
# 请问: 数据库当中有没有对应的数据呢？ 改的前提是数据是持久化的, 所以才需要进行先查再改
# 查了之后 返回的实例一定有pk, 改和删除 都是对持久态数据的操作
# 1. 先查到实例 对持久态的实例进行修改 最后save
# user = User(name='tom')
# user.name = 'TOM'
# user.save()
# print(user)
# user = User.objects(name='tom')[0]
# print(user)
# user.name = 'NIUBI'
# user.save()
# print(user)
# 2. 查询集.update_one() update_many()
# user = User.objects.get(name='NIUBI')
# print(user) # 持久态
# User.objects(name='NIUBI').update_one(name='tommy')
# print(user.pk, user.name) # pk不变 name是说明
# user.reload() # 只有进行reload之后才能进行查看到最新的数据
# print(user)

# 删除
# 先拿到持久态 后进行删除 可以对集合进行直接的删除
# users = User.objects(name='benny')
# print(*users)
# users.delete()
# print(*User.objects(name='benny'))
users = User.objects(name='alex')
user = users[0]
user.delete()
print(User.objects(name='alex').count())

print(*User.objects(name='tom')) # 返回的是一个集合所以可以进行使用*进行解构
# 使用Q对象进行处理
print(*User.objects(Q(name='alex') & Q(age=20)))
print(*User.objects(Q(name='alex') | Q(age=20)))
print(*User.objects(Q(name='alex')))

# 聚合 pipeline 参照 pymongo原生 帮助

# User.objects.create(name='alex')
# User.objects.create(name='benny')
# User.objects.create(name='hanbaowang', age=32)

# 新增: 新增说明持久化的数据库中数据存在否
# 持久态数据
# 在成功加入到数据库前 实例都是非持久态的
# 1. 管理器的create 本质上调用的也是save
# u1 = User.objects.create(name="jerry", age=32)
# print(u1,  type(u1)) u1如果能拿到 一定有id 也就是说数据有对应的持久化文件
# 2. 实例的save
# u2 = User(name='666dasd4asd5as542d4as65d4as86d478as6d45asd4as5d4156as5d41astom')
# u2.name = 'tom'
# u2.save() # save成功后

# pk
# for u in User.objects.filter(age__gt=20).filter(name='jerry'):
#     print(u.pk, u.id, u.name, u.age)
# 下面这种写法和上面的写法差不多 进行条件查询和ORM差不多
# for u in User.objects(name__in=['benny', 'tom']):
#     print(u.pk, u.id, u.name, u.age)
# for u in User.objects(age__not__gt=30).order_by('-name')[1:3]:
#     print(u.pk, u.id, u.name, u.age)
for u in User.objects(age__not__gt=30).order_by('-name').limit(2).skip(1):
    print(u.pk, u.id, u.name, u.age)

print(User.objects(age__not__gt=30).order_by('-name').limit(1)) # 集合里面仅有一个
print(User.objects(age__not__gt=30).order_by('-name')[0]) # 直接拿出来一个

# 查所有
# for user in User.objects:
#     print(user.pk, user.id, user.name, user.age)
#     print(user)

print(*User.objects)
print(User.objects.all())
# 使用get的时候只能去拿一个哦
# print(User.objects.get(age__gt=20))


