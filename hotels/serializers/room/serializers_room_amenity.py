# from rest_framework import serializers
# from hotels.models.room.models_room_amenity import (RoomAmenityCommon, RoomAmenityBathroom,
#                                                     RoomAmenityView, RoomAmenityCoffeeStation)
#
#
# class RoomAmenityCommonSerializer(serializers.ModelSerializer):
#     """Сериализатор Удобств для номера"""
#
#     class Meta:
#         model = RoomAmenityCommon
#         fields = ("id", "name",)
#
#
# class RoomAmenityBathroomSerializer(serializers.ModelSerializer):
#     """Сериализатор Удобств для номера"""
#
#     class Meta:
#         model = RoomAmenityBathroom
#         fields = ("id", "name",)
#
#
# class RoomAmenityViewSerializer(serializers.ModelSerializer):
#     """Сериализатор Удобств для номера"""
#
#     class Meta:
#         model = RoomAmenityView
#         fields = ("id", "name",)
#
#
# class RoomAmenityCoffeeStationSerializer(serializers.ModelSerializer):
#     """Сериализатор Удобств для номера"""
#
#     class Meta:
#         model = RoomAmenityCoffeeStation
#         fields = ("id", "name",)
