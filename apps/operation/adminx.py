import xadmin

from apps.operation.models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse
from apps.operation.models import Banner


class BannerAdmin(object):
    list_display = ['image', 'title', 'url', 'index']
    search_fields = ['image', 'title', 'url', 'index']
    list_filter = ['image', 'title', 'url', 'index']

class UserAskAdmin(object):
    list_display = ['name', 'mobile', 'course_name', 'add_times']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_times']


class CourseCommentsAdmin(object):
    list_display = ['user', 'course', 'comments', 'add_times']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_times']


class UserFavoriteAdmin(object):

    list_display = ['user', 'fav_id', 'fav_type', 'add_times']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_times']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read', 'add_times']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_times']


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_times']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_times']

    def save_models(self):
        # 重写save_models方法
        # 是新同学就把数量加一
        obj = self.new_obj
        if not obj.id:
            obj.save()
            course = obj.course
            course.students += 1
            course.save()


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(Banner, BannerAdmin)
