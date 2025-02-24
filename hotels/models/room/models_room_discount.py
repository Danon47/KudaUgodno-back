from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from all_fixture.fixture_views import NULLABLE


class RoomDiscount(models.Model):
    """
    Скидка
    """

    room = models.ForeignKey(
        "Room",
        on_delete=models.CASCADE,
        related_name="discounts",
        verbose_name="Номер",
        help_text="Номер, к которому применяется скидка",
        **NULLABLE,
    )
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
