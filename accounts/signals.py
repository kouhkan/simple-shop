from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#
# @receiver(pre_save, sender=settings.AUTH_USER_MODEL)
# def set_new_user_inactive(sender, instance, **kwargs):
#     if instance.state.adding is True:
#         instance.is_active = False


