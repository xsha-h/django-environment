from datetime import datetime

from django.db import models


# Create your models here.
class Videos(models.Model):
    addtime = models.DateTimeField(verbose_name="视频添加时间", default=datetime.now)
    name = models.CharField(verbose_name="视频名称", max_length=255, null=False)
    detail = models.CharField(verbose_name="视频描述", max_length=255)
    address = models.CharField(verbose_name="视频地址", max_length=255, null=False, unique=True)
    username = models.CharField(verbose_name="用户名", max_length=255, null=False)
    password = models.CharField(verbose_name="密码", max_length=255, null=False)

    class Meta:
        verbose_name = "视频监控表"

    def __str__(self):
        return self.name
