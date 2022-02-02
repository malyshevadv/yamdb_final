from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = [
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор'),
    ]

    password = models.CharField(_('password'), max_length=128, blank=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    bio = models.TextField(
        'биография',
        blank=True,
    )
    role = models.CharField('роль', choices=ROLES, default='user',
                            max_length=10)

    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['id']
