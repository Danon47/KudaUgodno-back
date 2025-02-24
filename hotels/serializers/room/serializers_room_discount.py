from rest_framework import serializers

from hotels.models.room.models_room_discount import RoomDiscount


class RoomDiscountSerializer(serializers.ModelSerializer):
    """Сериализатор модели скидок"""

    class Meta:
        model = RoomDiscount
        fields = "__all__"
