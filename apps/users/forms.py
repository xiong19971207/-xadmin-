from captcha.fields import CaptchaField
from django import forms


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
    captcha = CaptchaField()