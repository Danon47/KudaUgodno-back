from django.db import models


class RoomAmenity(models.Model):
    """
    Удобства в номере
    """

    name = models.CharField(
        max_length=50,
        verbose_name="Удобство",
    )

    class Meta:
        verbose_name = "Удобство в номере"
        verbose_name_plural = "Удобства в номерах"

    def __str__(self):
        return self.name
