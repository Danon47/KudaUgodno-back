from django.db import models


class RoomCategory(models.Model):
    """
    Категория номера
    """

    name = models.CharField(
        max_length=20,
        verbose_name="Категория номера",
    )

    class Meta:
        verbose_name = "Категория номера"
        verbose_name_plural = "Категории номеров"

    def __str__(self):
        return self.name