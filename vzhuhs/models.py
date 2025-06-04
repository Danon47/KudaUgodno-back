from django.contrib import admin
from django.db import models

from all_fixture.fixture_views import NULLABLE
from hotels.models import HotelPhoto


class Vzhuh(models.Model):
    """Маркетинговая сущность Вжух — спецпредложения по направлениям."""

    departure_city = models.CharField(max_length=100, verbose_name="Город вылета")
    arrival_city = models.CharField(max_length=100, verbose_name="Город прибытия")

    description = models.TextField(verbose_name="Описание", **NULLABLE)
    best_time_to_travel = models.TextField(verbose_name="Лучшее время для поездки", **NULLABLE)
    suitable_for_whom = models.TextField(verbose_name="Для кого подойдёт", **NULLABLE)

    # Туры
    tours = models.ManyToManyField("tours.Tour", related_name="vzhuhs", verbose_name="Вжухнутые туры", blank=True)

    # Отели
    hotels = models.ManyToManyField("hotels.Hotel", related_name="vzhuhs", verbose_name="Вжухнутые отели", blank=True)
    description_hotel = models.TextField(verbose_name="Описание к отелям", **NULLABLE)

    # Блог
    description_blog = models.TextField(verbose_name="Описание к блогу", **NULLABLE)

    # Флаг публикации
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Фото
    main_photo = models.ForeignKey(
        HotelPhoto,
        verbose_name="Главное фото для Вжуха",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vzhuhs",
    )

    class Meta:
        verbose_name = "Вжух"
        verbose_name_plural = "Вжухи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Вжух: {self.route}"

    @property
    def route(self):
        return f"{self.departure_city} → {self.arrival_city}"

    @admin.display(description="Маршрут")
    def display_route(self):
        return self.route
