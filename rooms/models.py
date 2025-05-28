from decimal import Decimal

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from all_fixture.choices import RoomCategoryChoices
from all_fixture.fixture_views import NULLABLE
from hotels.models import Hotel, TypeOfMeal
from users.models import User


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
        default=RoomCategoryChoices.STANDARD,
        max_length=100,
        verbose_name="Категория номера",
        help_text="Категория номера",
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
        "RoomRules",
        related_name="rooms",
        verbose_name="Название правила",
        help_text="Введите название правила, а потом выберите его возможность использования Да/Нет",
    )

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"
        ordering = (
            "hotel",
            "category",
        )

    def __str__(self):
        return f"№{self.pk} - {self.category} в {self.hotel.name} №{self.hotel.pk}"


class RoomCategory(models.Model):
    """
    Модель для создания нескольких номеров, чтобы им можно было присвоить в определённые даты свою стоимость.
    """

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name="Категория номера",
        help_text="Выберите категорию номера",
    )
    price = models.DecimalField(
        verbose_name="Стоимость категории номеров в сутки",
        help_text="Введите стоимость категории номеров в сутки",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("9999999.99"))],
    )

    class Meta:
        verbose_name = "Стоимость номера"
        verbose_name_plural = "Стоимости номеров"

    def __str__(self):
        return f"{self.room} ({self.price})"


class RoomDate(models.Model):
    """
    Даты для номеров
    """

    start_date = models.DateField(
        verbose_name="Дата начала действия скидки",
        help_text="Дата начала действия скидки",
    )
    end_date = models.DateField(
        verbose_name="Дата окончания действия скидки",
        help_text="Дата окончания действия скидки",
    )
    available_for_booking = models.BooleanField(
        verbose_name="Доступна для бронирования",
        help_text="Доступна Да/Нет?",
        default=True,
    )
    stock = models.BooleanField(
        verbose_name="Акция",
        help_text="Акция Да/Нет?",
        default=False,
    )
    share_size = models.DecimalField(
        verbose_name="Размер скидки",
        help_text="Введите размер скидки, где 0.01 - это 1%, 1.00 - это 100%, а всё что больше 1.00 - "
        "это уже величина, к примеру 0.53 - это 53%, а 2000 - это величина скидки в виде 2000 рублей",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01")), MaxValueValidator(Decimal("99999.99"))],
        **NULLABLE,
    )
    categories = models.ManyToManyField(
        RoomCategory,
        related_name="room_date",
        verbose_name="Категория номера и его стоимость за сутки",
        help_text="Выберите категорию номера и его стоимость за сутки",
    )

    class Meta:
        verbose_name = "Дата стоимости номера"
        verbose_name_plural = "Даты стоимости номеров"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"


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
