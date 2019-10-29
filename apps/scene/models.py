from datetime import datetime

from django.db import models


# Create your models here.
class Scene(models.Model):
    STATUS_CHOICE = (
        (1, "在线"),
        (0, "离线"),
    )

    addtime = models.DateTimeField(verbose_name="场景添加时间", default=datetime.now)
    name = models.CharField(verbose_name="场景名称", max_length=255, null=False, unique=True)
    code = models.CharField(verbose_name="场景识别码", max_length=255, null=False)
    status = models.IntegerField(verbose_name="场景状态", choices=STATUS_CHOICE, default=1)
    level = models.IntegerField(verbose_name="场景优先级", null=True, blank=True)
    password = models.CharField(verbose_name="网关密码", max_length=255)

    class Meta:
        verbose_name = "场景表"

    def __str__(self):
        return self.name


class Humidity(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="湿度传感器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='湿度更新时间')
    value = models.FloatField(verbose_name='湿度值')
    status = models.IntegerField(choices=STATUS1, verbose_name='传感器状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "湿度传感器"

    def __str__(self):
        return self.value


class Temperature(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="温度传感器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='温度更新时间')
    value = models.FloatField(verbose_name='温度值')
    status = models.IntegerField(choices=STATUS1, verbose_name='传感器状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "温度传感器"

    def __str__(self):
        return self.value


class Beam(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="光照强度传感器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='光照强度更新时间')
    value = models.FloatField(verbose_name='光照强度度值')
    status = models.IntegerField(choices=STATUS1, verbose_name='传感器状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "光照强度传感器"

    def __str__(self):
        return self.value


class Co2(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="Co2传感器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='二氧化碳传感器更新时间')
    value = models.FloatField(verbose_name='二氧化碳浓度值')
    status = models.IntegerField(choices=STATUS1, verbose_name='传感器状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "二氧化碳传感器"

    def __str__(self):
        return self.value


class Pm25(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="PM2.5传感器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='pm25更新时间')
    value = models.FloatField(verbose_name='pm25值')
    status = models.IntegerField(choices=STATUS1, verbose_name='pm25状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "PM2.5传感器"

    def __str__(self):
        return self.value


class Smoke(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="烟雾传感器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='烟雾更新时间')
    status = models.IntegerField(choices=STATUS1, verbose_name='烟雾状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "烟雾传感器"

    def __str__(self):
        return self.status


class Flame(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="火光传感器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='火光更新时间')
    status = models.IntegerField(choices=STATUS1, verbose_name='火光状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "火光传感器"

    def __str__(self):
        return self.status


class Methane(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="甲烷传感器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='甲烷更新时间')
    status = models.IntegerField(choices=STATUS1, verbose_name='甲烷状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "甲烷传感器"

    def __str__(self):
        return self.status


class Alarmlamp(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="报警灯", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='报警灯更新时间')
    status = models.IntegerField(choices=STATUS1, verbose_name='报警灯状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "报警灯"

    def __str__(self):
        return self.status


class Alertor(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="报警器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='报警器更新时间')
    status = models.IntegerField(choices=STATUS1, verbose_name='报警器状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "报警器"

    def __str__(self):
        return self.status


class Display(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="LCD显示屏", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='显示内容更新时间')
    content = models.CharField(max_length=255, default="当前无内容", verbose_name='显示内容')
    status = models.IntegerField(choices=STATUS1, verbose_name='设备状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "LCD显示器"

    def __str__(self):
        return self.content


class Light(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="灯光传感器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='灯光数据更新时间')
    status = models.IntegerField(choices=STATUS1, verbose_name='灯光状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "灯光传感器"

    def __str__(self):
        return self.status


class Pump(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="水泵传感器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='水泵更新时间')
    status = models.IntegerField(choices=STATUS1, verbose_name='水泵状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "水泵表"

    def __str__(self):
        return self.status


class Fan(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="风扇传感器", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='风扇更新时间')
    status = models.IntegerField(choices=STATUS1, verbose_name='风扇状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "风扇传感器"

    def __str__(self):
        return self.status


class Unlocking(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="开锁记录", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(verbose_name='开锁记录更新时间', default=datetime.now)
    username = models.CharField(verbose_name="开锁用户", max_length=255, null=True, blank=True)
    status = models.IntegerField(choices=STATUS1, verbose_name='开锁状态')
    close = models.DateTimeField(verbose_name='关锁时间')

    class Meta:
        verbose_name = "开锁记录表"

    def __str__(self):
        return self.status


class Invade(models.Model):
    STATUS1 = (
        (1, '正常'),
        (0, '异常')
    )
    STATUS2 = (
        (1, '在线'),
        (0, '离线')
    )
    name = models.CharField(default="入侵检测", max_length=255, verbose_name="表名")
    insert_time = models.DateTimeField(default=datetime.now, verbose_name='入侵检测更新时间')
    status = models.IntegerField(choices=STATUS1, verbose_name='入侵状态')
    online = models.IntegerField(choices=STATUS2, verbose_name='在线状态')

    class Meta:
        verbose_name = "入侵检测"

    def __str__(self):
        return self.status
