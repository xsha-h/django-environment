from django.db import connection
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from scene.schemas import UpdateSceneSchema, DeleteSceneSchema, AddSceneSchema
from scene.serializers import SceneSerializer, UpdateSceneSerializer
from .models import *


class SceneDeviceView(APIView):
    """
    场景设备界面
    """

    def get(self, request):
        # 实时消防监测设备
        smoke = Smoke.objects.last()
        flame = Flame.objects.last()
        methane = Methane.objects.last()
        alarmlamp = Alarmlamp.objects.last()
        alertor = Alertor.objects.last()

        # 实时环境监测设备
        humidity = Humidity.objects.last()
        temperature = Temperature.objects.last()
        beam = Beam.objects.last()
        co2 = Co2.objects.last()
        pm25 = Pm25.objects.last()

        # 实时显示大屏设备
        lcd = Display.objects.last()

        # 实时设备监测设备
        light = Light.objects.last()
        fan = Fan.objects.last()
        pump = Pump.objects.last()

        # 实时安防监测设备
        unlockings = Unlocking.objects.all()
        if len(unlockings) <= 4:
            unlockings = Unlocking.objects.all()
        else:
            unlockings = Unlocking.objects.all()[-5:]
        unlocking_list = []
        for unlock in unlockings:
            lock_dict = {}
            lock_dict["username"] = unlock.username
            lock_dict["insert_time"] = unlock.insert_time
            unlocking_list.append(lock_dict)

        # 入侵监测
        invade = Invade.objects.last()

        res_dict = {
            "实时消防监测": [
                {
                    "name": smoke.name,
                    "status": "正常" if smoke.status else "异常",
                },
                {
                    "name": flame.name,
                    "status": "正常" if flame.status else "异常",
                },
                {
                    "name": methane.name,
                    "status": "正常" if methane.status else "异常",
                },
                {
                    "name": alarmlamp.name,
                    "status": "正常" if alarmlamp.status else "异常",
                },
                {
                    "name": alertor.name,
                    "status": "关" if alertor.status else "开",
                },
            ],
            "实时环境监测": [
                {
                    "name": humidity.name,
                    "status": "在线" if humidity.status else "离线",
                    "value": humidity.value,
                },
                {
                    "name": temperature.name,
                    "status": "在线" if temperature.status else "离线",
                    "value": temperature.value,
                },
                {
                    "name": beam.name,
                    "status": "在线" if beam.status else "离线",
                    "value": beam.value,
                },
                {
                    "name": co2.name,
                    "status": "在线" if co2.status else "离线",
                    "value": co2.value,
                },
                {
                    "name": pm25.name,
                    "status": "在线" if pump.status else "离线",
                    "value": pm25.value,
                },
            ],
            "实时显示大屏": {
                "name": lcd.name,
                "content": lcd.content,
            },
            "实时设备监测": [
                {
                    "name": light.name,
                    "status": "开" if light.status else "关",
                },
                {
                    "name": fan.name,
                    "status": "开" if fan.status else "关",
                },
                {
                    "name": pump.name,
                    "status": "开" if pump.status else "关",
                },
            ],
            "实时安防监测": {
                "name": unlockings[0].name,
                "record": unlocking_list,
            },
            "入侵监测": {
                "name": invade.name,
                "status": "正常" if invade.status else "异常",
            },
        }
        return Response(res_dict)


class SceneView(generics.ListAPIView):
    """
    场景设置界面
    """
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer


class UpdateSceneView(generics.GenericAPIView):
    """
    修改场景
    """
    queryset = Scene.objects.all()
    serializer_class = UpdateSceneSerializer
    schema = UpdateSceneSchema

    def post(self, request):
        id = request.data.get("id")
        name = request.data.get("name")
        code = request.data.get("code")
        password = request.data.get("password")
        level = request.data.get("level")

        try:
            scene = Scene.objects.get(pk=id)
            scene.name = name
            scene.code = code
            scene.password = password
            scene.level = level
            scene.save()
        except:
            return Response(data={"code": 400, "message": "场景修改失败"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"code": 200, "message": "场景修改成功"}, status=status.HTTP_200_OK)


class DeleteSceneView(generics.GenericAPIView):
    """
    删除场景
    """
    queryset = Scene.objects.all()
    serializer_class = UpdateSceneSerializer
    schema = DeleteSceneSchema

    def post(self, request):
        id = request.data.get("id")

        try:
            scene = Scene.objects.get(pk=id)
            scene.delete()
        except:
            return Response(data={"code": 400, "message": "场景删除失败"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"code": 200, "message": "场景删除成功"}, status=status.HTTP_200_OK)


class AddSceneView(generics.GenericAPIView):
    """
    新增场景
    """
    queryset = Scene.objects.all()
    serializer_class = UpdateSceneSerializer
    schema = AddSceneSchema

    def post(self, request):
        name = request.data.get("name")
        code = request.data.get("code")
        password = request.data.get("password")
        level = request.data.get("level")

        try:
            scene = Scene()
            scene.name = name
            scene.code = code
            scene.password = password
            scene.level = level
            scene.save()
        except:
            return Response(data={"code": 400, "message": "场景新增失败"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"code": 200, "message": "场景新增成功"}, status=status.HTTP_200_OK)


class SceneStatusView(APIView):
    """
    场景状态
    """

    def get(self, request):
        sql = """
            select name, status, addtime
            from scene_scene;
        """
        cursor = connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        cursor.close()
        res_list = []
        for i in res:
            res_dict = {}
            res_dict["name"] = i[0]
            res_dict["status"] = "在线" if i[1] else "离线"
            res_dict["time"] = i[2].strftime("%Y-%m-%d")
            res_list.append(res_dict)
        return Response(res_list)


class DeviceView(APIView):
    """
    设备部分信息
    """

    def get(self, request):
        # 实时消防监测设备
        smoke = Smoke.objects.last()
        flame = Flame.objects.last()
        methane = Methane.objects.last()
        alarmlamp = Alarmlamp.objects.last()
        alertor = Alertor.objects.last()

        # 实时环境监测设备
        humidity = Humidity.objects.last()
        temperature = Temperature.objects.last()
        beam = Beam.objects.last()
        co2 = Co2.objects.last()
        pm25 = Pm25.objects.last()

        # 实时显示大屏设备
        lcd = Display.objects.last()

        # 实时设备监测设备
        light = Light.objects.last()
        fan = Fan.objects.last()
        pump = Pump.objects.last()

        # 入侵监测
        invade = Invade.objects.last()

        res_list = [
            {
                "name": smoke.name,
                "status": "正常" if smoke.status else "异常",
                "time": smoke.insert_time,
            },
            {
                "name": flame.name,
                "status": "正常" if flame.status else "异常",
                "time": flame.insert_time,
            },
            {
                "name": methane.name,
                "status": "正常" if methane.status else "异常",
                "time": methane.insert_time,
            },
            {
                "name": alarmlamp.name,
                "status": "正常" if alarmlamp.status else "异常",
                "time": alarmlamp.insert_time,
            },
            {
                "name": alertor.name,
                "status": "关" if alertor.status else "开",
                "time": alertor.insert_time,
            },
            {
                "name": humidity.name,
                "status": "在线" if humidity.status else "离线",
                "time": humidity.insert_time,
            },
            {
                "name": temperature.name,
                "status": "在线" if temperature.status else "离线",
                "time": temperature.insert_time,
            },
            {
                "name": beam.name,
                "status": "在线" if beam.status else "离线",
                "time": beam.insert_time,
            },
            {
                "name": co2.name,
                "status": "在线" if co2.status else "离线",
                "time": co2.insert_time,
            },
            {
                "name": pm25.name,
                "status": "在线" if pm25.status else "离线",
                "time": pm25.insert_time,
            },
            {
                "name": lcd.name,
                "status": "正常" if lcd.status else "异常",
                "time": lcd.insert_time,
            },
            {
                "name": light.name,
                "status": "开" if light.status else "关",
                "time": light.insert_time,
            },
            {
                "name": fan.name,
                "status": "开" if fan.status else "关",
                "time": fan.insert_time,
            },
            {
                "name": pump.name,
                "status": "开" if pump.status else "关",
                "time": pump.insert_time,
            },
            {
                "name": invade.name,
                "status": "正常" if invade.status else "异常",
                "time": invade.insert_time,
            },
        ]
        res_dict = {
            "result": res_list
        }
        return Response(res_dict)
