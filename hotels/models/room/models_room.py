from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from hotels.models.hotel.models_hotel import NULLABLE, Hotel


class Room(models.Model):
    """
    Класс номера отеля
    """
    # Отель
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        related_name="rooms",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    # Категория номера
    category = models.CharField(
        max_length=100,
        verbose_name="Категория номера",
        help_text="Категория номера",
    )
    # Цена за ночь
    price = models.IntegerField(
        verbose_name="Цена за ночь",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000000),
        ],
        default=0,
    )
    # Тип питания из отеля
    type_of_meals = models.CharField(
        max_length=99,
        verbose_name="Тип питания",
        help_text="Тип питания из отеля",
        **NULLABLE,
    )
    # Количество проживающих взрослых
    number_of_adults = models.IntegerField(
        verbose_name="Количество проживающих взрослых",
        help_text="Количество проживающих взрослых",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        **NULLABLE,
    )
    # Количество проживающих детей
    number_of_children = models.IntegerField(
        verbose_name="Количество проживающих детей",
        help_text="Количество проживающих детей",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        **NULLABLE,
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
    # Площадь номера
    area = models.IntegerField(
        verbose_name="Площадь номера",
        help_text="Площадь номера",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000),
        ],
    )
    # Количество номеров данного типа
    quantity_rooms = models.IntegerField(
        verbose_name="Количество номеров данного типа",
        help_text="Количество номеров данного типа",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(500),
        ],
        default=0,
    )
    # Скидка на номер
    discount = models.ManyToManyField(
        "RoomDiscount",
        verbose_name="Скидки",
        help_text="Скидки",
        related_name="rooms_discount",
        blank=True,
    )
    # Недоступность номера
    unavailable = models.ManyToManyField(
        "RoomUnavailable",
        verbose_name="Недоступность номера",
        help_text="Недоступность номера",
        related_name="rooms_unavailable",
        blank=True,
    )
    # Общие удобства в номере
    amenities_common = ArrayField(
        models.CharField(max_length=100),
        verbose_name="Общие удобства в номере",
        help_text="Общие удобства в номере",
        **NULLABLE,
    )
    # Удобства кофе станции в номере
    amenities_coffee = ArrayField(
        models.CharField(max_length=100),
        verbose_name="Удобства кофе станции в номере",
        help_text="Удобства кофе станции в номере",
        **NULLABLE,
    )
    # Удобства ванной комнаты в номере
    amenities_bathroom = ArrayField(
        models.CharField(max_length=100),
        verbose_name="Удобства ванной комнаты в номере",
        help_text="Удобства ванной комнаты в номере",
        **NULLABLE,
    )
    # Удобства вид в номере
    amenities_view = ArrayField(
        models.CharField(max_length=100),
        verbose_name="Удобства вид в номере",
        help_text="Удобства вид в номере",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ("category",)

    def __str__(self):
        return f"{self.id} {self.category}"
