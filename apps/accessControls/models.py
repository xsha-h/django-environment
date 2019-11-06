from datetime import datetime

from django.db import models


# Create your models here.
class Accesses(models.Model):
    APPLY_CHOICE = (
        (1, "待审核"),
        (2, "已通过"),
        (3, "已拒绝"),
    )
    addtime = models.DateTimeField(verbose_name="门禁申请时间", default=datetime.now)
    username = models.CharField(verbose_name="用户申请人", max_length=255)
    start_time = models.DateTimeField(verbose_name="申请开始时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="申请结束时间", null=True, blank=True)
    follow_users = models.CharField(verbose_name="随行人员", max_length=255)
    follow_nums = models.IntegerField(verbose_name="随性人数")
    detail = models.CharField(verbose_name="申请说明", max_length=255)
    status = models.IntegerField(verbose_name="申请状态", choices=APPLY_CHOICE, default=1)
    approval_time = models.DateTimeField(verbose_name="审批时间", null=True, blank=True)
    approval_user = models.CharField(verbose_name="审批人", max_length=255, null=True, blank=True)
    feedback = models.CharField(verbose_name="审批反馈", max_length=255)

    class Meta:
        verbose_name = "门禁审批表"
        permissions = (
            ("access_view", "门禁信息查看"),
            ("add_access", "门禁信息申请"),
            ("update_access", "门禁信息处理"),
        )

    def __str__(self):
        return self.detail
