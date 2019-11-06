import time
from datetime import datetime
from io import BytesIO

import xlwt
from django.db import connection
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from addlogs import addLog
from alarm.models import Alarm
from alarm.schemas import AlarmSchema, DealAlarmSchema, AuditAlarmSchema, DealManyAlarmSchema, AuditManyAlarmSchema, \
    AlarmRateSchema, AlarmStatusSchema, AlarmOutputSchema
from alarm.serializers import AlarmSerializer, DealAlarmSerializer
from scene.models import Scene


class AlarmView(generics.ListAPIView):
    """
    所有告警信息: 条件可选
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |page|分页|True|int|
    |type_id|告警类型的id|False|int|
    |level_id|告警级别的id|False|int|
    |scene_id|告警场景的id|False|int|
    |status|可以状态(1, "待处理"),(2, "待审核"),(3, "审核通过"),(4, "审核不通过")|False|int|
    |start_time|开始时间|False|string|
    |end_time|结束时间|False|string|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|告警记录id|--|int|
    |alarm_type|告警类型的信息|--|object|
    |alarm_level|告警级别的信息|--|object|
    |alarm_scene|告警场景的信息|--|object|
    |addtime|告警记录的添加时间|--|string|
    |device|设备名称|--|string|
    |content|告警内容|--|string|
    |status|告警状态(1, "待处理"),(2, "待审核"),(3, "审核通过"),(4, "审核不通过")|--|int|
    |start_time|开始时间|False|string|
    |end_time|结束时间|False|string|

    #### 注意说明
    - 1 列表中均为告警记录的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|返回告警信息列表|
    """
    queryset = None
    serializer_class = AlarmSerializer
    schema = AlarmSchema
    module_perms = ['alarm.alarm_view']

    def get_queryset(self):
        scene_id = self.request.query_params.get("scene_id")
        type_id = self.request.query_params.get("type_id")
        level_id = self.request.query_params.get("level_id")
        status = self.request.query_params.get("status")
        start_time = self.request.query_params.get("start_time")
        end_time = self.request.query_params.get("end_time")

        query_obj = Alarm.objects.all()
        if scene_id:
            query_obj = query_obj.filter(alarm_scene_id=scene_id)
        if type_id:
            query_obj = query_obj.filter(alarm_type_id=type_id)
        if level_id:
            query_obj = query_obj.filter(alarm_level_id=level_id)
        if status:
            query_obj = query_obj.filter(status=status)
        if start_time:
            query_obj = query_obj.filter(addtime__gte=start_time)
        if end_time:
            query_obj = query_obj.filter(addtime__lte=end_time)
        self.queryset = query_obj
        return self.queryset


class DealAlarmView(generics.GenericAPIView):
    """
    告警单条处理
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|告警记录的id|True|int|
    |deal_detail|处理的说明|False|string|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 id对应的状态为待处理,既 status=1

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|相应的处理信息|
    """
    queryset = Alarm.objects.all()
    serializer_class = DealAlarmSerializer
    schema = DealAlarmSchema
    module_perms = ['alarm.deal_alarm']

    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get("id")
            deal_detail = request.data.get("deal_detail")
            alarm = Alarm.objects.get(pk=id)
            alarm.status = 2
            scene_name = Scene.objects.filter(pk=alarm.alarm_scene_id).first().name
            alarm.deal_detail = deal_detail
            alarm.save()
        except:
            return Response(data={"code": 400, "message": "告警处理失败！"})
        addLog(user_id=request.user.username, scene=scene_name, log_module="告警管理", content="告警处理")
        return Response(data={"code": 200, "message": "告警处理成功！"})


class AuditAlarmView(generics.GenericAPIView):
    """
    告警单条审核
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|告警记录的id|True|int|
    |audit_detail|审核的说明|False|string|
    |status|可以状态(3, "审核通过"),(4, "审核不通过")|True|int|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 id对应的状态为待审核,既 status=2

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|相应的审核信息|
    """
    queryset = Alarm.objects.all()
    serializer_class = DealAlarmSerializer
    schema = AuditAlarmSchema
    module_perms = ['alarm.audit_alarm']

    def post(self, request):
        try:
            id = self.request.data.get("id")
            status = self.request.data.get("status")
            audit_detail = request.data.get("audit_detail")
            alarm = Alarm.objects.get(pk=id)
            scene_name = Scene.objects.filter(pk=alarm.alarm_scene_id).first().name
            if status == 3 or status == 4:
                alarm.status = status
            else:
                raise TypeError
            alarm.audit_detail = audit_detail
            alarm.save()
        except:
            return Response(data={"code": 400, "message": "告警审核失败！"})
        addLog(user_id=request.user.username, scene=scene_name, log_module="告警管理", content="告警审核")
        return Response(data={"code": 200, "message": "告警审核成功！"})


class DealManyAlarmView(generics.GenericAPIView):
    """
    告警信息批量处理
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |ids|告警记录的id集合，id之间以逗号隔开|True|string|
    |type_id|告警类型的id|True|int|
    |content|审核的说明|False|string|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 ids中的id对应的状态全为待处理,既 status=1

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|相应的处理信息|
    """
    queryset = Alarm.objects.all()
    serializer_class = DealAlarmSerializer
    schema = DealManyAlarmSchema
    module_perms = ['alarm.deal_alarm']

    def post(self, request):
        ids = request.data.get("ids")
        type_id = request.data.get("type_id")
        content = request.data.get("content")
        ids = ids.split(",")
        try:
            for i in range(ids):
                query_obj = Alarm.objects.get(pk=i)
                query_obj.alarm_type_id = type_id
                scene_name = Scene.objects.filter(pk=query_obj.alarm_scene_id).first().name
                query_obj.status = 2
                if content:
                    query_obj.content = content
                else:
                    query_obj.content = ""
                query_obj.save()
                addLog(user_id=request.user.username, scene=scene_name, log_module="告警管理", content="告警处理")
        except:
            return Response(data={"code": 400, "message": "告警批量处理失败！"})
        return Response(data={"code": 200, "message": "告警批量处理成功！"})


class AuditManyAlarmView(generics.GenericAPIView):
    """
    告警批量审核
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |ids|告警记录的id集合，id之间以逗号隔开|True|string|
    |type_id|告警类型的id|True|int|
    |content|审核的说明|False|string|
    |status|可以状态(3, "审核通过"),(4, "审核不通过")|True|int|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 ids中的id对应的状态全为待审核,既 status=2

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|相应的审核信息|
    """
    queryset = Alarm.objects.all()
    serializer_class = DealAlarmSerializer
    schema = AuditManyAlarmSchema
    module_perms = ['alarm.audit_alarm']

    def post(self, request):
        ids = request.data.get("ids")
        type_id = request.data.get("type_id")
        content = request.data.get("content")
        status = request.data.get("status")
        ids = ids.split(",")
        try:
            for i in range(ids):
                query_obj = Alarm.objects.get(pk=i)
                query_obj.alarm_type_id = type_id
                scene_name = Scene.objects.filter(pk=query_obj.alarm_scene_id).first().name
                if content:
                    query_obj.content = content
                else:
                    query_obj.content = ""
                if status == 3:
                    query_obj.status = 3
                    message = "审核通过"
                elif status == 4:
                    query_obj.status = 4
                    message = "审核不通过"
                else:
                    raise TypeError
                query_obj.save()
                addLog(user_id=request.user.username, scene=scene_name, log_module="告警管理", content="告警审核")
        except:
            return Response(data={"code": 400, "message": "告警批量审核失败！"})
        return Response(data={"code": 200, "message": "告警批量{}！".format(message)})


class AlarmCountView(generics.ListAPIView):
    """
    告警类型的告警次数占比
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |page|分页|True|int|
    |startTime|开始时间|False|string|
    |endTime|结束时间|False|string|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |name|告警状态|--|string|
    |count|告警类型的告警次数占比|--|float|

    #### 注意说明
    - 1 列表中为告警类型的告警次数占比

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|返回用户列表|
    """
    schema = AlarmRateSchema

    def get(self, request, *args, **kwargs):
        cursor = connection.cursor()
        sql = """
            select alarm_alarmtype.name as name, count(*)
            from alarm_alarm, alarm_alarmtype
            where alarm_type_id = alarm_alarmtype.id
            group by alarm_type_id;
        """
        startTime = request.query_params.get("startTime", "")
        endTime = request.query_params.get("endTime", "")
        if startTime:
            print(startTime)
            sql = """
                select alarm_alarmtype.name as name, count(*)
                from alarm_alarm, alarm_alarmtype
                where alarm_type_id = alarm_alarmtype.id and alarm_alarm.addtime >= '{}'
                group by alarm_type_id;
            """.format(startTime)

        if endTime:
            print(endTime)
            sql = """
                select alarm_alarmtype.name as name, count(*)
                from alarm_alarm, alarm_alarmtype
                where alarm_type_id = alarm_alarmtype.id and alarm_alarm.addtime <= '{}'
                group by alarm_type_id;
            """.format(endTime)
        cursor.execute(sql)
        query_obj = cursor.fetchall()
        data_res = []
        total = 0
        for obj in query_obj:
            total += obj[1]
        for obj in query_obj:
            res_dict = {}
            res_dict["name"] = obj[0]
            res_dict["count"] = obj[1]/total
            data_res.append(res_dict)
        cursor.close()
        return Response(data=data_res)


class AlarmStatusView(generics.ListAPIView):
    """
    各类告警状态百分比
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |page|分页|True|int|
    |startTime|开始时间|False|String|
    |endTime|结束时间|False|String|
    |type_id|告警类型id|True|int|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |name|告警状态|--|string|
    |count|告警状态的占比|--|float|

    #### 注意说明
    - 1 列表中为各类告警状态的占比,既 vr_audit_status=1

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|返回用户列表|
    """
    schema = AlarmStatusSchema

    def get(self, request, *args, **kwargs):
        cursor = connection.cursor()
        sql = """
            select status, count(*)
            from alarm_alarm
            group by status;
        """
        startTime = request.query_params.get("startTime", "")
        endTime = request.query_params.get("endTime", "")
        type_id = request.query_params.get("type_id", "")
        if startTime:
            print(startTime)
            sql = """
                select status, count(*)
                from alarm_alarm
                where addtime >= '{}' and addtime <= '{}'
                group by status;
            """.format(startTime, endTime)

        if type_id:
            if startTime:
                sql = """
                    select status, count(*)
                    from alarm_alarm
                    where addtime >= '{}' and addtime <= '{}' and alarm_type_id = '{}'
                    group by status;
                """.format(startTime, endTime, type_id)
            else:
                sql = """
                    select status, count(*)
                    from alarm_alarm
                    where alarm_type_id = '{}'
                    group by status;
                """.format(type_id)
        cursor.execute(sql)
        query_obj = cursor.fetchall()
        data_res = []
        total = 0
        for obj in query_obj:
            total += obj[1]
        for obj in query_obj:
            res_dict = {}
            if obj[0] == 1:
                res_dict["name"] = "待处理"
            elif obj[0] == 2:
                res_dict["name"] = "待审核"
            elif obj[0] == 3:
                res_dict["name"] = "审核通过"
            else:
                res_dict["name"] = "审核不通过"
            res_dict["count"] = obj[1]/total
            data_res.append(res_dict)
        cursor.close()
        return Response(data=data_res)


class AlarmOutputView(APIView):
    """
    告警信息导出excel
    """
    schema = AlarmOutputSchema

    def get(self, request):
        query_obj = Alarm.objects.all()

        start = request.query_params.get("startTime")
        end = request.query_params.get("endTime")

        if start:
            query_obj = Alarm.objects.filter(Q(addtime__gte=start) & Q(addtime__lte=end))

        # 设置HTTPResponse的类型
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=users.xls'  # 文件名称
        # 创建一个文件对象
        wb = xlwt.Workbook(encoding='utf8')
        # 创建一个sheet对象
        sheet = wb.add_sheet('access-sheet')

        # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
        style_heading = xlwt.easyxf("""
                    font:
                        name Arial,
                        colour_index white,
                        bold on,
                        height 0xA0;
                    align:
                        wrap off,
                        vert center,
                        horiz center;
                    pattern:
                        pattern solid,
                        fore-colour 0x19;
                    borders:
                        left THIN,
                        right THIN,
                        top THIN,
                        bottom THIN;
                    """)

        # 写入文件标题
        sheet.write(0, 0, '告警编号', style_heading)
        sheet.write(0, 1, '告警类型', style_heading)
        sheet.write(0, 2, '告警级别', style_heading)
        sheet.write(0, 3, '开始时间', style_heading)
        sheet.write(0, 4, '所属场景', style_heading)
        sheet.write(0, 5, '告警设备', style_heading)
        sheet.write(0, 6, '内容', style_heading)
        sheet.write(0, 7, '状态', style_heading)

        # 写入数据
        data_row = 1
        # User.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in query_obj:
            # 格式化datetime
            addtime = i.addtime.strftime('%Y-%m-%d')
            sheet.write(data_row, 0, i.id)
            sheet.write(data_row, 1, i.alarm_type.name)
            sheet.write(data_row, 2, i.alarm_level.name)
            sheet.write(data_row, 3, addtime)
            sheet.write(data_row, 4, i.alarm_scene.name)
            sheet.write(data_row, 5, i.device)
            sheet.write(data_row, 6, i.content)
            sheet.write(data_row, 7, i.status)
            data_row = data_row + 1

        # 写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response


class AlarmNotDealView(APIView):
    """
    某一时刻告警未处理时间的总和
    """
    schema = AlarmOutputSchema

    def get(self, request):
        cursor = connection.cursor()
        # 字符串转datetime类型
        start = datetime.strptime(request.query_params.get("startTime"), "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(request.query_params.get("endTime"), "%Y-%m-%d %H:%M:%S")

        # 通过时间间隔获取中间的时间
        notDealSeconds = (time.mktime(end.timetuple())-time.mktime(start.timetuple()))/5
        one_time = datetime.fromtimestamp(time.mktime(start.timetuple())+notDealSeconds)
        two_time = datetime.fromtimestamp(time.mktime(start.timetuple())+notDealSeconds*2)
        three_time = datetime.fromtimestamp(time.mktime(start.timetuple())+notDealSeconds*3)
        four_time = datetime.fromtimestamp(time.mktime(start.timetuple())+notDealSeconds*4)
        print(start, one_time, two_time, three_time, four_time, end)

        sql_one = """
            select sum(TIMESTAMPDIFF(MINUTE,addtime,deal_time)) as alarm_time
            from alarm_alarm
            where deal_time >= '{}' and  deal_time < '{}'
        """.format(start, one_time)
        sql_two = """
            select sum(TIMESTAMPDIFF(MINUTE,addtime,deal_time)) as alarm_time
            from alarm_alarm
            where deal_time >= '{}' and  deal_time < '{}'
        """.format(one_time, two_time)
        sql_three = """
                    select sum(TIMESTAMPDIFF(MINUTE,addtime,deal_time)) as alarm_time
                    from alarm_alarm
                    where deal_time >= '{}' and  deal_time < '{}'
                """.format(two_time, three_time)
        sql_four = """
                    select sum(TIMESTAMPDIFF(MINUTE,addtime,deal_time)) as alarm_time
                    from alarm_alarm
                    where deal_time >= '{}' and  deal_time < '{}'
                """.format(three_time, four_time)
        sql_five = """
                    select sum(TIMESTAMPDIFF(MINUTE,addtime,deal_time)) as alarm_time
                    from alarm_alarm
                    where deal_time >= '{}' and  deal_time < '{}'
                """.format(four_time, end)

        array = [sql_one, sql_two, sql_three, sql_four, sql_five]
        res_dict = {"one": None, "two": None, "three": None, "four": None, "five": None}
        for i in range(len(array)):
            cursor.execute(array[i])
            res = cursor.fetchone()
            temp = {}
            if res[0]:
                temp["minutes"] = res[0]
            else:
                temp["minutes"] = 0
            if i == 0:
                res_dict["one"] = temp
            elif i == 1:
                res_dict["two"] = temp
            elif i == 2:
                res_dict["three"] = temp
            elif i == 3:
                res_dict["four"] = temp
            else:
                res_dict["five"] = temp
        cursor.close()
        return Response(res_dict)
