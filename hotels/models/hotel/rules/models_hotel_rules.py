from django.db import models

from hotels.models.hotel.models_hotel import NULLABLE, Hotel


class HotelRules(models.Model):
    """Правила в отеле"""

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        related_name="hotels_rules",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Правила в отеле",
        help_text="Правила в отеле",
        **NULLABLE,
    )
    description = models.TextField(
        verbose_name="Описание правил",
        help_text="Описание правил",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Правило в отеле"
        verbose_name_plural = "Правила в отеле"
        ordering = ("name",)

    def __str__(self):
        return self.name
