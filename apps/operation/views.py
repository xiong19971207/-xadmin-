from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.base import View

from apps.operation.forms import UserFavForm, CommentForm
from apps.operation.models import UserFavorite, UserCourse, CourseComments
from apps.courses.models import Course, CourseResource
from apps.organizations.models import CourseOrg, Teacher


class CommentView(View):
    def post(self, request, *args, **kwargs):
        # 判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": 'fail',
                'msg': '用户未登录'
            })

        # 字段验证
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data['course']
            comments = comment_form.cleaned_data['comments']

            comment = CourseComments(user=request.user, course=course)
            comment.comments = comments
            comment.save()

            return JsonResponse({
                'status': 'success',
            })

        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误'
            })


class AddFavView(View):
    def post(self, request, *args, **kwargs):
        # 判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": 'fail',
                'msg': '用户未登录'
            })

        # 字段验证
        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data['fav_id']
            print(type(fav_id))
            fav_type = user_fav_form.cleaned_data['fav_type']

            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            print(bool(existed_records), request.user.id)
            if existed_records:
                existed_records.delete()
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': '收藏'
                })
            else:
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.save()
                return JsonResponse({
                    'status': 'success',
                    'msg': '已收藏'
                })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': '参数错误'
            })
