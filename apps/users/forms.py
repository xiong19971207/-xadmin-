import redis
from captcha.fields import CaptchaField
from django import forms
from django.http import JsonResponse

from apps.users.models import UserProfile


class ChangeEmailForm(forms.Form):
    """
        验证email和验证码
    """
    email = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField()
    code = forms.CharField(required=True, max_length=4, min_length=4)


class UserPwdForm(forms.Form):
    password1 = forms.CharField(min_length=5, required=True)
    password2 = forms.CharField(min_length=5, required=True)

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("密码不一致")
        return self.cleaned_data


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'birthday', 'address', 'gender']


class UploadImgForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class LoginForms(forms.Form):
    """
        username、password必须与前端页面input内容中的name属性一致
        required 表示这个字段必须存在，不为空
    """
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


class DynamicLoginForm(forms.Form):
    """
    动态验证码验证类
    """
    email = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField()


class RegisterForms(forms.Form):
    """
        验证email和验证码
    """
    email = forms.CharField(required=True, min_length=8)
    captcha = CaptchaField()
    password = forms.CharField(required=True)
    jsSendCode1234 = forms.CharField(required=True, max_length=4, min_length=4)

    # def clean(self):
    #     """
    #         此方法会在clean_data之前调用
    #         此处调用为了检查验证码
    #     :return:
    #     """
    #     email = self.cleaned_data['email']
    #     code = self.cleaned_data['jsSendCode1234']
    #     rds = redis.Redis(host='localhost', port=6379, db=0)
    #     rds_code = rds.get(email)
    #     if code != rds_code:
    #         raise forms.ValidationError('验证码不正确哦')
    #     return self.cleaned_data
