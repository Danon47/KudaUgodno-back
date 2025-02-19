from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Flight(models.Model):
    """
    Модель для хранения информации о рейсах
    """

    # Номер рейса
    flight_number = models.CharField(
        max_length=10,
        verbose_name="Номер рейса"
    )

    # Авиакомпания
    airline = models.CharField(
        max_length=100,
        verbose_name="Авиакомпания"
    )
    # Аэропорт вылета
    departure_airport = models.CharField(
        max_length=100,
        verbose_name="Аэропорт вылета"
    )
    # Аэропорт прибытия
    arrival_airport = models.CharField(
        max_length=100,
        verbose_name="Аэропорт прибытия"
    )
    # Дата вылета
    departure_date = models.DateField(
        verbose_name="Дата вылета"
    )
    # Время вылета
    departure_time = models.TimeField(
        verbose_name="Время вылета"
    )
    # Дата прибытия
    arrival_date = models.DateField(
        verbose_name="Дата прибытия"
    )
    # Время прибытия
    arrival_time = models.TimeField(
        verbose_name="Время прибытия"
    )
    # Цена за билет
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        validators=[MinValueValidator(Decimal('0.01'))],
    )
    # Клас обслуживания
    service_class = models.CharField(
        max_length=100,
        verbose_name="Класс обслуживания",
        default="Эконом-класс",
    )
    # Тип рейса
    flight_type = models.CharField(
        max_length=50,
        verbose_name="Тип рейса",
        default="Регулярный"
    )

    class Meta:
        verbose_name = "Рейс"
        verbose_name_plural = "Рейсы"
        ordering = ("departure_date",)

    def __str__(self):
        return f"{self.flight_number}"
