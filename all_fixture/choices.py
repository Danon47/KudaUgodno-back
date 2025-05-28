from django.db import models


class MedicalInsuranceChoices(models.TextChoices):
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


class NotLeavingInsuranceChoices(models.TextChoices):
    """
    Выбор страховых компаний
    """

    SOGAZINSURANCE = "СОГАЗ", "СОГАЗ"
    TSINSURANCE = "Т-Страхование", "Т-Страхование"
    SOVCOMINSURANCE = "Совкомбанк Страхование", "Совкомбанк Страхование"
    SBERINSURANCE = "Сбербанк Страхование", "Сбербанк Страхование"
    VSKINSURANCE = "ВСК Страхование", "ВСК Страхование"
    ROSGORINSURANCE = "Росгорстрах", "Росгорстрах"
    RESOINSURANCE = "РЕСО Страхование", "РЕСО Страхование"
    SOGLASIEINSURANCE = "Согласие", "Согласие"
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

    EXPLORE_THE_STREETS = "Что насчёт поисследовать улочки в Италии", "Что насчёт поисследовать улочки в Италии"
    ALL_WEEKEND = "Что насчёт на все выходные в Санкт-Петербурге", "Что насчёт на все выходные в Санкт-Петербурге"
    EXPLORE_THE_ASIA = (
        "Что насчёт исследовать китайскую культуру в Шанхае",
        "Что насчёт исследовать китайскую культуру в Шанхае",
    )
    RELAX_ON_THE_ISLAND = (
        "Что насчёт расслабиться на островах Таиланда",
        "Что насчёт расслабиться на островах Таиланда",
    )
    WARM = "Что насчёт погреться в Турции", "Что насчёт погреться в Турции"


class AirlinesChoices(models.TextChoices):
    """
    Авиакомпания
    """

    AEROFLOT = "Аэрофлот", "Аэрофлот"
    POBEDA = "Победа", "Победа"
    ROSSIA = "Россия", "Россия"
    S7 = "S7", "S7"
    URAL_AIRLINES = "Уральские авиалинии", "Уральские авиалинии"
    NORDWIND = "Северный ветер", "Северный ветер"
    TURKISH_AIRLINES = "Turkish airlines", "Turkish airlines"
    EMIRATES = "Emirates", "Emirates"
    AZIMUT = "Азимут", "Азимут"
    RED_WINGS = "Red Wings", "Red Wings"
    UTAIR = "UTair", "UTair"
    YAMAL = "Ямал", "Ямал"
    PEGASUS = "Pegasus Airlines", "Pegasus Airlines"
    AZUR = "Azur Air", "Azur Air"
    CORENDON = "Corendon Airlines", "Corendon Airlines"
    AIR_ARADIA = "Air Arabia", "Air Arabia"
    FLY_DYDAI = "Fly Dubai", "Fly Dubai"
    CHINA_S = "China Southern Airlines", "China Southern Airlines"
    CHINA_E = "China Eastern", "China Eastern"
    SICHUAN = "Sichuan Airlines", "Sichuan Airlines"
    QATAR = "Qatar Airways", "Qatar Airways"
    BELAVIA = "Белавиа", "Белавиа"


class ServicesClassChoices(models.TextChoices):
    """
    Класс обслуживания
    """

    ECONOMY = "Эконом", "Эконом"
    BUSINESS = "Бизнес", "Бизнес"
    FIRST = "Первый", "Первый"


class FlightTypeChoices(models.TextChoices):
    """
    Тип рейса
    """

    REGULAR = "Регулярный", "Регулярный"
    CHARTER = "Чартерный", "Чартерный"
    TRANZIT = "Транзитный", "Транзитный"


class RoomCategoryChoices(models.TextChoices):
    """
    Категория номера
    """

    STANDARD = "Standard", "Standard"
    SINGLE_ROOM = "Single Room", "Single Room"
    DOUBLE_ROOM = "Double Room", "Double Room"
    TWIN_ROOM = "Twin Room", "Twin Room"
    TRIPLE_ROOM = "Triple Room", "Triple Room"
    FAMILY_ROOM = "Family Room", "Family Room"
    SUPERIOR_ROOM = "Superior Room", "Superior Room"
    DELUXE_ROOM = "Deluxe Room", "Deluxe Room"
    STUDIO = "Studio", "Studio"
    SUITE = "Suite", "Suite"
    JUNIOR_SUITE = "Junior Suite", "Junior Suite"
    RESIDENCE = "Residence", "Residence"
    ROYAL_SUITE = "Royal Suite", "Royal Suite"
    PENTHOUSE = "Penthouse", "Penthouse"


class TypeOfMealChoices(models.TextChoices):
    """
    Тип питания
    """

    NO_MEAL = "Без питания", "Без питания"
    BREAKFAST = "Завтрак", "Завтрак"
    BREAKFAST_AND_DINNER = "Завтрак и ужин", "Завтрак и ужин"
    FULL_BOARD = "Полный пансион", "Полный пансион"
    ALL_INCLUSIVE = "All inclusive", "All inclusive"
    ULTRA_ALL_INCLUSIVE = "Ultra all inclusive", "Ultra all inclusive"


class StatusChoices(models.TextChoices):
    """
    Выбор статуса для заявки
    """

    CONFIRM = "Подтвержден", "Подтвержден"
    AWAIT_CONFIRM = "Ожидает подтверждения", "Ожидает подтверждения"
    NEED_CONTACT = "Необходимо связаться", "Необходимо связаться"


class RoleChoices(models.TextChoices):
    """
    Выбор роли пользователя
    """

    USER = "USER", "Пользователь"
    TOUR_OPERATOR = "TOUR_OPERATOR", "Туроператор"
    HOTELIER = "HOTELIER", "Отельер"
    ADMIN = "ADMIN", "Администратор"
