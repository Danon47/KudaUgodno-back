from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from applications.choices import StatusChoices

NULLABLE = {'blank': True, 'null': True}

class Guest(models.Model):
    """
    Модель Гостя
    """
    pass

class Application(models.Model):
    """
    Модель Заявки
    """

    Tour = models.ForeignKey(
        "tours.Tour",
        on_delete=models.PROTECT,
        verbose_name="Тур",
        help_text="Выберите тур",
    )
    email = models.EmailField(
        verbose_name="Email",
        help_text="Введите email"
    )
    phone_number = PhoneNumberField(
        region="RU",
        verbose_name="Телефон",
        help_text="Введите номер телефона"
    )
    quantity_rooms = models.ManyToManyField(
        "hotels.HotelRoom",
        verbose_name="Количество номеров",
        blank=True
    )
    quantity_guests = models.ManyToManyField(
        "Guest",
        verbose_name="Количество гостей",
        blank=True
    )
    visa = models.PositiveIntegerField(
        default=0,
        verbose_name="Оформление визы",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    med_insurance = models.BooleanField(
        default=False,
        verbose_name="Медицинская страховка"
    )
    cancellation_insurance = models.BooleanField(
        default=False,
        verbose_name="Страховка невыезда"
    )
    wishes = models.TextField(
        verbose_name="Пожелания",
        help_text="Введите пожелания",
        **NULLABLE
    )
    status = models.CharField(
        choices= StatusChoices.choices,
        default=StatusChoices.AWAIT_CONFIRM,
        verbose_name="Статус заявки"
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ("-pk",)

    def __str__(self):
        return self.pk



