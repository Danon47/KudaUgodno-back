from rest_framework import serializers
from hotels.models.room.models_room_amenity import RoomAmenity


class AmenityRoomSerializer(serializers.ModelSerializer):
    """Сериализатор Удобств для номера"""

    class Meta:
        model = RoomAmenity
        fields = ("id", "name",)
