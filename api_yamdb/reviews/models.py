import random
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.consts import (
    MAX_LEN_CONFIRMATION_CODE, MAX_LEN_EMAIL_AND_BIO, MAX_LEN_ROLE, ROLES
)
from reviews.consts import MAX_LEN_NAME
from reviews.validators import validate_year


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


class BaseModelCategoryGenre(models.Model):
    """
    Абстрактная модель для категории и жанра.
    """
    name = models.CharField(max_length=MAX_LEN_NAME, verbose_name='Название')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(BaseModelCategoryGenre):
    """Модель Категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(BaseModelCategoryGenre):
    """Модель жанра."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=MAX_LEN_NAME, verbose_name='Название')
    year = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=(validate_year,),
        verbose_name='Год',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
    )
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        verbose_name='Жанр'
    )

    class Meta:
        """Мета класс произведения."""

        ordering = ('name',)
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Описание произведения."""
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
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
    review = models.ForeignKey(
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
