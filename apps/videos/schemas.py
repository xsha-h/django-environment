import coreapi
import coreschema
from rest_framework.schemas import AutoSchema

token_field = coreapi.Field(
    name="Authorization",
    required=False,
    location="header",
    schema=coreschema.String(),
    description="格式：JWT 值",
)
TokenSchema = AutoSchema([
    token_field
])

# 视频监控过滤
MonitorSchema = AutoSchema([
    coreapi.Field("tag",
                  required=False,
                  location="query",
                  schema=coreschema.Integer(),
                  description="显示标志", ),

    coreapi.Field("name",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="视频名称", ),
])

# 视频信息过滤
VideosSchema = AutoSchema([
    coreapi.Field("id",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="视频id", ),
])

