from django.db import models

from hotels.models.hotel.models_hotel import Hotel, NULLABLE


class HotelAmenityCommon(models.Model):
    """
    Общие удобства
    """

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        related_name="hotels_amenities_common",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Общие удобства",
        help_text="Общие удобства"
    )

    class Meta:
        verbose_name = "Удобство в отеле Общие"
        verbose_name_plural = "Удобства в отеле Общие"

    def __str__(self):
        return self.name


class HotelAmenityInTheRoom(models.Model):
    """
    В номере
    """

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        related_name="hotels_amenities_room",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name="В номере",
        help_text="В номере"
    )

    class Meta:
        verbose_name = "Удобство в отеле В номере"
        verbose_name_plural = "Удобства в отеле В номерах"

    def __str__(self):
        return self.name


class HotelAmenitySportsAndRecreation(models.Model):
    """
    Спорт и отдых
    """

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        related_name="hotels_amenities_sports",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Спорт и отдых",
        help_text="Спорт и отдых"
    )

    class Meta:
        verbose_name = "Удобство в отеле Спорт и отдых"
        verbose_name_plural = "Удобства в отеле Спорт и отдых"

    def __str__(self):
        return self.name


class HotelAmenityForChildren(models.Model):
    """
    Для детей
    """

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        related_name="hotels_amenities_children",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Для детей",
        help_text="Для детей"
    )

    class Meta:
        verbose_name = "Удобство в отеле для детей"
        verbose_name_plural = "Удобства в отеле для детей"

    def __str__(self):
        return self.name
