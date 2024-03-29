from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from api_yamdb import constances

from .validator import username_valid


class User(AbstractUser):
    """Кастомная модель User"""

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

    ROLE_CHOICES = (
        (USER, "Пользователь"),
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
    )
    bio = models.TextField(verbose_name="Биография", blank=True)
    username = models.CharField(
        max_length=constances.LENGTH_NAME,
        unique=True,
        validators=[username_valid],
        verbose_name="Логин",
        help_text="Введите логин, не более 150 символов",
    )
    email = models.EmailField(
        unique=True,
        max_length=constances.LENGTH_EMAIL,
        verbose_name="email_адрес",
        help_text="Введите адрес электронной почты для регистрации.",
    )
    first_name = models.CharField(
        max_length=constances.LENGTH_NAME, blank=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=constances.LENGTH_NAME, blank=True, verbose_name="Фамилия"
    )
    role = models.CharField(
        max_length=max([len(role) for role, _ in ROLE_CHOICES]),
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name="Роль",
    )
    confirmation_code = models.CharField(
        max_length=constances.LENGTH_NAME,
        verbose_name="Код",
        default="XXXX",
        help_text=(
            "Введите код подтверждения," "который был отправлен на ваш email"
        ),
    )

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username[:30]

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser


@receiver(post_save, sender=User)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(instance)
        instance.confirmation_code = confirmation_code
        instance.save()
