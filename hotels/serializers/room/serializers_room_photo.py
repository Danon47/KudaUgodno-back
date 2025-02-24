from rest_framework import serializers

from hotels.models.room.models_room_photo import RoomPhoto


class RoomPhotoSerializer(serializers.ModelSerializer):
    """Сериализатор фотографий номера"""

    photo = serializers.ImageField()

    class Meta:
        model = RoomPhoto
        fields = "__all__"
        read_only_fields = (
            "id",
            "room",
        )
