from django.db import models

from all_fixture.fixture_views import NULLABLE
from flights.models import Flight
from hotels.models.hotel.models_hotel import Hotel
from users.models import User


class Tour(models.Model):
    """
    Модель для хранения информации о турах
    """

    start_date = models.DateField(verbose_name="Дата начала тура", help_text="Введите дату начала тура")
    end_date = models.DateField(verbose_name="Дата окончания тура", help_text="Введите дату окончания тура")
    flight_to = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        verbose_name="Рейс отправления",
        related_name="tours",
        help_text="Введите ID рейса отправления",
        **NULLABLE,
    )
    flight_from = models.ForeignKey(
        Flight,
        on_delete=models.SET_NULL,
        verbose_name="Рейс возвращения",
        help_text="Введите ID рейса возвращения",
        **NULLABLE,
    )
    departure_country = models.CharField(
        max_length=50,
        verbose_name="Страна вылета",
        help_text="Введите страну вылета",
        **NULLABLE,
    )
    departure_city = models.CharField(
        max_length=50,
        verbose_name="Город вылета",
        help_text="Введите город вылеты",
        **NULLABLE,
    )
    arrival_country = models.CharField(
        max_length=50,
        verbose_name="Страна прибытия",
        help_text="Страну прибытия",
        **NULLABLE,
    )
    arrival_city = models.CharField(
        max_length=50,
        verbose_name="Город прибытия",
        help_text="Город прибытия",
        **NULLABLE,
    )
    tour_operator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Туроператор",
        related_name="tours",
        help_text="Введите ID туроператора",
        **NULLABLE,
    )
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        verbose_name="Отель",
        related_name="tours",
        help_text="Введите ID отеля",
        **NULLABLE,
    )
    room = models.CharField(
        max_length=50,
        verbose_name="Категория номера",
        default="Standard",
        help_text="Введите категорию номера",
    )
    transfer = models.BooleanField(verbose_name="Трансфер", default=False, help_text="Отметьте наличие трансфера")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость тура",
        help_text="Введите стоимость тура",
        **NULLABLE,
    )

    document = models.FileField(
        upload_to="tour/documents", verbose_name="Документы", help_text="Загрузите документы по туру", **NULLABLE
    )
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
    is_active = models.BooleanField(
        default=True,
        verbose_name="Тур активен?",
        help_text="Тур активен?",
    )

    class Meta:
        verbose_name = "Тур"
        verbose_name_plural = "Туры"
        ordering = ("start_date",)

    def __str__(self):
        if self.tour_operator:
            if self.tour_operator.company_name:
                return f"Тур от {self.tour_operator.company_name} в {self.hotel.name}"
            return f"Тур от {self.tour_operator.email} в {self.hotel.name}"
        return f"Тур в {self.hotel.name}"
