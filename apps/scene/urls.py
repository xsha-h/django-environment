from django.conf.urls import url


from . import views

app_name = '[scene]'
urlpatterns = [
    url(r'^device_info/', views.SceneDeviceView.as_view(), name="device_info"),    # 场景设备界面
    url(r'^scene_info/', views.SceneView.as_view(), name="scene_info"),    # 场景设置界面
    url(r'^update_scene/', views.UpdateSceneView.as_view(), name="update_scene"),    # 场景修改界面
    url(r'^delete_scene/', views.DeleteSceneView.as_view(), name="delete_scene"),    # 场景删除界面
    url(r'^add_scene/', views.AddSceneView.as_view(), name="add_scene"),    # 场景新增界面
    url(r'^scene_status/', views.SceneStatusView.as_view(), name="scene_status"),    # 场景状态
    url(r'^scene_device/', views.DeviceView.as_view(), name="scene_device"),    # 场景设备
    url(r'^fire_history/', views.FireHistoryView.as_view(), name="fire_history"),    # 消防设备历史数据
    url(r'^fire_recent/', views.FireRecentView.as_view(), name="fire_recent"),    # 消防设备最近7天数据
    url(r'^fire_alarm/', views.FireAlarmView.as_view(), name="fire_alarm"),    # 消防设备最近7天数据

    url(r'^history/', views.HistoryView.as_view(), name="history"),    # 历史数据
    url(r'^recent/', views.RecentView.as_view(), name="recent"),    # 最近一周数据
    url(r'^alarm/', views.AlarmView.as_view(), name="alarm"),    # 报警统计表
    # url(r'^temperature_history/', views.TemperatureHistoryView.as_view(), name="temperature_history"),    # 温度历史数据
    # url(r'^temperature_recent/', views.TemperatureRecentView.as_view(), name="temperature_recent"),    # 温度最近一周数据
    # url(r'^temperature_alarm/', views.TemperatureAlarmView.as_view(), name="temperature_alarm"),    # 温度报警统计表
    # url(r'^humidity_history/', views.HumidityHistoryView.as_view(), name="humidity_history"),    # 湿度历史数据
    # url(r'^humidity_recent/', views.HumidityRecentView.as_view(), name="humidity_recent"),    # 湿度最近一周数据
    # url(r'^humidity_alarm/', views.HumidityAlarmView.as_view(), name="humidity_alarm"),    # 湿度报警统计表
    # url(r'^beam_history/', views.BeamHistoryView.as_view(), name="beam_history"),    # 光照强度历史数据
    # url(r'^beam_recent/', views.BeamRecentView.as_view(), name="beam_recent"),    # 光照强度最近一周数据
    # url(r'^beam_alarm/', views.BeamAlarmView.as_view(), name="beam_alarm"),    # 光照强度报警统计表
    # url(r'^co2_history/', views.CO2HistoryView.as_view(), name="co2_history"),    # CO2历史数据
    # url(r'^co2_recent/', views.CO2RecentView.as_view(), name="co2_recent"),    # CO2最近一周数据
    # url(r'^co2_alarm/', views.CO2AlarmView.as_view(), name="co2_alarm"),    # CO2报警统计表
    # url(r'^pm25_history/', views.PM25HistoryView.as_view(), name="pm25_history"),    # PM2.5历史数据
    # url(r'^pm25_recent/', views.PM25RecentView.as_view(), name="pm25_recent"),    # PM2.5最近一周数据
    # url(r'^pm25_alarm/', views.PM25AlarmView.as_view(), name="pm25_alarm"),    # PM2.5报警统计表

    url(r'^display_info', views.DisplayView.as_view(), name="display_info"),    # 大屏显示信息
    url(r'^update_display', views.UpdateDisplayView.as_view(), name="update_display"),    # 大屏显示信息

    url(r'^device_history/', views.DeviceHistoryView.as_view(), name="device_history"),    # 实时设备历史数据
    url(r'^device_recent/', views.DeviceRecentView.as_view(), name="device_recent"),    # 实时设备最近7天数据
    url(r'^device_rate/', views.DeviceRateView.as_view(), name="device_rate"),    # 实时设备开启次数占比
]
