from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from reviews.consts import MAX_LEN_ROLE, MAX_LEN_USERNAME
from reviews.validators import (
    symbol_validator, username_validator,
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
        return self.role in (self.UserRoles.ADMIN, self.UserRoles.MODERATOR)


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
    """Модель произведения."""

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
    description = models.TextField(null=True, blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='TitleGenre',
        blank=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    rating = models.IntegerField('Рейтинг', default=None, null=True)

    class Meta:
        """Мета класс произведения."""

        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Описание произведения."""
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
