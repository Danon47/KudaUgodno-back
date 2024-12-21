from django.db import models


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
