from rest_framework import serializers
from .models import Hotel, HotelRoom, AmenityRoom, AmenityHotel, PlaceHotel


class AmenityRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityRoom
        fields = ["id", "name"]


class HotelRoomSerializer(serializers.ModelSerializer):
    amenities = AmenityRoomSerializer(many=True)

    class Meta:
        model = HotelRoom
        fields = "__all__"


class AmenityHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityHotel
        fields = ["id", "name"]

class PlaceHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceHotel
        fields = ["id", "name"]


class HotelSerializer(serializers.ModelSerializer):
    amenities = AmenityHotelSerializer(many=True, read_only=True)
    place = PlaceHotelSerializer(many=True, read_only=True)
    hotel_room = HotelRoomSerializer(many=True, read_only=True)


    class Meta:
        model = Hotel
        fields = "__all__"
