from decimal import Decimal

from django.core.validators import RegexValidator, MinValueValidator
from django.db import models

from flights.choices import AirlinesChoices, ServicesClassChoices, FlightTypeChoices


class Flight(models.Model):
    """
    Модель для хранения информации о рейсах
    """

    flight_number = models.CharField(
        max_length=10,
        verbose_name="Номер рейса",
        help_text="Введите номер рейса в формате: AA XXXX, где A-латинские буквы в верхнем регистре, X- цифры",
        validators=[
            RegexValidator(
                regex=r"^[A-Z]{2} [0-9]{4}$",
                message="Введите номер рейса в формате: AA XXXX, где A-латинские буквы в верхнем регистре, X- цифры "
                "от 0 до 9)",
            )
        ],
    )
    airline = models.CharField(
        max_length=100,
        verbose_name="Авиакомпания",
        choices=AirlinesChoices.choices
    )
    departure_airport = models.CharField(
        max_length=100,
        verbose_name="Аэропорт вылета"
    )
    arrival_airport = models.CharField(
        max_length=100,
        verbose_name="Аэропорт прибытия"
    )
    departure_date = models.DateField(
        verbose_name="Дата вылета"
    )
    departure_time = models.TimeField(
        verbose_name="Время вылета"
    )
    arrival_date = models.DateField(
        verbose_name="Дата прибытия"
    )
    arrival_time = models.TimeField(
        verbose_name="Время прибытия"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    service_class = models.CharField(
        max_length=100,
        verbose_name="Класс обслуживания",
        choices=ServicesClassChoices.choices,
        default=ServicesClassChoices.ECONOMY,
    )
    flight_type = models.CharField(
        max_length=50,
        verbose_name="Тип рейса",
        choices=FlightTypeChoices.choices,
        default=FlightTypeChoices.REGULAR,
    )

    class Meta:
        verbose_name = "Рейс"
        verbose_name_plural = "Рейсы"
        ordering = ("departure_date",)

    def __str__(self):
        return f"{self.flight_number}"
