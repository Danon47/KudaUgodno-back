from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from flights.models import Flight
from flights.validators.validators import DateValidator, ForbiddenWordValidator


class FlightSerializer(ModelSerializer):
    """
    Сериализатор для модели Flight.
    """

    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "airline",
            "departure_airport",
            "arrival_airport",
            "departure_date",
            "departure_time",
            "arrival_date",
            "arrival_time",
            "price",
            "service_class",
            "flight_type",
            "description"
        )

        validators = [
            serializers.UniqueTogetherValidator(
                fields=["flight_number", "departure_date"],
                queryset=Flight.objects.all(),  # Валидатор для проверки уникальности рейса в конкретную дату
            ),
            ForbiddenWordValidator(fields=["departure_airport", "arrival_airport"]),
            DateValidator(),
        ]
