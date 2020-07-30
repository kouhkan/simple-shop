from django.apps import AppConfig
from .signals import save_user_profile, create_user_profile
# set_new_user_inactive
from django.db.models.signals import post_save, pre_save
from django.conf import settings


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
        post_save.connect(save_user_profile, sender=settings.AUTH_USER_MODEL)
        # pre_save.connect(set_new_user_inactive, sender=settings.AUTH_USER_MODEL)