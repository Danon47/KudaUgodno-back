from datetime import date
from rest_framework import serializers


class StartDateValidator:
    """
    Валидатор для проверки, что дата начала тура не в прошлом.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_val = value.get("start_date")
        if tmp_val < date.today():
            raise serializers.ValidationError(
                "Дата начала тура не может быть в прошлом."
            )


class EndDateValidator:
    """
    Валидатор для проверки, что дата окончания тура позже даты начала.
    """

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __call__(self, value):
        start_date_field = value.get("start_date")
        end_date_field = value.get("start_date")

        if end_date_field < start_date_field:
            raise serializers.ValidationError(
                "Дата окончания тура не может быть раньше даты начала."
            )
