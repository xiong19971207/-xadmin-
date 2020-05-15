import redis
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic.base import View

from apps.users.forms import LoginForms, DynamicLoginForm, RegisterForms, UploadImgForm
from apps.users.forms import ChangeEmailForm, UserInfoForm, UserPwdForm
from apps.users.logics import send_email
from apps.users.models import UserProfile
from apps.operation.models import UserFavorite, UserCourse, UserMessage, Banner
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course

from pure_pagination import Paginator, PageNotAnInteger


class CustomAuth(ModelBackend):
    # 检查用户是否登录
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 重写authenticate方法
        try:
            # 无论是电话号码登录还是用户名登录都可以
            user = UserProfile.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception:
            return None


class IndexView(View):
    def get(self, request):
        # 首页的全部数据
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)
        course_orgs = CourseOrg.objects.all()[:15]
        banners = Banner.objects.all().order_by('index')

        return render(request, 'index.html', {
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
            "banners": banners,
        })


class MessageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        current_page = 'message'
        # 获取用户消息
        message_list = []
        messages = UserMessage.objects.filter(user=request.user)
        for message in messages:
            message_list.append(message)

        # 进入之后变成True
        for message in message_list:
            message.has_read = True
            message.save()

        # 设置分页器
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(message_list, per_page=1, request=request)
        all_messages = p.page(page)

        return render(request, 'usercenter-message.html', {
            'current_page': current_page,
            'message_list': all_messages
        })


class UserFavTeacherView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # 用户收藏的授课机构
        user_fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        teacher_list = []
        for teacher in user_fav_teachers:
            # 通过id找出授课机构
            teachers = Teacher.objects.get(id=teacher.fav_id)
            teacher_list.append(teachers)

        current_page = 'myfavorg'

        return render(request, 'usercenter-fav-teacher.html', {
            'teacher_list': teacher_list,
            'current_page': current_page
        })


class UserFavCourseView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # 用户收藏的教师
        user_fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        course_list = []
        for course in user_fav_courses:
            # 通过id找出授课机构
            courses = Course.objects.get(id=course.fav_id)
            course_list.append(courses)

        current_page = 'myfavorg'

        return render(request, 'usercenter-fav-course.html', {
            'course_list': course_list,
            'current_page': current_page
        })


class UserFavOrgView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # 用户收藏的授课机构
        user_fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        org_list = []
        for org in user_fav_orgs:
            # 通过id找出授课机构
            courseorg = CourseOrg.objects.get(id=org.fav_id)
            org_list.append(courseorg)

        current_page = 'myfavorg'

        return render(request, 'usercenter-fav-org.html', {
            'org_list': org_list,
            'current_page': current_page
        })


class UserMycourseView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # 我的课程
        my_courses = UserCourse.objects.filter(user=request.user)
        # 选中状态
        current_page = 'mycourse'
        return render(request, 'usercenter-mycourse.html', {
            'my_courses': my_courses,
            'current_page': current_page
        })


class ChangeEmailView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        user_email_form = ChangeEmailForm(request.POST)
        if user_email_form.is_valid():
            email = user_email_form.cleaned_data['email']
            user = request.user
            user.email = email
            user.save()
            data = {
                'status': 'success'
            }
            return render(request, 'usercenter-info.html', context=data)
        return render(request, 'usercenter-info.html', {
            'status': 'fail'
        })


class UpdatePwdView(View):
    def post(self, request, *args, **kwargs):
        user_pwd_form = UserPwdForm(request.POST)
        if user_pwd_form.is_valid():
            user = request.user
            pwd = request.POST.get('password1')
            user.set_password(pwd)
            user.save()
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse(user_pwd_form.errors)


class UploadImgView(View):
    def post(self, request, *args, **kwargs):
        # instance 指定修改那个实例
        user_img_form = UploadImgForm(request.POST, files=request.FILES, instance=request.user)
        if user_img_form.is_valid():
            user_img_form.save()
            return JsonResponse({
                'status': 'success'
            })
        else:
            return JsonResponse({
                'status': 'fail'
            })


class UserInfoView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, *args, **kwargs):

        # 验证码
        captcha_form = RegisterForms()
        # 选中状态
        current_page = 'info'
        return render(request, 'usercenter-info.html', {
            'captcha_form': captcha_form,
            "current_page": current_page
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(user_info_form.errors)


class LoginView(View):
    def get(self, request, *args, **kwargs):

        # 這一步是把vcode_form傳到前端去，然後vcode_form.captcha显示验证码
        vcode_form = DynamicLoginForm()

        next = request.GET.get('next', '')

        # 判断用户是否登录
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return render(request, 'login.html', {
            'vcode_form': vcode_form,
            'next': next
        })

    def post(self, request, *args, **kwargs):

        # 表单验证
        forms_check = LoginForms(request.POST)

        if forms_check.is_valid():
            # clean_data是一个字典
            username = forms_check.cleaned_data['username']
            password = forms_check.cleaned_data['password']

            # Django中自带的方法，用以创建一个自己的UserProfile对象
            user = authenticate(username=username, password=password)

            if user:

                # login这个方法表示用户已经登陆，好像还能把数据传到前端页面
                login(request, user)

                # 没登录之前查看内容，必须登陆。
                # 登陆之后跳转到浏览前的位置
                next = request.GET.get('next', '')
                if next:
                    return redirect(next)
                return redirect(reverse('index'))
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'forms_check': forms_check})
        else:
            return render(request, 'login.html', {'forms_check': forms_check})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('index'))


class SendEmailView(View):

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        print(email)
        send_email(email)
        return JsonResponse('OK', safe=False)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        check_forms = RegisterForms()

        return render(request, 'register.html', {'check_forms': check_forms})

    def post(self, request, *args, **kwargs):

        # 验证请求
        check_forms = RegisterForms(request.POST)

        if check_forms.is_valid():

            rds = redis.Redis(host='localhost', port=6379, db=0)
            ajax_code = '17855370672@163.com'
            code = int(rds.get(ajax_code))
            print(code)

            rds_code = int(rds.get('17855370672@163.com'))
            print(bool(code == rds_code))
            if rds_code == code:
                email = check_forms.cleaned_data['email']
                password = check_forms.cleaned_data['password']
                isuser_exists = UserProfile.objects.filter(email=email)
                print(bool(isuser_exists))

                if isuser_exists:
                    user = isuser_exists[0]
                    login(request, user)
                else:
                    user = UserProfile()
                    # 给新建用户一个随机的验证码并加密
                    user.set_password(password)
                    user.email = email
                    user.username = email
                    user.save()
                    login(request, user)
                return render(request, 'index.html')
            else:
                return JsonResponse({'msg': '你写的不对'})
        else:
            check_forms = RegisterForms()

            return render(request, 'register.html', {'check_forms': check_forms})
