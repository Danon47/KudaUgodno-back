from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from all_fixture.fixture_views import NULLABLE
from applications.choices import StatusChoices
from guests.models import Guest
from hotels.models.hotel.models_hotel import Hotel
from hotels.models.room.models_room import Room
from tours.models import Tour


# from users.models import User


class Application(models.Model):
    """
    Модель Заявки
    """

    tour = models.ForeignKey(Tour, on_delete=models.PROTECT, verbose_name="Тур", **NULLABLE)
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        verbose_name="Отель",
        related_name="applications",
        help_text="Введите ID отеля",
        **NULLABLE,
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        verbose_name="Номер",
        related_name="applications",
        help_text="Введите ID номера",
        **NULLABLE,
    )
    email = models.EmailField(
        verbose_name="Email",
    )
    phone_number = PhoneNumberField(
        region="RU",
        verbose_name="Телефон",
        help_text="Формат: +X XXX XXX XX XX",
    )
    quantity_guests = models.ManyToManyField(
        Guest,
        verbose_name="Количество гостей",
        related_name="guests",
        blank=True,
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
    # user_owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь кто создал заявку")

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ("-pk",)

    def __str__(self):
        return f"Заявка N {self.pk}"
