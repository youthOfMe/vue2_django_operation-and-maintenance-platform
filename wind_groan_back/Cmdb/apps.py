from django.apps import AppConfig
from django.conf import settings


class CmdbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Cmdb'
    flag = False

    def ready(self):
        if not self.flag:
            # 最后这个配置, 连接和app有关
            # Django这个application被调用时加载配置文件 运行settings.py
            from mongoengine import connect  # pymongo
            from mongoengine import connection
            connect(**settings.MONGODB_DATABASES)