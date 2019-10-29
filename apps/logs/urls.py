from django.conf.urls import url
from . import views
app_name = 'logs'
urlpatterns = [
    url(r'^logs_info/', views.LogsView.as_view(), name='logs_info'),   # 日志信息
    url(r'^logs_output/', views.LogsOutputView.as_view(), name='logs_output'),   # 日志信息导出
]
