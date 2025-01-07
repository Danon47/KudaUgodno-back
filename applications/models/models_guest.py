from django.core.validators import RegexValidator
from django.db import models

from users.models import User


class Guest(models.Model):
    """
    Модель Гостя
    """

    # Имя
    firstname = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    # Фамилия
    lastname = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
    )
    # Отчество
    surname = models.CharField(
        max_length=50,
        verbose_name="Отчество",
        blank=True,
        null=True,
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
    )
    # Серия/номер российского паспорта
    russian_passport_no = models.CharField(
        verbose_name="Серия/номер российского паспорта",
        help_text="Формат: XXXX XXXXXX",
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r"^[0-9]{4} [0-9]{6}$",
                message="Введите серия/номер в формате: XXXX XXXXXX",
            )
        ],
    )
    # Серия/номер иностранного паспорта
    international_passport_no = models.CharField(
        verbose_name="Серия/номер иностранного паспорта",
        help_text="Формат: XX XXXXXXXX",
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex="^[0-9]{2} [0-9]{7}$",
                message="Введите серия/номер в формате: XX XXXXXXXX",
            )
        ],
    )
    # Срок действия иностранного паспорта
    validity_international_passport = models.DateField(
        verbose_name="Срок действия иностранного паспорта",
        help_text="Формат: YYYY-MM-DD",
        blank=True,
        null=True
    )
    user_owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name="Пользователь cоздавший гостя"
    )

    class Meta:
        verbose_name = "Гость"
        verbose_name_plural = "Гости"
        ordering = ("lastname",)

    def __str__(self):
        return f"{self.lastname} {self.firstname}"
