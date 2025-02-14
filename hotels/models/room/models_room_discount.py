from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class RoomDiscount(models.Model):
    """
    Скидка
    """

    name = models.CharField(
        verbose_name="Название скидки",
        help_text="Название скидки",
        max_length=100,
    )
    size = models.IntegerField(
        verbose_name="Размер скидки",
        help_text="Размер скидки",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    start_date = models.DateField(
        verbose_name="Дата начала действия скидки",
        help_text="Дата начала действия скидки",
    )
    end_date = models.DateField(
        verbose_name="Дата окончания действия скидки",
        help_text="Дата окончания действия скидки",
    )

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.name} ({self.size}%)"