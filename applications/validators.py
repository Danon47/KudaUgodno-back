from datetime import date

from rest_framework.exceptions import ValidationError


class DateBornValidator:
    """
    Проверка, что дата рождения не в будущем
    """

    def __call__(self, value):
        date_born = value.get("date_born")
        if date_born > date.today():
            raise ValidationError("Дата рождения не может быть в будущем")
