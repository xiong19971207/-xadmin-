from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.courses.models import Course, CourseTag, CourseResource, Video
from pure_pagination import Paginator, PageNotAnInteger

from apps.operation.models import UserFavorite, UserCourse, CourseComments


class PlayView(LoginRequiredMixin,View):
    # 检查是否登录，没有则返回登陆页面,Django中的基于类视图的LoginRequiredMixin
    login_url = '/login/'

    def get(self, request, course_id,play_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 关联用户与课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 视频
        video_play = Video.objects.get(id=int(play_id))

        # 所有用户的评论
        comments = CourseComments.objects.filter(course=course)

        # 显示学过该课程的人还学过哪些课程
        all_user_courses = UserCourse.objects.filter(course=course)  # 都学这门课的用户
        all_user_id = [user_course.user.id for user_course in all_user_courses]  # 都学这门课的用户ID
        all_courses = UserCourse.objects.filter(user_id__in=all_user_id)[:5]  # 都学这门课的用户学的别的课程
        # 所有学过当前课程人学的课程,排除当前课程
        related_course = []
        for course1 in all_courses:
            if course1.course.id != course.id:
                related_course.append(course1.course)

        # 课程资源
        all_resourse = CourseResource.objects.filter(course=course)

        return render(request, 'course-play.html', {
            "course": course,
            'all_resourse': all_resourse,
            'related_course': related_course,
            'comments': comments,
            'video_play':video_play
        })


class CourseCommentView(LoginRequiredMixin, View):
    # 检查是否登录，没有则返回登陆页面,Django中的基于类视图的LoginRequiredMixin
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 关联用户与课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 所有用户的评论
        comments = CourseComments.objects.filter(course=course)

        # 显示学过该课程的人还学过哪些课程
        all_user_courses = UserCourse.objects.filter(course=course)  # 都学这门课的用户
        all_user_id = [user_course.user.id for user_course in all_user_courses]  # 都学这门课的用户ID
        all_courses = UserCourse.objects.filter(user_id__in=all_user_id)[:5]  # 都学这门课的用户学的别的课程
        # 所有学过当前课程人学的课程,排除当前课程
        related_course = []
        for course1 in all_courses:
            if course1.course.id != course.id:
                related_course.append(course1.course)

        # 课程资源
        all_resourse = CourseResource.objects.filter(course=course)

        return render(request, 'course-comment.html', {
            "course": course,
            'all_resourse': all_resourse,
            'related_course': related_course,
            'comments': comments
        })


class CourseVideoView(LoginRequiredMixin, View):
    # 检查是否登录，没有则返回登陆页面,Django中的基于类视图的LoginRequiredMixin
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        # 关联用户与课程
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 显示学过该课程的人还学过哪些课程
        all_user_courses = UserCourse.objects.filter(course=course)  # 都学这门课的用户
        all_user_id = [user_course.user.id for user_course in all_user_courses]  # 都学这门课的用户ID
        all_courses = UserCourse.objects.filter(user_id__in=all_user_id)[:5]  # 都学这门课的用户学的别的课程
        # 所有学过当前课程人学的课程,排除当前课程
        related_course = []
        for course1 in all_courses:
            if course1.course.id != course.id:
                related_course.append(course1.course)

        # 课程资源
        all_resourse = CourseResource.objects.filter(course=course)

        return render(request, 'course-video.html', {
            "course": course,
            'all_resourse': all_resourse,
            'related_course': related_course
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):

        course = Course.objects.get(id=int(course_id))
        course.fav_nums += 1
        course.save()

        # 判断用户是否收藏
        is_fav_course = False
        is_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                is_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                is_fav_org = True

        # 相似课程
        all_tags = course.coursetag_set.all()
        tag_list = [tag.tag for tag in all_tags]
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course_id=course.id)
        related_courses = set()
        for bq in course_tags:
            related_courses.add(bq.course)

        return render(request, 'course-detail.html', {
            'course': course,
            'is_fav_course': is_fav_course,
            'is_fav_org': is_fav_org,
            'related_courses': related_courses
        })


class CourseListView(View):
    def get(self, request, *args, **kwargs):

        all_courses = Course.objects.order_by('-add_times')
        hot_course = Course.objects.order_by('-fav_nums')

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_courses = all_courses.order_by('-fav_nums')
        elif sort == 'students':
            all_courses = all_courses.order_by('-students')

        # 设置分页器
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=3, request=request)
        # orgs是page对象，而不是queryset对象，前端调用要有object_list
        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            'sort': sort,
            'hot_course': hot_course,
        })
