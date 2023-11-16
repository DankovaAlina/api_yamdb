from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import send_confirmation_code
from reviews.consts import (
    ERROR_MESSAGE_SIGNUP, MAX_LEN_EMAIL, MAX_LEN_USERNAME
)
from reviews.models import (
    Category, Comment,
    Genre, Review, Title, User)
from reviews.validators import username_validator, validate_username_me


class UserFullInfoSerializer(serializers.ModelSerializer):
    """Сериализатор полной информации пользователя."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserSignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    username = serializers.CharField(
        max_length=MAX_LEN_USERNAME,
        validators=(username_validator, validate_username_me)
    )
    email = serializers.EmailField(max_length=MAX_LEN_EMAIL)

    def create(self, validated_data):
        user = validated_data.get('user')
        if user is None:
            user = User.objects.create(**validated_data)
        send_confirmation_code(user)
        return user

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        errors = {}
        users = User.objects.filter(
            Q(email=email) | Q(username=username)
        )
        if users:
            if any(user.username != username for user in users):
                errors['email'] = ERROR_MESSAGE_SIGNUP.format(
                    'username', 'email'
                )
            if any(user.email != email for user in users):
                errors['username'] = ERROR_MESSAGE_SIGNUP.format(
                    'email', 'username'
                )
            if errors:
                raise serializers.ValidationError(errors)
            attrs['user'] = users.first()
        return attrs


class UserTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    confirmation_code = serializers.CharField()
    username = serializers.CharField()

    def create(self, validated_data):
        user = validated_data.get('user')
        token = RefreshToken.for_user(user)
        return token

    def validate(self, attrs):
        user = get_object_or_404(
            User,
            username=attrs.get('username')
        )
        if not default_token_generator.check_token(
            user, attrs.get('confirmation_code')
        ):
            raise serializers.ValidationError(
                'Неверный код подтверждения.'
            )
        attrs['user'] = user
        return attrs

    def to_representation(self, instance):
        return {'token': str(instance.access_token)}


class UserInfoForUserSerializer(serializers.ModelSerializer):
    """Сериализатор информации о себе."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор жанра."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


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

    class Meta:
        """Мета класс произведения."""

        fields = '__all__'
        model = Title

    def to_representation(self, instance):
        return TitleReadonlySerializer(instance).data


class TitleReadonlySerializer(serializers.ModelSerializer):
    """
    Сериализатор произведений для List и Retrieve.
    """

    rating = serializers.IntegerField(read_only=True, default=0)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)

    class Meta:
        """Мета класс произведения."""

        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзыва."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

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
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментария."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
