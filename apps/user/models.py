from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserInfo(models.Model):
    GENDER_CHOICE = (
        (1, "male"),
        (2, "female"),
        (3, "secret"),
        (4, "unknown"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    account = models.CharField(verbose_name="用户账号", max_length=255, unique=True, null=False)
    userNo = models.CharField(verbose_name="用户工号", max_length=255, unique=True, null=False)
    telephone = models.CharField(verbose_name="用户手机号", max_length=11, unique=True)
    gender = models.IntegerField(verbose_name="用户性别", choices=GENDER_CHOICE)
    detail = models.CharField(verbose_name="用户描述", max_length=255, null=True, blank=True)
    avatar = models.ImageField(verbose_name="用户头像", upload_to="upload/user/%Y/&m", null=True, blank=True)
    address = models.CharField(verbose_name="用户地址", max_length=255, null=True, blank=True)
