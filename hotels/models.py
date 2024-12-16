from datetime import time

from django.core.validators import MinValueValidator, MaxValueValidator
from .choices import FoodChoices, TypeOfHolidayChoices, PlaceChoices, TimeChoices
from django.db import models


NULLABLE = {"blank": True, "null": True}


class Room(models.Model):
    """
    Класс номера отеля
    """

    # Категория номера
    category = models.ForeignKey(
        "RoomCategory",
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name="Категория номера",
        help_text="Выберите категорию номера",
    )
    # Тип питания
    food = models.CharField(
        max_length=30,
        choices=FoodChoices.choices,
        default=FoodChoices.ONLY_BREAKFAST,
        verbose_name="Тип питания",
        help_text="Выберите тип питания",
    )
    # Тип отдыха
    type_of_holiday = models.CharField(
        max_length=15,
        choices=TypeOfHolidayChoices.choices,
        default=TypeOfHolidayChoices.BEACH,
        verbose_name="Тип отдыха",
        help_text="Выберите тип отдыха",
    )
    # Курение
    smoking = models.BooleanField(
        default=False,
        verbose_name="Курение разрешено?",
    )
    # С животными можно?
    pet = models.BooleanField(
        default=False,
        verbose_name="С животными разрешено?",
    )
    # Площадь номера
    area = models.IntegerField(
        verbose_name="Площадь номера",
        help_text="Введите площадь номера",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000),
        ],
    )
    # Количество номеров ?

    # Удобства в номере
    amenities = models.ManyToManyField(
        "RoomAmenity",
        verbose_name="Удобства в номере",
        help_text="Выберите удобства в номере",
        blank=True,
    )
    # Фотографии номера
    image = models.ImageField(
        upload_to="hotels/rooms/",
        verbose_name="Фотография",
        help_text="Загрузите фотографию номера",
        **NULLABLE,
    )
    # Количество проживающих людей
    capacity = models.IntegerField(
        verbose_name="Количество проживающих людей",
        help_text="Введите количество проживающих людей",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )
    # Односпальная кровать
    single_bed = models.IntegerField(
        verbose_name="Односпальная кровать",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ],
        **NULLABLE,
    )
    # Двуспальная кровать
    double_bed = models.IntegerField(
        verbose_name="Двуспальная кровать",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ],
        **NULLABLE,
    )
    # Цена за ночь
    nightly_price = models.PositiveIntegerField(
        verbose_name="Цена",
        help_text="Введите цену",
    )
    # Ближайшая свободная дата ?

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ("category",)

    def __str__(self):
        return f"{self.id} {self.category}"


class Hotel(models.Model):
    """
    Класс отеля
    """

    # Название отеля
    name = models.CharField(
        max_length=100,
        verbose_name="Название отеля",
        help_text="Введите название отеля",
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
        help_text="Выберите тип размещения",
    )
    # Страна отеля
    country = models.CharField(
        max_length=50,
        verbose_name="Страна",
        help_text="Введите страну",
    )
    # Город отеля
    city = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Введите город",
    )
    # Адрес отеля
    address = models.CharField(
        max_length=100,
        verbose_name="Адрес отеля",
        help_text="Введите адрес отеля",
    )
    # Расстояние до моря
    distance_to_sea = models.IntegerField(
        verbose_name="Расстояние до моря",
        help_text="Введите расстояние до моря",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10000),
        ],
        **NULLABLE,
    )
    # Расстояние до аэропорта
    distance_to_airport = models.IntegerField(
        verbose_name="Расстояние до аэропорта",
        help_text="Введите расстояние до аэропорта",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(200000),
        ],
        **NULLABLE,
    )
    # Описание отеля
    description = models.TextField(
        verbose_name="Описание отеля",
        help_text="Введите описание отеля",
    )
    # Фотографии отеля
    image = models.ImageField(
        upload_to="hotels/",
        verbose_name="Фотография",
        help_text="Загрузите фотографию отеля",
        **NULLABLE,
    )
    # Номера в отеле
    room = models.ManyToManyField(
        Room,
        verbose_name="Номера в отеле",
        blank=True,
    )
    # Удобства в номере
    amenities = models.ManyToManyField(
        "HotelAmenity",
        verbose_name="Удобства в отеле",
        help_text="Выберите удобства в отеле",
        blank=True,
    )
    # Пользовательская оценка
    user_rating = models.DecimalField(
        verbose_name="Пользовательская оценка",
        help_text="Введите оценку",
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
        help_text="Выберите время заезда",
    )
    # Время выезда
    check_out_time = models.TimeField(
        max_length=8,
        choices=TimeChoices.out_time(),
        default=time(12, 0),
        verbose_name="Время выезда",
        help_text="Выберите время выезда",
    )

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"
        ordering = ("name",)

    def __str__(self):
        return self.name


class RoomAmenity(models.Model):
    """
    Удобства в номере
    """

    name = models.CharField(
        max_length=50,
        verbose_name="Удобство",
        help_text="Введите удобство",
    )

    class Meta:
        verbose_name = "Удобство в номере"
        verbose_name_plural = "Удобства в номерах"

    def __str__(self):
        return self.name


class RoomCategory(models.Model):
    """
    Категория номера
    """

    name = models.CharField(
        max_length=20,
        verbose_name="Категория номера",
        help_text="Выберите категорию номера",
    )

    class Meta:
        verbose_name = "Категория номера"
        verbose_name_plural = "Категории номеров"

    def __str__(self):
        return self.name


class HotelAmenity(models.Model):
    """
    Удобства в отеле
    """

    name = models.CharField(
        max_length=50,
        verbose_name="Удобство",
        help_text="Введите удобство",
    )

    class Meta:
        verbose_name = "Удобство в отеле"
        verbose_name_plural = "Удобства в отеле"

    def __str__(self):
        return self.name
