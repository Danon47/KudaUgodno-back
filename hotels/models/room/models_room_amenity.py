from django.db import models
from all_fixture.fixture_views import NULLABLE
from hotels.models.room.models_room import Room


class RoomAmenityCommon(models.Model):
    """
    Общие удобства в номере
    """

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="rooms_amenities_common",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Общее удобство в номере",
        help_text="Общее удобство в номере",
    )

    class Meta:
        verbose_name = "Общее удобство в номере"
        verbose_name_plural = "Общие удобства в номерах"

    def __str__(self):
        return self.name

class RoomAmenityCoffeeStation(models.Model):
    """
    Удобство кофе станции в номере
    """

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="rooms_amenities_coffee_station",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Удобство кофе станции в номере",
        help_text="Удобство кофе станции в номере",
    )

    class Meta:
        verbose_name = "Удобство кофе станции в номере"
        verbose_name_plural = "Удобства кофе станций в номерах"

    def __str__(self):
        return self.name


class RoomAmenityBathroom(models.Model):
    """
    Удобства в ванной комнате в номере
    """

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="rooms_amenities_bathroom",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Удобство в ванной комнате в номере",
        help_text="Удобство в ванной комнате в номере",
    )

    class Meta:
        verbose_name = "Удобство в ванной комнате в номере"
        verbose_name_plural = "Удобства в ванной комнате в номерах"

    def __str__(self):
        return self.name


class RoomAmenityView(models.Model):
    """
    Удобства вид в номере
    """

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="rooms_amenities_view",
        verbose_name="Отель",
        help_text="Отель",
        **NULLABLE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Удобство вид в номере",
        help_text="Удобство вид в номере",
    )

    class Meta:
        verbose_name = "Удобство вид в номере"
        verbose_name_plural = "Удобства вид в номерах"

    def __str__(self):
        return self.name