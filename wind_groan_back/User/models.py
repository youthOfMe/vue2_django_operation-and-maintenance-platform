from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserProfile(AbstractUser):
    class Meta:
        db_table = 'auth_user' # auth_user
        verbose_name = '自定义用户' # 定义表的说明
    phone = models.CharField(max_length=32, verbose_name='电话号码', null=True, blank=True)
