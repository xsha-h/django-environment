import xlwt
from datetime import datetime
from io import BytesIO

from django.contrib.auth.models import User
from django.db import connection


from django.db.models import Count, Q
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accessControls.models import Accesses
from accessControls.schemas import AccessSchema, UpdateAccessSchema, AccessRateSchema
from accessControls.serializers import AccessSerializer, UpdateAccessSerializer, AddAccessSerializer
from addlogs import addLog


class AccessView(generics.ListAPIView):
    """
    门禁信息：条件可选
    ---
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |page|分页|True|int|
    |status|可以状态(1, "待审核"),(2, "已通过"),(3, "已拒绝")|False|int|
    |start|申请开始时间|False|string|
    |end|申请结束时间|False|string|
    |approval_start|审批开始时间|False|string|
    |approval_end|审批结束时间|False|string|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|门禁记录id|--|int|
    |addtime|门禁申请的添加时间|--|string|
    |username|申请门禁用户名称|--|int|
    |start_time|申请开始时间|--|string|
    |end_time|申请结束时间|--|string|
    |follow_users|跟随人员名称|--|string|
    |follow_nums|跟随人数|--|int|
    |detail|跟随人员声明|--|string|
    |status|告警状态(1, "待审核"),(2, "已通过"),(3, "已拒绝")|--|int|
    |approval_time|审批时间|--|string|
    |approval_user|审批人|--|int|
    |feedback|审核反馈|--|string|

    #### 注意说明
    - 1 列表中均为门禁记录的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|返回门禁信息列表|
    """
    serializer_class = AccessSerializer
    schema = AccessSchema
    module_perms = ['accessControls.access_view']

    def get_queryset(self):
        status = self.request.query_params.get("status", 0)
        start = self.request.query_params.get("start", "")
        end = self.request.query_params.get("end", "")
        approval_start = self.request.query_params.get("approval_start", "")
        approval_end = self.request.query_params.get("approval_end", "")

        # 门禁信息过滤
        query_obj = Accesses.objects.all()
        if status:
            query_obj = query_obj.filter(status=status)
        if start:
            query_obj = query_obj.filter(addtime__gte=start)
        if end:
            query_obj = query_obj.filter(addtime__lte=end)
        if approval_start:
            query_obj = query_obj.filter(approval_time__gte=approval_start)
        if approval_end:
            query_obj = query_obj.filter(approval_time__lte=approval_end)
        return query_obj


class AddAccessView(generics.CreateAPIView):
    """
    申请门禁
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |username|用户名称|True|string|
    |follow_users|跟随人员名称|True|string|
    |follow_nums|跟随人数|True|int|
    |detail|跟随人员声明|True|string|
    |start|申请开始时间|True|string|
    |end|申请结束时间|True|string|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 申请门禁保存记录的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|状态声明|
    """
    serializer_class = AddAccessSerializer
    module_perms = ['accessControls.add_access']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            addLog(user_id=request.user.username, log_module="门禁管理", content="申请门禁失败")
            return Response(data={"code": 400, "message": "门禁申请失败！"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        resp = Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        resp["code"] = 200
        resp["message"] = "门禁申请成功！"
        addLog(user_id=request.user.username, log_module="门禁管理", content="申请门禁成功")
        return resp


class UpdateAccessView(generics.GenericAPIView):
    """
    门禁审核
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|门禁记录id|True|int|
    |tag|审核标志：(0, "拒接申请"), (1, "通过申请")|True|int|
    |feedback|审核反馈|True|string|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|

    #### 注意说明
    - 1 申请门禁保存记录的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|状态声明|
    """
    queryset = Accesses.objects.all()
    serializer_class = UpdateAccessSerializer
    schema = UpdateAccessSchema
    module_perms = ['accessControls.update_access']

    def post(self, request, *args, **kwargs):
        try:
            id = request.data.get("id")
            # 审核标志
            tag = request.data.get("tag")
            feedback = request.data.get("feedback")
            access = Accesses.objects.get(pk=id)
            # 审批时间
            access.approval_time = datetime.now()
            access.feedback = feedback
            # 暂时设置默认值
            access.approval_user = 1
            if tag:
                # 通过之后申请状态
                access.status = 2
                message = "门禁申请成功！"
            else:
                # 拒绝之后申请状态
                access.status = 3
                message = "门禁申请拒绝！"
            access.save()
        except:
            return Response(data={"code": 400, "message": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)
        addLog(user_id=self.request.user.username, log_module="门禁管理", content=message)
        return Response(data={"code": 200, "message": message}, status=status.HTTP_200_OK)


class AccessCountView(generics.ListAPIView):
    """
    各用户开门次数百分比
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |page|分页|True|int|
    |startTime|开始时间|False|string|
    |endTime|结束时间|False|string|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |username|用户名称|--|string|
    |count|开门次数占比|--|float|

    #### 注意说明
    - 1 列表中均为各用户开门次数百分比。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|各用户开门次数百分比|
    """
    schema = AccessRateSchema

    def get(self, request, *args, **kwargs):
        startTime = request.query_params.get("startTime", "")
        endTime = request.query_params.get("endTime", "")
        query_obj = Accesses.objects.filter(status=2)
        if startTime:
            query_obj = query_obj.filter(start_time__gte=startTime)
        if endTime:
            query_obj = query_obj.filter(start_time_lte=endTime)
        query_obj = query_obj.values("username").annotate(count=Count("username"))
        total = 0
        for obj in query_obj:
            obj["username"] = obj["username"]
            total += obj["count"]
        for obj in query_obj:
            obj["count"] = obj["count"]/total
        return Response(data=query_obj)


class AccessTimeView(generics.ListAPIView):
    """
    各用户开门时间百分比
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |page|分页|True|int|
    |startTime|开始时间|False|string|
    |endTime|结束时间|False|string|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |user_name|用户名称|--|string|
    |count|开门次数占比|--|float|

    #### 注意说明
    - 1 列表中均为各用户开门时间百分比。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|各用户开门时间百分比|
    """
    schema = AccessRateSchema

    def get(self, request, *args, **kwargs):

        startTime = request.query_params.get("startTime", "")
        endTime = request.query_params.get("endTime", "")
        sql = """
            select auth_user.username, sum(timestampdiff(second,start_time,end_time)) as sum_time
            from accesscontrols_accesses, auth_user
            where status=2 and accesscontrols_accesses.username = auth_user.username
            group by accesscontrols_accesses.username;
        """
        if startTime:
            sql = """
                select auth_user.username, sum(timestampdiff(second,start_time,end_time)) as sum_time
                from accesscontrols_accesses, auth_user
                where status=2 and accesscontrols_accesses.username = auth_user.username and start_time >= '{}'
                group by accesscontrols_accesses.username;
            """.format(startTime)
        if endTime:
            sql = """
                select auth_user.username, sum(timestampdiff(second,start_time,end_time)) as sum_time
                from accesscontrols_accesses, auth_user
                where status=2 and accesscontrols_accesses.username = auth_user.username and start_time <= '{}'
                group by accesscontrols_accesses.username;
            """.format(endTime)
        # 创建数据库游标
        cursor = connection.cursor()
        # 游标执行sql语句
        cursor.execute(sql)
        # 获取符合条件的所有数据集
        rets = cursor.fetchall()
        res_list = []
        total = 0
        for ret in rets:
            res_dict = {}
            res_dict["username"] = ret[0]
            res_dict["single_time"] = int(ret[1])
            total += int(ret[1])
            res_list.append(res_dict)
        for res in res_list:
            res["single_time"] = res["single_time"]/total
        return Response(data=res_list)


class AccessOutputView(APIView):
    """
    门禁信息导出excel
    """
    schema = AccessRateSchema

    def get(self, request):
        query_obj = Accesses.objects.all()

        start = request.query_params.get("startTime")
        end = request.query_params.get("endTime")

        if start:
            query_obj = Accesses.objects.filter(Q(addtime__gte=start) & Q(addtime__lte=end))

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
        sheet.write(0, 0, '门禁编号', style_heading)
        sheet.write(0, 1, '申请人', style_heading)
        sheet.write(0, 2, '申请时间', style_heading)
        sheet.write(0, 3, '申请说明', style_heading)
        sheet.write(0, 4, '随行人数', style_heading)
        sheet.write(0, 5, '随性人员', style_heading)
        sheet.write(0, 6, '申请状态', style_heading)
        sheet.write(0, 7, '审批时间', style_heading)
        sheet.write(0, 8, '审批人', style_heading)
        sheet.write(0, 9, '审批反馈', style_heading)

        # 写入数据
        data_row = 1
        # User.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in query_obj:
            # 格式化datetime
            addtime = i.addtime.strftime('%Y-%m-%d')
            approval_time = i.approval_time.strftime('%Y-%m-%d')
            sheet.write(data_row, 0, i.id)
            sheet.write(data_row, 1, i.username)
            sheet.write(data_row, 2, addtime)
            sheet.write(data_row, 3, i.detail)
            sheet.write(data_row, 4, i.follow_nums)
            sheet.write(data_row, 5, i.follow_users)
            sheet.write(data_row, 6, i.status)
            sheet.write(data_row, 7, approval_time)
            sheet.write(data_row, 8, i.approval_user)
            sheet.write(data_row, 9, i.feedback)
            data_row = data_row + 1

        # 写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
