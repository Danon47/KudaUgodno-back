from django.db import models

from flights.models import Flight
from hotels.models import Room, Hotel
from users.models import User

NULLABLE = {"blank": True, "null": True}


class Tour(models.Model):
    """
    Модель для хранения информации о турах
    """

    # Дата начала тура
    start_date = models.DateField(
        verbose_name="Дата начала тура", help_text="Укажите дату начала тура"
    )
    # Дата окончания тура
    end_date = models.DateField(
        verbose_name="Дата окончания тура", help_text="Укажите дату окончания тура"
    )
    # Название тура (название отеля)
    name = models.CharField(
        max_length=100, verbose_name="Название", help_text="Введите название тура"
    )
    # Рейс туда
    flight_to = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        verbose_name="Рейс туда",
        help_text="Укажите рейс туда",
        related_name="tours",
        **NULLABLE,
    )
    # Рейс обратно
    flight_from = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        verbose_name="Рейс обратно",
        help_text="Укажите обратный рейс",
        **NULLABLE,
    )
    # Туроператор
    tour_operator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Туроператор",
        help_text="Укажите туроператора",
        related_name="tours",
        **NULLABLE,
    )
    # Отель
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        verbose_name="Отель",
        help_text="Укажите отель",
        related_name="tours",
        **NULLABLE,
    )
    # Номер
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        verbose_name="Номер",
        help_text="Укажите номер",
        related_name="tours",
        **NULLABLE,
    )
    # Страна тура
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        help_text="Введите страну",
        **NULLABLE,
    )
    # Город тура
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Введите город",
        **NULLABLE
    )
    # Тип отдыха
    type_of_holiday = models.CharField(
        max_length=100,
        verbose_name="Тип отдыха",
        help_text="Укажите тип отдыха",
        **NULLABLE,
    )
    # Стоимость питания
    meal_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость питания",
        help_text="Укажите стоимость питания",
        **NULLABLE,
    )
    # Стоимость тура
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость тура",
        help_text="Укажите стоимость тура",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
        ordering = ("start_date",)

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"
