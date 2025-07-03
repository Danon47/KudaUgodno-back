from decimal import Decimal
from typing import Any

from drf_spectacular.utils import extend_schema_field
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ImageField, ModelSerializer

from all_fixture.errors.list_error import TYPE_OF_MEAL_ERROR
from calendars.models import CalendarDate, CalendarPrice
from hotels.serializers_type_of_meals import TypeOfMealSerializer
from rooms.models import Room, RoomPhoto, RoomRules


class RoomPhotoSerializer(ModelSerializer):
    """
    Сериализатор фотографий номера.
    """

    photo = ImageField()

    class Meta:
        model = RoomPhoto
        fields = ("id", "photo", "room")
        read_only_fields = ("id", "room")


class RoomRulesSerializer(ModelSerializer):
    """
    Сериализатор правил в номере.
    """

    class Meta:
        model = RoomRules
        fields = ("name", "option")


class RoomBaseSerializer(ModelSerializer):
    """
    Базовый сериализатор номера.
    """

    rules = RoomRulesSerializer(many=True)

    class Meta:
        model = Room
        fields = (
            "id",
            "category",
            "type_of_meals",
            "number_of_adults",
            "number_of_children",
            "single_bed",
            "double_bed",
            "area",
            "quantity_rooms",
            "amenities_common",
            "amenities_coffee",
            "amenities_bathroom",
            "amenities_view",
            "rules",
        )
        extra_kwargs = {
            "type_of_meals": {
                "error_messages": {
                    "does_not_exist": TYPE_OF_MEAL_ERROR,
                    "invalid": "Неверный формат ID типа питания. Ожидается положительное число.",
                    "null": "ID рейса туда не может быть пустым.",
                    "blank": "ID рейса туда не может быть пустым.",
                }
            }
        }


class RoomCalendarDateSerializer(ModelSerializer):
    price = SerializerMethodField()

    class Meta:
        model = CalendarDate
        fields = (
            "id",
            "start_date",
            "end_date",
            "available_for_booking",
            "discount",
            "discount_amount",
            "price",
        )

    def get_price(self, obj: CalendarDate) -> Decimal | None:
        room = self.context.get("room")
        if not room:
            return None

        try:
            calendar_price = obj.calendar_prices.get(room=room)
            return calendar_price.price
        except CalendarPrice.DoesNotExist:
            return None


class RoomDetailSerializer(RoomBaseSerializer):
    """
    Сериалиазатор для вывода детальной информации о номере.
    """

    calendar_dates = SerializerMethodField(
        read_only=True,
    )
    photo = RoomPhotoSerializer(
        source="room_photos",
        many=True,
        read_only=True,
    )
    type_of_meals = TypeOfMealSerializer(
        many=True,
        read_only=True,
    )
    rules = RoomRulesSerializer(
        many=True,
        read_only=True,
    )

    class Meta(RoomBaseSerializer.Meta):
        model = Room
        fields = RoomBaseSerializer.Meta.fields + (
            "photo",
            "calendar_dates",
        )

    @extend_schema_field(
        {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "format": "int64"},
                    "start_date": {"type": "string", "format": "date"},
                    "end_date": {"type": "string", "format": "date"},
                    "available_for_booking": {"type": "boolean"},
                    "discount": {"type": "boolean"},
                    "discount_amount": {
                        "type": "integer",
                        "format": "decimal",
                        "nullable": True,
                    },
                    "price": {"type": "integer", "format": "decimal"},
                },
            },
        }
    )
    def get_calendar_dates(self, obj: Room) -> list[dict[str, Any]]:
        calendar_dates = obj.calendar_dates.all().order_by("start_date").distinct()
        context = self.context.copy()
        context["room"] = obj
        serializer = RoomCalendarDateSerializer(calendar_dates, many=True, context=context)
        return serializer.data
