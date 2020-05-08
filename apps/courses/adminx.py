import xadmin

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag


# xadmin 全局配置，可以写在任意adminx.py文件中
class GlobalSettings(object):
    site_title = '慕课网后台管理系统'
    site_footer = '慕课网'

    # menu_style = 'accordion'


class BaseSettings(object):
    # 可以为xadmin添加主题

    enable_themes = True

    # use_bootswatch = True


class CourseAdmin(object):
    # teacher__name 这样的格式可以在xadmin中显示外键相关的图标，可以点击然后显示一个图

    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]


class LessonAdmin(object):
    # course__name 这样的格式可以在xadmin中显示外键相关的图标，可以点击然后显示一个图

    list_display = ['course', 'name', 'add_times']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_times']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_times']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_times']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'add_times']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_times']


class CourseTagAdmin(object):
    list_display = ['course', 'tag', 'add_times']
    search_fields = ['course', 'tag']
    list_filter = ['course', 'tag', 'add_times']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)

# 配置全局xadmin样式
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
