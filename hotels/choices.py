from datetime import time
from django.db import models


class PlaceChoices(models.TextChoices):
    """
    Тип размещения
    """

    HOTEL = "Отель", "Отель"
    HOSTEL = "Хостел", "Хостел"
    VILLA = "Вилла", "Вилла"
    APARTMENT = "Апартаменты", "Апартаменты"
    GUEST_HOUSE = "Гостевой дом", "Гостевой дом"
    INN = "Гостиница", "Гостиница"


class MealChoices(models.TextChoices):
    """
    Питание
    """

    NO_MEALS = "Без питания", "Без питания"
    ULTRA_ALL_INCLUSIVE = "Ultra all inclusive", "Ultra all inclusive"
    ALL_INCLUSIVE = "All inclusive", "All inclusive"
    FULL_BOARD = "Полный пансион", "Полный пансион"
    HALF_BOARD = "Полупансион", "Полупансион"
    ONLY_BREAKFAST = "Только завтраки", "Только завтраки"


class TypeOfHolidayChoices(models.TextChoices):
    """
    Тип отдыха
    """

    BEACH = "Пляжный", "Пляжный"
    CITY = "Городской", "Городской"
    SPA = "Спа", "Спа"
    HEALING = "Лечебный", "Лечебный"
    WITH_CHILDREN = "С детьми", "С детьми"
    WITH_ANIMALS = "С животными", "С животными"


class TimeChoices:
    """
    Класс выбора времени заезда и выезда
    """

    @classmethod
    # Время заезда
    def in_time(cls):
        return [
            (time(14, 0), "14:00"),
            (time(15, 0), "15:00"),
            (time(16, 0), "16:00"),
            (time(17, 0), "17:00"),
            (time(18, 0), "18:00"),
            (time(19, 0), "19:00"),
            (time(20, 0), "20:00"),
            (time(21, 0), "21:00"),
            (time(22, 0), "22:00"),
            (time(23, 0), "23:00"),
            (time(00, 0), "00:00"),
        ]

    @classmethod
    # Время выезда
    def out_time(cls):
        return [
            (time(12, 0), "12:00"),
            (time(11, 0), "11:00"),
            (time(10, 0), "10:00"),
            (time(9, 0), "09:00"),
            (time(8, 0), "08:00"),
            (time(7, 0), "07:00"),
            (time(6, 0), "06:00"),
            (time(5, 0), "05:00"),
            (time(4, 0), "04:00"),
            (time(3, 0), "03:00"),
            (time(2, 0), "02:00"),
            (time(1, 0), "01:00"),
            (time(0, 0), "00:00"),
        ]
