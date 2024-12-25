from datetime import date

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from tours.models import Tour


class TourSerializer(ModelSerializer):
    """
    Сериализатор для модели Tour.
    """

    def validate_start_date(self, value):
        """Проверка, что дата начала тура не в прошлом."""
        if value < date.today():
            raise serializers.ValidationError(
                "Дата начала тура не может быть в прошлом."
            )
        return value

    def validate_end_date(self, value):
        """Проверка, что дата окончания тура позже даты начала."""
        start_date = self.initial_data.get("start_date")
        if start_date:
            if isinstance(start_date, str):
                start_date = date.fromisoformat(
                    start_date
                )  # Преобразование строки в объект date

            if value <= start_date:
                raise serializers.ValidationError(
                    "Дата окончания тура должна быть позже даты начала."
                )

        return value

    class Meta:
        model = Tour
        fields = (
            "id",
            "start_date",
            "end_date",
            "flight_to",
            "flight_from",
            "departure_city",
            "guests_number",
            "tour_operator",
            "hotel",
            "room",
            "price",
        )
        read_only_fields = ("price", )
