from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Кастомная модель User"""

    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

    ROLE_CHOICES = (  # Отлично
        (USER, "Пользователь"),
        (ADMIN, "Администратор"),
        (MODERATOR, "Модератор"),
    )
    bio = models.TextField(
        verbose_name="Биография", blank=True
    )  # Не консистентные кавычки.
    # И ниже тоже есть.
    username = models.CharField(
        max_length=150,
        #         Общее для всех моделей:
        # Смотрим редок внимательно и видим там правильное ограничение длинны для всех полей.
        # Все настройки длины выносим в файл с константами, для многих полей они будут одинаковыми, не повторяемся.
        # Для всех полей нужны verbose_name.
        # Для всех классов нужны в классах Meta verbose_name.
        # У всех классов где используется пагинация, должна быть умолчательная сортировка.
        # Для всех классов нужны методы __str__.
        unique=True,
        validators=[
            RegexValidator(r"^[\w.@-]+$")
        ],  # Нужно написать свой валидатор, с этим не понятно пользователю, что он сделал не так.
        # Рекомендую использовать re.sub.
        # В него же добавить и проверку на me.
        # ----
        # Можно лучше
        # Валидатор для юсернейма можно использовать в миксине вот так:
        # ИмяМиксина:
        #     def validate_username(self, username):
        #         return имя_метода_валидации(username)
        # И наследовать сериалайзеры от этого миксина так:
        # Сериалайзер(ОсновнойРодитель, Миксин)
        verbose_name="Логин",
        help_text="Введите логин, не более 150 символов",
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name="email_адрес",
        help_text="Введите адрес электронной почты для регистрации.",
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name="Имя"
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name="Фамилия"
    )
    role = models.CharField(
        max_length=16,  # Длину нужно подсчитать прямо тут, подсказка: используем лен и генератор.
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name="Роль",
    )
    confirmation_code = models.CharField(max_length=150, verbose_name="Код")

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    class Meta:  # Зачем 2 раза?
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username[:30]

    @property
    def is_user(self):  # Где это используется?
        return self.role == self.USER

    @property  # Отлично
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN or self.is_superuser
        )  # Если не открыта открывающая скобка, то не нужно открывать и закрывающую. Нужно исправить везде.
