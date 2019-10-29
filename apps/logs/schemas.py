import coreapi
import coreschema
from rest_framework.schemas import AutoSchema, ManualSchema

token_field = coreapi.Field(
                name="Authorization",
                required=False,
                location="header",
                schema=coreschema.String(),
                description="格式：JWT 值",
        )
TokenSchema = AutoSchema([
                token_field
        ]
)

LogsSchema = AutoSchema([
    # token_field
    # 设置前台传的参数名称、约束选项、方式、传参类型、描述等
    coreapi.Field("scene",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="所属场景", ),
    coreapi.Field("log_module",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="所属模块", ),
    coreapi.Field("begin",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="开始时间", ),
    coreapi.Field("end",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="结束时间", ),
    coreapi.Field("content",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="日志内容", ),
])

LogsOutputSchema = AutoSchema([
    coreapi.Field("startTime",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="开始时间", ),
    coreapi.Field("endTime",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="结束时间", ),
])
