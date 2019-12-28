from django.contrib import admin
# Register your models here.
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


admin.site.register(UserProfile, UserAdmin)
