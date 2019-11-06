from django.conf.urls import url

from . import views

app_name = '[alarm]'
urlpatterns = [
    url(r'^alarm_info/', views.AlarmView.as_view(), name="alarm_info"),   # 告警信息展示
    url(r'^deal_alarm/', views.DealAlarmView.as_view(), name="deal_alarm"),   # 告警信息处理
    url(r'^audit_alarm/', views.AuditAlarmView.as_view(), name="audit_alarm"),   # 告警信息审核
    url(r'^deal_many_alarm/', views.DealManyAlarmView.as_view(), name="deal_many_alarm"),   # 告警信息批量处理
    url(r'^audit_many_alarm/', views.AuditManyAlarmView.as_view(), name="audit_many_alarm"),   # 告警信息批量审核
    url(r'^alarm_count/', views.AlarmCountView.as_view(), name="alarm_count"),   # 告警类型告警占比
    url(r'^alarm_status/', views.AlarmStatusView.as_view(), name="alarm_status"),   # 告警类型告警占比
    url(r'^alarm_output/', views.AlarmOutputView.as_view(), name="alarm_output"),   # 告警信息导出
    url(r'^alarm_notDeal/', views.AlarmNotDealView.as_view(), name="alarm_notDeal"),   # 告警未处理时间走势图
]
