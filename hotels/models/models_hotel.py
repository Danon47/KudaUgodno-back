from datetime import time
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from hotels.choices import TypeOfHolidayChoices, PlaceChoices, TimeChoices


NULLABLE = {"blank": True, "null": True}


class Hotel(models.Model):
    """
    Класс отеля
    """

    # Название отеля
    name = models.CharField(
        max_length=100,
        verbose_name="Название отеля",
    )
    # Категория отеля в звёздах
    star_category = models.IntegerField(
        verbose_name="Категория отеля",
        help_text="Выберите категорию отеля (от 0 до 5)",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
    )
    # Тип размещения
    place = models.CharField(
        max_length=13,
        choices=PlaceChoices.choices,
        default=PlaceChoices.HOTEL,
        verbose_name="Тип размещения",
    )
    # Тип отдыха
    type_of_holiday = models.CharField(
        max_length=15,
        choices=TypeOfHolidayChoices.choices,
        default=TypeOfHolidayChoices.BEACH,
        verbose_name="Тип отдыха",
    )
    # Страна отеля
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
    )
    # Город отеля
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
    )
    # Адрес отеля
    address = models.CharField(
        max_length=100,
        verbose_name="Адрес отеля",
    )
    # Расстояние до моря
    distance_to_sea = models.IntegerField(
        verbose_name="Расстояние до моря",
        help_text="Введите расстояние до моря в метрах",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10000),
        ],
        **NULLABLE,
    )
    # Расстояние до аэропорта
    distance_to_airport = models.IntegerField(
        verbose_name="Расстояние до аэропорта",
        help_text="Введите расстояние до аэропорта в метрах",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(200000),
        ],
        **NULLABLE,
    )
    # Описание отеля
    description = models.TextField(
        verbose_name="Описание отеля",
    )
    # Удобства в номере
    amenities = models.ManyToManyField(
        "HotelAmenity",
        verbose_name="Удобства в отеле",
        related_name="hotels",
        blank=True,
    )
    # Пользовательская оценка
    user_rating = models.DecimalField(
        verbose_name="Пользовательская оценка",
        max_digits=3,
        decimal_places=1,
        **NULLABLE,
    )
    # Время заселения
    check_in_time = models.TimeField(
        max_length=8,
        choices=TimeChoices.in_time(),
        default=time(14, 0),
        verbose_name="Время заезда",
    )
    # Время выезда
    check_out_time = models.TimeField(
        max_length=8,
        choices=TimeChoices.out_time(),
        default=time(12, 0),
        verbose_name="Время выезда",
    )

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"
        ordering = ("name",)

    def __str__(self):
        return self.name


