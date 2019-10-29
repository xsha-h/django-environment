from datetime import datetime

from django.db import models


# Create your models here.
from scene.models import Scene


class AlarmType(models.Model):
    addtime = models.DateTimeField(verbose_name="告警类型添加时间", default=datetime.now)
    name = models.CharField(verbose_name="告警类型名称", max_length=255, null=False, unique=True)
    detail = models.CharField(verbose_name="告警类型说明", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "告警类型表"

    def __str__(self):
        return self.name


class AlarmLevel(models.Model):
    addtime = models.DateTimeField(verbose_name="告警级别添加时间")
    name = models.CharField(verbose_name="告警级别名称", max_length=255, null=False, unique=True)
    detail = models.CharField(verbose_name="告警级别说明", max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "告警级别表"

    def __str__(self):
        return self.name


class Alarm(models.Model):
    STATUS_CHOICE = (
        (1, "待处理"),
        (2, "待审核"),
        (3, "审核通过"),
        (4, "审核不通过"),
    )
    addtime = models.DateTimeField(verbose_name="告警添加时间", default=datetime.now)
    device = models.CharField(verbose_name="告警设备", max_length=255, null=False)
    content = models.CharField(verbose_name="告警内容", max_length=255, null=True, blank=True)
    status = models.IntegerField(verbose_name="告警状态", choices=STATUS_CHOICE, default=1)
    deal_user = models.IntegerField(verbose_name="告警处理人")
    deal_time = models.DateTimeField(verbose_name="告警处理时间", null=True, blank=True)
    deal_detail = models.CharField(verbose_name="告警处理说明", max_length=255, null=True, blank=True)
    audit_user = models.IntegerField(verbose_name="告警审核人")
    audit_time = models.DateTimeField(verbose_name="告警审核时间", null=True, blank=True)
    audit_detail = models.CharField(verbose_name="告警审核说明", max_length=255, null=True, blank=True)

    alarm_type = models.ForeignKey(AlarmType, on_delete=models.CASCADE, verbose_name="告警类型")
    alarm_level = models.ForeignKey(AlarmLevel, on_delete=models.CASCADE, verbose_name="告警级别")
    alarm_scene = models.ForeignKey(Scene, on_delete=models.CASCADE, verbose_name="所属场景", default=1)

    class Meta:
        verbose_name = "告警表"

    def __str__(self):
        return self.device
