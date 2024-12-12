from datetime import time
from django.db import models



class PetChoices(models.TextChoices):
    """
    Разрешено ли с животными в данном отеле
    """

    Authorized = "Разрешено", "Разрешено"
    Forbidden = "Запрещено", "Запрещено"


class SmokingChoices(models.TextChoices):
    """
    Разрешено ли курить в данным отеле
    """

    Authorized = "Разрешено", "Разрешено"
    Forbidden = "Запрещено", "Запрещено"


class CategoryChoices(models.TextChoices):
    """
    Категория номера
    """

    Standard = "Стандарт", "Стандарт"
    Comfort = "Комфорт", "Комфорт"
    Family = "Семейный", "Семейный"
    Lux = "Люкс", "Люкс"


class FoodChoices(models.TextChoices):
    """
    Питание
    """

    No_meals = "Без питания", "Без питания"
    Ultra_all_inclusive = "Ultra all inclusive", "Ultra all inclusive"
    All_inclusive = "All inclusive", "All inclusive"
    Full_board = "Полный пансион", "Полный пансион"
    Half_board = "Полупансион", "Полупансион"
    Only_breakfast = "Только завтраки", "Только завтраки"


class BedChoices(models.TextChoices):
    """
    Тип кровати
    """

    Single_1 = "1 Односпальная", "1 Односпальная"
    Double_2 = "1 Двуспальная", "1 Двуспальная"
    Singles_2 = "2 Односпальные", "2 Односпальные"
    Doubles_2 = "2 Двуспальные", "2 Двуспальные"
    Single_and_Double_1 = (
        "1 Односпальная и 1 Двуспальная",
        "1 Односпальная и 1 Двуспальная",
    )
    Singles_and_Double_1 = (
        "2 Односпальные и 1 Двуспальная",
        "2 Односпальные и 1 Двуспальная",
    )
    Singles_and_Doubles_2 = (
        "2 Односпальные и 2 Двуспальные",
        "2 Односпальные и 2 Двуспальные",
    )


class StarsChoices(models.TextChoices):
    """
    Количество звезд
    """

    One_star = "1 Звезда", "1 Звезда"
    Two_stars = "2 Звезды", "2 Звезды"
    Three_stars = "3 Звезды", "3 Звезды"
    Four_stars = "4 Звезды", "4 Звезды"
    Five_stars = "5 Звезд", "5 Звезд"


class TypeOfHolidayChoices(models.TextChoices):
    """
    Тип отдыха
    """

    Beach = "Пляжный", "Пляжный"
    City = "Городской", "Городской"
    With_children = "С детьми", "С детьми"
    With_animals = "С животными", "С животными"


class TimeChoices:
    """
    Класс выбора времени заезда и выезда
    """


    @classmethod
    # Время заезда
    def in_time(cls):
        return [
            (time(14,0), "14:00"),
            (time(15,0), "15:00"),
            (time(16,0), "16:00"),
            (time(17,0), "17:00"),
            (time(18,0), "18:00"),
            (time(19,0), "19:00"),
            (time(20,0), "20:00"),
            (time(21,0), "21:00"),
            (time(22,0), "22:00"),
            (time(23,0), "23:00"),
            (time(00,0), "00:00"),
        ]

    @classmethod
    # Время выезда
    def out_time(cls):
        return [
            (time(0,0), "00:00"),
            (time(1,0), "01:00"),
            (time(2,0), "02:00"),
            (time(3,0), "03:00"),
            (time(4,0), "04:00"),
            (time(5,0), "05:00"),
            (time(6,0), "06:00"),
            (time(7,0), "07:00"),
            (time(8,0), "08:00"),
            (time(9,0), "09:00"),
            (time(10,0), "10:00"),
            (time(11,0), "11:00"),
            (time(12,0), "12:00"),
        ]

