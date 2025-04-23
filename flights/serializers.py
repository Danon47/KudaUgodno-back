from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from all_fixture.validators.validators import DateValidator, ForbiddenWordValidator
from flights.models import Flight


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
            "departure_city",
            "departure_airport",
            "arrival_city",
            "arrival_airport",
            "departure_date",
            "departure_time",
            "arrival_date",
            "arrival_time",
            "price",
            "price_for_child",
            "service_class",
            "flight_type",
            "description",
        )

        validators = [
            serializers.UniqueTogetherValidator(
                fields=["flight_number", "departure_date"],
                queryset=Flight.objects.all(),  # Валидатор для проверки уникальности рейса в конкретную дату
            ),
            ForbiddenWordValidator(fields=["departure_airport", "arrival_airport"]),
            DateValidator(),
        ]
