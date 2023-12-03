# Generated by Django 4.2.7 on 2023-11-29 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Jumpserver', '0002_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_ip', models.GenericIPAddressField()),
                ('op_date', models.DateTimeField(auto_now_add=True)),
                ('op_type', models.IntegerField(choices=[(1, '登录'), (2, '登出'), (3, '命令')])),
                ('command', models.CharField(blank=True, max_length=250, null=True, verbose_name='命令')),
                ('op_state', models.BooleanField(default=True, verbose_name='执行结果的状态值')),
                ('host', models.ForeignKey(db_column='host_id', on_delete=django.db.models.deletion.PROTECT, to='Jumpserver.host')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'js_track',
            },
        ),
    ]