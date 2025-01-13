import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from .choices import MealChoices
from .models import (
    Hotel,
    HotelAmenity,
    HotelPhoto,
    Room,
    RoomAmenity,
    RoomPhoto,
    RoomCategory,
    MealPlan,
)
from .services import calculate_nightly_prices


class MealSerializer(serializers.ModelSerializer):
    """ Сериализатор питания """
    price_per_person = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = MealPlan
        fields = ("name", "price_per_person",)


class BaseAmenitySerializer(serializers.ModelSerializer):
    """ Базовый сериализатор Удобств """
    class Meta:
        fields = ("id", "name",)


class AmenityRoomSerializer(BaseAmenitySerializer):
    """ Сериализатор Удобств для номера """
    class Meta(BaseAmenitySerializer.Meta):
        model = RoomAmenity


class AmenityHotelSerializer(BaseAmenitySerializer):
    """ Сериализатор Удобств для отеля """
    class Meta(BaseAmenitySerializer.Meta):
        model = HotelAmenity


class CategoryRoomSerializer(serializers.ModelSerializer):
    """ Категория номера """
    class Meta:
        model = RoomCategory
        fields = "__all__"


class RoomPhotoSerializer(serializers.ModelSerializer):
    """ Сериализатор фотографий номера """
    photo = serializers.CharField()

    class Meta:
        model = RoomPhoto
        fields = ("photo",)

    def to_internal_value(self, data):
        # Проверяем, что поле photo содержит base64-строку
        if "data:image" in data["photo"]:
            # Извлекаем base64-часть строки
            photo_data = data["photo"].split("base64,")[1]
            # Декодируем base64
            decoded_file = base64.b64decode(photo_data)
            # Создаем объект файла
            file_name = "room.jpg"
            return {"photo": ContentFile(decoded_file, name=file_name)}
        else:
            # Если это не base64, возвращаем данные как есть
            return super().to_internal_value(data)


class HotelPhotoSerializer(serializers.ModelSerializer):
    """ Сериализатор фотографий отеля """
    photo = serializers.CharField()

    class Meta:
        model = HotelPhoto
        fields = ("photo",)

    def to_internal_value(self, data):
        # Проверяем, что поле photo содержит base64-строку
        if "data:image" in data["photo"]:
            # Извлекаем base64-часть строки
            photo_data = data["photo"].split("base64,")[1]
            # Декодируем base64
            decoded_file = base64.b64decode(photo_data)
            # Создаем объект файла
            file_name = "hotel.jpg"
            return {"photo": ContentFile(decoded_file, name=file_name)}
        else:
            # Если это не base64, возвращаем данные как есть
            return super().to_internal_value(data)


class RoomBaseSerializer(serializers.ModelSerializer):
    """ Базовый сериализатор номера """

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
        category_instance, created = RoomCategory.objects.get_or_create(name=category_name)

        # Создаем объект Room
        room = Room.objects.create(category=category_instance, **validated_data)

        # Добавляем тип питания "Без питания" к номеру, стоимость которого равна 0
        no_meals_plan, created = MealPlan.objects.get_or_create(
            name=MealChoices.NO_MEALS,
            defaults={'price_per_person': 0}
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
            amenity, created = RoomAmenity.objects.get_or_create(name=amenity_data.get("name"))
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
        category_instance, created = RoomCategory.objects.get_or_create(name=category_name)
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
            amenity, created = RoomAmenity.objects.get_or_create(name=amenity_data.get("name"))
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


class HotelBaseSerializer(serializers.ModelSerializer):
    amenities = AmenityHotelSerializer(many=True,)
    photo = HotelPhotoSerializer(source="hotel_photos", many=True,)
    user_rating = serializers.FloatField()

    class Meta:
        model = Hotel
        fields = (
            "id",
            "name",
            "star_category",
            "place",
            "type_of_holiday",
            "amenities",
            "country",
            "city",
            "address",
            "distance_to_sea",
            "distance_to_airport",
            "description",
            "user_rating",
            "check_in_time",
            "check_out_time",
            "photo",
        )

    def create(self, validated_data):
        # Извлекаем вложенные данные
        amenities_data = validated_data.pop("amenities", [])
        photos_data = validated_data.pop("hotel_photos", [])

        # Создаем объект Hotel
        hotel = Hotel.objects.create(**validated_data)

        # Создаем связанные объекты Amenity
        for amenity_data in amenities_data:
            amenity, created = HotelAmenity.objects.get_or_create(**amenity_data)
            hotel.amenities.add(amenity)

        # Создаем связанные объекты Photo
        for photo_data in photos_data:
            HotelPhoto.objects.create(hotel=hotel, **photo_data)

        return hotel

    def update(self, instance, validated_data):
        # Обновляем вложенные данные (amenities и photo)
        amenities_data = validated_data.pop("amenities", [])
        photos_data = validated_data.pop("hotel_photos", [])

        # Обновляем основные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем удобства
        instance.amenities.clear()
        for amenity_data in amenities_data:
            amenity, _ = HotelAmenity.objects.get_or_create(**amenity_data)
            instance.amenities.add(amenity)

        # Обновляем фотографии
        instance.hotel_photos.all().delete()
        for photo_data in photos_data:
            HotelPhoto.objects.create(hotel=instance, **photo_data)

        return instance


class HotelDetailSerializer(HotelBaseSerializer):
    amenities = AmenityHotelSerializer(many=True, read_only=True,)
    rooms = RoomBaseSerializer(many=True, read_only=True,)
    photo = HotelPhotoSerializer(source="hotel_photos", many=True, read_only=True,)
    user_rating = serializers.FloatField(read_only=True,)

    class Meta:
        model = Hotel
        fields = HotelBaseSerializer.Meta.fields + ("rooms",)
