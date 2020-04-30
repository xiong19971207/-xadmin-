import random

import redis
from django.core.mail import send_mail
from django.http import JsonResponse


def gen_random_code():
    return ''.join([str(random.randint(0, 9)) for code in range(4)])


def send_email(email):
    '''发送email'''

    vcode = gen_random_code()
    print(vcode)

    # 把验证码写进redis
    rds = redis.Redis(host='localhost', port=6379, db=0)
    rds.set(str('17855370672@163.com'), vcode)
    print(rds.get(str(email)))

    subject = '熊氏老方'
    message = '没有用，但必须写'

    from_email = '17855370672@163.com'
    recipient_list = [email]
    print(recipient_list)

    html_message = '<h1>你的验证码是:</h1>' + vcode

    send_mail(subject=subject, message=message, html_message=html_message, from_email=from_email,
              recipient_list=recipient_list)

    return JsonResponse('OK', safe=False)
