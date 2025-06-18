from decimal import Decimal
from typing import Any, Dict, List

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ImageField, ModelSerializer

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
    type_of_meals = TypeOfMealSerializer(many=True, read_only=True)
    rules = RoomRulesSerializer(many=True, read_only=True)

    class Meta(RoomBaseSerializer.Meta):
        model = Room
        fields = RoomBaseSerializer.Meta.fields + (
            "photo",
            "calendar_dates",
        )

    def get_calendar_dates(self, obj: Room) -> List[Dict[str, Any]]:
        calendar_dates = obj.calendar_dates.all().order_by("start_date").distinct()
        context = self.context.copy()
        context["room"] = obj
        serializer = RoomCalendarDateSerializer(calendar_dates, many=True, context=context)
        return serializer.data
