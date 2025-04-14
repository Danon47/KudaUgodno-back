from datetime import date

from rest_framework import serializers


class StartDateValidator:
    """
    Валидатор для проверки, что дата начала тура не в прошлом.
    """

    def __call__(self, value):
        tmp_val = value.get("start_date")
        if tmp_val is not None and tmp_val < date.today():
            raise serializers.ValidationError("Дата начала тура не может быть в прошлом.")


class EndDateValidator:
    """
    Валидатор для проверки, что дата окончания тура позже даты начала.
    """

    def __call__(self, value):
        start_date_field = value.get("start_date")
        end_date_field = value.get("end_date")

        if start_date_field is not None and end_date_field is not None:
            raise serializers.ValidationError("Дата окончания тура не может быть раньше даты начала.")
