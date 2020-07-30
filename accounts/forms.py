from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)


class UserRegisterForm(forms.Form):
    username = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': 'Phone number'}),
            label='Phone number',
            min_length=11,
            max_length=11,
    )
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={'placeholder': 'پست الکترونیکی معتبر وارد کنید'}),
            label='پست الکترونیکی'
    )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور قوی و بیشتر از ۷ کاراکتر انتخاب کنید'}),
            label='رمز عبور',
            min_length=7,
    )


class UserLoginForm(forms.Form):
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={'placeholder': 'پست الکترونیکی خود را وارد کنید'}),
            label='پست الکترونیکی'
    )
    password = forms.CharField(
            widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور خود را وارد کنید'}),
            label='رمز عبور',
            min_length=7
    )


class UserActiveForm(forms.Form):
    code = forms.CharField(
            label='کد فعال‌سازی',
            min_length=4,
            max_length=4,
            widget=forms.TextInput(attrs={'placeholder': 'کد فعال‌سازی ارسال شده را وارد کنید'}))


class UserForgetForm(forms.Form):
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={'placeholder': 'پست الکترونیکی خود را وارد کنید'}),
            label='پست الکترونیکی')


class UserChangePasswordForm(forms.Form):
    password1 = forms.CharField(
            label='رمز عبور جدید',
            min_length=7,
            widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور قوی و بیشتر از ۷ کاراکتر'}))

    password2 = forms.CharField(
            label='تایید رمز عبور',
            min_length=7,
            widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور خود را تایید کنید'}))

    def clean_password2(self):
        pass1 = self.cleaned_data['password1']
        pass2 = self.cleaned_data['password2']

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('رمز عبور تایید نمی‌شود')

        return pass2