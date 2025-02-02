from datetime import time
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from hotels.choices import TypeOfHolidayChoices, PlaceChoices, TimeChoices
from hotels.models.hotel.models_hotel_amenity import (HotelAmenityForChildren, HotelAmenitySportsAndRecreation,
                                                      HotelAmenityInTheRoom, HotelAmenityCommon)
from hotels.models.hotel.models_hotel_rules import HotelRules

NULLABLE = {"blank": True, "null": True}


class Hotel(models.Model):
    """
    Класс отеля
    """

    # Название отеля
    name = models.CharField(
        max_length=100,
        verbose_name="Название отеля",
        help_text="Название отеля",
        unique=True,
    )
    # Категория отеля в звёздах
    star_category = models.IntegerField(
        verbose_name="Категория отеля",
        help_text="Выберите категорию отеля (от 0 до 5)",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        **NULLABLE,
    )
    # Тип размещения
    place = models.CharField(
        max_length=13,
        choices=PlaceChoices.choices,
        default=PlaceChoices.HOTEL,
        verbose_name="Тип размещения",
        help_text="Тип размещения",
        **NULLABLE,
    )
    # Страна отеля
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        help_text="Страна",
        **NULLABLE,
    )
    # Город отеля
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Город",
        **NULLABLE,
    )
    # Адрес отеля
    address = models.CharField(
        max_length=100,
        verbose_name="Адрес отеля",
        help_text="Адрес отеля",
        **NULLABLE,
    )
    # Расстояние до станции
    distance_to_the_station = models.IntegerField(
        verbose_name="Расстояние до вокзала",
        help_text="Введите расстояние до вокзала в метрах",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(200000),
        ],
        **NULLABLE,
    )
    # Расстояние до моря
    distance_to_the_sea = models.IntegerField(
        verbose_name="Расстояние до моря",
        help_text="Введите расстояние до моря в метрах",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(200000),
        ],
        **NULLABLE,
    )
    # Расстояние до центра
    distance_to_the_center = models.IntegerField(
        verbose_name="Расстояние до центра",
        help_text="Введите расстояние до центра в метрах",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(200000),
        ],
        **NULLABLE,
    )
    # Расстояние до метро
    distance_to_the_metro = models.IntegerField(
        verbose_name="Расстояние до метро",
        help_text="Введите расстояние до метро в метрах",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(200000),
        ],
        **NULLABLE,
    )
    # Расстояние до аэропорта
    distance_to_the_airport = models.IntegerField(
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
        help_text="Описание отеля",
        **NULLABLE,
    )
    # Время заселения
    check_in_time = models.TimeField(
        max_length=8,
        choices=TimeChoices.in_time(),
        default=time(14, 0),
        verbose_name="Время заезда",
        help_text="Время заселения",
        **NULLABLE,
    )
    # Время выезда
    check_out_time = models.TimeField(
        max_length=8,
        choices=TimeChoices.out_time(),
        default=time(12, 0),
        verbose_name="Время выезда",
        help_text="Время выезда",
        **NULLABLE,
    )
    # Общин удобства в отеле
    amenities_common = models.ManyToManyField(
        HotelAmenityCommon,
        verbose_name="Общие",
        related_name="hotels_common",
        help_text="Общие",
        **NULLABLE,
    )
    # Удобства в номере
    amenities_in_the_room = models.ManyToManyField(
        HotelAmenityInTheRoom,
        verbose_name="В номере",
        related_name="hotels_in_the_room",
        help_text="В номере",
        **NULLABLE,
    )
    # Удобства спорт и номер
    amenities_sports_and_recreation = models.ManyToManyField(
        HotelAmenitySportsAndRecreation,
        verbose_name="Спорт и отдых",
        related_name="hotels_sports_and_recreation",
        help_text="Спорт и отдых",
        **NULLABLE,
    )
    # Удобства для детей
    amenities_for_children = models.ManyToManyField(
        HotelAmenityForChildren,
        verbose_name="Для детей",
        related_name="hotels_children",
        help_text="Для детей",
        **NULLABLE,
    )
    # Тип питания Ultra All inclusive
    type_of_meals_ultra_all_inclusive = models.IntegerField(
        verbose_name="Тип питания Ultra All inclusive",
        help_text="Стоимость за одного человека",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10000),
        ],
        **NULLABLE,
    )
    # Тип питания All inclusive
    type_of_meals_all_inclusive = models.IntegerField(
        verbose_name="Тип питания All inclusive",
        help_text="Стоимость за одного человека",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10000),
        ],
        **NULLABLE,
    )
    # Тип питания полный пансион
    type_of_meals_full_board = models.IntegerField(
        verbose_name="Тип питания полный пансион",
        help_text="Стоимость за одного человека",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10000),
        ],
        **NULLABLE,
    )
    # Тип питания полупансион
    type_of_meals_half_board = models.IntegerField(
        verbose_name="Тип питания полу пансион",
        help_text="Стоимость за одного человека",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10000),
        ],
        **NULLABLE,
    )
    # Тип питания полупансион
    type_of_meals_only_breakfast = models.IntegerField(
        verbose_name="Тип питания только завтрак",
        help_text="Стоимость за одного человека",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10000),
        ],
        **NULLABLE,
    )
    # Пользовательская оценка
    user_rating = models.DecimalField(
        verbose_name="Пользовательская оценка",
        max_digits=3,
        decimal_places=1,
        default=0.0,
        help_text="Пользовательская оценка",
        **NULLABLE,
    )
    # Тип отдыха
    type_of_rest = models.CharField(
        max_length=15,
        choices=TypeOfHolidayChoices.choices,
        default=TypeOfHolidayChoices.BEACH,
        verbose_name="Тип отдыха",
        help_text="Тип отдыха",
        **NULLABLE,
    )
    # Правила
    rules = models.ManyToManyField(
        HotelRules,
        verbose_name="Правила в отеле",
        related_name="hotels_rules",
        help_text="Правила в отеле",
        **NULLABLE,
    )


    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"
        ordering = ("name",)

    def __str__(self):
        return self.name
