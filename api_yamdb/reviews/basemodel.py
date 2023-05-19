from django.db import models

from api_yamdb import constances
from users.models import User


class GenreCategoryBase(models.Model):  # ГОТОВО! Абстрактным моделям принято
    # давать имена по их полям, чтобы было сразу понятно - что в них.
    """Модель для жанров и категорий."""

    name = models.CharField("Имя", max_length=constances.LENGTH_REALNAME)
    slug = models.SlugField(
        "Slug", max_length=constances.LENGTH_SLUG, unique=True
    )

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name[:30]


class ReviewCommentBase(models.Model):  # ГОТОВО! См. выше
    """Модель для отзывов и комментариев."""

    text = models.TextField(verbose_name="Текст")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True
        ordering = ("pub_date",)

    def __str__(self):
        return self.text[:30]
