from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from applications.choices import StatusChoices

NULLABLE = {'blank': True, 'null': True}

class Guest(models.Model):
    """
    Модель Гостя
    """
    # Имя
    firstname = models.CharField(
        max_length=50,
        verbose_name="Имя",
        help_text="Введите имя"
    )
    # Фамилия
    lastname = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        help_text="Введите фамилию"
    )
    # Отчество
    surname = models.CharField(
        max_length=50,
        verbose_name="Отчество",
        help_text="Введите отчество",
        **NULLABLE
    )
    # Дата рождения
    date_born = models.DateField(
        verbose_name="Дата рождения",
        help_text="Формат: YYYY-MM-DD",
    )
    # Гражданство
    citizenship = models.CharField(
        max_length=100,
        verbose_name="Гражданство",
        help_text="Введите гражданство",
    )
    # Серия/номер российского паспорта
    russian_passport_no = models.CharField(
        unique=True,
        verbose_name="Серия/номер российского паспорта",
        help_text="Формат: XXXX XXXXXX",
        **NULLABLE,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{4} [0-9]{6}$',
                message='Введите серия/номер в формате: XXXX XXXXXX'
            )
        ]
    )
    # Серия/номер иностранного паспорта
    international_passport_no = models.CharField(
        unique=True,
        verbose_name="Серия/номер иностранного паспорта",
        help_text="Формат: XX XXXXXXXX",
        **NULLABLE,
        validators=[
            RegexValidator(
                regex="^[0-9]{2} [0-9]{7}$",
                message="Введите серия/номер в формате: XX XXXXXXXX"
            )
        ]
    )
    # Срок действия иностранного паспорта
    validity_international_passport = models.DateField(
        verbose_name="Срок действия иностранного паспорта",
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
    # Тур
    tour = models.ForeignKey(
        "tours.Tour",
        on_delete=models.PROTECT,
        verbose_name="Тур",
        help_text="Тур который хотят оформить",
    )
    # Email пользователя
    email = models.EmailField(
        verbose_name="Email",
    )
    # Номер телефона
    phone_number = PhoneNumberField(
        region="RU",
        verbose_name="Телефон",
        help_text="Номер телефона в формате: +7 (999) 999-99-99",
    )
    # Количество номеров
    quantity_rooms = models.ManyToManyField(
        "hotels.Room",
        verbose_name="Количество номеров",
        help_text="Количество номеров которые хотят забронировать",
        blank=True,
        # related_name="room_applications"
    )
    # Количество гостей
    quantity_guests = models.ManyToManyField(
        Guest,
        verbose_name="Количество гостей",
        blank=True,
        # related_name="guest_applications"
    )
    #Оформление визы
    visa = models.PositiveIntegerField(
        default=0,
        verbose_name="Оформление визы",
        help_text="Количество виз необходимых для оформления",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    # Страховка жизни
    med_insurance = models.BooleanField(
        default=False,
        verbose_name="Медицинская страховка"
    )
    # Страховка от невыезда
    cancellation_insurance = models.BooleanField(
        default=False,
        verbose_name="Страховка невыезда"
    )
    # Пожелания
    wishes = models.TextField(
        verbose_name="Пожелания",
        help_text="Вводится клиентом при бронировании по желанию",
        **NULLABLE
    )
    # Статус заявки
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

