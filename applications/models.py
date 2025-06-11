from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from all_fixture.choices import StatusChoices
from all_fixture.fixture_views import NULLABLE
from guests.models import Guest
from hotels.models import Hotel
from rooms.models import Room
from tours.models import Tour


class Application(models.Model):
    email = models.EmailField(
        verbose_name="Email",
    )
    phone_number = PhoneNumberField(
        region="RU",
        verbose_name="Телефон",
        help_text="Формат: +X XXX XXX XX XX",
    )
    visa = models.BooleanField(default=False, verbose_name="Оформление визы")
    med_insurance = models.BooleanField(default=False, verbose_name="Медицинская страховка")
    cancellation_insurance = models.BooleanField(default=False, verbose_name="Страховка невыезда")
    wishes = models.TextField(verbose_name="Пожелания", **NULLABLE)
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.AWAIT_CONFIRM,
        verbose_name="Статус заявки",
    )
    price = models.DecimalField(
        verbose_name="Итоговая стоимость",
        help_text="Итоговая стоимость",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00")), MaxValueValidator(Decimal("9999999.99"))],
        **NULLABLE,
    )

    class Meta:
        abstract = True


class ApplicationTour(Application):
    """
    Модель Заявки на тур
    """

    tour = models.ForeignKey(Tour, on_delete=models.PROTECT, verbose_name="Тур", **NULLABLE)
    quantity_guests = models.ManyToManyField(
        Guest,
        verbose_name="Количество гостей",
        related_name="application_tour_guests",
        blank=True,
    )

    class Meta:
        verbose_name = "Заявка на тур"
        verbose_name_plural = "Заявки на тур"
        ordering = ("-pk",)

    def __str__(self):
        return f"Заявка на тур № {self.pk}"


class ApplicationHotel(Application):
    """
    Модель Заявки на отель
    """

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        verbose_name="Отель",
        related_name="hotel_applications",
        help_text="Введите ID отеля",
        **NULLABLE,
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        verbose_name="Номер",
        related_name="hotel_applications",
        help_text="Введите ID номера",
        **NULLABLE,
    )
    quantity_guests = models.ManyToManyField(
        Guest,
        verbose_name="Количество гостей",
        related_name="application_hotel_guests",
        blank=True,
    )

    class Meta:
        verbose_name = "Заявка на отель"
        verbose_name_plural = "Заявки на отель"
        ordering = ("-pk",)

    def __str__(self):
        return f"Заявка на отель № {self.pk}"
