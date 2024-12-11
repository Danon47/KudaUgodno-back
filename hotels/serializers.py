from rest_framework import serializers
from .models import Hotel, HotelRoom, AmenityRoom, AmenityHotel


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"


class HotelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoom
        fields = "__all__"


class AmenityRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityRoom
        fields = "__all__"


class AmenityHotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmenityHotel
        fields = "__all__"
