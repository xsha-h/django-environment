from django.conf.urls import url
from . import views


app_name = '[permission]'
urlpatterns = [
    url(r'^permission_info/', views.PermissionView.as_view(), name="permission_info"),    # 权限管理表
    url(r'^update_permission/', views.UpdatePermissionView.as_view(), name="update_permission"),    # 修改权限管理表
    url(r'^delete_permission/', views.DeletePermissionView.as_view(), name="delete_permission"),    # 删除权限管理表
    url(r'^add_permission/', views.AddPermissionView.as_view(), name="add_permission"),    # 删除权限管理表
]
