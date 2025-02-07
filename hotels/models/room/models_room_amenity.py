from django.db import models
from hotels.models.hotel.models_hotel import NULLABLE
from hotels.models.room.models_room import Room


class RoomAmenity(models.Model):
    """
    Удобства в номере
    """

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="rooms_amenities",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Удобство",
        help_text="Удобство",
    )

    class Meta:
        verbose_name = "Удобство в номере"
        verbose_name_plural = "Удобства в номерах"

    def __str__(self):
        return self.name
