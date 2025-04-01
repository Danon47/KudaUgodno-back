from django.db import models

from all_fixture.fixture_views import NULLABLE
from flights.models import Flight
from hotels.models.hotel.models_hotel import Hotel
from users.models import User


class Tour(models.Model):
    """
    Модель для хранения информации о турах
    """

    start_date = models.DateField(verbose_name="Дата начала тура")
    end_date = models.DateField(verbose_name="Дата окончания тура")
    flight_to = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        verbose_name="Рейс отправления",
        related_name="tours",
        **NULLABLE,
    )
    flight_from = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        verbose_name="Рейс возвращения",
        **NULLABLE,
    )
    departure_country = models.CharField(
        max_length=50,
        verbose_name="Страна вылета",
        **NULLABLE,
    )
    departure_city = models.CharField(
        max_length=50,
        verbose_name="Город вылета",
        **NULLABLE,
    )
    arrival_country = models.CharField(
        max_length=50,
        verbose_name="Страна прибытия",
        **NULLABLE,
    )
    arrival_city = models.CharField(
        max_length=50,
        verbose_name="Город прибытия",
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
    room = models.CharField(
        max_length=50,
        verbose_name="Категория номера",
        default="Standard",
    )
    transfer = models.BooleanField(verbose_name="Трансфер", default=False)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость тура",
        **NULLABLE,
    )

    document = models.FileField(upload_to="tour/documents", verbose_name="Документы", **NULLABLE)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        **NULLABLE,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
        ordering = ("start_date",)

    def __str__(self):
        return f"{self.hotel.name}"
