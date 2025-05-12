from rest_framework import serializers

from hotels.models.room.date.models_room_date import RoomDate
from hotels.models.room.models_room import Room
from hotels.serializers.hotel.type_of_meals.serializers_type_of_meals import TypeOfMealSerializer
from hotels.serializers.room.date.serializers_room_date import RoomDateSerializer
from hotels.serializers.room.photo.serializers_room_photo import RoomPhotoSerializer


class RoomBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор номера"""

    type_of_meals = TypeOfMealSerializer(many=True)

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
            # "discount",
            # "unavailable",
            "amenities_common",
            "amenities_coffee",
            "amenities_bathroom",
            "amenities_view",
        )


class RoomDetailSerializer(RoomBaseSerializer):

    photo = RoomPhotoSerializer(
        source="room_photos",
        many=True,
        read_only=True,
    )
    date = serializers.SerializerMethodField()

    class Meta(RoomBaseSerializer.Meta):
        model = Room
        fields = RoomBaseSerializer.Meta.fields + (
            "date",
            "photo",
        )

    def get_date(self, obj):
        """Получение всех RoomDate, связанных с этим Room через RoomCategory"""
        # сначала идёт RoomDate, потом RoomCategory
        room_dates = RoomDate.objects.filter(categories__room=obj).distinct()
        return RoomDateSerializer(room_dates, many=True).data
