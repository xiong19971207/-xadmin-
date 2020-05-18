import xadmin

from apps.organizations.models import Teacher, City, CourseOrg


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company']
    search_fields = ['org', 'name', 'work_years', 'work_company']
    list_filter = ['org', 'name', 'work_years', 'work_company']


class CityAdmin(object):
    """
    这个类下面配置的内容都会出现在Xadmin的页面上
    分别表示不同的功能
    list_display： 列表中的关键字会显示列
    search_fields：会出现搜索框
    list_filter：  会出现过滤器
    list_editable：里面的字段可以单独修改了
    """

    list_display = ["id", "name", "desc"]
    search_fields = ["name", "desc"]
    list_filter = ["name", "desc", "add_times"]
    list_editable = ["name", "desc"]


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']
    # 富文本编辑
    style_fields = {
        'desc': 'ueditor'
    }


# 激活同一App下的模型，可在xadmin中显示。显示的是课程机构下的可选项
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
