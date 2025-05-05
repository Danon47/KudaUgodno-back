from rest_framework.serializers import DecimalField, ModelSerializer, SerializerMethodField

from all_fixture.fixture_views import decimal_ivalid
from flights.serializers import FlightSerializer
from hotels.serializers.hotel.serializers_hotel import HotelListWithPhotoSerializer
from tours.models import Tour, TourStock
from tours.validators import EndDateValidator, PriceValidator, StartDateValidator


class TourSerializer(ModelSerializer):
    """
    Сериализатор для модели Tour, для ручек.
    POST, PUT.
    Создание, Обновление.
    """

    price = DecimalField(
        max_digits=10,
        decimal_places=2,
        coerce_to_string=False,
        required=False,
        help_text="Стоимость тура",
        error_messages=decimal_ivalid,
    )

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
            "created_at",
            "updated_at",
            "is_active",
        )
        read_only_fields = ("created_at", "updated_at")
        validators = [StartDateValidator(), EndDateValidator(), PriceValidator()]


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

    hotel = HotelListWithPhotoSerializer()
    tour_operator = SerializerMethodField()
    flight_to = FlightSerializer()
    flight_from = FlightSerializer()

    class Meta(TourSerializer.Meta):
        fields = TourSerializer.Meta.fields

    def get_tour_operator(self, obj: Tour) -> str:
        return obj.tour_operator.company_name


class TourStockSerializer(ModelSerializer):
    class Meta:
        model = TourStock
        fields = ("id", "active_stock", "end_date", "discount_amount")
