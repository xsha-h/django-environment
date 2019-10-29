from django.conf.urls import url
from . import views


app_name = '[accessControls]'
urlpatterns = [
    url(r'^access/', views.AccessView.as_view(), name="access"),    # 所有门禁信息
    url(r'^add_access/', views.AddAccessView.as_view(), name="add_access"),    # 申请开门
    url(r'^update_access/', views.UpdateAccessView.as_view(), name="update_access"),    # 处理门禁申请
    url(r'^access_count/', views.AccessCountView.as_view(), name="access_count"),    # 各用户开门次数百分比
    url(r'^access_time/', views.AccessTimeView.as_view(), name="access_time"),    # 各用户开门时间百分比
    url(r'^access_output/', views.AccessOutputView.as_view(), name="access_output"),    # 导出门禁信息
]
