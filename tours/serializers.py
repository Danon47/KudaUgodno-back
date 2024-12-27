from datetime import date

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from tours.models import Tour
from tours.validators import StartDateValidator, EndDateValidator


class TourSerializer(ModelSerializer):
    """
    Сериализатор для модели Tour.
    """

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
        read_only_fields = ("price",)
        validators = [StartDateValidator(),
                      EndDateValidator()]
