from reviews.validators import year_validator
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=256, help_text="Введите название категории"
    )
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name[:30]


class Genre(models.Model):
    name = models.CharField(max_length=256, help_text="Введите название жанра")
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name[:30]


class Title(models.Model):
    name = models.CharField(max_length=255)
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
    )
    category = models.ForeignKey(
        Category, related_name="titles", on_delete=models.SET_NULL, null=True
    )
    rating = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True,
        # validators=[rating_validator]
    )
    year = models.PositiveSmallIntegerField(
        default=None, validators=[year_validator]
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name[:30]
