from rest_framework import serializers
from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_amenity import (
    HotelAmenityCommon,
    HotelAmenityInTheRoom,
    HotelAmenitySportsAndRecreation,
    HotelAmenityForChildren,
)
from hotels.models.hotel.models_hotel_rules import HotelRules
from hotels.serializers.hotel.serializers_hotel_amenity import (
    HotelAmenityCommonSerializer,
    HotelAmenityInTheRoomSerializer,
    HotelAmenitySportsAndRecreationSerializer,
    HotelAmenityForChildrenSerializer,
)
from hotels.serializers.hotel.serializers_hotel_photo import HotelPhotoSerializer
from hotels.serializers.hotel.serializers_hotel_rules import HotelRulesSerializer
from hotels.serializers.room.serializers_room import RoomDetailSerializer


class HotelBaseSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        amenities_common_data = validated_data.pop("amenities_common", [])
        amenities_in_the_room_data = validated_data.pop("amenities_in_the_room", [])
        amenities_sports_and_recreation_data = validated_data.pop("amenities_sports_and_recreation", [])
        amenities_for_children_data = validated_data.pop("amenities_for_children", [])
        rules_data = validated_data.pop("rules", [])

        hotel = Hotel.objects.create(**validated_data)

        # Создаём связанные объекты
        hotel.amenities_common.set(
            [
                HotelAmenityCommon.objects.get_or_create(**data)[0]
                for data in amenities_common_data
            ]
        )
        hotel.amenities_in_the_room.set(
            [
                HotelAmenityInTheRoom.objects.get_or_create(**data)[0]
                for data in amenities_in_the_room_data
            ]
        )
        hotel.amenities_sports_and_recreation.set(
            [
                HotelAmenitySportsAndRecreation.objects.get_or_create(**data)[0]
                for data in amenities_sports_and_recreation_data
            ]
        )
        hotel.amenities_for_children.set(
            [
                HotelAmenityForChildren.objects.get_or_create(**data)[0]
                for data in amenities_for_children_data
            ]
        )
        hotel.rules.set([HotelRules.objects.get_or_create(**data)[0] for data in rules_data])

        return hotel

    def update(self, instance, validated_data):
        amenities_common_data = validated_data.pop("amenities_common", [])
        amenities_in_the_room_data = validated_data.pop("amenities_in_the_room", [])
        amenities_sports_and_recreation_data = validated_data.pop("amenities_sports_and_recreation", [])
        amenities_for_children_data = validated_data.pop("amenities_for_children", [])
        rules_data = validated_data.pop("rules", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if amenities_common_data:
            instance.amenities_common.clear()
            instance.amenities_common.set(
                [
                    HotelAmenityCommon.objects.get_or_create(**data)[0]
                    for data in amenities_common_data
                ]
            )

        if amenities_in_the_room_data:
            instance.amenities_in_the_room.clear()
            instance.amenities_in_the_room.set(
                [HotelAmenityInTheRoom.objects.get_or_create(**data)[0] for data in amenities_in_the_room_data]
            )

        if amenities_sports_and_recreation_data:
            instance.amenities_sports_and_recreation.clear()
            instance.amenities_sports_and_recreation.set(
                [
                    HotelAmenitySportsAndRecreation.objects.get_or_create(**data)[0]
                    for data in amenities_sports_and_recreation_data
                ]
            )

        if amenities_for_children_data:
            instance.amenities_for_children.clear()
            instance.amenities_for_children.set(
                [
                    HotelAmenityForChildren.objects.get_or_create(**data)[0]
                    for data in amenities_for_children_data
                ]
            )

        if rules_data:
            instance.rules.clear()
            instance.rules.set([HotelRules.objects.get_or_create(**data)[0] for data in rules_data])

        return instance


class HotelDetailSerializer(HotelBaseSerializer):
    rooms = RoomDetailSerializer(many=True,)
    photo = HotelPhotoSerializer(source="hotel_photos", many=True,)

    class Meta:
        model = Hotel
        fields = HotelBaseSerializer.Meta.fields + (
            "rooms",
            "photo",
        )
        read_only_fields = (
            "photo",
            "rooms",
            "amenities_common",
            "amenities_in_the_room",
            "amenities_sports_and_recreation",
            "amenities_for_children",
        )
