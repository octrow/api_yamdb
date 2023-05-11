from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Title, Genre, Category
from users.models import User
from users.validator import username_valid


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ("name", "category", "genre", "description", "year", "rating")


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=(
            username_valid,
            UniqueValidator(queryset=User.objects.all()),
        )
    )

    class Meta:
        model = User
        fields = ('bio', 'username', 'email', 'first_name',
                  'last_name', 'role')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            ),
        ]

       