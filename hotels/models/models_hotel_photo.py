from hotels.models.models_hotel import Hotel
from django.db import models


class HotelPhoto(models.Model):
    """
    Класс для загрузки нескольких фотографий отеля
    """

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name="hotel_photos",
        verbose_name="Отель",
        blank=True,
    )
    photo = models.ImageField(
        upload_to="hotels/hotels/",
        verbose_name="Фотография отеля",
        blank=True,
    )

    class Meta:
        verbose_name = "Фотография отеля"
        verbose_name_plural = "Фотографии отеля"
