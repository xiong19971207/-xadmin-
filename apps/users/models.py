from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime


class BaseModel(models.Model):
    # 类型别设置成InterField,会报错
    add_times = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        # abstract = True 设置这个模型不生成表
        abstract = True


class UserProfile(AbstractUser):
    '''
        用户信息表
    '''
    GENDER_CHOICES = (
        ('male', '男'),
        ('female', '女')
    )

    nickname = models.CharField(max_length=10, null=True, default='', verbose_name='昵称')
    birthday = models.DateField(max_length=12, blank=True, null=True, verbose_name='生日')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name='性别')
    address = models.CharField(max_length=30, default='', verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    image = models.ImageField(max_length=50, upload_to='head_img', default="default.jpg", verbose_name='头像')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username

    def unread_message(self):
        # 有多少未读消息
        return self.usermessage_set.all().filter(has_read=False).count()
