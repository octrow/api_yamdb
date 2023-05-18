from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api_yamdb.settings import LENGTH_REALNAME
from reviews.basemodel import BaseModelCategoryGenre, BaseModelReviewComment
from reviews.validators import year_validator


class Category(BaseModelCategoryGenre):
    """Модель для категорий произведений"""

    class Meta(BaseModelCategoryGenre.Meta):
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(BaseModelCategoryGenre):
    """Модель для жанров произведений"""

    class Meta(BaseModelCategoryGenre.Meta):
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Title(models.Model):
    """Модель для произведений"""

    name = models.CharField(
        "Название произведения", max_length=LENGTH_REALNAME
    )
    genre = models.ManyToManyField(
        Genre,
        through="GenreTitle",
        related_name="titles",
        verbose_name="Жанр произведения",
    )
    category = models.ForeignKey(
        Category,
        related_name="titles",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория произведения",
    )
    year = models.SmallIntegerField(
        "Год выпуска",
        validators=[year_validator],
        db_index=True,
    )
    description = models.TextField("Описание произведения", blank=True)

    class Meta:
        ordering = (
            "name",
            "year",
        )
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name[:30]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="title",
        verbose_name="Произведение",
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name="genre",
        verbose_name="Жанр",
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return f"{self.title} {self.genre}"


class Review(BaseModelReviewComment):
    """Модель отзывов для произведений."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name="Произведение",
    )
    score = models.PositiveSmallIntegerField(
        "Оценка",
        validators=[
            MinValueValidator(1, message="Диапозон для оценки меньше 1"),
            MaxValueValidator(10, message="Диапозон для оценки больше 10"),
        ],
    )

    class Meta(BaseModelReviewComment.Meta):
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        default_related_name = "reviews"
        constraints = (
            models.UniqueConstraint(
                fields=("author", "title"), name="unique_title_author"
            ),
        )


class Comment(BaseModelReviewComment):
    """Модель комментариев для отзывов."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name="Отзыв",
    )

    class Meta(BaseModelReviewComment.Meta):
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        default_related_name = "comments"
