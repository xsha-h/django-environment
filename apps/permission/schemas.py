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

UpdatePermissionSchema = AutoSchema([
    coreapi.Field("id",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="角色的id"),
    coreapi.Field("names",
                  required=True,
                  location="form",
                  schema=coreschema.String(),
                  description="权限或者名称,以逗号隔开"),
    coreapi.Field("tag",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="角色修改标志(1, ‘修改权限’),(2, '修改用户')"),
])

DeletePermissionSchema = AutoSchema([
    coreapi.Field("id",
                  required=True,
                  location="form",
                  schema=coreschema.Integer(),
                  description="角色的id"),
])

AddPermissionSchema = AutoSchema([
    coreapi.Field("role_name",
                  required=True,
                  location="form",
                  schema=coreschema.String(),
                  description="角色的名称"),
    coreapi.Field("permission_names",
                  location="form",
                  schema=coreschema.String(),
                  description="权限名称，以逗号隔开"),
    coreapi.Field("user_names",
                  location="form",
                  schema=coreschema.String(),
                  description="用户名称，以逗号隔开"),
])
