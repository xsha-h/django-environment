# 12
from io import BytesIO

import xlwt
from django.core.serializers import json
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view,schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group,Permission
# 12!

from rest_framework import generics


from logs.models import Logs
from logs.schemas import LogsSchema, LogsOutputSchema
from logs.serializers import LogsSerializer


class LogsView(generics.ListAPIView):
    """
    日志信息: 条件可选
    #### 参数说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |page|分页|False|int|
    |scene|所属场景|False|string|
    |log_module|所属模块|False|string|
    |begin|开始时间|False|string|
    |end|结束时间|False|string|
    |content|日志内容|False|string|

    #### 响应字段说明
    |字段名称|描述|必须|类型|
    |--|--|--|--|
    |id|日志记录id|--|int|
    |addtime|日志记录的添加时间|--|string|
    |username|用户名称|--|string|
    |content|日志内容|--|string|
    |log_module|所属模块|--|string|
    |scene|所属场景|--|string|

    #### 注意说明
    - 1 申请门禁保存记录的所有信息。

    #### 响应消息：
    |Http响应码|原因|响应模型|
    |--|--|--|
    |200|请求成功|状态声明|
    """
    queryset = Logs.objects.all()
    serializer_class = LogsSerializer
    schema = LogsSchema

    def get_queryset(self):
        begin = self.request.query_params.get("begin", "")
        end = self.request.query_params.get("end", "")
        content = self.request.query_params.get("content", "")
        scene = self.request.query_params.get("scene", "")
        log_module = self.request.query_params.get("log_module", "")

        # 日志过滤
        query_obj = Logs.objects.all()
        if begin:
            query_obj = Logs.objects.filter(addtime__gte=begin)
        if end:
            query_obj = query_obj.filter(addtime__lte=end)
        if content:
            query_obj = query_obj.filter(content__contains=content)
        if scene:
            query_obj = query_obj.filter(scene=scene)
        if log_module:
            query_obj = query_obj.filter(log_module=log_module)
        if query_obj:
            return query_obj

        else:
            return self.queryset


class LogsOutputView(APIView):
    """
    日志信息导出excel
    """
    schema = LogsOutputSchema

    def get(self, request):

        query_obj = Logs.objects.all()

        start = request.query_params.get("startTime")
        end = request.query_params.get("endTime")

        if start:
            query_obj = Logs.objects.filter(Q(addtime__gte=start) & Q(addtime__lte=end))

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
        sheet.write(0, 0, '日志编号', style_heading)
        sheet.write(0, 1, '日志时间', style_heading)
        sheet.write(0, 2, '所属场景', style_heading)
        sheet.write(0, 3, '所属模块', style_heading)
        sheet.write(0, 4, '日志描述', style_heading)

        # 写入数据
        data_row = 1
        # User.objects.all()这个是查询条件,可以根据自己的实际需求做调整.
        for i in query_obj:
            # 格式化datetime
            addtime = i.addtime.strftime('%Y-%m-%d')
            sheet.write(data_row, 0, i.id)
            sheet.write(data_row, 1, addtime)
            sheet.write(data_row, 2, i.scene)
            sheet.write(data_row, 3, i.log_module)
            sheet.write(data_row, 4, i.content)

            data_row = data_row + 1

        # 写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response
