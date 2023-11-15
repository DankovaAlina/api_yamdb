from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from reviews.consts import MAX_LEN_ROLE, MAX_LEN_USERNAME, MAX_LEN_NAME
from reviews.validators import (
    username_validator,
    validate_username_me, validate_year
)


class User(AbstractUser):
    """Модель пользователя."""

    class UserRoles(models.TextChoices):
        USER = 'user', _('Пользователь')
        ADMIN = 'admin', _('Администратор')
        MODERATOR = 'moderator', _('Модератор')
    email = models.EmailField(
        'Электронная почта',
        unique=True
    )
    bio = models.TextField(
        'Информация о пользователе',
        blank=True
    )
    role = models.CharField(
        'Роль',
        choices=UserRoles.choices,
        max_length=MAX_LEN_ROLE,
        default=UserRoles.USER
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=MAX_LEN_USERNAME,
        unique=True,
        validators=(username_validator, validate_username_me)
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.UserRoles.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.UserRoles.MODERATOR


class Category(models.Model):
    """Модель категории."""

    name = models.CharField(max_length=MAX_LEN_NAME, verbose_name='Название')
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""

    name = models.CharField(max_length=MAX_LEN_NAME, verbose_name='Название')
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(max_length=MAX_LEN_NAME, verbose_name='Название')
    year = models.PositiveIntegerField(
        validators=(validate_year,),
        verbose_name='Год',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    description = models.TextField(
        blank=True, verbose_name='Описание'
    )
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
    """Модель отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение для оценки',
    )
    text = models.TextField('Ваш отзыв')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
    )
    score = models.SmallIntegerField(
        'Рейтинг',
        validators=(
            MaxValueValidator(10, message='Оценка не может быть выше 10'),
            MinValueValidator(1, message='Оценка не может быть ниже 1')
        )
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        default_related_name = 'reviews'
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title_id'],
                                    name='unique_review')
        ]

    def __str__(self):
        return f"Отзыв от {self.author} на {self.title}"


class Comment(models.Model):
    """Модель комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментируемый отзыв',
    )
    text = models.TextField('Ваш комментарий')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
