from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Profile


class ProfileInline(admin.StackedInline):
   model = Profile
   fields = ['birth_date', 'avatar']

class ProfileAdmin(UserAdmin):
   inlines = [ProfileInline]


admin.site.register(get_user_model(), ProfileAdmin)
