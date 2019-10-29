from django.conf.urls import url
from . import views


app_name = '[videos]'
urlpatterns = [
    url(r'^monitor/', views.MonitorView.as_view(), name="monitor"),   # 视频监控
    url(r'^videos', views.VideosView.as_view(), name="video"),    # 所有视频信息
    url(r'^add_video', views.AddVideosView.as_view(), name="add_video"),  # 添加视频信息
    url(r'^update_video', views.UpdateVideosView.as_view(), name="update_video"),  # 修改视频信息
    url(r'^delete_video', views.DeleteVideosView.as_view(), name="delete_video"),  # 删除视频信息
]
