import redis
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic.base import View

from apps.users.forms import LoginForms, DynamicLoginForm, RegisterForms
from apps.users.logics import send_email, gen_random_code
from apps.users.models import UserProfile


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
