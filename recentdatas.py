import datetime


def getRecentDatas(cursor, tag):
    """
    获取最近一周的数据
    :param cursor: 数据库游标
    :param tag: 根据tag标志选取操作的表名
    :return: 最近一周的数据（dict）
    """
    if tag == 1:
        tablename = "scene_temperature"
    elif tag == 2:
        tablename = "scene_humidity"
    elif tag == 3:
        tablename = "scene_beam"
    elif tag == 4:
        tablename = "scene_co2"
    else:
        tablename = "scene_pm25"

    # 最近7天的日期
    one_day = datetime.datetime.now()
    two_day = one_day - datetime.timedelta(days=1)
    three_day = one_day - datetime.timedelta(days=2)
    four_day = one_day - datetime.timedelta(days=3)
    five_day = one_day - datetime.timedelta(days=4)
    six_day = one_day - datetime.timedelta(days=5)
    seven_day = one_day - datetime.timedelta(days=6)
    days = [one_day, two_day, three_day, four_day, five_day, six_day, seven_day]

    # 最近7天的数据（每一天数据的平均值）
    res_dict = {"周一": [], "周二": [], "周三": [], "周四": [], "周五": [], "周六": [], "周日": []}

    for day in days:
        sql = """
            select name, avg(value) as value
            from {}
            where insert_time like '%{}%';
        """.format(tablename, day.strftime("%Y-%m-%d"))
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

        temp_dict = {}
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:
            temp_dict["name"] = res[0]
            temp_dict["value"] = res[1]
        else:
            temp_dict["name"] = ""
            temp_dict["value"] = 0
        temp_list.append(temp_dict)

    return res_dict
