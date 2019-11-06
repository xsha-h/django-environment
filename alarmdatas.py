from fetchdata import dictfetchall


def getAlarmDatas(cursor, tag):
    """
    根据设备查询设备的告警时间
    :param cursor: 数据库游标
    :param tag: 根据tag标志选取告警设备名称
    :return: dict
    """
    if tag == 1:
        device = "温度传感器"
    elif tag == 2:
        device = "湿度传感器"
    elif tag == 3:
        device = "光照强度传感器"
    elif tag == 4:
        device = "CO2传感器"
    else:
        device = "PM2.5传感器"

    sql = """
        select device, TIMESTAMPDIFF(MINUTE,addtime,deal_time) as time
        from alarm_alarm
        where device='{}';
    """.format(device)

    cursor.execute(sql)
    res_list = dictfetchall(cursor)
    res_dict = {"results": res_list}
    return res_dict
