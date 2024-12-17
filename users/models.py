from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """
    Модель Пользователя
    """

    phone_number = PhoneNumberField(
        region="RU",
        verbose_name="Телефон",
        help_text="Номер телефона в формате: +7 (999) 999-99-99",
    )  # Добавлено поле телефона

    def __str__(self):
        return self.username
