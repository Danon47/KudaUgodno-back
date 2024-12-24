from rest_framework.exceptions import ValidationError


class AirportValidator:
    def __init__(self, field):
        self.field = field

    forbidden_words = ["крипта", "оскорбления", "мат", "реклама"]

    def __call__(self, value):
        tmp_val = dict(value).get(self.field)
        if tmp_val.lower() in self.forbidden_words:
            raise ValidationError("Название аэропорта содержит недопустимые слова")
