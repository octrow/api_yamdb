from django.contrib import admin
from reviews.models import Category, Genre, Title, Review, Comment


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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "author", "pub_date")
    search_fields = ["text"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "review", "author", "pub_date")
    search_fields = ["text", "review"]
