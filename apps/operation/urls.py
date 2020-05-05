from django.conf.urls import url

from apps.operation.views import AddFavView

urlpatterns = [
    # 用户收藏功能
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),


]
