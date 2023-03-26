from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import UserRole


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Email'
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.USER,
        blank=True,
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )

    confirmation_code = models.CharField(
        max_length=255,
        null=True,
        blank=False,
        default='XXXX',
        verbose_name='Код подтверждения'
    )

    @property
    def is_user(self):
        return self.role == UserRole.USER

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
