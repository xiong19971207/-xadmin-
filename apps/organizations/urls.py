from django.conf.urls import url

from apps.organizations.views import OrgListView, AddAskView

urlpatterns = [
    # 授课机构
    url(r'^list/$', OrgListView.as_view(), name='list'),

    # 用户咨询页面的显示
    url(r'^add_ask/$',AddAskView.as_view(),name='add_ask')
]
