from rest_framework import serializers
from hotels.models.room.models_room_category import RoomCategory


class CategoryRoomSerializer(serializers.ModelSerializer):
    """Категория номера"""

    class Meta:
        model = RoomCategory
        fields = ("name",)
