from rest_framework import serializers
from hotels.choices import MealChoices
from hotels.models.models_hotel_meal import MealPlan
from hotels.models.models_room import Room
from hotels.models.models_room_amenity import RoomAmenity
from hotels.models.models_room_caterogy import RoomCategory
from hotels.models.models_room_photo import RoomPhoto
from hotels.serializers.serializers_meal import MealSerializer
from hotels.services import calculate_nightly_prices


class AmenityRoomSerializer(serializers.ModelSerializer):
    """Сериализатор Удобств для номера"""

    class Meta:
        model = RoomAmenity
        fields = ("id", "name",)


class CategoryRoomSerializer(serializers.ModelSerializer):
    """Категория номера"""

    class Meta:
        model = RoomCategory
        fields = ("name",)


class RoomPhotoSerializer(serializers.ModelSerializer):
    """Сериализатор фотографий номера"""

    class Meta:
        model = RoomPhoto
        fields = ("photo", "room",)


class RoomBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор номера"""

    amenities = AmenityRoomSerializer(many=True,)
    category = serializers.CharField()
    photo = RoomPhotoSerializer(source="room_photos", many=True,)
    meal = MealSerializer(many=True,)

    class Meta:
        model = Room
        fields = (
            "id",
            "category",
            "meal",
            "smoking",
            "area",
            "amenities",
            "capacity",
            "single_bed",
            "double_bed",
            "nightly_price",
            "photo",
        )

    def create(self, validated_data):
        # Извлекаем вложенные данные
        amenities_data = validated_data.pop("amenities", [])
        meal_data = validated_data.pop("meal", [])
        photos_data = validated_data.pop("room_photos", [])

        # Передача имени категории
        category_name = validated_data.pop("category")
        category_instance, created = RoomCategory.objects.get_or_create(
            name=category_name
        )

        # Создаем объект Room
        room = Room.objects.create(category=category_instance, **validated_data)

        # Добавляем тип питания "Без питания" к номеру, стоимость которого равна 0
        no_meals_plan, created = MealPlan.objects.get_or_create(
            name=MealChoices.NO_MEALS,
            defaults={"price_per_person": 0}
        )
        room.meal.add(no_meals_plan)

        # Добавляем остальные типы питания
        for meal in meal_data:
            meal_instance, created = MealPlan.objects.get_or_create(
                name=meal.get("name"),
                price_per_person=meal.get("price_per_person")
            )
            room.meal.add(meal_instance)
        room.save()

        # Рассчитываем цены с учетом типов питания и сохраняем
        calculate_nightly_prices(room)
        room.save()

        # Создаем связанные объекты amenities
        for amenity_data in amenities_data:
            amenity, created = RoomAmenity.objects.get_or_create(
                name=amenity_data.get("name")
            )
            room.amenities.add(amenity)

        # Создаем связанные объекты photo
        for photo_data in photos_data:
            RoomPhoto.objects.create(room=room, **photo_data)

        return room

    def update(self, instance, validated_data):
        # Извлекаем вложенные данные
        amenities_data = validated_data.pop("amenities", [])
        meal_data = validated_data.pop("meal", [])
        photos_data = validated_data.pop("room_photos", [])

        # Обновляем категорию
        category_name = validated_data.pop("category")
        category_instance, created = RoomCategory.objects.get_or_create(
            name=category_name
        )
        instance.category = category_instance

        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Обновляем тип питания "Без питания"
        no_meals_plan, created = MealPlan.objects.get_or_create(
            name=MealChoices.NO_MEALS,
            defaults={"price_per_person": 0}
        )
        instance.meal.clear()  # Очищаем типы питания
        instance.meal.add(no_meals_plan)  # Добавляем "Без питания"

        # Рассчитываем цены с учетом типов питания и сохраняем
        calculate_nightly_prices(instance)
        instance.save()

        # Обновляем связанные объекты amenities
        instance.amenities.clear()  # Удаляем все существующие удобства
        for amenity_data in amenities_data:
            amenity, created = RoomAmenity.objects.get_or_create(
                name=amenity_data.get("name")
            )
            instance.amenities.add(amenity)

        # Обновляем связанные объекты photo
        instance.room_photos.all().delete()  # Удаляем все существующие фотографии
        for photo_data in photos_data:
            RoomPhoto.objects.create(room=instance, **photo_data)

        return instance


class RoomDetailSerializer(RoomBaseSerializer):
    photo = RoomPhotoSerializer(source="room_photos", many=True, read_only=True,)
    meal = MealSerializer(many=True, read_only=True,)
    nightly_price_no_meals = serializers.IntegerField(read_only=True)
    nightly_price_ultra_all_inclusive = serializers.IntegerField(read_only=True)
    nightly_price_all_inclusive = serializers.IntegerField(read_only=True)
    nightly_price_full_board = serializers.IntegerField(read_only=True)
    nightly_price_half_board = serializers.IntegerField(read_only=True)
    nightly_price_only_breakfast = serializers.IntegerField(read_only=True)

    class Meta(RoomBaseSerializer.Meta):
        model = Room
        fields = RoomBaseSerializer.Meta.fields + (
            "nightly_price_no_meals",
            "nightly_price_ultra_all_inclusive",
            "nightly_price_all_inclusive",
            "nightly_price_full_board",
            "nightly_price_half_board",
            "nightly_price_only_breakfast",
        )