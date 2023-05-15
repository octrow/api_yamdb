from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


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
    rating = serializers.IntegerField(read_only=True)

    def to_representation(self, instance):
        return TitleShowSerializer(instance).data

    class Meta:
        model = Title
        fields = "__all__"


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")

    def validate_username(self, value):
        if value.lower() == "me":
            raise ValidationError(
                'Нельзя использовать "me" в качестве username!'
            )
        return value


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


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "bio",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
        )
        model = User
        read_only_fields = ("role",)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов к произведениям"""

    title = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    def validate(self, data):
        request = self.context["request"]
        if request.method == "POST":
            title_id = self.context["view"].kwargs["title_id"]
            author = self.context["request"].user
            title = get_object_or_404(Title, pk=title_id)
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    "Запрещено добавлять второй отзыв."
                )
        return data

    class Meta:
        model = Review
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев к отзывам"""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
