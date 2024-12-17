from django.db import models


class Flight(models.Model):
    """
    Модель для хранения информации о рейсах
    """

    # Номер рейса
    flight_number = models.CharField(
        max_length=10, verbose_name="Номер рейса", help_text="Введите номер рейса"
    )
    # Авиакомпания
    airline = models.CharField(
        max_length=100,
        verbose_name="Авиакомпания",
        help_text="Введите название авиакомпании",
    )
    # Аэропорт вылета
    departure_airport = models.CharField(
        max_length=100,
        verbose_name="Аэропорт вылета",
        help_text="Укажите аэропорт вылета",
    )
    # Аэропорт прибытия
    arrival_airport = models.CharField(
        max_length=100,
        verbose_name="Аэропорт прибытия",
        help_text="Укажите аэропорт прибытия",
    )
    # Дата вылета
    departure_date = models.DateField(
        verbose_name="Дата вылета", help_text="Укажите дату вылета"
    )
    # Время вылета
    departure_time = models.TimeField(
        verbose_name="Время вылета", help_text="Укажите время вылета"
    )
    # Дата прибытия
    arrival_date = models.DateField(
        verbose_name="Дата прибытия", help_text="Укажите дату прибытия"
    )
    # Время прибытия
    arrival_time = models.TimeField(
        verbose_name="Время прибытия", help_text="Укажите время прибытия"
    )
    # Цена за билет
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Укажите цену билета",
    )

    class Meta:
        verbose_name = "Рейс"
        verbose_name_plural = "Рейсы"
        ordering = ("departure_date",)

    def __str__(self):
        return f"{self.flight_number}"
