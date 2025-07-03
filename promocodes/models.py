from datetime import date
from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from all_fixture.views_fixture import NULLABLE
from hotels.models import Hotel
from tours.models import Tour


class Promocode(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.DecimalField(
        verbose_name="Величина скидки",
        help_text="Введите размер скидки, где 0.01 - это 1%, 1.00 - это 100%, а всё что больше 1.00 - "
        "это уже величина, к примеру 0.53 - это 53%, а 2000 - это величина скидки в виде 2000 рублей",
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
            MaxValueValidator(Decimal("99999.99")),
        ],
    )
    description = models.TextField()
    tours = models.ManyToManyField(Tour, verbose_name="Туры", help_text="Туры", blank=True)
    hotels = models.ManyToManyField(Hotel, verbose_name="Отели", help_text="Отели", blank=True)
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        now = date.today()
        return self.is_active and self.start_date <= now <= self.end_date

    def apply_discount(self, original_price):
        discount_amount = self.discount_amount
        if discount_amount < 1:
            discounted = original_price * (1 - Decimal(discount_amount))
        else:
            discounted = original_price - discount_amount
        return round(discounted, 2)


class PromocodePhoto(models.Model):
    image = models.ImageField(upload_to="promocodes/", **NULLABLE)
    promocode = models.ForeignKey(Promocode, on_delete=models.CASCADE, related_name="promocode_image")
