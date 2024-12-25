from datetime import datetime

from rest_framework.exceptions import ValidationError


class ForbiddenWordValidator:
    """
    Валидатор на наличие недопустимых слов в названии.
    """
    def __init__(self, fields: list):
        self.fields = fields

    forbidden_words = ["крипта", "оскорбления", "мат", "реклама"]

    def __call__(self, value):
        for field in self.fields:
            tmp_val = dict(value).get(field)
            if tmp_val.lower() in self.forbidden_words:
                raise ValidationError("Название аэропорта содержит недопустимые слова")


class DateValidator:
    """
    Валидатор для проверки, что дата и время прибытия позже даты и времени отправления.
    """

    def  __init__(self, departure_date, departure_time, arrival_date, arrival_time):
        self.departure_date = departure_date
        self.departure_time = departure_time
        self.arrival_date = arrival_date
        self.arrival_time = arrival_time

    def __call__(self, value):
        departure_date_field = value.get("departure_date")
        departure_time_field = value.get("departure_time")
        arrival_date_field = value.get("arrival_date")
        arrival_time_field = value.get("arrival_time")

        departure_datetime = datetime.combine(departure_date_field, departure_time_field)
        arrival_datetime = datetime.combine(arrival_date_field, arrival_time_field)
        if arrival_datetime <= departure_datetime:
            raise ValidationError("Дата и время прилета должны быть позже даты и времени вылета.")