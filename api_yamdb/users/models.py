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
