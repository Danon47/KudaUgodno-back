from django.core.validators import MaxValueValidator
from django.db import models

from all_fixture.fixture_views import NULLABLE
from flights.models import Flight
from hotels.models.hotel.models_hotel import Hotel
from hotels.models.room.models_room import Room
from users.models import User


class Tour(models.Model):
    """
    Модель для хранения информации о турах
    """

    start_date = models.DateField(
        verbose_name="Дата начала тура"
    )
    end_date = models.DateField(
        verbose_name="Дата окончания тура"
    )
    flight_to = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        verbose_name="Рейс туда",
        related_name="tours",
        **NULLABLE,
    )
    flight_from = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        verbose_name="Рейс обратно",
        **NULLABLE,
    )
    departure_city = models.CharField(
        max_length=50,
        verbose_name="Город вылета",
        **NULLABLE,
    )
    tour_operator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Туроператор",
        related_name="tours",
        **NULLABLE,
    )
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        verbose_name="Отель",
        related_name="tours",
        **NULLABLE,
    )
    number_of_adults = models.PositiveIntegerField(
        verbose_name="Количество взрослых",
        default=2,
        validators=[
            MaxValueValidator(10),
        ]
    )
    number_of_children = models.PositiveIntegerField(
        verbose_name="Количество детей",
        default=0,
        validators=[
            MaxValueValidator(10),
        ]
    )
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
