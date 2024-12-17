from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Модель Пользователя
    """

    USER_TYPE_CHOICES = (
        ("admin", "Администратор"),
        ("tour_operator", "Туроператор"),
        ("regular_user", "Пользователь"),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default="regular_user")
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Добавлено поле телефона

    def __str__(self):
        return self.username
