# Generated by Django 2.2.6 on 2019-10-29 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accessControls', '0004_auto_20191023_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesses',
            name='user_id',
            field=models.CharField(max_length=255, verbose_name='用户申请人'),
        ),
    ]