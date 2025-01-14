from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from hotels.models.models_hotel import NULLABLE
from hotels.services import calculate_nightly_prices


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