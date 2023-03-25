from django.db import models


class UserRole(models.TextChoices):
    USER = 'user', 'USER'
    MODERATOR = 'moderator', 'MODERATOR'
    ADMIN = 'admin', 'ADMIN'
