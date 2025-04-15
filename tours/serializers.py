from rest_framework.serializers import CharField, ModelSerializer, SerializerMethodField

from tours.models import Tour
from tours.validators import EndDateValidator, StartDateValidator


class TourSerializer(ModelSerializer):
    """
    Сериализатор для модели Tour, для ручек.
    POST, PUT.
    Создание, Обновление.
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
    Сериализатор для модели Tour, для единственного действия - ставить тур в архив, и убирать его из архива.
    PATCH.
    Частичное обновление.
    """

    class Meta:
        model = Tour
        fields = ("is_active",)


class TourListSerializer(TourSerializer):
    """
    Сериализатор для модели Tour, для ручек.
    GET, GET(RETRIEVE).
    Список всех туров, детальная информация о туре.
    """

    hotel = CharField()
    tour_operator = SerializerMethodField()
    flight_to = CharField()
    flight_from = CharField()

    class Meta(TourSerializer.Meta):
        fields = TourSerializer.Meta.fields

    def get_tour_operator(self, obj: Tour) -> str:
        return obj.tour_operator.company_name
