from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Кастомная модель User"""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
    )
    bio = models.TextField(verbose_name="Биография", blank=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(r'^[\w.@-]+$')
        ],
        verbose_name='Логин',
        help_text='Введите логин, не более 150 символов',
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email_адрес',
        help_text='Введите адрес электронной почты для регистрации.',
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name='Фамилия'
    )
    role = models.CharField(
        max_length=16,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль',
    )
    confirmation_code = models.CharField(
        max_length=150, verbose_name='Код')

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username[:30]

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return (self.role == self.ADMIN
                or self.is_superuser
                )
