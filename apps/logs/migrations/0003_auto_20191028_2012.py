# Generated by Django 2.2.6 on 2019-10-28 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0002_logs_scene'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logs',
            name='user_id',
        ),
        migrations.AddField(
            model_name='logs',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='操作用户'),
        ),
    ]