import random
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from api.consts import (
    MAX_LEN_CONFIRMATION_CODE, MAX_LEN_EMAIL_AND_BIO, MAX_LEN_ROLE, ROLES
)
from reviews.validators import symbol_validator, validate_year


def generate_confirmation_code():
    """Генерирует код подтверждения при регистрации пользователя."""
    return str(random.randint(100000, 999999))


class User(AbstractUser):
    email = models.EmailField(
        'Электронная почта',
        max_length=MAX_LEN_EMAIL_AND_BIO,
        unique=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=MAX_LEN_CONFIRMATION_CODE,
        default=generate_confirmation_code()
    )
    bio = models.TextField(
        'Информация и пользователе',
        max_length=MAX_LEN_EMAIL_AND_BIO,
        blank=True
    )
    role = models.CharField(
        'Роль',
        choices=ROLES,
        max_length=MAX_LEN_ROLE,
        default='user'
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель Категории."""

    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50,
                            validators=[symbol_validator],
                            verbose_name='Идентификатор')

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=50,
                            verbose_name='Идентификатор')

    class Meta:
        ordering = ['name']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель заголовка."""

    name = models.CharField(max_length=256, verbose_name='Название')
    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[validate_year],
        verbose_name='Год',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория'
    )
    descriptions = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Заголовок'
        verbose_name_plural = 'Заголовки'

    def __str__(self):
        return self.name


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    score = models.IntegerField(
        null=True,
        validators=[
            MaxValueValidator(10, message='Оценка не может быть выше 10'),
            MinValueValidator(1, message='Оценка не может быть ниже 1')
        ]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        default_related_name = 'reviews'
        ordering = ['pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title_id'],
                                    name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
