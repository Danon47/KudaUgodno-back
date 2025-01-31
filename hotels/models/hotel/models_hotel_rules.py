from django.db import models


class HotelRules(models.Model):
    """ Правила в отеле"""

    name = models.CharField(
        max_length=100,
        verbose_name="Правила в отеле",
        help_text="Правила в отеле",
    )
    description = models.TextField(
        verbose_name="Описание правил",
        help_text="Описание правил",
    )

    class Meta:
        verbose_name = "Правило в отеле"
        verbose_name_plural = "Правила в отеле"
        ordering = ("name",)

    def __str__(self):
        return self.name
