from django.db.models import Q
from django.http import JsonResponse
from pure_pagination import Paginator, PageNotAnInteger
from django.shortcuts import render

from django.views.generic.base import View
from apps.organizations.models import CourseOrg, City, Teacher
from apps.organizations.forms import AddAskForm
from apps.operation.models import UserFavorite


class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        # 当前老师
        teacher = Teacher.objects.get(id=int(teacher_id))

        # 老师热度榜
        hot_teachers = Teacher.objects.all().order_by('-click_nums')

        # 判断收藏还是没有收藏
        has_teacher_fav = False
        has_org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_org_fav = True

        return render(request, 'teacher-detail.html', {
            'teacher': teacher,
            "hot_teachers": hot_teachers,
            "has_teacher_fav": has_teacher_fav,
            "has_org_fav": has_org_fav,
        })


class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        teachers = Teacher.objects.all()

        # 所有教师数量
        teachers_nums = teachers.count()

        # 热度老师
        hot_teachers = teachers.order_by('-click_nums')
        # 按热度对老师排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-click_nums')

        # 搜索关键字
        keywords = request.GET.get('keywords', '')
        s_type = 'teacher'
        if keywords:
            teachers = teachers.filter(Q(name__icontains=keywords))

        # 设置分页器
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, per_page=1, request=request)
        all_teachers = p.page(page)

        return render(request, 'teachers-list.html', {
            'all_teachers': all_teachers,
            'teachers_nums': teachers_nums,
            'hot_teachers': hot_teachers,
            'sort': sort,
            "keywords":keywords,
            "s_type": s_type

        })


class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        # 前端页面选中状态判断用的
        current_page = 'desc'

        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()

        course_org.click_nums = course_org.click_nums + 1
        course_org.save()

        # 判断收藏还是没有收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            "all_courses": all_courses,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        # 前端页面选中状态判断用的
        current_page = 'course'

        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums = course_org.click_nums + 1
        course_org.save()

        all_courses = course_org.course_set.all()

        # 设置分页器
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=3, request=request)
        # orgs是page对象，而不是queryset对象，前端调用要有object_list
        courses = p.page(page)

        # 判断收藏还是没有收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-course.html', {
            'course_org': course_org,
            'all_courses': courses,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgTeacherView(View):

    def get(self, request, org_id, *args, **kwargs):
        # 前端页面选中状态判断用的
        current_page = 'teacher'

        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums = course_org.click_nums + 1
        course_org.save()

        all_teacher = course_org.teacher_set.all()

        # 判断收藏还是没有收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-teachers.html', {
            'course_org': course_org,
            'all_teacher': all_teacher,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums = course_org.click_nums + 1
        course_org.save()

        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()
        current_page = 'home'

        # 判断收藏还是没有收藏
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-homepage.html', {
            'course_org': course_org,
            'all_courses': all_courses,
            'all_teacher': all_teacher,
            'current_page': current_page,
            'has_fav': has_fav
        })


class AddAskView(View):
    """
    用户咨询页面的视图
    """

    def post(self, request, *args, **kwargs):
        user_ask_form = AddAskForm(request.POST)
        if user_ask_form.is_valid():
            user_ask_form.save(commit=True)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错"
            })


class OrgListView(View):
    """
    授课机构的显示
    """

    def get(self, request, *args, **kwargs):

        all_orgs = CourseOrg.objects.all()
        all_citys = City.objects.all()
        # 根据收藏数显示机构
        hot_orgs = all_orgs.order_by('-fav_nums')[:3]

        # 根据机构查询
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 根据城市查询
        city_id = request.GET.get('city', '')
        if city_id:
            if city_id.isdigit():  # 判断对象是不是字符串
                all_orgs = all_orgs.filter(city_id=int(city_id))

        # 根据学生人数、课程数排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        # 机构数量
        all_orgs_nums = all_orgs.count()

        # 搜索关键字
        keywords = request.GET.get('keywords', '')
        s_type = 'org'
        if keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        # 设置分页器
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, per_page=3, request=request)
        # orgs是page对象，而不是queryset对象，前端调用要有object_list
        orgs = p.page(page)

        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'all_orgs_nums': all_orgs_nums,
            'category': category,
            'city_id': city_id,
            'sort': sort,
            'hot_orgs': hot_orgs,
            "keywords": keywords,
            "s_type": s_type
        })
