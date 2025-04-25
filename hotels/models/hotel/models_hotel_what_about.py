from django.db import models

from all_fixture.choices import WhatAboutChoices
from hotels.models.hotel.models_hotel import Hotel


class HotelWhatAbout(models.Model):
    """
    Класс модели Что насчёт... Необходим да создания подборок.
    В выборе названия подборки такие вариации:
    1. Что насчёт поисследовать улочки и Что насчёт на все выходные в - тут может быть любой город
    2. Что насчёт исследовать азиатскую культуру в - тут только города Азии
    3. Что насчёт расслабиться на островах - тут только те города, где есть острова и есть море
    4. Что насчёт поисследовать улочки и Что насчёт расслабиться на островах - должен быть выбрана страна, а не город
    """

    name_set = models.CharField(
        max_length=100,
        verbose_name="Название подборки",
        help_text="Выберите название подборки",
        choices=WhatAboutChoices.choices,
        default="",
    )
    hotel = models.ManyToManyField(
        Hotel,
        verbose_name="Отель",
        help_text="Выберите отель",
        related_name="what_about_hotels",
    )

    class Meta:
        verbose_name = "Подборка что насчёт..."
        verbose_name_plural = "Подборки что на счёт..."

    def __str__(self):
        return self.name_set
