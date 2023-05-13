from reviews.validators import year_validator, rating_validator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


class Category(models.Model):
    """Модель для категорий произведений"""

    name = models.CharField(
        "Название категории",
        max_length=256,
        help_text="Введите название категории",
    )
    slug = models.SlugField(
        "Путь slug к категории", max_length=50, unique=True
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name[:30]


class Genre(models.Model):
    """Модель для жанров произведений"""

    name = models.CharField(
        "Название жанра", max_length=256, help_text="Введите название жанра"
    )
    slug = models.SlugField("Путь slug жанра", max_length=50, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name[:30]


class Title(models.Model):
    """Модель для произведений"""

    name = models.CharField("Название произведения", max_length=255)
    genre = models.ManyToManyField(
        Genre,
        related_name="titles",
        verbose_name="Жанр произведения",
    )
    category = models.ForeignKey(
        Category,
        related_name="titles",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Категория произведения",
    )
    rating = models.PositiveSmallIntegerField(
        default=None, blank=True, null=True, validators=[rating_validator]
    )
    year = models.PositiveSmallIntegerField(
        "Год выпуска", blank=True, validators=[year_validator]
    )
    description = models.TextField("Описание", blank=True)

    class Meta:
        ordering = ("id",)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name[:30]

    # def delete(self, *args, **kwargs):
    #     self.reviews.all().delete()
    #     super().delete(*args, **kwargs)


# class GenreTitle(models.Model):
#     genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
#     title_id = models.ForeignKey(Title, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.genre_id.name} - {self.title_id.name}"


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ("pub_date", )
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = (models.UniqueConstraint(
            fields=("author", "title"),
            name="unique_title_author"), )

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )
    
    class Meta:
        ordering = ("pub_date", )
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:30]
