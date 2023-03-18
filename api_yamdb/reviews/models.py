from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


User = get_user_model()


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
