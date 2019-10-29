from rest_framework import generics, status
from rest_framework.response import Response

from videos.models import Videos
from videos.schemas import MonitorSchema, VideosSchema
from videos.serializers import MonitorSerializer, VideosSerializer, DeleteVideosSerializer


class MonitorView(generics.ListAPIView):
    """
    视频监控：分屏与独屏
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |page|分页|False|int|
    |tag|显示标志(0, "分屏"),(1, "独屏")|False|int|
    |name|视频名称|False|string|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |name|视频名称|--|string|
    |address|视频地址|--|string|

    #### 注意说明
    - 1 列表中均为视频的相关信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|返回视频信息列表|
    """
    queryset = Videos.objects.all()
    serializer_class = MonitorSerializer
    schema = MonitorSchema

    def get_queryset(self):
        # tag: 1表示独屏 0表示分屏
        tag = self.request.query_params.get("tag", 0)
        name = self.request.query_params.get("name", "")
        if tag:
            if name:
                self.queryset = Videos.objects.filter(name=name)
            else:
                # 默认视频为数据库中第一个视频
                self.queryset = Videos.objects.all()[0: 1]
        else:
            self.queryset = Videos.objects.all()[0: 4]

        return self.queryset


class VideosView(generics.ListAPIView):
    """
    所有视频信息
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |page|分页|False|int|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|视频id|--|int|
    |name|视频名称|--|string|
    |address|视频地址|--|string|
    |addtime|视频添加时间|--|string|
    |detail|视频描述|--|string|
    |username|用户名（和当前系统的用户无关）|--|string|
    |password|用户密码（和当前系统的用户密码无关）|--|string|

    #### 注意说明
    - 1 列表中均为视频的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|返回视频信息列表|
    """
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer


class AddVideosView(generics.CreateAPIView):
    """
    添加视频信息
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |name|视频名称|True|string|
    |username|用户名称|True|string|
    |password|用户密码|True|string|
    |address|视频地址信息|True|string|
    |detail|视频描述|True|string|


    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 存储视频的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|响应状态|
    """
    serializer_class = VideosSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(data={"code": 400, "message": "视频添加失败！"}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        resp = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        resp["code"] = 200
        resp["message"] = "视频添加成功！"
        return resp


class UpdateVideosView(generics.GenericAPIView):
    """
    修改视频信息
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|视频id|True|int|
    |name|视频名称|True|string|
    |username|用户名称|True|string|
    |password|用户密码|True|string|
    |address|视频地址信息|True|string|
    |detail|视频描述|True|string|


    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 存储视频的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|响应状态|
    """
    queryset = Videos.objects.all()
    serializer_class = VideosSerializer
    schema = VideosSchema

    def post(self, request, *args, **kwargs):
        try:
            video = Videos.objects.get(pk=request.data.get("id"))
            video.name = request.data.get("name")
            address = request.data.get("address")
            username = request.data.get("username")
            password = request.data.get("password")
            detail = request.data.get("detail")
            after_address = username+password
            if after_address != address:
                raise TypeError
            video.address = address
            video.username = username
            video.password = password
            video.detail = detail
            video.save()
        except:
            return Response(data={"code": 400, "message": "视频信息修改失败！"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"code": 200, "message": "视频信息修改成功"}, status=status.HTTP_200_OK)


class DeleteVideosView(generics.GenericAPIView):
    """
    删除视频信息
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|视频id|True|int|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 删除的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|响应状态|
    """
    queryset = Videos.objects.all()
    serializer_class = DeleteVideosSerializer
    schema = VideosSchema

    def post(self, request, *args, **kwargs):
        try:
            Videos.objects.get(pk=request.data.get("id")).delete()
        except:
            return Response(data={"code": 400, "message": "视频信息删除失败！"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"code": 200, "message": "视频信息删除成功！"}, status=status.HTTP_200_OK)
