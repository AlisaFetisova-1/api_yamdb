from datetime import datetime
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    RegexValidator)
from django.db import models
from users.models import User

TEXT_LENGTH = 15


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
        )]
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
        )]
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        db_index=True,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        validators=[
            MaxValueValidator(
                int(datetime.now().year),
                message='Введите год не больше текущего'
            )
        ],
        db_index=True,
        verbose_name='Год издания',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        default_related_name = 'titles'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )

    class Meta:
        verbose_name = 'Соответствие жанра и произведения'
        verbose_name_plural = 'Полное соответствие жанров и произведений'
        ordering = ('id',)

    def __str__(self):
        return f'произведение {self.title} имеет жанр: {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Aвтор'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Минимум 1 '
            ),
            MaxValueValidator(
                10,
                message='Максимум  10'
            )
        ],
        verbose_name='Oценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_field')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Aвтор'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )
    review = models.ForeignKey(
        Review,
        related_name='coments',
        on_delete=models.CASCADE,
        verbose_name='Отзыв'
    )

    class Meta:
        ordering = ('id',)
        default_related_name = 'comments'
        verbose_name = 'Коментарий к отзыву'

    def __str__(self):
        return self.text
