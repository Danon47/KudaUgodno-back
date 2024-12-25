import os
from datetime import datetime

from rest_framework.exceptions import ValidationError


class ForbiddenWordValidator:
    """
    Валидатор на наличие недопустимых слов в названии.
    """

    def __init__(self, fields: list):
        self.fields = fields
        self.forbidden_words = self.load_forbidden_words()

    def load_forbidden_words(self):
        """
        Загружает запрещенные слова из файла forbidden_words.txt.
        """
        file_path = os.path.join(os.path.dirname(__file__), "forbidden_words.txt")
        with open(file_path, "r", encoding="utf-8") as file:
            return [line.strip().lower() for line in file if line.strip()]

    def __call__(self, value):
        for field in self.fields:
            tmp_val = dict(value).get(field)
            if tmp_val and any(
                word in tmp_val.lower() for word in self.forbidden_words
            ):
                raise ValidationError("Введено недопустимое слово")


class DateValidator:
    """
    Валидатор для проверки, что дата и время прибытия позже даты и времени отправления.
    """

    def __init__(self, departure_date, departure_time, arrival_date, arrival_time):
        self.departure_date = departure_date
        self.departure_time = departure_time
        self.arrival_date = arrival_date
        self.arrival_time = arrival_time

    def __call__(self, value):
        departure_date_field = value.get("departure_date")
        departure_time_field = value.get("departure_time")
        arrival_date_field = value.get("arrival_date")
        arrival_time_field = value.get("arrival_time")

        departure_datetime = datetime.combine(
            departure_date_field, departure_time_field
        )
        arrival_datetime = datetime.combine(arrival_date_field, arrival_time_field)
        if arrival_datetime <= departure_datetime:
            raise ValidationError(
                "Дата и время прилета должны быть позже даты и времени вылета."
            )
