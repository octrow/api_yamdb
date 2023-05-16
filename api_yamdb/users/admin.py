from django.contrib import admin

# Могу кстати пару фишек показать, например если хочешь, чтобы кликабельным было другое поле, то либо указываешь его первым в list_display либо если нужно 2 поля то можно прописать  list_display_links и в нём указать нужные поля.
# Для того чтобы была возможность в админке изменять пароль для пользователя то можно импортировать это:
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin и унаследовать класс AdminUser от него.
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = ("username", "email")
    # Можно сделать роль - редактируемой.
