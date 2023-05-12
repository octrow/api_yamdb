from django.contrib import admin

from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = (
        'pk', 'username', 'email','first_name',
        'last_name', 'bio', 'role'
    )
    list_editable = ('role', )
    search_fields = ('username',)
