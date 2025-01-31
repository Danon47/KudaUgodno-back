from rest_framework import serializers
from hotels.models.hotel.models_hotel import Hotel
from hotels.serializers.hotel.serializers_hotel_amenity import HotelAmenityCommonSerializer, \
    HotelAmenityInTheRoomSerializer, HotelAmenitySportsAndRecreationSerializer, HotelAmenityForChildrenSerializer
from hotels.serializers.hotel.serializers_hotel_photo import HotelPhotoSerializer
from hotels.serializers.hotel.serializers_hotel_rules import HotelRulesSerializer
from hotels.serializers.room.serializers_room import RoomDetailSerializer


class HotelBaseSerializer(serializers.ModelSerializer):
    user_rating = serializers.FloatField(required=False)
    amenities_common = HotelAmenityCommonSerializer(many=True)
    amenities_in_the_room = HotelAmenityInTheRoomSerializer(many=True)
    amenities_sports_and_recreation = HotelAmenitySportsAndRecreationSerializer(many=True)
    amenities_for_children = HotelAmenityForChildrenSerializer(many=True)
    rules = HotelRulesSerializer(many=True)

    class Meta:
        model = Hotel
        fields = (
            "id",
            "name",
            "star_category",
            "place",
            "country",
            "city",
            "address",
            "distance_to_the_station",
            "distance_to_the_sea",
            "distance_to_the_center",
            "distance_to_the_metro",
            "distance_to_the_airport",
            "description",
            "check_in_time",
            "check_out_time",
            "amenities_common",
            "amenities_in_the_room",
            "amenities_sports_and_recreation",
            "amenities_for_children",
            "type_of_meals_ultra_all_inclusive",
            "type_of_meals_all_inclusive",
            "type_of_meals_full_board",
            "type_of_meals_half_board",
            "type_of_meals_only_breakfast",
            "user_rating",
            "type_of_rest",
            "rules",
        )


class HotelDetailSerializer(HotelBaseSerializer):
    rooms = RoomDetailSerializer(many=True, read_only=True,)
    photo = HotelPhotoSerializer(source="hotel_photos", many=True, read_only=True)
    user_rating = serializers.FloatField(read_only=True,)

    class Meta:
        model = Hotel
        fields = HotelBaseSerializer.Meta.fields + ("rooms", "photo",)
