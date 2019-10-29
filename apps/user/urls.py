from django.conf.urls import url
from . import views

app_name = '[user]'
urlpatterns = [
    url(r'^user_info/', views.UserView.as_view(), name="user_info"),    # 用户信息
    url(r'^add_user/', views.AddUserView.as_view(), name="add_user"),    # 添加用户信息
    url(r'^update_user/', views.UpdateUserView.as_view(), name="update_user"),    # 修改用户信息
    url(r'^delete_user/', views.DeleteUserView.as_view(), name="delete_user"),    # 修改用户信息
    url(r'^activate_user/', views.ActivateUserView.as_view(), name="activate_user"),    # 激活或冻结用户
]
