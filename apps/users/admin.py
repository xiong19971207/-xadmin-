from django.contrib import admin

# 解决用户密码无法实现自动加密登陆不上的问题
from django.contrib.auth.admin import UserAdmin

from apps.users.models import UserProfile


# 将自己的UserProfile表注册到后台管理系统
class UserProfileAdmin(admin.ModelAdmin):
    pass


# 将表与管理器连接起来
# xadmin能够自己注册进来不需要下列代码

admin.site.register(UserProfile, UserAdmin)
