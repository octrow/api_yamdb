from django.db import models
from django.contrib.auth.models import AbstractUser
from .validator import username_valid


class Role(models.TextChoices):
    """Выбор ролей"""
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class User(AbstractUser):
    """Кастомная модель User"""
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(username_valid,),
        verbose_name='Пользователь',
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email_адрес'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия'
    )
    role = models.CharField(
        max_length=16,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль',
    )

    class Meta:
        verbose_name = "Пользователь"
        unique_together = ('username',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_user(self):
        return self.role == Role.USER

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_admin(self):
        return (self.role == Role.ADMIN
                or self.is_superuser
                or self.is_staff
                )