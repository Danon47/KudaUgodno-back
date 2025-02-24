from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from all_fixture.fixture_views import NULLABLE
from users.choices import RoleChoices


class User(AbstractUser):
    """
    Базовая модель Пользователя с расширением для Туроператора и Отельера.
    """

    username = None
    # Общие поля для всех пользователей
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = PhoneNumberField(
        region="RU",
        verbose_name="Телефон",
        help_text="Телефон в формате: +7 (XXX) XXX-XX-XX",
    )
    avatar = models.ImageField(upload_to="users/", verbose_name="Аватар", **NULLABLE)
    birth_date = models.DateField(verbose_name="Дата рождения", **NULLABLE)
    # Поля для Туроператора и Отельера
    company_name = models.CharField(max_length=150, verbose_name="Название компании", **NULLABLE)
    documents = models.FileField(upload_to="documents/", verbose_name="Документы", **NULLABLE)
    role = models.CharField(
        choices=RoleChoices.choices,
        default=RoleChoices.USER,
        verbose_name="Роль пользователя",
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
        """
        super().clean()

        # Валидация для роли "Пользователь"
        if self.role == RoleChoices.USER:
            if self.company_name or self.documents:
                raise ValidationError("У обычного пользователя не могут быть заполнены поля: company_name, documents.")

        # Валидация для роли "Туроператор" и "Отельер"
        elif self.role in [RoleChoices.TOUR_OPERATOR, RoleChoices.HOTELIER]:
            if not self.company_name:
                raise ValidationError("Для Туроператора и Отельера поле 'Название компании' является обязательным.")
            if not self.documents:
                raise ValidationError("Для Туроператора и Отельера необходимо загрузить документы.")
