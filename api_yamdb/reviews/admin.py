from django.contrib import admin

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


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
    # Нужно вывести список жанров в списке Произведения, но и этого мало.
    # Если зайти в само произведение то ничего не будет, а хочется редактировать
    # жанры произведения, поможет это https://stackoverflow.com/questions/64325709/using-tabularinline-in-django-admin


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("text", "title_id", "author", "pub_date")
    search_fields = ["text"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "review_id", "author", "pub_date")
    search_fields = ["text", "review"]


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ("title", "genre")
    # Можно импортировать это - from django.contrib.auth.models import Group и
    # тут его убрать из регистрации, пропадет не нужное поле группы  в админке.
