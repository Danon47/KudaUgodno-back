from rest_framework import serializers
from hotels.models.room.models_room import Room
from hotels.models.room.models_room_amenity import (
    RoomAmenityCommon,
    RoomAmenityCoffeeStation,
    RoomAmenityBathroom,
    RoomAmenityView,
)
# from hotels.models.room.models_room_category import RoomCategory
from hotels.serializers.room.serializers_room_discount import RoomDiscountSerializer
# from hotels.serializers.room.serializers_room_amenity import (
#     RoomAmenityCommonSerializer,
#     RoomAmenityViewSerializer,
#     RoomAmenityBathroomSerializer,
#     RoomAmenityCoffeeStationSerializer,
# )
from hotels.serializers.room.serializers_room_photo import RoomPhotoSerializer
from hotels.serializers.room.serializers_room_unavaliable import RoomUnavailableSerializer


class RoomBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор номера"""

    # amenities_common = RoomAmenityCommonSerializer(many=True, required=False)
    # amenities_coffee_station = RoomAmenityCoffeeStationSerializer(many=True, required=False)
    # amenities_bathroom = RoomAmenityBathroomSerializer(many=True, required=False)
    # amenities_view = RoomAmenityViewSerializer(many=True, required=False)
    discount = RoomDiscountSerializer(many=True, required=False)
    unavailable = RoomUnavailableSerializer(many=True, required=False)

    class Meta:
        model = Room
        fields = (
            "id",
            "category",
            "price",
            "type_of_meals",
            "number_of_adults",
            "number_of_children",
            "single_bed",
            "double_bed",
            "area",
            "quantity_rooms",
            "discount",
            "unavailable",
            "amenities_common",
            "amenities_coffee",
            "amenities_bathroom",
            "amenities_view",
        )

    # def create(self, validated_data):
        # Извлекаем вложенные данные
        # amenities_common_data = validated_data.pop("amenities_common", [])
        # amenities_coffee_station_data = validated_data.pop("amenities_coffee_station", [])
        # amenities_bathroom_data = validated_data.pop("amenities_bathroom", [])
        # amenities_view_data = validated_data.pop("amenities_view", [])

        # # Передача имени категории
        # category_name = validated_data.pop("category")
        # category_instance, created = RoomCategory.objects.get_or_create(
        #     name=category_name
        # )
        #
        # # Создаем объект Room
        # room = Room.objects.create(category=category_instance, **validated_data)
        # room.save()

        # # Создаем связанные объекты общих удобств
        # for amenity_data in amenities_common_data:
        #     amenities_common, created = RoomAmenityCommon.objects.get_or_create(
        #         name=amenity_data.get("name")
        #     )
        #     room.amenities.add(amenities_common)
        #
        # # Создаем связанные объекты удобства кофе станции
        # for amenity_data in amenities_coffee_station_data:
        #     amenities_coffee_station, created = RoomAmenityCoffeeStation.objects.get_or_create(
        #         name=amenity_data.get("name")
        #     )
        #     room.amenities.add(amenities_coffee_station)
        #
        # # Создаем связанные объекты удобства ванной комнаты
        # for amenity_data in amenities_bathroom_data:
        #     amenities_bathroom, created = RoomAmenityBathroom.objects.get_or_create(
        #         name=amenity_data.get("name")
        #     )
        #     room.amenities.add(amenities_bathroom)
        #
        # # Создаем связанные объекты удобства вид
        # for amenity_data in amenities_view_data:
        #     amenities_view, created = RoomAmenityView.objects.get_or_create(
        #         name=amenity_data.get("name")
        #     )
        #     room.amenities.add(amenities_view)
        # return room

    # def update(self, instance, validated_data):
        # Извлекаем вложенные данные
        # amenities_common_data = validated_data.pop("amenities_common", [])
        # amenities_coffee_station_data = validated_data.pop("amenities_coffee_station", [])
        # amenities_bathroom_data = validated_data.pop("amenities_bathroom", [])
        # amenities_view_data = validated_data.pop("amenities_view", [])

        # # Обновляем категорию
        # category_name = validated_data.pop("category")
        # category_instance, created = RoomCategory.objects.get_or_create(
        #     name=category_name
        # )
        # instance.category = category_instance
        #
        # # Обновляем остальные поля
        # for attr, value in validated_data.items():
        #     setattr(instance, attr, value)
        # instance.save()

        # # Обновляем связанные объекты amenities
        # instance.amenities.clear()  # Удаляем все существующие удобства
        # for amenity_data in amenities_common_data:
        #     amenity, created = RoomAmenityCommon.objects.get_or_create(
        #         name=amenity_data.get("name")
        #     )
        #     instance.amenities.add(amenity)
        #
        # for amenity_data in amenities_coffee_station_data:
        #     amenity, created = RoomAmenityCoffeeStation.objects.get_or_create(
        #         name=amenity_data.get("name")
        #     )
        #     instance.amenities.add(amenity)
        #
        # for amenity_data in amenities_bathroom_data:
        #     amenity, created = RoomAmenityBathroom.objects.get_or_create(
        #         name=amenity_data.get("name")
        #     )
        #     instance.amenities.add(amenity)
        #
        # for amenity_data in amenities_view_data:
        #     amenity, created = RoomAmenityView.objects.get_or_create(
        #         name=amenity_data.get("name")
        #     )
        #     instance.amenities.add(amenity)
        #
        # return instance

class RoomDetailSerializer(RoomBaseSerializer):
    photo = RoomPhotoSerializer(
        source="room_photos",
        many=True,
        read_only=True,
    )

    class Meta(RoomBaseSerializer.Meta):
        model = Room
        fields = RoomBaseSerializer.Meta.fields + ("photo",)
