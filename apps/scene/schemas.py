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
