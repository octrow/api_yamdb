from rest_framework import serializers
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

    class Meta:
        model = User
        fields = ('bio', 'username', 'email', 'first_name',
                  'last_name', 'role')

       