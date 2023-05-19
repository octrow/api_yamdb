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
    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])

    get_genres.short_description = "Жанры"
    list_display = ("name", "year", "description", "category", "get_genres")
    search_fields = ["name", "year"]
    list_filter = ("category", "genre")
    list_editable = ("category", "year")
    inlines = [GenreTitleTabular]

    # ГОТОВО! Вторая часть замечания решена, но не первая, повторю:
    # Нужно вывести список Жанров в списке Произведений.
    # old: Нужно вывести список жанров в списке Произведения, но и этого мало.
    # Если зайти в само произведение то ничего не будет, а хочется
    # редактировать жанры произведения, поможет это
    # https://stackoverflow.com/questions/
    # 64325709/using-tabularinline-in-django-admin


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "title_id", "author", "pub_date")
    search_fields = ["text"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "review_id", "author", "pub_date")
    search_fields = ["text", "review"]


admin.site.unregister(Group)
