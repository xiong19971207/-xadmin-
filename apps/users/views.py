from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic.base import View

from apps.users.forms import LoginForms, DynamicLoginForm, DynamicRegisterForms


def chat(request):
    return render(request, 'chat.html')


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        d_login_form = DynamicRegisterForms()

        return render(request, 'register.html', {'d_login_form': d_login_form})

    def post(self, request, *args, **kwargs):
        return render(request, 'register.html')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('index'))


class LoginView(View):
    def get(self, request, *args, **kwargs):

        # 這一步是把vcode_form傳到前端去，然後vcode_form.captcha显示验证码
        vcode_form = DynamicLoginForm()

        # 判断用户是否登录
        if request.user.is_authenticated:
            return redirect(reverse('index'))
        return render(request, 'login.html', {'vcode_form': vcode_form})

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
                return redirect(reverse('index'))
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误', 'forms_check': forms_check})
        else:
            return render(request, 'login.html', {'forms_check': forms_check})
