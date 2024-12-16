from rest_framework.serializers import ModelSerializer

from flights.models import Flight


class FlightSerializer(ModelSerializer):
    """
    Сериализатор для модели Flight.
    """

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
            "price"
        )
