# Generated by Django 2.2.6 on 2019-10-23 09:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accesses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addtime', models.DateTimeField(default=datetime.datetime.now, verbose_name='门禁申请时间')),
                ('user_id', models.IntegerField(verbose_name='用户申请人')),
                ('start_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='申请开始时间')),
                ('end_time', models.DateTimeField(verbose_name='申请结束时间')),
                ('follow_users', models.CharField(max_length=255, verbose_name='随行人员')),
                ('follow_nums', models.IntegerField(verbose_name='随性人数')),
                ('detail', models.CharField(max_length=255, verbose_name='申请说明')),
                ('status', models.IntegerField(verbose_name='申请状态')),
                ('approval_time', models.DateTimeField(verbose_name='审批时间')),
                ('approval_user', models.IntegerField(verbose_name='审批人')),
                ('feedback', models.CharField(max_length=255, verbose_name='审批反馈')),
            ],
            options={
                'verbose_name': '门禁审批表',
            },
        ),
    ]