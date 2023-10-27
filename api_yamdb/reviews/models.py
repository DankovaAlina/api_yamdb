import random
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

from api.consts import (
    MAX_LEN_CONFIRMATION_CODE, MAX_LEN_EMAIL_AND_BIO, MAX_LEN_ROLE, ROLES
)


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


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
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
        ordering = ['pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ['pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
