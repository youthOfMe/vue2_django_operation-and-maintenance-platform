import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wind_groan_back.settings')
django.setup(set_prefix=False)

# 想使用django.contrib.auth.models必须写上面的代码
from django.contrib.auth.models import ContentType, Permission

content_type = ContentType.objects.create(app_label='cmdb', model='citype')
permission = Permission.objects.create(
    codename='use_citype',
    name='使用资产类型',
    content_type=content_type
)