import coreapi
import coreschema
from rest_framework.schemas import AutoSchema


token_field = coreapi.Field(
    name="Authorization",
    required=False,
    location="head",
    schema=coreschema.String(),
    description="格式：JWT 值",
)

TokenSchema = AutoSchema([
    token_field
])

UpdateSceneSchema = AutoSchema([
    coreapi.Field("id",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="场景id"),
    coreapi.Field("name",
                  required=True,
                  location="form",
                  schema=coreschema.String(),
                  description="场景名称"),
    coreapi.Field("code",
                  required=True,
                  location="form",
                  schema=coreschema.String(),
                  description="场景识别码"),
    coreapi.Field("password",
                  required=True,
                  location="form",
                  schema=coreschema.String(),
                  description="网关密码"),
    coreapi.Field("level",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="优先级"),
])

DeleteSceneSchema = AutoSchema([
    coreapi.Field("id",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="场景id"),
])

AddSceneSchema = AutoSchema([
    coreapi.Field("name",
                  required=True,
                  location="form",
                  schema=coreschema.String(),
                  description="场景名称"),
    coreapi.Field("code",
                  required=True,
                  location="form",
                  schema=coreschema.String(),
                  description="场景识别码"),
    coreapi.Field("password",
                  required=True,
                  location="form",
                  schema=coreschema.String(),
                  description="网关密码"),
    coreapi.Field("level",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="优先级"),
])

HistoryTimeSchema = AutoSchema([
    coreapi.Field("tag",
                  required=True,
                  location="query",
                  schema=coreschema.Integer(),
                  description="设备标志(1, '温度'),(2， '湿度'),(3, '光照强度'),(4, 'CO2'),(5, 'PM2.5')"),
    coreapi.Field("startTime",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="开始时间"),
    coreapi.Field("endTime",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="结束时间"),
])
TagSchema = AutoSchema([
    coreapi.Field("tag",
                  required=True,
                  location="query",
                  schema=coreschema.Integer(),
                  description="设备标志(1, '温度'),(2， '湿度'),(3, '光照强度'),(4, 'CO2'),(5, 'PM2.5')"),
])

HistoryTimeSchema1 = AutoSchema([
    coreapi.Field("startTime",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="开始时间"),
    coreapi.Field("endTime",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="结束时间"),
])

UpdateDisplaySchema = AutoSchema([
    coreapi.Field("id",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="当前显示大屏记录的id"),
    coreapi.Field("content",
                  required=True,
                  location="form",
                  schema=coreschema.String(),
                  description="修改显示大屏的内容"),
])
