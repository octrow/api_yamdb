from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import year_validator
from users.models import User
from reviews.basemodel import BaseModelCategoryGenre


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


# ГОТОВО! Модели Категорий и Жанров, по сути ни чем не отличаются, лучше сделать абстрактную модель и занаследоваться от неё.
# Также нужно добавить сортировку по имени.
# Незабываем унаследовать и мету от меты абстрактного класса.
# Так же в абстрактном классе размещаем и метод стр.


class Title(models.Model):
    """Модель для произведений"""

    name = models.CharField("Название произведения", max_length=255)
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
    year = models.SmallIntegerField(  # Отлично
        "Год выпуска",
        validators=[year_validator],
        db_index=True,  # ГОТОВО! Чтобы ускорить поиск произведений по году, лучше добавить индекс.
    )
    description = models.TextField("Описание произведения", blank=True)

    class Meta:
        ordering = (
            "id",
        )  # Никакого прока от сортировки по техническому полю "ключ" нет.
        # Учти, что значения ключей - это случайные величины (точнее они могут непредсказуемо измениться).
        # Поэтому сортировка по ним - это опять случайная последовательность объектов.
        # Лучше заменить на предметное поле (можно на несколько полей - ведь это перечисление)
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name[:30]


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="title"
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name="genre"
    )

    def __str__(self):
        return f"{self.title} {self.genre}"

    class Meta:
        verbose_name = "жанр"
        verbose_name_plural = "жанры"


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="reviews"
    )
    score = models.PositiveSmallIntegerField(  # ГОТОВО! Есть тип данных еще меньше.
        validators=[
            MinValueValidator(1, message="Диапозон для оценки меньше 1"),
            MaxValueValidator(10, message="Диапозон для оценки больше 10"),
        ]  # ГОТОВО! Отлично, но лучше добавить еще и сообщения об ошибках.
    )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)

    class Meta:
        ordering = ("pub_date",)
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        constraints = (
            models.UniqueConstraint(
                fields=("author", "title"), name="unique_title_author"
            ),
        )

    def __str__(self):
        return self.text[:30]


# Оба класса (Ревью и Комменты) имеют одинаковые поля и в мете тоже, значит можно
# создать базовый абстрактный класс и унаследовать от него обе модели.
# Но не забудьте что мету тоже нужно наследовать иначе она перезапишет всё,
# а не только то что 'другое'. Класс наследуется от класса, мета от меты.
# Еще в моделях ревью и комментов можно в мете добавить умолчательное значение
# related_name, чтобы не указывать его для каждого поля.


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="comments"
    )
    pub_date = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("pub_date",)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:30]


# Общее для всех моделей:
# Смотрим редок внимательно и видим там правильное ограничение длинны для всех полей.
# Все настройки длины выносим в файл с константами, для многих полей они будут одинаковыми, не повторяемся.
# Для всех полей нужны verbose_name.
# Для всех классов нужны в классах Meta verbose_name.
# У всех классов где используется пагинация, должна быть умолчательная сортировка.
# Для всех классов нужны методы __str__.
