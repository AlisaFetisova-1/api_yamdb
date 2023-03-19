from django.core.validators import RegexValidator
from django.db import models

TEXT_LENGTH = 15


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
        )]
    )

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(
        unique=True,
        validators=[RegexValidator(
            regex=r'^[-a-zA-Z0-9_]+$',
        )]
    )

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField(blank=True)
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True
    )

    class Meta:
        default_related_name = 'titles'

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'произведение {self.title} имеет жанр: {self.genre}'
