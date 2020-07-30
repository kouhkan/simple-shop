from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import MyUserManager


class User(AbstractUser):
    email = models.EmailField(max_length=250, unique=True)
    username = models.CharField(max_length=11, unique=True, verbose_name='Phone Number')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=150, null=True)
    province = models.CharField(max_length=150, null=True)

    def __str__(self):
        return self.user