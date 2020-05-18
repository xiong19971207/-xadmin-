from DjangoUeditor.models import UEditorField
from django.db import models

from apps.users.models import BaseModel, UserProfile


class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name='城市名')
    desc = models.CharField(max_length=150, verbose_name='描述')

    # 魔法方法，使添加城市时返回self.name这个名字，不然会返回objects
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name


class CourseOrg(BaseModel):
    '''
        授课机构表
    '''

    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = UEditorField(verbose_name='描述', width=600, height=300, imagePath='org/ueditor/images/',
                        filePath='org/ueditor/files/', default='')
    tag = models.CharField(default="全国知名", max_length=10, verbose_name="机构标签")
    category = models.CharField(default="pxjg", verbose_name="机构类别", max_length=4,
                                choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")))
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")

    is_gold = models.BooleanField(default=False, verbose_name='是否金牌')
    is_identification = models.BooleanField(default=False, verbose_name='是否认证')

    def __str__(self):
        return self.name

    def courses(self):
        """
        通过主表查询字表的数据
        利用Django外键的显性方法
        :return: courses
        """
        courses = self.course_set.filter(is_classics=True)
        return courses

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name


class Teacher(BaseModel):
    '''
        老师表
    '''
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name=u"教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)

    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True, verbose_name='用户')

    def __str__(self):
        return self.name

    def get_teacher_courses(self):
        """
        自定义方法求出教师的课程数
        :return:
        """
        teacher_courses = self.course_set.all().count()
        return teacher_courses

    class Meta:
        verbose_name = "讲师"
        verbose_name_plural = verbose_name
