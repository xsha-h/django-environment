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

AccessSchema = AutoSchema([
    coreapi.Field("status",
                  required=False,
                  location="query",
                  schema=coreschema.Integer(),
                  description="申请状态", ),
    coreapi.Field("start",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="申请开始时间", ),
    coreapi.Field("end",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="申请结束时间", ),
    coreapi.Field("approval_start",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="审批开始时间", ),
    coreapi.Field("approval_end",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="审批结束时间", ),
])
UpdateAccessSchema = AutoSchema([
    coreapi.Field("id",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="门禁id", ),
    coreapi.Field("tag",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="审批处理标志", ),
])

AccessRateSchema = AutoSchema([
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
