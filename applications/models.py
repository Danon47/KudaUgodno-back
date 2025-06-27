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


class BaseApplication(models.Model):
    """
    Абстрактная базовая модель для заявок.

    Содержит общие поля для всех типов заявок:
    - count: количество человек
    - price: цена за одного человека
    - total_price: общая стоимость
    """

    count = models.PositiveSmallIntegerField(
        verbose_name="Количество",
        help_text="Введите количество",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена за одного человека",
        help_text="Введите цену за одного человека",
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("9999999.99")),
        ],
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая стоимость",
        help_text="Общая стоимость",
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("9999999.99")),
        ],
    )

    class Meta:
        abstract = True


class ApplicationVisa(BaseApplication):
    """
    Модель данных о визе в заявке.

    Наследует все поля от BaseApplication и добавляет специфичные для визы атрибуты.
    """

    class Meta:
        verbose_name = "Виза"
        verbose_name_plural = "Визы"


class ApplicationMedicalInsurance(BaseApplication):
    """
    Модель данных о медицинской страховке в заявке.

    Содержит информацию о стоимости и условиях медицинского страхования.
    """

    class Meta:
        verbose_name = "Медицинская страховка"
        verbose_name_plural = "Медицинские страховки"


class ApplicationCancellationInsurance(models.Model):
    """
    Модель данных о страховке невыезда.

    Атрибуты:
        total_price: Общая стоимость страховки
    """

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Общая стоимость",
        help_text="Общая стоимость",
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("9999999.99")),
        ],
    )

    class Meta:
        verbose_name = "Страховка невыезда"
        verbose_name_plural = "Страховки невыезда"


class Application(models.Model):
    """
    Базовая модель заявки.

    Содержит общие поля для всех типов заявок:
    - Контактная информация (email, телефон)
    - Дополнительные услуги (виза, страховки)
    - Статус заявки
    - Даты создания и обновления
    """

    email = models.EmailField(
        verbose_name="Email",
        help_text="Введите email",
    )
    phone_number = PhoneNumberField(
        region="RU",
        verbose_name="Телефон",
        help_text="Формат: +X XXX XXX XX XX",
    )
    visa = models.ForeignKey(
        ApplicationVisa,
        on_delete=models.PROTECT,
        verbose_name="Оформление визы",
        help_text="Введите данные по визе",
        **NULLABLE,
    )
    med_insurance = models.ForeignKey(
        ApplicationMedicalInsurance,
        on_delete=models.PROTECT,
        verbose_name="Медицинская страховка",
        help_text="Введите данные по медицинской страховке",
        **NULLABLE,
    )
    cancellation_insurance = models.ForeignKey(
        ApplicationCancellationInsurance,
        on_delete=models.PROTECT,
        verbose_name="Страховка невыезда",
        help_text="Введите данные по страховке невыезда",
        **NULLABLE,
    )
    wishes = models.TextField(
        verbose_name="Пожелания",
        help_text="Введите данные по пожеланиям",
        **NULLABLE,
    )
    status = models.CharField(
        choices=StatusChoices.choices,
        default=StatusChoices.AWAIT_CONFIRM,
        verbose_name="Статус заявки",
        help_text="Выберите статус заявки",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Заявка {self._meta.verbose_name} №{self.pk}"


class BaseApplicationWithGuests(Application):
    """
    Абстрактная модель заявки с гостями.

    Добавляет связь ManyToMany с моделью Guest.

    Атрибуты:
        quantity_guests: Список гостей в заявке
    """

    quantity_guests = models.ManyToManyField(
        Guest,
        verbose_name="Гости",
        help_text="Выберите гостей",
        related_name="%(class)s_guests",
        blank=True,
    )

    class Meta:
        abstract = True


class ApplicationTour(BaseApplicationWithGuests):
    """
    Модель заявки на тур.

    Содержит информацию о туре и связанных с ним услугах.

    Атрибуты:
        tour: Ссылка на выбранный тур
        quantity_guests: Список гостей, участвующих в туре
        created_at: Дата и время создания заявки
        updated_at: Дата и время последнего обновления
    """

    tour = models.ForeignKey(
        Tour,
        on_delete=models.SET_NULL,
        verbose_name="Тур",
        help_text="Выберите тур",
        related_name="tour_applications",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Заявка на тур"
        verbose_name_plural = "Заявки на тур"
        ordering = ("-pk",)


class ApplicationHotel(BaseApplicationWithGuests):
    """
    Модель заявки на отель.

    Содержит информацию о бронировании отеля и связанных услугах.

    Атрибуты:
        hotel: Выбранный отель
        room: Забронированный номер
        quantity_guests: Список гостей
        created_at: Дата и время создания заявки
        updated_at: Дата и время последнего обновления
    """

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.SET_NULL,
        verbose_name="Отель",
        help_text="Выберите отель",
        related_name="hotel_applications",
        **NULLABLE,
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        verbose_name="Номер",
        related_name="room_applications",
        help_text="Выберите номер",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Заявка на отель"
        verbose_name_plural = "Заявки на отель"
        ordering = ("-pk",)
