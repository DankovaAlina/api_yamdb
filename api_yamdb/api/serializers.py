from django.core.exceptions import ValidationError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import check_confirmation_code, send_confirmation_code
from reviews.consts import MAX_LEN_EMAIL, MAX_LEN_USERNAME
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
        email = validated_data.get('email')
        username = validated_data.get('username')
        user = User.objects.filter(email=email, username=username).first()
        if not user:
            user = User.objects.create(**validated_data)
            user.save()
        send_confirmation_code(user)
        return user

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        errors = {}
        emailUser = User.objects.filter(email=email).first()
        if emailUser and emailUser.username != username:
            errors['email'] = ('Поле username не соответствует '
                               'пользователю с данным email.')
        usernameUser = User.objects.filter(username=username).first()
        if usernameUser and usernameUser.email != email:
            errors['username'] = ('Поле email не соответствует '
                                  'пользователю с данным username.')
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class UserTokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    confirmation_code = serializers.CharField()
    username = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.get(username=validated_data.get('username'))
        token = RefreshToken.for_user(user)
        return token

    def validate(self, attrs):
        user = get_object_or_404(
            User,
            username=attrs.get('username')
        )
        if not check_confirmation_code(user, attrs.get('confirmation_code')):
            raise serializers.ValidationError(
                'Неверный код подтверждения.'
            )
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

    rating = serializers.IntegerField(read_only=True)
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
