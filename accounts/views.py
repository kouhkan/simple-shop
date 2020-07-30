from random import randint

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from .forms import (UserRegisterForm,
                    UserLoginForm,
                    UserForgetForm,
                    UserActiveForm,
                    UserChangePasswordForm)
from .tasks import (user_register_task,
                    user_resend_code_task,
                    user_change_password_task,
                    user_verify_task,
                    user_login_task,
                    user_forget_task,

                    signer)


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = user_register_task.delay(cd['username'], cd['email'], cd['password'])
            if user.get() == 1:
                request.session['user_email'] = cd['email']
                messages.success(request, 'ثبت نام', 'success')
                request.session['user_email'] = cd['email']
                return redirect('accounts:user_active')
            elif user.get() == 2:
                messages.error(request, 'کاربری با این پست الکترونیکی وجود دارد', 'danger')
                return redirect('accounts:user_register')
            else:
                pass
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/user_register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            check_login = user_login_task.delay(cd['email'])

            if check_login.get() == 2:
                request.session['user_email'] = cd['email']
                messages.error(request, 'کاربر فعال نیست', 'danger')
                return redirect('accounts:user_active')
            elif check_login.get() == 3:
                request.session['user_email'] = cd['email']
                messages.error(request, 'کاربر وجود ندارد', 'danger')
                return redirect('accounts:user_register')
            else:
                user = authenticate(request, email=cd['email'], password=cd['password'])
                login(request, user)
                messages.success(request, 'وارد شدید', 'success')
                return redirect('accounts:user_index')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/user_login.html', context)


def user_active(request):
    return render(request, 'accounts/user_active.html')


@login_required
def user_change_password(request, email=None, code=None):
    if email is not None and code is not None:
        if request.method == 'POST':
            form = UserChangePasswordForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                result = user_change_password_task.delay(email, code, cd['password1'], cd['password2'])

                if result.get() == 1:
                    messages.success(request, 'رمز عوض شد', 'success')
                    return redirect('accounts:user_login')
                elif result.get() == 2:
                    messages.success(request, 'رمز عوض نشد', 'danger')
                    return redirect('accounts:user_forget')
                elif result.get() == 3:
                    messages.success(request, 'لینک معتبر نیست', 'danger')
                    return redirect('accounts:user_forget')
                else:
                    pass
        else:
            form = UserChangePasswordForm()

        context = {
            'form': form
        }
        return render(request, 'accounts/user_change_pssword.html', context)
    else:
        return render(request, 'accounts/send_link.html')


def user_forget(request):
    if request.method == 'POST':
        form = UserForgetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            get_user = get_object_or_404(User, email=user_email)
            if get_user.is_active:
                active_code = randint(1000, 9999)
                result = user_forget_task.delay(user_email, active_code)
                if result.get() == 1:
                    messages.success(request, 'لینک تغییر رمز عبور ارسال شد', 'success')
                    return redirect('accounts:user_change_password_reset')
                else:
                    messages.error(request, 'خطایی رخ داده است', 'danger')
                    return redirect('accounts:user_forget')
            else:
                user_resend_code_task.delay(user_email)
                messages.error(request, 'حساب شما فعال نیست', 'danger')
                return redirect('accounts:user_active')
    else:
        form = UserForgetForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/user_forget.html', context)


def resend_code(request):
    user = get_object_or_404(User, email=request.session['user_email'])
    if user.is_active:
        messages.error(request, 'حساب شما فعال است', 'warning')
        return redirect('accounts:user_login')
    else:
        user_resend_code_task.delay(user.email)
        return render(request, 'accounts/user_active.html')

    # return render(request, 'accounts/user_resend_code.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'خروج', 'success')
    return redirect('accounts:user_login')


def user_verify(request, email, code):
    user_email = signer.unsign(email)
    result = user_verify_task.delay(user_email, code)

    if result.get() == 1:
        messages.success(request, 'فعال شد', 'success')
        del request.session['user_email']
        return redirect('accounts:user_login')
    elif result.get() == 2:
        messages.error(request, 'کد نادرست است', 'danger')
        return redirect('accounts:user_register')
    elif result.get() == 3:
        messages.error(request, 'کد  منقضی شده است', 'danger')
        return redirect('accounts:resend_code')


@login_required
def user_index(request):
    return render(request, 'accounts/index.html')