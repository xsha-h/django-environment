# Generated by Django 2.2.6 on 2019-10-31 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scene', '0008_auto_20191029_1945'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scene',
            options={'permissions': (('scene_view', '场景浏览'), ('scene_control', '场景控制')), 'verbose_name': '场景表'},
        ),
        migrations.AlterField(
            model_name='flame',
            name='status',
            field=models.IntegerField(choices=[(1, '无'), (0, '有')], verbose_name='火光状态'),
        ),
        migrations.AlterField(
            model_name='methane',
            name='status',
            field=models.IntegerField(choices=[(1, '无'), (0, '有')], verbose_name='甲烷状态'),
        ),
        migrations.AlterField(
            model_name='smoke',
            name='status',
            field=models.IntegerField(choices=[(1, '无'), (0, '有')], verbose_name='烟雾状态'),
        ),
    ]
