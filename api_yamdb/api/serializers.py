from rest_framework import serializers
from reviews.models import User, Category, Genre, Title, Review, Comment


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'role',
                  'bio', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = serializers.StringRelatedField()

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title_id = TitleSerializer()
    author = UserSerializer()

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    title_id = ReviewSerializer()
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанра.
    """

    class Meta:
        model = Genre
        fields = '__all__'