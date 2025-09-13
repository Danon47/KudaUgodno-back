from decimal import Decimal

from drf_spectacular.utils import extend_schema_field
from rest_framework.serializers import (
    CharField,
    DateField,
    DecimalField,
    FloatField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    SlugRelatedField,
)

from all_fixture.errors.list_error import (
    DECIMAL_ERROR,
    MIN_ERROR,
    TOUR_MAX_PRICE_ERROR,
)
from all_fixture.errors.serializers_error import (
    FLIGHT_FROM_ERROR_MESSAGES,
    FLIGHT_TO_ERROR_MESSAGES,
    HOTEL_ERROR_MESSAGES,
    ROOMS_ERROR_MESSAGES,
    TOUROPERATOR_ERROR_MESSAGES,
    TYPE_OF_MEALS_ERROR_MESSAGES,
)
from all_fixture.serializers.const import DATE_FIELD_SETTINGS, TOUR_FIELDS
from flights.serializers import FlightSerializer
from hotels.serializers import HotelListWithPhotoSerializer, HotelShortSerializer
from hotels.serializers_type_of_meals import TypeOfMealSerializer
from rooms.serializers import RoomDetailSerializer
from tours.models import Tour
from tours.validators import EndDateValidator, PriceValidator, StartDateValidator


class PriceFieldsMixin:
    """
    Миксин для стоимостей в туре.
    """

    total_price = DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text="Итоговая стоимость тура",
        min_value=Decimal("0.00"),
        max_value=Decimal("99999999.00"),
        error_messages={
            "min_value": MIN_ERROR,
            "max_value": TOUR_MAX_PRICE_ERROR,
            "invalid": DECIMAL_ERROR,
        },
        default=Decimal("150000.00"),
    )
    discount_amount = DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text="Величина скидки",
        min_value=Decimal("0.00"),
        max_value=Decimal("99999999.00"),
        error_messages={
            "min_value": MIN_ERROR,
            "max_value": TOUR_MAX_PRICE_ERROR,
            "invalid": DECIMAL_ERROR,
        },
        default=Decimal("5000.00"),
    )
    markup_amount = DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        help_text="Наценка на тур",
        min_value=Decimal("0.00"),
        max_value=Decimal("99999999.00"),
        error_messages={
            "min_value": MIN_ERROR,
            "max_value": TOUR_MAX_PRICE_ERROR,
            "invalid": DECIMAL_ERROR,
        },
        default=Decimal("20000.00"),
    )


class DateFieldsMixin:
    """
    Миксин дат в туре.
    """

    start_date = DateField(**DATE_FIELD_SETTINGS)
    end_date = DateField(**DATE_FIELD_SETTINGS)
    discount_start_date = DateField(**DATE_FIELD_SETTINGS)
    discount_end_date = DateField(**DATE_FIELD_SETTINGS)
    publish_start_date = DateField(**DATE_FIELD_SETTINGS)
    publish_end_date = DateField(**DATE_FIELD_SETTINGS)


class AbstractTourSerializer(ModelSerializer):
    """
    Абстрактный сериализатор для модели Тура.
    Содержит в себе модель Тура, валидаторы по датам и стоимостям.
    """

    class Meta:
        abstract = True
        model = Tour
        validators = [
            StartDateValidator(),
            EndDateValidator(),
            PriceValidator(),
        ]
        read_only_fields = (
            "created_at",
            "updated_at",
        )


class TourSerializer(PriceFieldsMixin, DateFieldsMixin, AbstractTourSerializer):
    """
    Сериализатор для модели Tour, для ручек.
    POST, PUT.
    Создание, Обновление.
    """

    class Meta(AbstractTourSerializer.Meta):
        fields = TOUR_FIELDS
        extra_kwargs = {
            "flight_to": {"error_messages": FLIGHT_TO_ERROR_MESSAGES},
            "flight_from": {"error_messages": FLIGHT_FROM_ERROR_MESSAGES},
            "tour_operator": {"error_messages": TOUROPERATOR_ERROR_MESSAGES},
            "hotel": {"error_messages": HOTEL_ERROR_MESSAGES},
            "rooms": {"error_messages": ROOMS_ERROR_MESSAGES},
            "type_of_meals": {"error_messages": TYPE_OF_MEALS_ERROR_MESSAGES},
        }


class TourPatchSerializer(AbstractTourSerializer):
    """
    Сериализатор для модели Tour, для единственного действия - ставить тур в архив, и убирать его из архива.
    PATCH.
    Частичное обновление.
    """

    class Meta(AbstractTourSerializer.Meta):
        fields = ("is_active",)


class TourListSerializer(PriceFieldsMixin, DateFieldsMixin, AbstractTourSerializer):
    """
    Сериализатор для модели Tour.
    GET(RETRIEVE).
    Детальная информация о туре.
    """

    hotel = HotelListWithPhotoSerializer(read_only=True)
    flight_to = FlightSerializer(read_only=True)
    flight_from = FlightSerializer(read_only=True)
    rooms = RoomDetailSerializer(many=True, read_only=True)
    type_of_meals = TypeOfMealSerializer(many=True, read_only=True)
    tour_operator = SlugRelatedField(slug_field="company_name", read_only=True)

    class Meta(AbstractTourSerializer.Meta):
        fields = TOUR_FIELDS


class TourPopularSerializer(PriceFieldsMixin, AbstractTourSerializer):
    """
    Сериализатор для списка популярных туров.
    GET
    """

    photo = SerializerMethodField()
    tours_count = IntegerField(
        min_value=0,
        required=True,
    )

    class Meta(AbstractTourSerializer.Meta):
        fields = (
            "arrival_country",
            "photo",
            "total_price",
            "tours_count",
        )

    def get_photo(self, obj) -> str:
        """
        Возвращает URL первой фотографии отеля.
        """
        request = self.context.get("request")
        first_photo = obj.hotel.hotel_photos.first()
        if first_photo:
            return request.build_absolute_uri(first_photo.photo.url) if request else first_photo.photo.url
        return None


class TourShortSerializer(PriceFieldsMixin, DateFieldsMixin, AbstractTourSerializer):
    """
    Общий сокращённый сериализатор Тура.
    GET.
    """

    number_of_adults = IntegerField(
        min_value=1,
    )
    number_of_children = IntegerField(
        min_value=0,
    )
    hotel = HotelShortSerializer(read_only=True)
    tour_operator = SlugRelatedField(slug_field="company_name", read_only=True)
    total_price_with_discount = DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta(AbstractTourSerializer.Meta):
        fields = (
            "id",
            "hotel",
            "number_of_adults",
            "number_of_children",
            "publish_start_date",
            "publish_end_date",
            "tour_operator",
            "total_price",
            "total_price_with_discount",
        )

    @extend_schema_field(
        {
            "type": "string",
            "format": "string",
            "example": {
                "number_of_adults": 2,
                "number_of_children": 1,
            },
        }
    )
    def get_guests(self, obj: Tour):
        print("Adults:", obj.number_of_adults)
        print("Children:", obj.number_of_children)
        return {
            "number_of_adults": obj.number_of_adults,
            "number_of_children": obj.number_of_children,
        }


class TourShortWithPriceSerializer(TourShortSerializer):
    total_price_with_discount = DecimalField(
        max_digits=10,
        decimal_places=2,
        default="100000.00",
    )

    class Meta:
        model = Tour
        fields = TourShortSerializer.Meta.fields + (
            "id",
            "total_price_with_discount",
        )


class TourFiltersRequestSerializer(Serializer):
    """Сериализатор для параметров расширенного поиска (все поля необязательные)."""

    departure_city = CharField(
        required=False,
    )
    arrival_city = CharField(
        required=False,
    )
    start_date = DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        error_messages={"invalid": "Некорректный формат даты. Используйте YYYY-MM-DD"},
    )
    nights = IntegerField(
        min_value=1,
        required=False,
    )
    guests = IntegerField(
        min_value=1,
        required=False,
    )
    city = CharField(
        required=False,
    )
    type_of_rest = CharField(
        required=False,
    )
    place = CharField(
        required=False,
    )
    price_gte = IntegerField(
        min_value=0,
        required=False,
    )
    price_lte = IntegerField(
        min_value=0,
        required=False,
    )
    user_rating = FloatField(
        min_value=0,
        max_value=10,
        required=False,
    )
    star_category = IntegerField(
        min_value=0,
        max_value=5,
        required=False,
    )
    distance_to_the_airport = IntegerField(
        min_value=0,
        required=False,
    )
    tour_operator = CharField(
        required=False,
    )
    validators = [
        StartDateValidator(),
    ]
