from django.db import models


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
    BUSINESS = "Бизнес ", "Бизнес"
    FIRST = "Первый", "Первый"


class FlightTypeChoices(models.TextChoices):
    """
    Тип рейса
    """

    REGULAR = "Регулярный", "Регулярный"
    CHARTER = "Чартерный", "Чартерный"
    TRANZIT = "Транзитный", "Транзитный"

