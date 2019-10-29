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
]
