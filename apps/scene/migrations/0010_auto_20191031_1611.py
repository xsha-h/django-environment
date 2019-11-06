# Generated by Django 2.2.6 on 2019-10-31 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scene', '0009_auto_20191031_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='display',
            name='online',
            field=models.IntegerField(choices=[(1, '在线'), (0, '离线')], default=1, verbose_name='在线状态'),
        ),
        migrations.AlterField(
            model_name='display',
            name='status',
            field=models.IntegerField(choices=[(1, '正常'), (0, '异常')], default=1, verbose_name='设备状态'),
        ),
    ]