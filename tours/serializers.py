from rest_framework.serializers import ModelSerializer

from tours.models import Tour
from tours.validators import EndDateValidator, StartDateValidator


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
            "departure_country",
            "departure_city",
            "arrival_country",
            "arrival_city",
            "tour_operator",
            "hotel",
            "room",
            "transfer",
            "price",
            "document",
            "created_at",
            "updated_at",
            "is_active",
        )
        read_only_fields = ("created_at", "updated_at")
        validators = [StartDateValidator(), EndDateValidator()]


class TourPatchSerializer(ModelSerializer):
    """
    Сериализатор для единственного действия - ставить тур в архив, и убирать его из архива
    """

    class Meta:
        model = Tour
        fields = ("is_active",)
