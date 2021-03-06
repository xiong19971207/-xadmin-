"""
Django settings for Xadministration project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1fk2sv&d%d*w9%o(y_3-$hh_&ytglp!9z-k_-jm2+i4xk#_0+$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 添加模块的App配置
    # 用户模块
    'apps.users.apps.UsersConfig',
    # 课程模块
    'apps.courses.apps.CoursesConfig',
    # 用户浏览模块
    'apps.operation.apps.OperationConfig',
    # 教育机构模块
    'apps.organizations.apps.OrganizationsConfig',

    'crispy_forms',
    'xadmin.apps.XAdminConfig',

    # 验证码
    'captcha',

    # 分页器设置
    'pure_pagination',

    # 富文本编辑器
    'DjangoUeditor',

    # 导入导出设置
    'import_export'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Xadministration.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 这个中间件会把设置的MEDIA_URL返回给前端页面，这样我们就不用每次在后端传递了
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                # 上下文管理器
                # 'apps.users.views.message_nums'
            ],
        },
    },
]

WSGI_APPLICATION = 'Xadministration.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xadmin',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'USER': 'root',
        'PORT': 3306
    }
}

# 必须填写，Django才知道关联的是哪个模型
AUTH_USER_MODEL = 'users.UserProfile'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/


LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
# 下面两个只能存在一个
STATICFILES_DIRS = [BASE_DIR, os.path.join('static')]
# STATIC_ROOT = os.path.join(BASE_DIR,'static')

# MEDIA的配置,配置之后文件自动存到media下
MEDIA_URL = "/media/"
# 不能写成MEDIA_ROOT = [BASE_DIR, os.path.join('media')]会报错
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 网易邮箱设置
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = '17855370672@163.com'
EMAIL_HOST_PASSWORD = 'sx123456'

# 分页器设置
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 2,
    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}

# 设置登录检验
AUTHENTICATION_BACKENDS = ['apps.users.views.CustomAuth']











