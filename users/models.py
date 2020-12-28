from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user', _('пользователь')
        MODERATOR = 'moderator', _('модератор')
        ADMIN = 'admin', _('админ')

    role = models.CharField(
        max_length=9,
        choices=Role.choices,
        default=Role.USER
    )
    bio = models.TextField(max_length=500, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
