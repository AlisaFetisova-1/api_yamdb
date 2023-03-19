from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

TEXT_LENGTH = 15

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=255,
        null=True,
        blank=False,
        default='XXXX'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
    

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
    genre = models.ManyToManyField(Genre, through='GenreTitle')
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE, null=True)

    class Meta:
        default_related_name = 'titles'

    def __str__(self):
        return self.name[:TEXT_LENGTH]


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'произведение {self.title} имеет жанр: {self.genre}'


class Review(models.Model):
    title = models.ForeignKey(
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
        ordering = ['id']
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
        ordering = ['id']
        default_related_name = 'comments'
        verbose_name = 'Коментарий к отзыву'

    def __str__(self):
        return self.text



