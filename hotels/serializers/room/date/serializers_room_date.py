from rest_framework import serializers

from hotels.models.room.date.models_room_date import RoomCategory, RoomDate


class RoomCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор категорий номеров в отеле и их стоимость
    """

    class Meta:
        model = RoomCategory
        fields = ("id", "room", "price")


class RoomDateSerializer(serializers.ModelSerializer):
    """
    Сериализатор дат для номеров
    """

    categories = RoomCategorySerializer(many=True)

    class Meta:
        model = RoomDate
        fields = (
            "id",
            "start_date",
            "end_date",
            "available_for_booking",
            "stock",
            "share_size",
            "categories",
        )
