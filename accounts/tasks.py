from celery import shared_task
from django.conf import settings
from django.contrib.auth import authenticate
from .models import User
import redis
from django.shortcuts import get_object_or_404
from random import randint
from django.core.mail import send_mail
from django.core.signing import Signer
from django.conf import settings

redis = redis.StrictRedis(host=settings.REDIS_HOST,
                          db=settings.REDIS_DB,
                          port=settings.REDIS_PORT)
signer = Signer(salt=settings.SECRET_KEY)


@shared_task
def user_register_task(username, email, password):
    check_user = User.objects.filter(email=email)
    if check_user.exists():
        return 2
    else:
        User.objects.create_user(
                username=username,
                email=email,
                password=password)
        active_code = randint(1000, 9999)
        redis.set(email, active_code)
        redis.expire(email, 120)
        body = 'http://localhost:8000/accounts/verify/{}/{}/'.format(signer.sign(email), active_code)
        send_mail('فعال‌سازی حساب', body, settings.EMAIL_HOST_USER, [email])
        return 1


@shared_task
def user_login_task(email):
    check_user = User.objects.filter(email=email)
    if check_user.exists() and check_user.filter(is_active=True).exists():
        # user = authenticate(request, email=email, password=password)
        return 1
    elif check_user.exists() and not(check_user.filter(is_active=True).exists()):
        active_code = randint(1000, 9999)
        redis.set(email, active_code)
        redis.expire(email, 120)
        body = 'http://localhost:8000/accounts/verify/{}/{}/'.format(signer.sign(email), active_code)
        send_mail('فعال‌سازی حساب', body, settings.EMAIL_HOST_USER, [email])
        return 2
    else:
        return 3


@shared_task
def user_verify_task(email, code):
    check_email = redis.get(email)
    if check_email is not None:
        get_user = User.objects.get(email=email)
        if check_email.decode('utf-8') == code:
            get_user.is_active = True
            get_user.save()

            return 1
        else:
            return 2
    else:
        return 3


@shared_task
def user_resend_code_task(email):
    active_code = randint(1000, 9999)
    redis.set(email, active_code)
    redis.expire(email, 120)
    body = 'http://localhost:8000/accounts/verify/{}/{}/'.format(signer.sign(email), active_code)
    send_mail('فعال‌سازی حساب', body, settings.EMAIL_HOST_USER, [email])
    return 1


@shared_task
def user_change_password_task(email, code, password, confirm_password):
    get_user = User.objects.get(email=signer.unsign(email))
    user_code = redis.get(get_user.email)
    if user_code is not None and user_code.decode('utf-8') == signer.unsign(code):
        if password == confirm_password:
            get_user.set_password(confirm_password)
            get_user.save()

            return 1
        else:
            return 2
    else:
        return 3


@shared_task
def user_forget_task(email, active_code):
    redis.set(email, active_code)
    redis.expire(email, 120)
    body = 'http://localhost:8000/accounts/change-password/{}/{}/'.format(signer.sign(email), signer.sign(active_code))
    send_mail('فعال‌سازی حساب', body, settings.EMAIL_HOST_USER, [email])
    return 1