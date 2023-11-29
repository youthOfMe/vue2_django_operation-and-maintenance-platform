from django.db import models
from User.models import UserProfile

# Create your models here.
class Organization(models.Model):
    class Meta:
        db_table = 'js_org'

    # id
    name = models.CharField(max_length=24)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, verbose_name='父级ID')
    # hosts
    is_deleted = models.BooleanField(default=False) # 逻辑删除

    def __str__(self):
        return "<Org {}, {} -> {}>".format(self.pk, self.name, self.parent_id)

class Host(models.Model):
    class Meta:
        db_table = 'js_host'
    # id
    # 类似于cmdb中的字段, 自行添加
    name = models.CharField(max_length=48, verbose_name='主机名称')
    # WEB SHELL
    org = models.ForeignKey(Organization, models.PROTECT,
                            related_name='hosts')
    ip = models.GenericIPAddressField(blank=False, verbose_name='被管理主机的ip')
    username = models.CharField(max_length=48, verbose_name='登录主机用户名')
    password = models.CharField(max_length=48,null=True, blank=True, verbose_name='登录密码') # ssh 使用明文进行登录
    ssh_pkey_path = models.CharField(null=True, blank=True, max_length=250, verbose_name='密钥的存储路径') # 使用私钥
    # 密钥存储在服务器端, 服务器代码内部使用
    is_deleted = models.BooleanField(default=False) # 逻辑删除

class Track(models.Model):
    class OPTYPES(models.IntegerChoices):
        LOFIN = (1, '登录')
        LOGOUT = (2, '登出')
        COMMAND = (3, '命令')
    class Meta:
        db_table = 'js_track'
    user = models.ForeignKey(UserProfile, models.PROTECT, db_column='user_id')
    host = models.ForeignKey(Host, models.PROTECT, db_column='host_id')
    source_ip = models.GenericIPAddressField() # ipv4 ipv6
    op_date = models.DateTimeField(auto_now_add=True) # 新增的时候记录当前时间
    op_type = models.IntegerField(choices=OPTYPES.choices)
    command = models.CharField(null=True, blank=True, max_length=250, verbose_name='命令')
    op_state = models.BooleanField(default=True, verbose_name='执行结果的状态值')
