from rest_framework import serializers
from .models import (
    Hotel,
    Room,
    RoomAmenity,
    HotelAmenity,
    RoomCategory,
    RoomPhoto,
    HotelPhoto,
)


class AmenityRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAmenity
        fields = ("id", "name")


class AmenityHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelAmenity
        fields = ("id", "name")


class CategoryRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomCategory
        fields = ("id", "name",)


class RoomPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomPhoto
        fields = ("id", "photo")


class HotelPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelPhoto
        fields = ("id", "photo")


class RoomSerializer(serializers.ModelSerializer):
    amenities = AmenityRoomSerializer(many=True, read_only=True)
    category = CategoryRoomSerializer(many=False, read_only=True)
    photos = RoomPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = (
            "id",
            "category",
            "food",
            "type_of_holiday",
            "smoking",
            "pet",
            "area",
            "amenities",
            "capacity",
            "single_bed",
            "double_bed",
            "nightly_price",
            "photos",
        )


class HotelSerializer(serializers.ModelSerializer):
    amenities = AmenityHotelSerializer(many=True, read_only=True)
    rooms = RoomSerializer(source="room", many=True, read_only=True)
    photos = HotelPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = (
            "id",
            "name",
            "star_category",
            "place",
            "amenities",
            "country",
            "city",
            "address",
            "distance_to_sea",
            "distance_to_airport",
            "description",
            "rooms",
            "user_rating",
            "check_in_time",
            "check_out_time",
            "photos",
        )
