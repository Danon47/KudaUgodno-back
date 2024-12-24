from datetime import datetime

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from flights.models import Flight
from flights.validarors import AirportValidator


class FlightSerializer(ModelSerializer):
    """
    Сериализатор для модели Flight.
    """

    def validate(self, data):
        """
        Проверка, что дата и время прибытия позже даты и времени отправления.
        """
        departure_date = data.get("departure_date")
        arrival_date = data.get("arrival_date")

        if not departure_date or not arrival_date:
            raise serializers.ValidationError("Дата вылета и/или прилета отсутствует.")

        departure_time = data.get("departure_time")
        arrival_time = data.get("arrival_time")

        if not departure_time or not arrival_time:
            raise serializers.ValidationError("Время вылета и/или прилета отсутствует.")

        departure_datetime = datetime.combine(departure_date, departure_time)
        arrival_datetime = datetime.combine(arrival_date, arrival_time)

        if arrival_datetime <= departure_datetime:
            raise serializers.ValidationError(
                {
                    "arrival_date": "Дата и время прилета должны быть позже даты и времени вылета."
                }
            )

        return data

    class Meta:
        model = Flight
        fields = (
            "flight_number",
            "airline",
            "departure_airport",
            "arrival_airport",
            "departure_date",
            "departure_time",
            "arrival_date",
            "arrival_time",
            "price",
        )

        validators = [
            serializers.UniqueTogetherValidator(
                fields=["flight_number", "departure_date"],
                queryset=Flight.objects.all(),  # Валидатор для проверки уникальности рейса в конкретную дату
            ),
            AirportValidator(field="departure_airport"),
            AirportValidator(field="arrival_airport"),
        ]
