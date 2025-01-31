from rest_framework import serializers
from hotels.models.room.models_room import Room
from hotels.models.room.models_room_amenity import RoomAmenity
from hotels.models.room.models_room_caterogy import RoomCategory
from hotels.serializers.room.serializers_room_amenity import AmenityRoomSerializer
from hotels.serializers.room.serializers_room_photo import RoomPhotoSerializer


class RoomBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор номера"""

    amenities = AmenityRoomSerializer(many=True, required=False)
    category = serializers.CharField()

    class Meta:
        model = Room
        fields = (
            "id",
            "category",
            "smoking",
            "area",
            "amenities",
            "capacity",
            "single_bed",
            "double_bed",
            "nightly_price",
        )

    def create(self, validated_data):
        # Извлекаем вложенные данные
        amenities_data = validated_data.pop("amenities", [])
        # meal_data = validated_data.pop("meal", [])

        # Передача имени категории
        category_name = validated_data.pop("category")
        category_instance, created = RoomCategory.objects.get_or_create(
            name=category_name
        )

        # Создаем объект Room
        room = Room.objects.create(
            category=category_instance,
            **validated_data
        )

        # # Добавляем остальные типы питания
        # for meal in meal_data:
        #     meal_instance, created = MealPlan.objects.get_or_create(
        #         name=meal.get("name"),
        #         price_per_person=meal.get("price_per_person")
        #     )
        #     room.meal.add(meal_instance)
        room.save()

        # Рассчитываем цены с учетом типов питания и сохраняем
        # calculate_nightly_prices(room)
        # room.save()

        # Создаем связанные объекты amenities
        for amenity_data in amenities_data:
            amenity, created = RoomAmenity.objects.get_or_create(
                name=amenity_data.get("name")
            )
            room.amenities.add(amenity)
        return room

    def update(self, instance, validated_data):
        # Извлекаем вложенные данные
        amenities_data = validated_data.pop("amenities", [])
        # meal_data = validated_data.pop("meal", [])

        # Обновляем категорию
        category_name = validated_data.pop("category")
        category_instance, created = RoomCategory.objects.get_or_create(
            name=category_name
        )
        instance.category = category_instance

        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # for meal in meal_data:
        #     meal_instance, created = MealPlan.objects.get_or_create(
        #         name=meal.get("name"),
        #         price_per_person=meal.get("price_per_person")
        #     )
        #     instance.meal.add(meal_instance)
        instance.save()

        # Рассчитываем цены с учетом типов питания и сохраняем
        # calculate_nightly_prices(instance)
        # instance.save()

        # Обновляем связанные объекты amenities
        instance.amenities.clear()  # Удаляем все существующие удобства
        for amenity_data in amenities_data:
            amenity, created = RoomAmenity.objects.get_or_create(
                name=amenity_data.get("name")
            )
            instance.amenities.add(amenity)
        return instance


class RoomDetailSerializer(RoomBaseSerializer):
    photo = RoomPhotoSerializer(source="room_photos", many=True, read_only=True,)
    # meal = MealPlanSerializer(many=True, read_only=True, )


    class Meta(RoomBaseSerializer.Meta):
        model = Room
        fields = RoomBaseSerializer.Meta.fields + ("photo",)
