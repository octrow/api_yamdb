from rest_framework import serializers
from reviews.models import Title, Genre, Category, Review, Comment


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


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ("text", "author", "title", "score", "pub_date")


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ("text", "author", "review", "pub_date")
