from django.db import models

from api_yamdb.settings import LENGTH_REALNAME, LENGTH_SLUG
from users.models import User


class BaseModelCategoryGenre(models.Model):  # Абстрактным моделям принято
    # давать имена по их полям, чтобы было сразу понятно - что в них.
    """Модель для жанров и категорий."""

    name = models.CharField("Имя", max_length=LENGTH_REALNAME)
    slug = models.SlugField("Slug", max_length=LENGTH_SLUG, unique=True)

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name[:30]


class BaseModelReviewComment(models.Model):  # См. выше
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
