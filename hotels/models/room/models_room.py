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
    # Бронь возможна только с выбором типа питания
    food_is_a_must = models.BooleanField(
        default=False,
        verbose_name="Бронь возможна только с выбором типа питания",
    )
    # Тип питания из отеля
    type_of_meal = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Тип питания",
        help_text="Тип питания из отеля (словарь)",
    )
    # Курение
    smoking = models.BooleanField(
        default=False,
        verbose_name="Курение разрешено?",
    )
    # С животными
    pet = models.BooleanField(
        default=False,
        verbose_name="С животными разрешено?",
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
        related_name="rooms_amenities",
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

    def save(self, *args, **kwargs):
        if self.hotel:
            # Передаем значения типов питания из отеля в словарь
            self.type_of_meal = {
                "ultra_all_inclusive": self.hotel.type_of_meals_ultra_all_inclusive,
                "all_inclusive": self.hotel.type_of_meals_all_inclusive,
                "full_board": self.hotel.type_of_meals_full_board,
                "half_board": self.hotel.type_of_meals_half_board,
                "only_breakfast": self.hotel.type_of_meals_only_breakfast,
            }
        super().save(*args, **kwargs)
