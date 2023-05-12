from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from users.validator import username_valid
from rest_framework.serializers import ValidationError
from reviews.models import Title, Genre, Category, Review, Comment
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
    rating = serializers.SerializerMethodField(read_only=True)

    def get_rating(self, obj):
        if obj.rating:
            return obj.rating
        return None

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
    rating = serializers.IntegerField(
        default=None,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        model = Title
        fields = "__all__"


<<<<<<< HEAD
class UserSerializer(serializers.ModelSerializer):  # заглушка
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(
            username_valid,
            UniqueValidator(queryset=User.objects.all()),
        ),
    )

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
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(), fields=("username", "email")
            ),
        ]
=======
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
        return User.objects.create_user(data['username'])


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('bio', 'username', 'email', 'first_name',
                  'last_name', 'role')
        

class UserEditSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('bio', 'username', 'email',
                  'first_name', 'last_name', 'role')
        model = User
        read_only_fields = ('role',)

>>>>>>> origin/develop


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("text", "author", "title", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text", "author", "review", "pub_date")
