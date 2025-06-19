from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from all_fixture.choices import RoomCategoryChoices
from all_fixture.fixture_views import DISCOUNT, NULLABLE
from hotels.models import Hotel, TypeOfMeal
from users.models import User


class CalendarDate(models.Model):
    start_date = models.DateField(
        verbose_name="Начало периода стоимости категорий номеров", help_text="Введите дату в формате YYYY-MM-DD"
    )
    end_date = models.DateField(
        verbose_name="Конец периода стоимости категорий номеров", help_text="Введите дату в формате YYYY-MM-DD"
    )
    available_for_booking = models.BooleanField(
        verbose_name="Доступна для бронирования",
        help_text="Доступность категории для бронирования в этот период",
        default=True,
    )
    discount = models.BooleanField(verbose_name="Акция", help_text="Применяется ли скидка на период", default=False)
    discount_amount = models.DecimalField(
        verbose_name="Размер скидки", help_text=DISCOUNT, max_digits=8, decimal_places=2, **NULLABLE, default=None
    )
    calendar_prices = models.ManyToManyField(
        "Category",
        verbose_name="Категории номеров",
        help_text="Категории номеров",
        related_name="categories_price",
        blank=True,
    )

    class Meta:
        verbose_name = "Календарь стоимости номеров"
        verbose_name_plural = "Календари стоимости номеров"

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"


class CalendarPrice(models.Model):
    """
    Модель для создания нескольких номеров, чтобы им можно было присвоить в определённые даты свою стоимость.
    """

    room = models.ForeignKey(
        "Room",
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Номер",
        help_text="Номер",
    )
    price = models.DecimalField(
        verbose_name="Стоимость категории номеров в сутки",
        help_text="Введите стоимость категории номеров в сутки",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("9999999.99"))],
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Категория номера"
        verbose_name_plural = "Категории номеров"

    def __str__(self):
        return f"{self.room} - {self.price}"


class RoomRules(models.Model):
    """Правила в номере"""

    name = models.CharField(
        max_length=100,
        verbose_name="Правила в номере",
        help_text="Правила в номере",
        **NULLABLE,
    )
    option = models.BooleanField(
        verbose_name="Да/Нет",
        help_text="Да/Нет",
        default=False,
    )
    created_by = models.ForeignKey(User, verbose_name="Создана пользователем", on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = "Правило в номере"
        verbose_name_plural = "Правила в номерах"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} ({self.option})"


class Room(models.Model):
    """
    Класс номера отеля
    """

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="rooms",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    category = models.CharField(
        choices=RoomCategoryChoices.choices,
        max_length=100,
        verbose_name="Категория номера",
        help_text="Категория номера",
        **NULLABLE,
    )
    type_of_meals = models.ManyToManyField(
        TypeOfMeal,
        related_name="rooms",
        verbose_name="Тип питания",
        help_text="Тип питания",
    )
    number_of_adults = models.IntegerField(
        verbose_name="Количество проживающих взрослых",
        help_text="Количество проживающих взрослых",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        **NULLABLE,
    )
    number_of_children = models.IntegerField(
        verbose_name="Количество проживающих детей",
        help_text="Количество проживающих детей",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        **NULLABLE,
    )
    double_bed = models.IntegerField(
        verbose_name="Двуспальная кровать",
        help_text="Двуспальная кровать",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(3),
        ],
        **NULLABLE,
    )
    single_bed = models.IntegerField(
        verbose_name="Односпальная кровать",
        help_text="Односпальная кровать",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ],
        **NULLABLE,
    )
    area = models.IntegerField(
        verbose_name="Площадь номера",
        help_text="Площадь номера",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(1000),
        ],
    )
    quantity_rooms = models.IntegerField(
        verbose_name="Количество номеров данного типа",
        help_text="Количество номеров данного типа",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(500),
        ],
        default=0,
    )
    amenities_common = ArrayField(
        models.CharField(max_length=100),
        verbose_name="Общие удобства в номере",
        help_text="Общие удобства в номере, введите через запятую",
        **NULLABLE,
    )
    amenities_coffee = ArrayField(
        models.CharField(max_length=100),
        verbose_name="Удобства кофе станции в номере",
        help_text="Удобства кофе станции в номере, введите через запятую",
        **NULLABLE,
    )
    amenities_bathroom = ArrayField(
        models.CharField(max_length=100),
        verbose_name="Удобства ванной комнаты в номере",
        help_text="Удобства ванной комнаты в номере, введите через запятую",
        **NULLABLE,
    )
    amenities_view = ArrayField(
        models.CharField(max_length=100),
        verbose_name="Удобства вид в номере",
        help_text="Удобства вид в номере, введите через запятую",
        **NULLABLE,
    )
    rules = models.ManyToManyField(
        RoomRules,
        related_name="rooms",
        verbose_name="Название правила",
        help_text="Введите название правила, а потом выберите его возможность использования Да/Нет",
    )
    booking_dates = models.ManyToManyField(
        CalendarDate,
        verbose_name="Календарь бронирования",
        help_text="Календарь бронирования",
        blank=True,
        related_name="booking_dates",
    )

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = ("hotel",)

    def __str__(self):
        return f"№{self.pk} - {self.category} в {self.hotel.name} №{self.hotel.pk}"


class RoomPhoto(models.Model):
    """
    Класс для загрузки нескольких фотографий номеров отеля
    """

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="room_photos",
        verbose_name="Номер",
        help_text="Номер",
        blank=True,
    )
    photo = models.ImageField(
        upload_to="hotels/hotels/rooms/",
        verbose_name="Фотография номера",
        help_text="Фотография номера",
        blank=True,
    )

    class Meta:
        verbose_name = "Фотография номера"
        verbose_name_plural = "Фотографии номера"
