from rest_framework import serializers
from .models import Hotel, HotelRoom, AmenityRoom, AmenityHotel, PlaceHotel


class AmenityRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityRoom
        fields = ["id", "name"]


class AmenityHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityHotel
        fields = ["id", "name"]


class HotelRoomSerializer(serializers.ModelSerializer):
    amenities = serializers.PrimaryKeyRelatedField(queryset=AmenityRoom.objects.all(), many=True, write_only=True)
    amenities_room = AmenityRoomSerializer(source="amenities", many=True, read_only=True)

    class Meta:

        model = HotelRoom
        fields = "__all__"


class PlaceHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceHotel
        fields = ["id", "name"]


class HotelSerializer(serializers.ModelSerializer):
    amenities = serializers.PrimaryKeyRelatedField(queryset=AmenityHotel.objects.all(), many=True, write_only=True)
    amenities_hotel = AmenityHotelSerializer(source="amenities", many=True, read_only=True)
    place = serializers.PrimaryKeyRelatedField(queryset=PlaceHotel.objects.all(), many=False, write_only=True)
    place_hotel = PlaceHotelSerializer(source="place", many=False, read_only=True)
    hotel_room = HotelRoomSerializer(many=True, read_only=True)

    class Meta:
        model = Hotel
        fields = "__all__"
