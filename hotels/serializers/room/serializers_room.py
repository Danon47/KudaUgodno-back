from rest_framework import serializers

from hotels.models.room.date.models_room_date import RoomDate
from hotels.models.room.models_room import Room
from hotels.serializers.hotel.type_of_meals.serializers_type_of_meals import TypeOfMealSerializer
from hotels.serializers.room.date.serializers_room_date import RoomDateDetailSerializer
from hotels.serializers.room.photo.serializers_room_photo import RoomPhotoSerializer
from hotels.serializers.room.rules.serializers_room_rules import RoomRulesSerializer


class RoomBaseSerializer(serializers.ModelSerializer):
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


class RoomDetailSerializer(RoomBaseSerializer):
    """
    Сериалиазатор для вывода детальной информации о номере.
    """

    photo = RoomPhotoSerializer(
        source="room_photos",
        many=True,
        read_only=True,
    )
    date = serializers.SerializerMethodField()
    type_of_meals = TypeOfMealSerializer(many=True)
    rules = RoomRulesSerializer(many=True)

    class Meta(RoomBaseSerializer.Meta):
        model = Room
        fields = RoomBaseSerializer.Meta.fields + (
            "date",
            "photo",
        )

    def get_date(self, obj: RoomDate) -> list:
        """
        Получает список объектов RoomDate связанных с номером.
        Этот метод фильтрует объекты RoomDate, связанные с указанным номером, по его категориям, обеспечивая
        уникальность и упорядочивая их по дате начала.
        Затем он сериализует список с помощью RoomDateSerializer.
        Аргументы:
            obj (Room): Экземпляр номера, для которого извлекаются даты.
        Returns:
            list: Список сериализованных объектов RoomDate.
        """
        room_dates = RoomDate.objects.filter(categories__room=obj).distinct().order_by("start_date")
        return RoomDateDetailSerializer(room_dates, many=True, context={"room": obj}).data
