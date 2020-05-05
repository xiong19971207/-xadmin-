from django.conf.urls import url

from apps.organizations.views import OrgListView, AddAskView, OrgHomeView,OrgTeacherView,OrgCourseView,OrgDescView

urlpatterns = [
    # 授课机构
    url(r'^list/$', OrgListView.as_view(), name='list'),

    # 用户咨询页面的显示
    url(r'^add_ask/$', AddAskView.as_view(), name='add_ask'),

    # 授课机构详情页面
    # 正则表达式，匹配后面是数字
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='home'),
    # 机构教师
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name='teacher'),
    # 机构课程
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name='course'),
    # 机构描述
    url(r'^(?P<org_id>\d+)/desc/$', OrgDescView.as_view(), name='desc'),


]
