from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import time
from .choices import MealChoices, TypeOfHolidayChoices, PlaceChoices, TimeChoices
from .services import calculate_nightly_prices

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
        default=1,
    )
    # Тип питания
    meal = models.ManyToManyField(
        "MealPlan",
        related_name="room_meals",
        verbose_name="Тип питания",
        blank=True,
    )
    # Курение
    smoking = models.BooleanField(
        default=False,
        verbose_name="Курение разрешено?",
    )
    # Площадь номера
    area = models.IntegerField(
        verbose_name="Площадь номера",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000),
        ],
    )
    # Удобства в номере
    amenities = models.ManyToManyField(
        "RoomAmenity",
        verbose_name="Удобства в номере",
        blank=True,
    )
    # Количество проживающих людей
    capacity = models.IntegerField(
        verbose_name="Количество проживающих людей",
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
    nightly_price = models.IntegerField(
        verbose_name="Цена за ночь",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000000),
        ],
    )
    # Отель
    hotel = models.ForeignKey(
        "Hotel",
        on_delete=models.SET_NULL,
        related_name="rooms",
        verbose_name="Отель",
        **NULLABLE,
    )
    # Цена за ночь без питания
    nightly_price_no_meals = models.DecimalField(
        verbose_name="Цена за ночь без питания",
        max_digits=10,
        decimal_places=2,
        default=0,
        **NULLABLE,
    )
    # Цена за ночь Ultra всё включено
    nightly_price_ultra_all_inclusive = models.DecimalField(
        verbose_name="Цена за ночь Ultra всё включено",
        max_digits=10,
        decimal_places=2,
        default=0,
        **NULLABLE,
    )
    # Цена за ночь всё включено
    nightly_price_all_inclusive = models.DecimalField(
        verbose_name="Цена за ночь всё включено",
        max_digits=10,
        decimal_places=2,
        default=0,
        **NULLABLE,
    )
    # Цена за ночь полный пансион
    nightly_price_full_board = models.DecimalField(
        verbose_name="Цена за ночь с полным пансионом",
        max_digits=10,
        decimal_places=2,
        default=0,
        **NULLABLE,
    )
    # Цена за ночь полупансион
    nightly_price_half_board = models.DecimalField(
        verbose_name="Цена за ночь с полупансионом",
        max_digits=10,
        decimal_places=2,
        default=0,
        **NULLABLE,
    )
    # Цена за ночь с завтраком
    nightly_price_only_breakfast = models.DecimalField(
        verbose_name="Цена за ночь с завтраком",
        max_digits=10,
        decimal_places=2,
        default=0,
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ("category",)

    def __str__(self):
        return f"{self.id} {self.category}"

    def save(self, *args, **kwargs):
        # Проверяем, создается ли объект впервые
        is_new = self._state.adding
        # Сохраняем объект, чтобы получить id
        super().save(*args, **kwargs)
        # Теперь, когда объект сохранен, можно рассчитать стоимость
        calculate_nightly_prices(self)
        # Если объект создается впервые, обновляем только поля с ценами
        if is_new:
            Room.objects.filter(id=self.id).update(
                nightly_price_no_meals=self.nightly_price_no_meals,
                nightly_price_ultra_all_inclusive=self.nightly_price_ultra_all_inclusive,
                nightly_price_all_inclusive=self.nightly_price_all_inclusive,
                nightly_price_full_board=self.nightly_price_full_board,
                nightly_price_half_board=self.nightly_price_half_board,
                nightly_price_only_breakfast=self.nightly_price_only_breakfast,
            )
        else:
            # Если объект обновляется, сохраняем его с force_update=True
            super().save(force_update=True, *args, **kwargs)


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


class RoomAmenity(models.Model):
    """
    Удобства в номере
    """

    name = models.CharField(
        max_length=50,
        verbose_name="Удобство",
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
    )

    class Meta:
        verbose_name = "Удобство в отеле"
        verbose_name_plural = "Удобства в отеле"

    def __str__(self):
        return self.name


class RoomPhoto(models.Model):
    """
    Класс для загрузки нескольких фотографий номеров отеля
    """

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="room_photos",
        verbose_name="Номер",
        blank=True,
    )
    photo = models.ImageField(
        upload_to="hotels/hotels/rooms/",
        verbose_name="Фотография номера",
        blank=True,
    )

    class Meta:
        verbose_name = "Фотография номера"
        verbose_name_plural = "Фотографии номера"


class HotelPhoto(models.Model):
    """
    Класс для загрузки нескольких фотографий отеля
    """

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="hotel_photos",
        verbose_name="Отель",
        blank=True,
    )
    photo = models.ImageField(
        upload_to="hotels/hotels/",
        verbose_name="Фотография отеля",
        blank=True,
    )

    class Meta:
        verbose_name = "Фотография отеля"
        verbose_name_plural = "Фотографии отеля"


class MealPlan(models.Model):
    """
    Класс для выбора типа питания
    """

    name = models.CharField(
        max_length=20,
        verbose_name="Тип питания",
        choices=MealChoices.choices,
    )
    price_per_person = models.IntegerField(
        verbose_name="Цена за человека",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(50000),
        ]
    )
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="hotel_meal",
        verbose_name="Отель",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Тип питания"
        verbose_name_plural = "Типы питания"

    def __str__(self):
        return f"{self.name} {self.price_per_person}"
