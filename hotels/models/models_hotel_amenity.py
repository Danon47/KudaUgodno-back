from django.db import models


class HotelAmenity(models.Model):
    """
    Удобства в отеле
    """

    name = models.CharField(
        max_length=50,
        verbose_name="Удобство",
    )

    class Meta:
        verbose_name = "Удобство в отеле"
        verbose_name_plural = "Удобства в отеле"

    def __str__(self):
        return self.name
