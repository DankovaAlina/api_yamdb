from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.db.models import Avg

from reviews.models import Category, Comment, Genre, Review, Title, User


class UserFullInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value


class UserSignupSerializer(UserFullInfoSerializer):

    class Meta(UserFullInfoSerializer.Meta):
        fields = ('email', 'username')


class UserTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField()
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserInfoForUserSerializer(UserFullInfoSerializer):

    class Meta(UserFullInfoSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор жанра.
    """

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleCreateDeleteSerializer(serializers.ModelSerializer):
    """
    Сериализатор произведений для Create, Partial_Update и Delete.
    """

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    def to_representation(self, instance):
        return TitleReadonlySerializer(instance).data

    class Meta:
        """Мета класс произведения."""

        fields = '__all__'
        model = Title


class TitleReadonlySerializer(serializers.ModelSerializer):
    """
    Сериализатор произведений для List и Retrieve.
    """

    rating = serializers.SerializerMethodField(read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']

    class Meta:
        """
        Мета класс произведения.
        """

        fields = '__all__'
        model = Title
        read_only_fields = ('id', 'name', 'year', 'description')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    title = TitleCreateDeleteSerializer(read_only=True)

    def validate(self, value):
        author = self.context['request'].user
        title_id = (self.context['request'].
                    parser_context['kwargs'].get('title_id'))
        title = get_object_or_404(
            Title,
            id=title_id
        )
        if (self.context['request'].method == 'POST'
                and title.reviews.filter(author=author).exists()):
            raise serializers.ValidationError(
                f'Отзыв на произведение {title.name} уже существует!'
            )
        return value

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
