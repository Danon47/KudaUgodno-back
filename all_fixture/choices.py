from django.db import models


class TypeInsuranceChoices(models.TextChoices):
    """
    Выбор страховых компаний
    """

    TSINSURANCE = "Т-Страхование", "Т-Страхование"
    SOVCOMINSURANCE = "Совкомбанк Страхование", "Совкомбанк Страхование"
    SBERINSURANCE = "Сбербанк Страхование", "Сбербанк Страхование"
    VSKINSURANCE = "ВСК Страхование", "ВСК Страхование"
    ROSGORINSURANCE = "Росгорстрах", "Росгорстрах"
    RESOINSURANCE = "РЕСО Страхование", "РЕСО Страхование"
    SOGLASIEINSURANCE = "Согласие", "Согласие"
    SOGAZINSURANCE = "СОГАЗ", "СОГАЗ"
    ALFAINSURANCE = "Альфа Страхование", "Альфа Страхование"
    RENESSANSINSURANCE = "Ренессанс Страхование", "Ренессанс Страхование"
    INGOSTRAHINSURANCE = "Ингострах", "Ингострах"
    INTOUCHINSURANCE = "INTOUCH", "INTOUCH"
    NOTSELECTED = "Не выбрано", "Не выбрано"


class PlaceChoices(models.TextChoices):
    """
    Выбор типом размещения
    """

    HOTEL = "Отель", "Отель"
    HOSTEL = "Хостел", "Хостел"
    VILLA = "Вилла", "Вилла"
    APARTMENT = "Апартаменты", "Апартаменты"
    GUEST_HOUSE = "Гостевой дом", "Гостевой дом"
    INN = "Гостиница", "Гостиница"


class TypeOfHolidayChoices(models.TextChoices):
    """
    Выбор типов отдыха
    """

    BEACH = "Пляжный", "Пляжный"
    CITY = "Городской", "Городской"
    SPA = "Спа", "Спа"
    HEALING = "Лечебный", "Лечебный"
    WITH_CHILDREN = "С детьми", "С детьми"
    WITH_ANIMALS = "С животными", "С животными"


class CurrencyChoices(models.TextChoices):
    """Валюты, используемые пользователем."""

    RUB = "RUB", "Рубль"
    EUR = "EUR", "Евро"
    USD = "USD", "Доллар"


class LanguageChoices(models.TextChoices):
    """Языки интерфейса, доступные пользователем."""

    RU = "RU", "Русский"
    EN = "EN", "Английский"


class ContactPriorityChoices(models.TextChoices):
    """Предпочтительный канал связи с пользователем."""

    PHONE = "phone", "Телефон"
    EMAIL = "email", "Email"


class WhatAboutChoices(models.TextChoices):
    """
    Выбор подборок для Что насчёт...
    """

    CLEAN = "---", "---"
    EXPLORE_THE_STREETS = "Что насчёт поисследовать улочки", "Что насчёт поисследовать улочки"
    ALL_WEEKEND = "Что насчёт на все выходные в", "Что насчёт на все выходные в"
    EXPLORE_THE_ASIA = "Что насчёт исследовать азиатскую культуру", "Что насчёт исследовать азиатскую культуру"
    RELAX_ON_THE_ISLAND = "Что насчёт расслабиться на островах", "Что насчёт расслабиться на островах"
    WARM = "Что насчёт погреться в", "Что насчёт погреться в"
