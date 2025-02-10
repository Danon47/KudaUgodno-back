from django.db import models


class RoleChoices(models.TextChoices):
    """
    Выбор роли пользователя
    """

    USER = "USER", "Пользователь"
    TOUR_OPERATOR = "TOUR_OPERATOR", "Туроператор"
    HOTELIER = "HOTELIER", "Отельер"
