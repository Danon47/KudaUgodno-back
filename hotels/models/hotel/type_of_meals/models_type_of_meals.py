from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from all_fixture.choices import TypeOfMealChoices
from all_fixture.fixture_views import NULLABLE
from hotels.models.hotel.models_hotel import Hotel


class TypeOfMeal(models.Model):
    """
    Модель типов питания.
    """

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="type_of_meals",
        verbose_name="Отель",
        help_text="Отель, к которому добавляются типы питания",
        **NULLABLE,
    )
    name = models.CharField(
        choices=TypeOfMealChoices.choices,
        default=TypeOfMealChoices.BREAKFAST,
        verbose_name="Выберите типа питания",
        help_text="Выберите тип питания",
        max_length=100,
    )
    price = models.PositiveIntegerField(
        verbose_name="Стоимость типа питания",
        help_text="Введите стоимость типа питания",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(500000),
        ],
    )

    class Meta:
        verbose_name = "Тип питания"
        verbose_name_plural = "Типы питания"
        constraints = [models.UniqueConstraint(fields=["hotel", "name"], name="unique_type_of_meal_in_hotel")]

    def __str__(self):
        return f"{self.name} ({self.price})"
