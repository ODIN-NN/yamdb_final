from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    ]

    bio = models.TextField(
        'Биография',
        blank=True,
        null=True
    )
    role = models.CharField(
        'Роль', max_length=30, choices=ROLE_CHOICES, default='user'
    )
    email = models.EmailField(
        'Email', max_length=254, unique=True, null=True, blank=False
    )
    confirmation_code = models.TextField('Код подтверждения', null=True)

    class Meta:
        ordering = ('-id',)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'
