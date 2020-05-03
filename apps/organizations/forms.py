import re

from django import forms

from apps.operation.models import UserAsk


class AddAskForm(forms.ModelForm):
    mobile = forms.CharField(min_length=11, max_length=11, required=True)

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        :return:
        """
        mobile = self.cleaned_data['mobile']
        check_mobile = r"^1[35678]\d{9}"
        p = re.compile(check_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法', code='mobile_invalid')
