from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator,
                                    RegexValidator)
from django.db import models

User = get_user_model()

TEXT_LENGTH = 15


class Category(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
        )]
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Genre(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
        )]
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Title(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    year = models.IntegerField(
        validators=[
            MaxValueValidator(
                int(datetime.now().year),
                message='Введите год не больше текущего'
            )
        ],
        db_index=True
    )
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True)

    class Meta:
        default_related_name = 'titles'
        ordering = ('name',)

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'произведение {self.title} имеет жанр: {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
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
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name_plural = 'Отзывы'
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_field')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True, db_index=True
    )
    review = models.ForeignKey(
        Review, related_name='coments',
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('id',)
        default_related_name = 'comments'
        verbose_name = 'Коментарий к отзыву'

    def __str__(self):
        return self.text
