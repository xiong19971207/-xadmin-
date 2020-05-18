import xadmin
from import_export import resources

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag, BannerCourse
from xadmin.layout import Fieldset, Main, Side, Row


# xadmin 全局配置，可以写在任意adminx.py文件中
class GlobalSettings(object):
    site_title = '慕课网后台管理系统'
    site_footer = '慕课网'

    # menu_style = 'accordion'


class BaseSettings(object):
    # 可以为xadmin添加主题

    enable_themes = True

    # use_bootswatch = True


# class CourseAdmin(object):
#     # teacher__name 这样的格式可以在xadmin中显示外键相关的图标，可以点击然后显示一个图
#
#     list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
#     search_fields = ['name', 'desc', 'detail', 'degree', 'students']
#     list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
#     list_editable = ["degree", "desc"]


class LessonInline(object):
    model = Lesson
    style = 'tab'
    extra = 0


class CourseResourceInline(object):
    # 把课程资源编辑
    model = CourseResource
    # style = 'tab'
    extra = 0


class MyCourseResource(resources.ModelResource):
    class Meta:
        model = Course


class NewCourseAdmin(object):
    # 导入导出设置
    import_export_args = {'import_resource_class': MyCourseResource, 'export_resource_class': MyCourseResource}
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'show_image', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]
    # 设置只读
    readonly_fields = ['fav_nums', 'click_nums']
    # 设置看不到
    exclude = ['students', 'add_times']
    # 设置排序
    ordering = ['students']
    # 自定义图标
    model_icon = 'fa fa-address-book'
    # 关联字段显示
    inlines = [LessonInline, CourseResourceInline]
    # 显示Ueditor富文本的字段
    style_fields = {
        'detail': 'ueditor'
    }

    # 自定义xadmin显示格式
    def get_form_layout(self):
        if self.org_obj:
            # 只有在修改页面才变
            self.form_layout = (
                Main(
                    # Fieldset表示一块
                    Fieldset('讲师信息',
                             'teacher', 'course_org',
                             css_class='unsort no_title'
                             ),
                    Fieldset('基本信息'),
                    'name', 'desc',
                    Row('learn_times', 'degree'),
                    Row('category', 'tag'),
                    'you_need_know', 'teacher_tell', 'detail',
                ),

                # Side(
                #     # 右侧的信息
                #     Fieldset('访问信息'),
                #     'fav_nums', 'click_nums', 'students', 'add_times'
                # ),
                Side(
                    # 右侧的信息
                    Fieldset('选择信息'),
                    'is_classics', 'is_banner', 'image'
                ),
            )
        return super(NewCourseAdmin, self).get_form_layout()

    def queryset(self):
        # 返回自己能看到的课程
        qs = super().queryset()
        if not self.request.user.is_superuser:
            # 在讲师页面设置一个用户外键，指定这个讲师就是这个用户
            qs = qs.filter(teacher=self.request.user.teacher)
        # 返回用户
        return qs


class LessonAdmin(object):
    # course__name 这样的格式可以在xadmin中显示外键相关的图标，可以点击然后显示一个图

    list_display = ['course', 'name', 'add_times']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_times']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_times']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_times']
    model_icon = 'fa fa-superpowers'


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'add_times']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_times']


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'teacher__name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    list_editable = ["degree", "desc"]

    def queryset(self):
        # 返回自己能看到的课程
        qs = super().queryset()
        qs = qs.filter(is_banner=True)
        return qs


class CourseTagAdmin(object):
    list_display = ['course', 'tag', 'add_times']
    search_fields = ['course', 'tag']
    list_filter = ['course', 'tag', 'add_times']


# 注册激活xadmin
# xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Course, NewCourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)

# 配置全局xadmin样式
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
