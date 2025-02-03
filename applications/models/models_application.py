from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from applications.choices import StatusChoices
from applications.models.models_guest import Guest
from tours.models import Tour
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Application(models.Model):
    """
    Модель Заявки
    """

    # Тур
    tour = models.ForeignKey(
        Tour,
        on_delete=models.PROTECT,
        verbose_name="Тур",
    )
    # Email пользователя
    email = models.EmailField(
        verbose_name="Email",
    )
    # Номер телефона
    phone_number = PhoneNumberField(
        region="RU",
        verbose_name="Телефон",
        help_text="Формат: +X XXX XXX XX XX",
    )
    # Количество гостей
    quantity_guests = models.ManyToManyField(
        Guest,
        verbose_name="Количество гостей",
        blank=True,
    )
    # Оформление визы
    visa = models.BooleanField(
        default=False,
        verbose_name="Оформление визы"
    )
    # Страховка жизни
    med_insurance = models.BooleanField(
        default=False,
        verbose_name="Медицинская страховка"
    )
    # Страховка от невыезда
    cancellation_insurance = models.BooleanField(
        default=False,
        verbose_name="Страховка невыезда"
    )
    # Пожелания
    wishes = models.TextField(
        verbose_name="Пожелания",
        **NULLABLE
    )
    # Статус заявки
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.AWAIT_CONFIRM,
        verbose_name="Статус заявки",
    )
    # Пользователь кто создал заявку
    user_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь кто создал заявку"
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ("-pk",)

    def __str__(self):
        return f"Заявка N {self.pk}"
