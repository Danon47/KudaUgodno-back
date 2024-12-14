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

    start_date = models.DateField(
        verbose_name="Дата начала тура",
        help_text="Введите дату начала тура"
    )
    end_date = models.DateField(
        verbose_name="Дата окончания тура",
    )
    hotel = models.ForeignKey(
        "hotels.Hotel",
        on_delete=models.SET_NULL,
        verbose_name="Отель",
        null=True
    )
    airline = models.CharField(
        max_length=50,
        verbose_name="Авиакомпания",
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



