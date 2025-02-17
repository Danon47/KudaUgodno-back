from rest_framework import serializers
from hotels.models.room.models_room import Room
from hotels.models.room.models_room_discount import RoomDiscount
from hotels.models.room.models_room_unavailable import RoomUnavailable
from hotels.serializers.room.serializers_room_discount import RoomDiscountSerializer
from hotels.serializers.room.serializers_room_photo import RoomPhotoSerializer
from hotels.serializers.room.serializers_room_unavaliable import (
    RoomUnavailableSerializer,
)


class RoomBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор номера"""

    discount = RoomDiscountSerializer(many=True, required=False)
    unavailable = RoomUnavailableSerializer(many=True, required=False)

    class Meta:
        model = Room
        fields = (
            "id",
            "category",
            "price",
            "type_of_meals",
            "number_of_adults",
            "number_of_children",
            "single_bed",
            "double_bed",
            "area",
            "quantity_rooms",
            "discount",
            "unavailable",
            "amenities_common",
            "amenities_coffee",
            "amenities_bathroom",
            "amenities_view",
        )

    def create(self, validated_data):
        discount_data = validated_data.pop('discount', [])
        unavailable_data = validated_data.pop('unavailable', [])

        room = Room.objects.create(**validated_data)

        # Создаем связанные объекты, но добавляем через ManyToManyField
        discount_objs = [RoomDiscount.objects.create(**item) for item in discount_data]
        unavailable_objs = [RoomUnavailable.objects.create(**item) for item in unavailable_data]

        room.discount.set(discount_objs)
        room.unavailable.set(unavailable_objs)

        return room

    def update(self, instance, validated_data):
        discount_data = validated_data.pop('discount', None)
        unavailable_data = validated_data.pop('unavailable', None)

        instance = super().update(instance, validated_data)

        if discount_data is not None:
            instance.discount.clear()
            discount_objs = [RoomDiscount.objects.create(**item) for item in discount_data]
            instance.discount.set(discount_objs)

        if unavailable_data is not None:
            instance.unavailable.clear()
            unavailable_objs = [RoomUnavailable.objects.create(**item) for item in unavailable_data]
            instance.unavailable.set(unavailable_objs)

        return instance


class RoomDetailSerializer(RoomBaseSerializer):
    photo = RoomPhotoSerializer(
        source="room_photos",
        many=True,
        read_only=True,
    )

    class Meta(RoomBaseSerializer.Meta):
        model = Room
        fields = RoomBaseSerializer.Meta.fields + ("photo",)
