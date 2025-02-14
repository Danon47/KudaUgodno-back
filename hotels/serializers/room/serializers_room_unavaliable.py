from rest_framework import serializers
from hotels.models.room.models_room_unavailable import RoomUnavailable


class RoomUnavailableSerializer(serializers.ModelSerializer):
    """Сериализатор причин запрета на бронь"""

    class Meta:
        model = RoomUnavailable
        fields = "__all__"