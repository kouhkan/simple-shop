from django.contrib import admin
from .models import Profile, User
from django.conf import settings
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(User, UserAdmin)
