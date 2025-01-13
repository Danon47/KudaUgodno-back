from django.db import models


class RoleChoices(models.TextChoices):
    """
    Выбор роли пользователя
    """

    USER = "Пользователь", "Пользователь"
    TOUR_OPERATOR = "Туроператор", "Туроператор"
