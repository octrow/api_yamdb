from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from reviews.validators import year_validator
from users.validator import username_valid
from users.models import User
from api_yamdb.settings import LENGTH_NAME, LENGTH_EMAIL


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанров"""

    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleShowSerializer(serializers.ModelSerializer):
    """Сериализатор для выдачи произведений"""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = "__all__"
        model = Title


class TitleAddSerializer(serializers.ModelSerializer):
    """Сериализатор для добавления произведения"""

    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Genre.objects.all(),
        many=True,
    )
    year = serializers.IntegerField(validators=[year_validator])
    rating = serializers.IntegerField(read_only=True)

    # ГОТОВО! 1.Нужна валидация года.

    # ГОТОВО! 2. Нужна валидация поля Жанра, у нас по ТЗ это поля обязательное,
    # если сейчас передать пустой список через Postman, то Произведение создастся вообще без Жанров.

    class Meta:  # ГОТОВО! Класс Meta должен быть выше методов, но ниже полей.
        model = Title
        fields = "__all__"

    def to_representation(self, instance):  # Отлично
        return TitleShowSerializer(instance).data

    def validate_genre(self, value):
        if not value:
            raise serializers.ValidationError("Требуется выбрать жанр")
        return value


class SignUpSerializer(serializers.ModelSerializer):
    # Для классов Регистрации и Проверки токена не нужно общение с БД, нужно переопределить родительский класс.

    username = serializers.CharField(
        required=True,
        max_length=LENGTH_NAME,
        validators=[
            username_valid,
        ],
    )
    email = serializers.EmailField(
        required=True,
        max_length=LENGTH_EMAIL,
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def validate(self, data):
        if User.objects.filter(
            username=data["username"], email=data["email"]
        ).exists():
            return data
        if (
            User.objects.filter(username=data["username"]).exists()
            or User.objects.filter(email=data["email"]).exists()
        ):
            raise serializers.ValidationError(
                "Пользователь с такими данными уже существует!"
            )
        return data


class CustomTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        fields = ("username",)
        model = User

    def create(self, data):
        return User.objects.create_user(data["username"])


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "bio",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        )


class UserEditSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ("role",)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов к произведениям"""

    # ГОТОВО! Лишнее переопределение поля, нужно указать его в мете как только для чтения.
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    def validate(self, data):
        request = self.context["request"]
        if request.method == "POST":
            title_id = self.context["view"].kwargs["title_id"]
            author = self.context["request"].user
            # ГОТОВО! Не нужно доставать объект, нужно передавать id в следующей строке.
            if author.reviews.filter(
                title=title_id
            ).exists():  # ГОТОВО (!,?) Автор получен, почему бы из него и не доставать используя related_name
                raise serializers.ValidationError(
                    "Запрещено добавлять второй отзыв."
                )
        return data

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("title",)


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев к отзывам"""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
