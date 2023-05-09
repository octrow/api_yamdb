from reviews.validators import year_validator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
         User, on_delete=models.CASCADE, related_name='rewiews')
    title = models.ForeignKey(
         Title, on_delete=models.CASCADE, related_name='titles')
    score = models.PositiveIntegerField(default=5,
                                        validators=[MinValueValidator(1),
                                                    MaxValueValidator(10)])

    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text

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
