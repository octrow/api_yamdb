from django.db import models

from api_yamdb.settings import LENGTH_REALNAME, LENGTH_SLUG


class BaseModelCategoryGenre(models.Model):
    """Модель для жанров и категорий."""

    name = models.CharField("Имя", max_length=LENGTH_REALNAME)
    slug = models.SlugField("Slug", max_length=LENGTH_SLUG, unique=True)

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self):
        return self.name[:30]
