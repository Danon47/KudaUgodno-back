from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from hotels.models.hotel.models_hotel import NULLABLE, Hotel
from hotels.models.room.models_room_category import RoomCategory


class Room(models.Model):
    """
    Класс номера отеля
    """

    # Категория номера
    category = models.ForeignKey(
        RoomCategory,
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name="Категория номера",
        help_text="Категория номера",
        default=1,
    )
    # Курение
    smoking = models.BooleanField(
        default=False,
        verbose_name="Курение разрешено?",
    )
    # Площадь номера
    area = models.IntegerField(
        verbose_name="Площадь номера",
        help_text="Площадь номера",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000),
        ],
    )
    # Удобства в номере
    amenities = models.ManyToManyField(
        "RoomAmenity",
        verbose_name="Удобства в номере",
        help_text="Удобства в номере",
        blank=True,
    )
    # Количество проживающих людей
    capacity = models.IntegerField(
        verbose_name="Количество проживающих людей",
        help_text="Количество проживающих людей",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )
    # Односпальная кровать
    single_bed = models.IntegerField(
        verbose_name="Односпальная кровать",
        help_text="Односпальная кровать",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ],
        **NULLABLE,
    )
    # Двуспальная кровать
    double_bed = models.IntegerField(
        verbose_name="Двуспальная кровать",
        help_text="Двуспальная кровать",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ],
        **NULLABLE,
    )
    # Цена за ночь
    nightly_price = models.IntegerField(
        verbose_name="Цена за ночь",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000000),
        ],
        default=0,
    )
    # Отель
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        related_name="rooms",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )


    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ("category",)

    def __str__(self):
        return f"{self.id} {self.category}"
