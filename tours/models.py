from django.core.validators import MaxValueValidator
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
    start_date = models.DateField(verbose_name="Дата начала тура")
    # Дата окончания тура
    end_date = models.DateField(verbose_name="Дата окончания тура")
    # Рейс туда
    flight_to = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        verbose_name="Рейс туда",
        related_name="tours",
        **NULLABLE,
    )
    # Рейс обратно
    flight_from = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        verbose_name="Рейс обратно",
        **NULLABLE,
    )
    #   Город вылета
    departure_city = models.CharField(
        max_length=50,
        verbose_name="Город вылета",
        **NULLABLE,
    )
    # Туроператор
    tour_operator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Туроператор",
        related_name="tours",
        **NULLABLE,
    )
    # Отель
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        verbose_name="Отель",
        related_name="tours",
        **NULLABLE,
    )
    room = models.ManyToManyField(
        Room,
        verbose_name="Номер",
        related_name="tours",
        blank=True,
    )
    # Количество человек
    guests_number = models.PositiveIntegerField(
        verbose_name="Количество человек",
        default=2,
        validators=[
            MaxValueValidator(10),
        ],
        **NULLABLE,
    )

    # Стоимость тура
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость тура",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
        ordering = ("start_date",)

    def __str__(self):
        return f"{self.hotel.name}"
