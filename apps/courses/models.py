from DjangoUeditor.models import UEditorField
from django.db import models
from django.utils.safestring import mark_safe

from apps.organizations.models import Teacher, CourseOrg
from apps.users.models import BaseModel


class Course(BaseModel):
    """
        课程表字段
        课程关联老师外键
    """

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='老师')
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=models.CASCADE, verbose_name='授课机构')

    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    degree = models.CharField(verbose_name="难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(default=u"后端开发", max_length=20, verbose_name="课程类别")
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10)
    you_need_know = models.CharField(default="", max_length=300, verbose_name="课程须知")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="老师告诉你")

    detail = UEditorField(verbose_name='课程详情',width=600,height=300,imagePath='courses/ueditor/images/',
                          filePath='courses/ueditor/files/',default='')
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)

    is_classics = models.BooleanField(default=False, verbose_name='是否是经典')
    is_banner = models.BooleanField(default=False, verbose_name='是否是广告位')

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def show_image(self):
        # 在xadmin中显示图片
        return mark_safe('<img src="{}" style="width: 102.4px;height:76.8px">'.format(self.image.url))

    show_image.short_description = '图片'

    def go_to(self):
        # 配置跳转
        return mark_safe('<a href="/course/{}">跳转</a>'.format(self.id))
    go_to.short_description = '跳转'

    def __str__(self):
        # 添加字段时返回名字
        return self.name


class BannerCourse(Course):
    # 管理轮播课程
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True

    def __str__(self):
        return self.name


class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    tag = models.CharField(max_length=100, verbose_name='标签')

    class Meta:
        verbose_name = "课程标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Lesson(BaseModel):
    '''
        章节表
    '''
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=50, verbose_name='章节名')
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")

    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='关联章节')
    name = models.CharField(max_length=50, verbose_name='视频名')
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    url = models.CharField(max_length=1000, verbose_name='播放地址')

    class Meta:
        verbose_name = "课程视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    '''
        课程资源表
    '''
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name="名称")
    file = models.FileField(max_length=200, upload_to="course/resourse/%Y/%m", verbose_name="下载地址")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
