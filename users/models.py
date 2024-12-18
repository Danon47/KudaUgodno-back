from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """
    Модель Пользователя
    """

    username = None

    phone_number = PhoneNumberField(
        region="RU",
        verbose_name="Телефон",
        unique=True,
        help_text="Номер телефона в формате: +7 (999) 999-99-99",
    )  # Добавлено поле телефона

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
