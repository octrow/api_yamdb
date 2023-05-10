from reviews.validators import year_validator, rating_validator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


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
        default=None, blank=True, null=True, validators=[rating_validator]
    )
    year = models.PositiveSmallIntegerField(
        default=None, validators=[year_validator]
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("id",)

    def __str__(self):
        return self.name[:30]

    def delete(self, *args, **kwargs):
        self.reviews.all().delete()
        super().delete(*args, **kwargs)


class GenreTitle(models.Model):
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.genre_id.name} - {self.title_id.name}"


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rewiews"
    )
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="titles"
    )
    score = models.PositiveIntegerField(
        default=None, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    def __str__(self):
        return self.text
