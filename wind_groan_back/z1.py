# from mongoengine import (
#     Document,
#     StringField,
#     IntField,
# )
#
# class User(Document):
#     meta = {'collection': 'users'}
#     # BlogUser -> blog_user
#     # 字段 id呢? 主键呢? 如果没有指定主键 那么就使用id
#     name = StringField(required=True, max_length=24)
#     age = IntField(min_value=0, max_value=150, default=20)
#
#     def __str__(self):
#         return "<User {}, {}, {}>".format(self.pk, self.name, self.age)

print(666666666666666666666666)

MONGODB_DATABASES = {
    'host': '127.0.0.1',
    'port': 27017,
    # 'username': 'youthOfMe',
    # 'password': '123456',
    'name': 'wind-groan',
    'tz_aware': True,
}

from mongoengine import connect
connect(**MONGODB_DATABASES)

from Cmdb.models import CiType, CiTypeField
# citypes文档中的一条记录
ct_ni = CiType()
ct_ni.name = 'Network Interface'
ct_ni.version = 1
ct_ni.label = '网络接口'
ct_ni.fields = [
    CiTypeField(name="interface name", label="接口名称", type="str", required=True, ),
    CiTypeField(name="IP Address", label="IP", type="str", required=True, ),
    CiTypeField(name="MAC Address", label="MAC", type="str", required=True, ),
    CiTypeField(name="Gateway", label="网关", type="str", required=False, ),
    CiTypeField(name="Mask", label="掩码", type="str", required=False, ),
]
ct_ni.save()
print(ct_ni.to_json())

ct = CiType()
ct .name = "Server"
ct.label ="服务器"
ct.fields = [
    CiTypeField(name='name',label='资产名称', type='str', required=True),
    CiTypeField(name='Asset number',label='资产编号',type='str'),
    CiTypeField(name='Brand',label='品牌' ,type='str'),
    CiTypeField(name='Model',label='型号',type='str'),
    CiTypeField(name='OS Family',label='操作系统',type='str'),
    CiTypeField(name='OS Version',label='OS版本', type='str'),
    CiTypeField(name='Management Ip',label='管理IP',type='str'),
    CiTypeField(name='CPU',label='CPU',type='str'),
    CiTypeField(name='RAM',label='内存' ,type='str'),
    CiTypeField(name='Rack',label='机架',type='str'),
    CiTypeField(name='Production Date',label='上线时间', type='date'),
    CiTypeField(name='Purchase Date',label='购买日期',type='date'),
    CiTypeField(name='End of warranty',label='保修期结束',type='date'),
    # 一台服务器有多个网络接口
    CiTypeField(name='Network Interface', label='网络接口', type='list:Network Interface')
]

ct.save()
print(ct.to_json())

