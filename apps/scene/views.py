
from django.db import connection
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from alarmdatas import getAlarmDatas
from fetchdata import dictfetchall
from historydatas import getHistoryDatas
from recentdatas import getRecentDatas
from scene.schemas import UpdateSceneSchema, DeleteSceneSchema, AddSceneSchema, HistoryTimeSchema, UpdateDisplaySchema, \
    TagSchema, HistoryTimeSchema1
from scene.serializers import SceneSerializer, UpdateSceneSerializer, DisplaySerializer
from .models import *
import datetime


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


class FireHistoryView(generics.GenericAPIView):
    """
    消防设备历史数据
    """
    queryset = None
    schema = HistoryTimeSchema1

    def get(self, request):
        start = request.query_params.get("startTime")
        end = request.query_params.get("endTime")
        cursor = connection.cursor()
        methane_sql = """
            select name, insert_time, status
            from scene_methane;
        """
        flame_sql = """
            select name, insert_time, status
            from scene_flame;
        """
        smoke_sql = """
            select name, insert_time, status
            from scene_smoke;
        """
        alarmlamp_sql = """
            select name, insert_time, status
            from scene_alarmlamp;
        """
        alertor_sql = """
            select name, insert_time, status
            from scene_alertor;
        """
        if start and end:
            methane_sql = """
                select name, insert_time, status
                from scene_methane
                where insert_time>='{}' and insert_time<='{}'
            """.format(start, end)
            flame_sql = """
                select name, insert_time, status
                from scene_flame
                where insert_time>='{}' and insert_time<='{}'
            """.format(start, end)
            smoke_sql = """
                select name, insert_time, status
                from scene_smoke
                where insert_time>='{}' and insert_time<='{}'
            """.format(start, end)
            alarmlamp_sql = """
                select name, insert_time, status
                from scene_alarmlamp
                where insert_time>='{}' and insert_time<='{}'
            """.format(start, end)
            alertor_sql = """
                select name, insert_time, status
                from scene_alertor
                where insert_time>='{}' and insert_time<='{}'
            """.format(start, end)

        res_list = []
        res_dict = {"result": res_list}
        array = [methane_sql, flame_sql, smoke_sql, alarmlamp_sql, alertor_sql]
        for arr in array:
            temp_dict = {}
            cursor.execute(arr)
            res = cursor.fetchall()
            for i in res:
                temp_dict["name"] = i[0]
                temp_dict["time"] = i[1].strftime("%Y-%m-%d")
                temp_dict["status"] = "正常" if i[2] else "异常"
                res_list.append(temp_dict)

        cursor.close()
        return Response(res_dict)


class FireRecentView(generics.GenericAPIView):
    """
    消防设备最近一周的状态
    """
    queryset = None

    def get(self, request):
        cursor = connection.cursor()

        # 最近7天的日期
        one_day = datetime.datetime.now()
        two_day = one_day - datetime.timedelta(days=1)
        three_day = one_day - datetime.timedelta(days=2)
        four_day = one_day - datetime.timedelta(days=3)
        five_day = one_day - datetime.timedelta(days=4)
        six_day = one_day - datetime.timedelta(days=5)
        seven_day = one_day - datetime.timedelta(days=6)
        days = [one_day, two_day, three_day, four_day, five_day, six_day, seven_day]

        # 最近7天的数据
        res_dict = {"周一": [], "周二": [], "周三": [], "周四": [], "周五": [], "周六": [], "周日": []}
        for day in days:
            methane_sql = """
                select name, status
                from scene_methane
                where insert_time like '%{}%'
                order by insert_time desc
                limit 1;
            """.format(day.strftime("%Y-%m-%d"))
            flame_sql = """
                select name, status
                from scene_flame
                where insert_time like '%{}%'
                order by insert_time desc
                limit 1;
            """.format(day.strftime("%Y-%m-%d"))
            smoke_sql = """
                select name, status
                from scene_smoke
                where insert_time like '%{}%'
                order by insert_time desc
                limit 1;
            """.format(day.strftime("%Y-%m-%d"))
            alarmlamp_sql = """
                select name, status
                from scene_alarmlamp
                where insert_time like '%{}%'
                order by insert_time desc
                limit 1;
            """.format(day.strftime("%Y-%m-%d"))
            alertor_sql = """
                select name, status
                from scene_alertor
                where insert_time like '%{}%'
                order by insert_time desc
                limit 1;
            """.format(day.strftime("%Y-%m-%d"))

            week = day.weekday()
            if week == 0:
                temp_list = res_dict["周一"]
            elif week == 1:
                temp_list = res_dict["周二"]
            elif week == 2:
                temp_list = res_dict["周三"]
            elif week == 3:
                temp_list = res_dict["周四"]
            elif week == 4:
                temp_list = res_dict["周五"]
            elif week == 5:
                temp_list = res_dict["周六"]
            else:
                temp_list = res_dict["周日"]

            array = [methane_sql, flame_sql, smoke_sql, alarmlamp_sql, alertor_sql]
            for arr in array:
                temp_dict = {}
                cursor.execute(arr)
                res = cursor.fetchone()
                if res:
                    temp_dict["name"] = res[0]
                    temp_dict["status"] = "正常" if res[1] else "异常"
                else:
                    temp_dict["name"] = ""
                    temp_dict["status"] = ""
                temp_list.append(temp_dict)
        return Response(res_dict)


class FireAlarmView(APIView):
    """
    消防设备告警统计报表
    """

    def get(self, request):
        cursor = connection.cursor()
        sql = """
            select device, TIMESTAMPDIFF(MINUTE,addtime,deal_time) as minute
            from alarm_alarm
            where device="甲烷传感器" or device="火光传感器" or device="烟雾传感器" 
            or device="报警灯" or device="报警器";
        """

        cursor.execute(sql)
        res_list = dictfetchall(cursor)
        res_dict = {"results": res_list}
        cursor.close()
        return Response(res_dict)


class HistoryView(generics.GenericAPIView):
    """
    历史数据
    """
    queryset = None
    schema = HistoryTimeSchema

    def get(self, request):
        start = request.query_params.get("startTime")
        end = request.query_params.get("endTime")
        tag = int(request.query_params.get("tag"))
        cursor = connection.cursor()

        res_dict = getHistoryDatas(cursor, tag, start, end)
        print(res_dict)
        cursor.close()
        return Response(res_dict)


class RecentView(generics.GenericAPIView):
    """
    最近一周的数据
    """
    queryset = None
    schema = TagSchema

    def get(self, request):
        tag = int(request.query_params.get("tag"))
        cursor = connection.cursor()

        res_dict = getRecentDatas(cursor, tag)
        cursor.close()
        return Response(res_dict)


class AlarmView(APIView):
    """
    报警统计表
    """
    schema = TagSchema

    def get(self, request):
        tag = int(request.query_params.get("tag"))
        cursor = connection.cursor()
        res_dict = getAlarmDatas(cursor, tag)
        cursor.close()
        return Response(res_dict)


# class TemperatureHistoryView(generics.GenericAPIView):
#     """
#     温度历史数据
#     """
#     queryset = None
#     schema = HistoryTimeSchema
#
#     def get(self, request):
#         start = request.query_params.get("startTime")
#         end = request.query_params.get("endTime")
#         cursor = connection.cursor()
#         tablename = "scene_temperature"
#
#         res_dict = getHistoryDatas(cursor, tablename, start, end)
#         cursor.close()
#         return Response(res_dict)
#
#
# class TemperatureRecentView(generics.GenericAPIView):
#     """
#     温度最近一周的数据
#     """
#     queryset = None
#
#     def get(self, request):
#         cursor = connection.cursor()
#         tablename = "scene_temperature"
#
#         res_dict = getRecentDatas(cursor, tablename)
#         cursor.close()
#         return Response(res_dict)
#
#
# class TemperatureAlarmView(APIView):
#     """
#     温度报警统计表
#     """
#
#     def get(self, request):
#         cursor = connection.cursor()
#         device = "温度传感器"
#         res_dict = getAlarmDatas(cursor, device)
#         cursor.close()
#         return Response(res_dict)
#
#
# class HumidityHistoryView(generics.GenericAPIView):
#     """
#     湿度历史数据
#     """
#     queryset = None
#     schema = HistoryTimeSchema
#
#     def get(self, request):
#         start = request.query_params.get("startTime")
#         end = request.query_params.get("endTime")
#         cursor = connection.cursor()
#         tablename = "scene_humidity"
#
#         res_dict = getHistoryDatas(cursor, tablename, start, end)
#         cursor.close()
#         return Response(res_dict)
#
#
# class HumidityRecentView(generics.GenericAPIView):
#     """
#     湿度最近一周的数据
#     """
#     queryset = None
#
#     def get(self, request):
#         cursor = connection.cursor()
#         tablename = "scene_humidity"
#
#         res_dict = getRecentDatas(cursor, tablename)
#         cursor.close()
#         return Response(res_dict)
#
#
# class HumidityAlarmView(APIView):
#     """
#     温度报警统计表
#     """
#
#     def get(self, request):
#         cursor = connection.cursor()
#         device = "湿度传感器"
#         res_dict = getAlarmDatas(cursor, device)
#         cursor.close()
#         return Response(res_dict)
#
#
# class BeamHistoryView(generics.GenericAPIView):
#     """
#     光照强度历史数据
#     """
#     queryset = None
#     schema = HistoryTimeSchema
#
#     def get(self, request):
#         start = request.query_params.get("startTime")
#         end = request.query_params.get("endTime")
#         cursor = connection.cursor()
#         tablename = "scene_beam"
#
#         res_dict = getHistoryDatas(cursor, tablename, start, end)
#         cursor.close()
#         return Response(res_dict)
#
#
# class BeamRecentView(generics.GenericAPIView):
#     """
#     光照强度最近一周的数据
#     """
#     queryset = None
#
#     def get(self, request):
#         cursor = connection.cursor()
#         tablename = "scene_beam"
#
#         res_dict = getRecentDatas(cursor, tablename)
#         cursor.close()
#         return Response(res_dict)
#
#
# class BeamAlarmView(APIView):
#     """
#     光照强度报警统计表
#     """
#
#     def get(self, request):
#         cursor = connection.cursor()
#         device = "光照强度传感器"
#         res_dict = getAlarmDatas(cursor, device)
#         cursor.close()
#         return Response(res_dict)
#
#
# class CO2HistoryView(generics.GenericAPIView):
#     """
#     CO2历史数据
#     """
#     queryset = None
#     schema = HistoryTimeSchema
#
#     def get(self, request):
#         start = request.query_params.get("startTime")
#         end = request.query_params.get("endTime")
#         cursor = connection.cursor()
#         tablename = "scene_co2"
#
#         res_dict = getHistoryDatas(cursor, tablename, start, end)
#         cursor.close()
#         return Response(res_dict)
#
#
# class CO2RecentView(generics.GenericAPIView):
#     """
#     CO2最近一周的数据
#     """
#     queryset = None
#
#     def get(self, request):
#         cursor = connection.cursor()
#         tablename = "scene_co2"
#
#         res_dict = getRecentDatas(cursor, tablename)
#         cursor.close()
#         return Response(res_dict)
#
#
# class CO2AlarmView(APIView):
#     """
#     CO2报警统计表
#     """
#
#     def get(self, request):
#         cursor = connection.cursor()
#         device = "CO2传感器"
#         res_dict = getAlarmDatas(cursor, device)
#         cursor.close()
#         return Response(res_dict)
#
#
# class PM25HistoryView(generics.GenericAPIView):
#     """
#     PM2.5历史数据
#     """
#     queryset = None
#     schema = HistoryTimeSchema
#
#     def get(self, request):
#         start = request.query_params.get("startTime")
#         end = request.query_params.get("endTime")
#         cursor = connection.cursor()
#         tablename = "scene_pm25"
#
#         res_dict = getHistoryDatas(cursor, tablename, start, end)
#         cursor.close()
#         return Response(res_dict)
#
#
# class PM25RecentView(generics.GenericAPIView):
#     """
#     PM2.5最近一周的数据
#     """
#     queryset = None
#
#     def get(self, request):
#         cursor = connection.cursor()
#         tablename = "scene_pm25"
#
#         res_dict = getRecentDatas(cursor, tablename)
#         cursor.close()
#         return Response(res_dict)
#
#
# class PM25AlarmView(APIView):
#     """
#     PM2.5报警统计表
#     """
#
#     def get(self, request):
#         cursor = connection.cursor()
#         device = "PM2.5传感器"
#         res_dict = getAlarmDatas(cursor, device)
#         cursor.close()
#         return Response(res_dict)


class DisplayView(APIView):
    """
    实时显示大屏
    """

    def get(self, request):
        cursor = connection.cursor()
        sql = """
            select id, content
            from scene_display
            order by insert_time desc
            limit 1;
        """
        cursor.execute(sql)
        res_dict = dictfetchall(cursor)
        cursor.close()
        return Response(res_dict)


class UpdateDisplayView(generics.GenericAPIView):
    """
    大屏信息修改
    """
    queryset = Display.objects.all()
    serializer_class = DisplaySerializer
    schema = UpdateDisplaySchema

    def post(self, request):
        try:
            id = request.data.get("id")
            content = request.data.get("content")
            query_obj = Display.objects.get(pk=id)
            query_obj.content = content
            query_obj.save()
        except:
            return Response(data={"code": 400, "message": "修改失败！"})
        return Response(data={"code": 200, "message": "修改成功！"})


class DeviceHistoryView(generics.GenericAPIView):
    """
    实时设备历史数据
    """
    queryset = None
    schema = HistoryTimeSchema

    def get(self, request):
        start = request.query_params.get("startTime")
        end = request.query_params.get("endTime")
        cursor = connection.cursor()
        fan_sql = """
            select name, insert_time, status
            from scene_fan
            where insert_time>='{}' and insert_time<='{}'
        """.format(start, end)
        pump_sql = """
            select name, insert_time, status
            from scene_pump
            where insert_time>='{}' and insert_time<='{}'
        """.format(start, end)
        light_sql = """
            select name, insert_time, status
            from scene_light
            where insert_time>='{}' and insert_time<='{}'
        """.format(start, end)


        res_list = []
        res_dict = {"result": res_list}
        array = [fan_sql, pump_sql, light_sql]
        for arr in array:
            temp_dict = {}
            cursor.execute(arr)
            res = cursor.fetchall()
            for i in res:
                temp_dict["name"] = i[0]
                temp_dict["time"] = i[1].strftime("%Y-%m-%d")
                temp_dict["status"] = "开" if i[2] else "关"
                res_list.append(temp_dict)

        cursor.close()
        return Response(res_dict)


class DeviceRecentView(generics.GenericAPIView):
    """
    实时设备最近一周的状态
    """
    queryset = None

    def get(self, request):
        cursor = connection.cursor()

        # 最近7天的日期
        one_day = datetime.datetime.now()
        two_day = one_day - datetime.timedelta(days=1)
        three_day = one_day - datetime.timedelta(days=2)
        four_day = one_day - datetime.timedelta(days=3)
        five_day = one_day - datetime.timedelta(days=4)
        six_day = one_day - datetime.timedelta(days=5)
        seven_day = one_day - datetime.timedelta(days=6)
        days = [one_day, two_day, three_day, four_day, five_day, six_day, seven_day]

        # 最近7天的数据
        res_dict = {"周一": [], "周二": [], "周三": [], "周四": [], "周五": [], "周六": [], "周日": []}
        for day in days:
            fan_sql = """
                select name, status
                from scene_fan
                where insert_time like '%{}%'
                order by insert_time desc
                limit 1;
            """.format(day.strftime("%Y-%m-%d"))
            pump_sql = """
                select name, status
                from scene_pump
                where insert_time like '%{}%'
                order by insert_time desc
                limit 1;
            """.format(day.strftime("%Y-%m-%d"))
            light_sql = """
                select name, status
                from scene_light
                where insert_time like '%{}%'
                order by insert_time desc
                limit 1;
            """.format(day.strftime("%Y-%m-%d"))

            week = day.weekday()
            if week == 0:
                temp_list = res_dict["周一"]
            elif week == 1:
                temp_list = res_dict["周二"]
            elif week == 2:
                temp_list = res_dict["周三"]
            elif week == 3:
                temp_list = res_dict["周四"]
            elif week == 4:
                temp_list = res_dict["周五"]
            elif week == 5:
                temp_list = res_dict["周六"]
            else:
                temp_list = res_dict["周日"]

            array = [fan_sql, pump_sql, light_sql]
            for arr in array:
                temp_dict = {}
                cursor.execute(arr)
                res = cursor.fetchone()
                if res:
                    temp_dict["name"] = res[0]
                    temp_dict["status"] = "开" if res[1] else "关"
                else:
                    temp_dict["name"] = ""
                    temp_dict["status"] = ""
                temp_list.append(temp_dict)
        return Response(res_dict)


class DeviceRateView(APIView):
    """
    消防设备在线时间占比
    """

    def get(self, request):
        cursor = connection.cursor()
        fan_sql = """
            select name, count(*)
            from scene_fan;
        """
        pump_sql = """
            select name, count(*)
            from scene_pump;
        """
        light_sql = """
            select name, count(*)
            from scene_light;
        """

        array = [fan_sql, pump_sql, light_sql]
        data_set = tuple()
        total = 0
        for arr in array:
            cursor.execute(arr)
            data_set += cursor.fetchall()

        for data in data_set:
            total += data[1]
        res_list = []
        res_dict = {"result": res_list}
        for data in data_set:
            temp_dict = {}
            temp_dict["name"] = data[0]
            temp_dict["rate"] = data[1]/total
            temp_dict["nums"] = data[1]
            res_list.append(temp_dict)
        cursor.close()
        return Response(res_dict)
