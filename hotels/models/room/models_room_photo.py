from django.db import models

from hotels.models.room.models_room import Room


class RoomPhoto(models.Model):
    """
    Класс для загрузки нескольких фотографий номеров отеля
    """

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="room_photos",
        verbose_name="Номер",
        help_text="Номер",
        blank=True,
    )
    photo = models.ImageField(
        upload_to="hotels/hotels/rooms/",
        verbose_name="Фотография номера",
        help_text="Фотография номера",
        blank=True,
    )

    class Meta:
        verbose_name = "Фотография номера"
        verbose_name_plural = "Фотографии номера"
