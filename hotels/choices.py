from datetime import time
from django.db import models


class CategoryChoices(models.TextChoices):
    """
    Категория номера
    """

    STANDARD = "Стандарт", "Стандарт"
    COMFORT = "Комфорт", "Комфорт"
    FAMILY = "Семейный", "Семейный"
    LUX = "Люкс", "Люкс"


class FoodChoices(models.TextChoices):
    """
    Питание
    """

    NO_MEALS = "Без питания", "Без питания"
    ULTRA_ALL_INCLUSIVE = "Ultra all inclusive", "Ultra all inclusive"
    ALL_INCLUSIVE = "All inclusive", "All inclusive"
    FULL_BOARD = "Полный пансион", "Полный пансион"
    HALF_BOARD = "Полупансион", "Полупансион"
    ONLY_BREAKFAST = "Только завтраки", "Только завтраки"


class BedChoices(models.TextChoices):
    """
    Тип кровати
    """

    SINGLE_1 = "1 Односпальная", "1 Односпальная"
    DOUBLE_1 = "1 Двуспальная", "1 Двуспальная"
    SINGLES_2 = "2 Односпальные", "2 Односпальные"
    DOUBLES_2 = "2 Двуспальные", "2 Двуспальные"
    SINGLE_AND_DOUBLE_1 = (
        "1 Односпальная и 1 Двуспальная",
        "1 Односпальная и 1 Двуспальная",
    )
    SINGLES_AND_DOUBLE_1 = (
        "2 Односпальные и 1 Двуспальная",
        "2 Односпальные и 1 Двуспальная",
    )
    SINGLES_AND_DOUBLES_2 = (
        "2 Односпальные и 2 Двуспальные",
        "2 Односпальные и 2 Двуспальные",
    )


class StarsChoices(models.TextChoices):
    """
    Количество звезд
    """

    ONE_STAR = "1 Звезда", "1 Звезда"
    TWO_STARS = "2 Звезды", "2 Звезды"
    THREE_STARS = "3 Звезды", "3 Звезды"
    FOUR_STARS = "4 Звезды", "4 Звезды"
    FIVE_STARS = "5 Звезд", "5 Звезд"


class TypeOfHolidayChoices(models.TextChoices):
    """
    Тип отдыха
    """

    BEACH = "Пляжный", "Пляжный"
    CITY = "Городской", "Городской"
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
