from rest_framework import serializers

from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категории.
    """

    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор заголовка.
    """

    category = CategorySerializer()
    genre = serializers.StringRelatedField()

    class Meta:
        model = Title
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанра.
    """

    class Meta:
        model = Genre
        fields = '__all__'
