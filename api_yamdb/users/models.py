from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ("user", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Администратор"),
    )

    bio = models.TextField(verbose_name="Биография", blank=True)
    username = models.CharField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        unique=True, max_length=254, verbose_name="Почта"
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name="Фамилия"
    )
    role = models.CharField(
        max_length=255,
        choices=ROLE_CHOICES,
        default="user",
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username[:30]

    def save(self, *args, **kwargs):  # заглушка
        if self.role == "moderator":
            self.is_staff = True
        if self.role == "admin":
            self.is_superuser = True
        super().save(*args, **kwargs)

    @property  # заглушка
    def is_moderator(self):
        return self.role == "moderator"

    @property  # заглушка
    def is_admin(self):
        return self.role == "admin"
