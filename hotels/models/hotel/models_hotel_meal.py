# from django.db import models
# from django.core.validators import MinValueValidator, MaxValueValidator
# from hotels.choices import MealChoices
# from hotels.models.hotel.models_hotel import NULLABLE, Hotel
#
#
# class MealPlan(models.Model):
#     """
#     Класс для выбора типа питания
#     """
#
#     name = models.CharField(
#         max_length=20,
#         verbose_name="Тип питания",
#         choices=MealChoices.choices,
#     )
#     price_per_person = models.IntegerField(
#         verbose_name="Цена за человека",
#         validators=[
#             MinValueValidator(0),
#             MaxValueValidator(50000),
#         ],
#     )
#     hotel = models.ForeignKey(
#         Hotel,
#         on_delete=models.CASCADE,
#         related_name="hotel_meal",
#         verbose_name="Отель",
#         **NULLABLE,
#     )
#
#     class Meta:
#         verbose_name = "Тип питания"
#         verbose_name_plural = "Типы питания"
#
#     def __str__(self):
#         return f"{self.name} {self.price_per_person}"
