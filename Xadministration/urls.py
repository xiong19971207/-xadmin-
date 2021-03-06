"""Xadministration URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

# 导入视图
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from Xadministration.settings import MEDIA_ROOT
from apps.users.views import LoginView, LogoutView, RegisterView, SendEmailView, IndexView

import xadmin
from apps.organizations.views import OrgListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),

    # 首页、登陆、注册
    path('', IndexView.as_view(), name='index'),
    # 利用CBV编程：class base view
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', csrf_exempt(RegisterView.as_view()), name='register'),
    path('send_email/', csrf_exempt(SendEmailView.as_view()), name='send_email'),

    # 课程机构urls
    # url(r'^org_list/', OrgListView.as_view(), name='org_list'),
    url(r'^org/', include(('apps.organizations.urls', 'organizations'), namespace='org')),

    # 用户相关操作
    url(r'^op/', include(('apps.operation.urls', 'operation'), namespace='op')),

    # 公开课
    url(r'^course/', include(('apps.courses.urls', 'courses'), namespace='course')),

    # 用户个人中心
    url(r'^users/', include(('apps.users.urls', 'users'), namespace='users')),

    # 配置全局图片显示的URL
    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    # url(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
    # 加入图形验证码
    url(r'^captcha/', include('captcha.urls')),

    # ueditor的配置url
    url(r'^ueditor/', include('DjangoUeditor.urls')),

]
