from rest_framework.serializers import (
    CharField,
    DateField,
    DecimalField,
    FloatField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from all_fixture.fixture_views import decimal_ivalid
from flights.serializers import FlightSerializer
from hotels.serializers import HotelListWithPhotoSerializer, HotelShortSerializer
from hotels.serializers_type_of_meals import TypeOfMealSerializer
from rooms.serializers import RoomDetailSerializer
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
            "rooms",
            "type_of_meals",
            "price",
            "transfer",
            "is_active",
            "created_at",
            "updated_at",
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
    rooms = RoomDetailSerializer(many=True, read_only=True)
    type_of_meals = TypeOfMealSerializer(many=True, read_only=True)
    tour_operator = SerializerMethodField()
    flight_to = FlightSerializer()
    flight_from = FlightSerializer()

    class Meta(TourSerializer.Meta):
        fields = TourSerializer.Meta.fields

    def get_tour_operator(self, obj: Tour) -> str:
        return obj.tour_operator.company_name


class TourShortSerializer(ModelSerializer):
    """
    Сериализатор для списка горящих туров.
    """

    hotel = HotelShortSerializer()
    guests = SerializerMethodField()

    class Meta:
        model = Tour
        fields = ("hotel", "price", "start_date", "end_date", "guests")

    def get_guests(self, obj):
        return {
            "number_of_adults": obj.number_of_adults,
            "number_of_children": obj.number_of_children,
        }


class TourStockSerializer(ModelSerializer):
    class Meta:
        model = TourStock
        fields = ("id", "active_stock", "end_date", "discount_amount")


class TourSearchRequestSerializer(Serializer):
    """Сериализатор только для валидации параметров запроса поиска (все поля обязательные).."""

    departure_city = CharField(required=True)
    arrival_city = CharField(required=True)
    start_date = DateField(
        required=True,
        input_formats=["%Y-%m-%d"],
        error_messages={"invalid": "Некорректный формат даты. Используйте YYYY-MM-DD"},
    )
    nights = IntegerField(min_value=1, required=True)
    guests = IntegerField(min_value=1, required=True)
    validators = [StartDateValidator()]


class TourFiltersRequestSerializer(Serializer):
    """Сериализатор для параметров расширенного поиска (все поля необязательные)."""

    # Параметры фильтрации верхнего поиска
    departure_city = CharField(required=False)
    arrival_city = CharField(required=False)
    start_date = DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        error_messages={"invalid": "Некорректный формат даты. Используйте YYYY-MM-DD"},
    )
    nights = IntegerField(min_value=1, required=False)
    guests = IntegerField(min_value=1, required=False)

    # Параметры фильтрации
    city = CharField(required=False)
    type_of_rest = CharField(required=False)
    place = CharField(required=False)
    price_gte = IntegerField(min_value=0, required=False)
    price_lte = IntegerField(min_value=0, required=False)
    user_rating = FloatField(min_value=0, max_value=10, required=False)
    star_category = IntegerField(min_value=0, required=False)
    distance_to_the_airport = IntegerField(min_value=0, required=False)
    tour_operator = CharField(required=False)
    validators = [StartDateValidator()]
