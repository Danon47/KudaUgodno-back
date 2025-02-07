from rest_framework import serializers
from hotels.models.hotel.models_hotel_amenity import (
    HotelAmenityCommon,
    HotelAmenityForChildren,
    HotelAmenitySportsAndRecreation,
    HotelAmenityInTheRoom,
)


class HotelAmenityCommonSerializer(serializers.ModelSerializer):
    """Сериализатор Удобств для отеля"""

    name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = HotelAmenityCommon
        fields = ("name",)


class HotelAmenityRoomSerializer(serializers.ModelSerializer):
    """Сериализатор Удобств для отеля"""

    name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = HotelAmenityInTheRoom
        fields = ("name",)


class HotelAmenitySportsSerializer(serializers.ModelSerializer):
    """Сериализатор Удобств для отеля"""

    name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = HotelAmenitySportsAndRecreation
        fields = ("name",)


class HotelAmenityChildrenSerializer(serializers.ModelSerializer):
    """Сериализатор Удобств для отеля"""

    name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = HotelAmenityForChildren
        fields = ("name",)
