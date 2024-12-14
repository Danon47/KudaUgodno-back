from rest_framework import serializers
from .models import (
    Hotel,
    Room,
    AmenityRoom,
    AmenityHotel,
    CategoryRoom,
)


class AmenityRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityRoom
        fields = ("id", "name")


class AmenityHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityHotel
        fields = ("id", "name")


class CategoryRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRoom
        fields = ("id", "name",)


class RoomSerializer(serializers.ModelSerializer):
    amenities = serializers.PrimaryKeyRelatedField(queryset=AmenityRoom.objects.all(), many=True, write_only=True)
    amenities_room = AmenityRoomSerializer(source="amenities", many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryRoom.objects.all(), many=False, write_only=True)
    category_hotel = CategoryRoomSerializer(source="category", many=False, read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


class HotelSerializer(serializers.ModelSerializer):
    amenities = serializers.PrimaryKeyRelatedField(queryset=AmenityHotel.objects.all(), many=True, write_only=True)
    amenities_hotel = AmenityHotelSerializer(source="amenities", many=True, read_only=True)
    hotel_room = RoomSerializer(many=True, read_only=True)
    user_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Hotel
        fields = "__all__"
