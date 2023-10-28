from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import symbol_validator, validate_year


class User(models.Model):
    """Модель пользователя."""

    username = models.CharField(max_length=255,
                                unique=True,
                                verbose_name='Имя пользователя')
    email = models.EmailField(unique=True,
                              verbose_name='Электронная почта')
    role = models.CharField(max_length=255, verbose_name='Роль')
    bio = models.TextField(verbose_name='Биография')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    """
    Модель Категории.
    """

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
    """
    Модель жанра.
    """

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


class Review(models.Model):
    title_id = models.ForeignKey(
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
            models.UniqueConstraint(fields=['author', 'title_id'],
                                    name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review_id = models.ForeignKey(
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


class TitleGenre(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
