from django.conf.urls import url

from apps.courses.views import CourseListView, CourseDetailView, CourseVideoView, CourseCommentView,PlayView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='list'),

    # 课程详情页面
    url(r'^(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='detail'),

    # 课程资源页面
    url(r'^(?P<course_id>\d+)/video/$', CourseVideoView.as_view(), name='video'),

    # 课程评论
    url(r'^(?P<course_id>\d+)/comment/$', CourseCommentView.as_view(), name='comment'),

    # 播放视频
    url(r'^(?P<course_id>\d+)/play/(?P<play_id>\d+)/$', PlayView.as_view(), name='play'),

]
