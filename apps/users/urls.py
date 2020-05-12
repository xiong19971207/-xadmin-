from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from apps.users.views import UserInfoView, UploadImgView, UpdatePwdView, ChangeEmailView, MessageView
from apps.users.views import UserMycourseView, UserFavOrgView, UserFavTeacherView, UserFavCourseView

urlpatterns = [
    # 用户个人中心
    url(r'^info/$', UserInfoView.as_view(), name='info'),

    # 修改头像
    url(r'^uploadimg/$', UploadImgView.as_view(), name='uploadimg'),

    # 修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 修改电子邮箱
    url(r'^update/email/$', ChangeEmailView.as_view(), name='update_email'),

    # 个人课表页面
    # url(r'^mycourse/$', UserMycourseView.as_view(), name='mycourse'),
    # 第二种方法,不用写视图类了,但是前端页面必须有资源
    url(r'^mycourse/$', login_required(TemplateView.as_view(template_name='usercenter-mycourse.html')),
        {'current_page': 'mycourse'}, name='mycourse'),

    # 我的收藏页面
    url(r'^myfavorg/$', UserFavOrgView.as_view(), name='myfavorg'),
    url(r'^myfavteacher/$', UserFavTeacherView.as_view(), name='myfavteacher'),
    url(r'^myfavcourse/$', UserFavCourseView.as_view(), name='myfavcourse'),

    # 我的消息
    url(r'^message/$', MessageView.as_view(), name='message')
]
