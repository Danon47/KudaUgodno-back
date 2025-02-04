from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from users.choices import RoleChoices


class User(AbstractUser):
    """
    Модель Пользователя
    """

    username = models.CharField(
        max_length=100,
        verbose_name="Название туроператора",
        help_text="Заполняется в случае если роль Туроператор",
        blank=True,
        null=True
    )
    password = models.CharField(
        max_length=88,
        verbose_name="Пароль-код для входа",
        blank=True,
        null=True
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name="Имя",
        help_text="Заполняется в случае если роль Пользователь",
        blank=True,
        null=True
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Фамилия",
        help_text="Заполняется в случае если роль Пользователь",
        blank=True,
        null=True
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )
    phone_number = PhoneNumberField(
        region="RU",
        verbose_name="Телефон",
        help_text="Номер телефона в формате: +7 (XXX) XXX-XX-XX",
        blank=True,
        null=True
    )
    avatar = models.ImageField(
        upload_to='users/',
        null=True,
        blank=True,
        verbose_name="Аватар",
    )
    # Юридический адрес организации
    address = models.CharField(
        verbose_name="Адрес",
        help_text="Юридический адрес для Туроператора",
        blank=True,
        null=True
    )
    # Роль пользователя на платформе
    role = models.CharField(
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
        verbose_name="Роль пользователя"
    )
    # Краткое описание пользователя туроператора
    description = models.TextField(
        verbose_name="Краткое описание",
        blank=True,
        null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("-pk",)

    def __str__(self):
        return self.email

    def clean(self):
        """
        Проверка значений полей в зависимости от роли.
        Вызывается при full_clean() в ModelForm, DRF ModelSerializer (если включена валидация модели)
        или вручную при вызове instance.full_clean().
        """
        super().clean()

        # Если роль = Пользователь
        if self.role == RoleChoices.USER:
            # Запрещаем заполнять поля, которые относятся к Туроператору
            if self.username or self.address or self.description:
                raise ValidationError(
                    "У пользователя (role=USER) не могут быть заполнены поля: username, address, description."
                )

        # Если роль = Туроператор
        elif self.role == RoleChoices.TOUR_OPERATOR:
            # Запрещаем заполнять поля, которые относятся к обычному пользователю
            if self.first_name or self.last_name:
                raise ValidationError(
                    "У туроператора (role=TOUR_OPERATOR) не могут быть заполнены поля: first_name, last_name."
                )
