from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from all_fixture.fixture_views import NULLABLE
from hotels.models.room.models_room import Room


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
    price = models.PositiveIntegerField(
        verbose_name="Стоимость категории номеров в сутки",
        help_text="Введите стоимость категории номеров в сутки",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(500000),
        ],
    )

    class Meta:
        verbose_name = "Категория и номер"
        verbose_name_plural = "Категории и номера"

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
    share_size = models.PositiveIntegerField(
        verbose_name="Размер скидки",
        help_text="Введите размер скидки от 0 до 100",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        **NULLABLE,
    )
    categories = models.ManyToManyField(
        RoomCategory,
        related_name="room_date",
        verbose_name="Категория номера и его стоимость за сутки",
        help_text="Выберите категорию номера и его стоимость за сутки",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Дата стоимости номера"
        verbose_name_plural = "Даты стоимости номеров"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.start_date} - {self.end_date}"
