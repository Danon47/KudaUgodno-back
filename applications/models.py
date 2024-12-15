from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from applications.choices import StatusChoices

NULLABLE = {'blank': True, 'null': True}

class Guest(models.Model):
    """
    Модель Гостя
    """

    firstname = models.CharField(
        max_length=50,
        verbose_name="Имя",
        help_text="Введите имя"
    )
    lastname = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        help_text="Введите фамилию"
    )
    surname = models.CharField(
        max_length=50,
        verbose_name="Отчество",
        help_text="Введите отчество",
        **NULLABLE
    )
    date_born = models.DateField(
        verbose_name="Дата рождения",
        help_text="Введите дату рождения",
    )
    citizenship = models.CharField(
        max_length=100,
        verbose_name="Гражданство",
        help_text="Введите гражданство",
    )
    russian_passport_no = models.CharField(
        unique=True,
        verbose_name="Серия/номер российского паспорта",
        help_text="Введите серия/номер российского паспорта в формате: XXXX XXXXXX",
        **NULLABLE,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{4} [0-9]{6}$',
                message='Введите серия/номер в формате: XXXX XXXXXX'
            )
        ]
    )
    international_passport_no = models.CharField(
        unique=True,
        verbose_name="Серия/номер иностранного паспорта",
        help_text="Введите серия/номер иностранного паспорта в формате: XX XXXXXXXX",
        **NULLABLE,
        validators=[
            RegexValidator(
                regex="^[0-9{2} [0-9]{7}$",
                message='Введите серия/номер в формате: XX XXXXXXXX'
            )
        ]
    )
    validity_international_passport = models.DateField(
        verbose_name="Срок действия иностранного паспорта",
        help_text="Введите срок действия иностранного паспорта",
        **NULLABLE
    )

    class Meta:
        verbose_name = "Гость"
        verbose_name_plural = "Гости"
        ordering = ("lastname",)

    def __str__(self):
        return f"{self.lastname} {self.firstname} {self.surname}"


class Application(models.Model):
    """
    Модель Заявки
    """

    tour = models.ForeignKey(
        "tours.Tour",
        on_delete=models.PROTECT,
        verbose_name="Тур",
        help_text="Выберите тур",
    )
    email = models.EmailField(
        verbose_name="Email",
        help_text="Введите email"
    )
    phone_number = PhoneNumberField(
        region="RU",
        verbose_name="Телефон",
        help_text="Введите номер телефона"
    )
    quantity_rooms = models.ManyToManyField(
        "hotels.Room",
        verbose_name="Количество номеров",
        blank=True
    )
    quantity_guests = models.ManyToManyField(
        Guest,
        verbose_name="Количество гостей",
        blank=True,
        related_name="guest_applications"
    )
    visa = models.PositiveIntegerField(
        default=0,
        verbose_name="Оформление визы",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    med_insurance = models.BooleanField(
        default=False,
        verbose_name="Медицинская страховка"
    )
    cancellation_insurance = models.BooleanField(
        default=False,
        verbose_name="Страховка невыезда"
    )
    wishes = models.TextField(
        verbose_name="Пожелания",
        help_text="Введите пожелания",
        **NULLABLE
    )
    status = models.CharField(
        choices= StatusChoices.choices,
        default=StatusChoices.AWAIT_CONFIRM,
        verbose_name="Статус заявки"
    )

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
        ordering = ("-pk",)

    def __str__(self):
        return self.pk



