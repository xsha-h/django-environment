from datetime import datetime

from django.db import models


# Create your models here.
class Logs(models.Model):
    addtime = models.DateTimeField(verbose_name="日志添加时间", default=datetime.now)
    content = models.CharField(verbose_name="日志内容", max_length=500, null=False)
    username = models.CharField(verbose_name="操作用户", max_length=255, null=True, blank=True)
    log_module = models.CharField(verbose_name="所属模块", max_length=255, null=True, blank=True)
    scene = models.CharField(verbose_name="所属场景", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "日志信息表"

    def __str__(self):
        return str(self.content)
