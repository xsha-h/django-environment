"""environment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# 14
from django.conf.urls import url, include
from django.contrib import admin
import rest_framework.authtoken.views
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='动力环境监测系统')
# 14!

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 15
    url(r'^api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api_token_auth/', obtain_jwt_token),
    url(r'^api/', schema_view),
    url(r'^logs/', include('logs.urls', namespace='logs')),  # 日志板块
    url(r'^videos/', include("videos.urls", namespace="videos")),   # 视频板块
    url(r'^accessControls/', include("accessControls.urls", namespace="accessControls")),   # 门禁板块
    url(r'^user/', include("user.urls", namespace="user")),   # 用户板块
    url(r'^alarm/', include("alarm.urls", namespace="alarm")),   # 告警板块
    url(r'^scene/', include("scene.urls", namespace="scene")),   # 场景板块
    # 15!

]
