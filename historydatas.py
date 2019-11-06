from fetchdata import dictfetchall


def getHistoryDatas(cursor, tag=None, start=None, end=None):
    """
    根据时间获取历史数据
    :param cursor: 数据库游标
    :param tag: 根据tag标志选取操作的表名
    :param start: 开始时间
    :param end: 结束时间
    :return: 历史数据（dict）
    """
    if tag == 1:
        tablename = "scene_temperature"
    elif tag == 2:
        tablename = "scene_humidity"
    elif tag == 3:
        tablename = "scene_beam"
    elif tag == 4:
        tablename = "scene_co2"
    elif tag == 5:
        tablename = "scene_pm25"

    sql = """
        select name, insert_time, status, value
        from {};
    """.format(tablename)
    if start:
        sql = """
            select name, insert_time, status, value
            from {}
            where insert_time>='{}' and insert_time<='{}'
        """.format(tablename, start, end)
    cursor.execute(sql)
    print(sql)
    res_list = dictfetchall(cursor)
    res_dict = {"results": res_list}
    return res_dict
