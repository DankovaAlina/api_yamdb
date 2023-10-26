import random
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
