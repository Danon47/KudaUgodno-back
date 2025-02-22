from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from all_fixture.fixture_views import NULLABLE


class Flight(models.Model):
    """
    Модель для хранения информации о рейсах
    """

    flight_number = models.CharField(
        max_length=10,
        verbose_name="Номер рейса"
    )
    airline = models.CharField(
        max_length=100,
        verbose_name="Авиакомпания"
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
        default="Эконом-класс",
    )
    flight_type = models.CharField(
        max_length=50,
        verbose_name="Тип рейса",
        default="Регулярный"
    )
    description = models.TextField(
        verbose_name="Описание",
        **NULLABLE,
        help_text="Наличие пересадки, багаж, ручная кладь, питание на борту, сайт авиакомпании"
    )

    class Meta:
        verbose_name = "Рейс"
        verbose_name_plural = "Рейсы"
        ordering = ("departure_date",)

    def __str__(self):
        return f"{self.flight_number}"
