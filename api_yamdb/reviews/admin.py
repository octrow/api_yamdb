from django.contrib import admin
from django.contrib.auth.models import Group

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ["name"]


class GenreTitleTabular(admin.TabularInline):
    model = GenreTitle


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ("name", "year", "description", "category")
    search_fields = ["name", "year"]
    list_filter = ("category", "genre")
    list_editable = ("category", "year", "description")
    inlines = [GenreTitleTabular]
    # Вторая часть замечания решена, но не первая, повторю:
    # Нужно вывести список Жанров в списке Произведений.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "title_id", "author", "pub_date")
    search_fields = ["text"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "review_id", "author", "pub_date")
    search_fields = ["text", "review"]


admin.site.unregister(Group)
