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

AlarmSchema = AutoSchema([
    coreapi.Field("type_id",
                  required=False,
                  location="query",
                  schema=coreschema.Integer(),
                  description="告警类型id",),
    coreapi.Field("level_id",
                  required=False,
                  location="query",
                  schema=coreschema.Integer(),
                  description="告警级别id",),
    coreapi.Field("scene_id",
                  required=False,
                  location="query",
                  schema=coreschema.Integer(),
                  description="所属场景id",),
    coreapi.Field("status",
                  required=False,
                  location="query",
                  schema=coreschema.Integer(),
                  description="确认状态",),
    coreapi.Field("start_time",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="开始时间",),
    coreapi.Field("end_time",
                  required=False,
                  location="query",
                  schema=coreschema.String(),
                  description="结束时间",),
])

DealAlarmSchema = AutoSchema([
    coreapi.Field("id",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="告警id",),
    coreapi.Field("deal_detail",
                  required=False,
                  location="form",
                  schema=coreschema.String(),
                  description="告警处理说明",),
])

AuditAlarmSchema = AutoSchema([
    coreapi.Field("id",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="告警id",),
    coreapi.Field("status",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="告警状态", ),
    coreapi.Field("audit_detail",
                  required=False,
                  location="form",
                  schema=coreschema.String(),
                  description="告警审核说明",),
])

DealManyAlarmSchema = AutoSchema([
    coreapi.Field("ids",
                  required=True,
                  location="form",
                  schema=coreschema.String(),
                  description="告警信息id集以逗号隔开"),
    coreapi.Field("type_id",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="告警类型id"),
    coreapi.Field("content",
                  required=False,
                  location="form",
                  schema=coreschema.String(),
                  description="说明"),
])

AuditManyAlarmSchema = AutoSchema([
    coreapi.Field("ids",
                  required=True,
                  location="form",
                  schema=coreschema.String(),
                  description="告警信息id集以逗号隔开"),
    coreapi.Field("type_id",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="告警类型id"),
    coreapi.Field("content",
                  required=False,
                  location="form",
                  schema=coreschema.String(),
                  description="说明"),
    coreapi.Field("status",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="审核状态：3表示审核通过，4表示审核不通过"),
])

AlarmRateSchema = AutoSchema([
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

AlarmStatusSchema = AutoSchema([
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
    coreapi.Field("type_id",
                  required=True,
                  location="query",
                  schema=coreschema.Integer(),
                  description="告警类型id")
])

AlarmOutputSchema = AutoSchema([
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
