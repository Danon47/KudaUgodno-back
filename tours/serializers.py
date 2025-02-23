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
            "number_of_adults",
            "number_of_children",
            "tour_operator",
            "hotel",
            "transfer",
            "price",
            "document",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("created_at", "updated_at")
        validators = [StartDateValidator(), EndDateValidator()]
