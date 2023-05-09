from django.contrib import admin
from reviews.models import Category, Genre, Title

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]
    
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]
    
@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "description")
    search_fields = ["name", "year"]