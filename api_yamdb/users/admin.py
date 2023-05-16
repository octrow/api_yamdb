from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'role')
    list_display_links = ('username', 'email')
    list_editable = ('role',)
