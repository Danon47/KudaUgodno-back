from django.db import models
from rest_framework import serializers
from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_amenity import (
    HotelAmenityCommon,
    HotelAmenityInTheRoom,
    HotelAmenitySportsAndRecreation,
    HotelAmenityForChildren,
)
from hotels.models.hotel.models_hotel_rules import HotelRules
# from hotels.serializers.hotel.serializers_hotel_amenity import (
#     HotelAmenityCommonSerializer,
#     HotelAmenityRoomSerializer,
#     HotelAmenitySportsSerializer,
#     HotelAmenityChildrenSerializer,
# )
from hotels.serializers.hotel.serializers_hotel_photo import HotelPhotoSerializer
from hotels.serializers.hotel.serializers_hotel_rules import HotelRulesSerializer
from hotels.serializers.room.serializers_room import RoomDetailSerializer


class HotelBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = (
            "id",
            "name",
        )

    def create(self, validated_data):
        return Hotel.objects.create(**validated_data)


class HotelDetailSerializer(serializers.ModelSerializer):
    # amenities_common = HotelAmenityCommonSerializer(
    #     many=True,
    # )
    # amenities_in_the_room = HotelAmenityRoomSerializer(
    #     many=True,
    # )
    # amenities_sports_and_recreation = HotelAmenitySportsSerializer(
    #     many=True,
    # )
    # amenities_for_children = HotelAmenityChildrenSerializer(
    #     many=True,
    # )
    rules = HotelRulesSerializer(many=True, source="hotels_rules")
    user_rating = serializers.FloatField()

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
            "is_active",
            "room_categories",
        )

    # def update(self, instance, validated_data):
    #     # Обновляем связанные поля, используя корректные ключи
    #     self._update_related_field(
    #         instance, validated_data, "amenities_common", HotelAmenityCommon
    #     )
    #     self._update_related_field(
    #         instance, validated_data, "amenities_in_the_room", HotelAmenityInTheRoom
    #     )
    #     self._update_related_field(
    #         instance,
    #         validated_data,
    #         "amenities_sports_and_recreation",
    #         HotelAmenitySportsAndRecreation,
    #     )
    #     self._update_related_field(
    #         instance, validated_data, "amenities_for_children", HotelAmenityForChildren
    #     )
    #     self._update_related_field(instance, validated_data, "rules", HotelRules)
    #
    #     # Обновляем остальные поля (только те, которые не являются связанными)
    #     for attr, value in validated_data.items():
    #         # Опционально: проверить, является ли поле ManyToMany
    #         try:
    #             field = instance._meta.get_field(attr)
    #             if isinstance(field, models.ManyToManyField):
    #                 # Если это ManyToManyField, то пропускаем его, т.к. он уже обработан
    #                 continue
    #         except Exception:
    #             # Если поле не найдено в модели – пропускаем
    #             continue
    #         setattr(instance, attr, value)
    #
    #     instance.save()
    #     return instance
    #
    # def _update_related_field(self, instance, validated_data, field_name, model):
    #     """
    #     Обновляет ManyToMany или обратные отношения (для правил) с использованием .set()
    #     """
    #     if field_name in validated_data:
    #         items_data = validated_data.pop(field_name)
    #         items = []
    #         for item_data in items_data:
    #             # Создаем или получаем связанный объект с учетом отеля
    #             item, _ = model.objects.get_or_create(hotel=instance, **item_data)
    #             items.append(item)
    #         # Обновляем поле через менеджер
    #         getattr(instance, field_name).set(items)


class HotelListSerializer(HotelDetailSerializer):
    photo = HotelPhotoSerializer(
        source="hotel_photos",
        many=True,
        read_only=True,
    )
    rooms = RoomDetailSerializer(
        many=True,
        read_only=True,
    )
    # created_by = serializers.SerializerMethodField()

    class Meta(HotelDetailSerializer.Meta):
        fields = HotelDetailSerializer.Meta.fields + (
            "photo",
            "rooms",
            # "created_by",
        )

    # def get_created_by(self, obj):
    #     # Например, возвращаем email пользователя
    #     return obj.created_by.email if obj.created_by else None
