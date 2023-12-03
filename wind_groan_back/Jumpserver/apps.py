from django.apps import AppConfig
from django.conf import settings

class JumpserverConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Jumpserver'
    flag = False

    def ready(self):
        if not self.flag:
            pass
            # import z5