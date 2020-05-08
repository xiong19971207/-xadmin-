from django.conf.urls import url

from apps.operation.views import AddFavView,CommentView

urlpatterns = [
    # 用户收藏功能
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    # 用户评论功能
    url(r'^comment/$', CommentView.as_view(), name='comment'),

]
