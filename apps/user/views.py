from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from user.models import UserInfo
from user.schemas import AddUserSchema, UpdateUserSchema, DeleteUserSchema
from user.serializers import UserSerializer, UserInfoSerializer, AddUserSerializer, UpdateUserSerializer


class UserView(generics.ListAPIView):
    """
    用户信息：条件可选
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |page|分页|False|int|
    |search|模糊查询用户名|False|string|


    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|用户信息id|--|int|
    |user1|用户外表|--|object|
    |password|用户密码可忽略|--|string|
    |last_login|上次登录时间|--|string|
    |is_superuser|是否是超级用户|--|bool|
    |username|用户名称|--|string|
    |first_name|用户祖姓|--|string|
    |last_name|用户名字--|string|
    |email|用户邮箱|--|email|
    |is_staff|是否是用户成员|--|bool|
    |is_active|活跃状态|--|bool|
    |date_joined|用户信息添加时间|--|string|
    |group|用户分组|--|array|
    |user_permissions|用户权限|--|array|

    #### 注意说明
    - 1 列表中均为用户的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|返回门禁信息列表|
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    search_fields = ("username", )


class AddUserView(generics.CreateAPIView):
    """
    添加用户信息
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |address|用户地址信息|True|string|
    |account|用户账号|True|string|
    |password|用户密码|True|string|
    |username|用户名称|True|string|
    |telephone|用户手机号码|True|string|
    |gender|用户性别(1, "male"),(2, "female"),(3, "secret"),(4, "unknown")|True|int|
    |is_active|用户性别(1, "活跃"),(0, "冻结")|True|int|
    |userNo|用户工号|True|string|
    |detail|用户描述|True|string|
    |avatar|用户头像|True|file|


    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 存储用户的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|响应状态|
    """
    serializer_class = AddUserSerializer
    schema = AddUserSchema

    def post(self, request, *args, **kwargs):
        try:
            password = self.request.data.get("password")
            username = self.request.data.get("username")
            is_active = self.request.data.get("is_active")
            account = self.request.data.get("account")
            telephone = self.request.data.get("telephone")
            gender = self.request.data.get("gender")
            userNo = self.request.data.get("userNo")
            address = self.request.data.get("address")
            detail = self.request.data.get("detail")
            avatar = self.request.data.get("avatar")
            user = User(username=username, password=make_password(password), is_active=is_active)
            user.save()
            userInfo = UserInfo(account=account, telephone=telephone, gender=gender,
                                userNo=userNo, address=address, detail=detail, avatar=avatar)
            userInfo.user = user
            userInfo.save()
        except:
            return Response(data={"code": 400, "message": "新增用户失败！"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"code": 200, "message": "新增用户成功"}, status=status.HTTP_201_CREATED)


class UpdateUserView(generics.GenericAPIView):
    """
    修改用户信息
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|用户id|True|int|
    |address|用户地址信息|True|string|
    |username|用户名称|True|string|
    |telephone|用户手机号码|True|string|
    |gender|用户性别(1, "male"),(2, "female"),(3, "secret"),(4, "unknown")|True|int|
    |is_active|用户性别(1, "活跃"),(0, "冻结")|True|int|
    |detail|用户描述|True|string|
    |avatar|用户头像|True|file|


    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 存储用户的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|响应状态|
    """
    serializer_class = UpdateUserSerializer
    schema = UpdateUserSchema

    def post(self, request, *args, **kwargs):
        try:
            id = self.request.data.get("id")
            username = self.request.data.get("username")
            telephone = self.request.data.get("telephone")
            gender = self.request.data.get("gender")
            is_active = self.request.data.get("is_active")
            address = self.request.data.get("address")
            detail = self.request.data.get("detail")
            avatar = self.request.data.get("avatar")
            userInfo = UserInfo.objects.get(pk=id)
            userInfo.telephone = telephone
            userInfo.gender = gender
            userInfo.address = address
            userInfo.detail = detail
            userInfo.avatar = avatar
            user = User.objects.get(pk=userInfo.user_id)
            user.username = username
            user.is_active = is_active
            user.save()
            userInfo.save()
        except:
            return Response(data={"code": 400, "message": "用户信息修改失败！"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"code": 200, "message": "用户信息修改成功！"}, status=status.HTTP_200_OK)


class DeleteUserView(generics.GenericAPIView):
    """
    删除用户信息
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|用户id|True|int|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 删除用户的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|响应状态|
    """
    serializer_class = UpdateUserSerializer
    schema = DeleteUserSchema

    def post(self, request, *args, **kwargs):
        id  = self.request.data.get("id")
        try:
            userInfo = UserInfo.objects.get(pk=id)

            temp_id = userInfo.user_id
            user = User.objects.get(pk=temp_id)
            if not user.is_active:
                userInfo.delete()
                user.delete()
            else:
                return Response(data={"code": 400, "message": "用户信息删除失败！"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={"code": 400, "message": "用户信息删除失败！"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"code": 200, "message": "用户信息删除成功！"}, status=status.HTTP_200_OK)


class ActivateUserView(generics.GenericAPIView):
    """
    激活与冻结用户
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|用户id|True|int|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 存储用户的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|响应状态|
    """
    serializer_class = UpdateUserSerializer
    schema = DeleteUserSchema

    def post(self, request, *args, **kwargs):
        id = self.request.data.get("id")
        userInfo = UserInfo.objects.get(pk=id)
        user = User.objects.get(pk=userInfo.user_id)
        user.is_active = not user.is_active
        user.save()
        if user.is_active:
            message = "已激活"
        else:
            message = "已冻结"
        return Response(data={"code": 200, "message": message})
