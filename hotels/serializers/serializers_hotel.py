from rest_framework import serializers
from hotels.models.models_hotel import Hotel
from hotels.models.models_hotel_amenity import HotelAmenity
from hotels.models.models_hotel_photo import HotelPhoto
from hotels.serializers.serializers_room import RoomBaseSerializer


class AmenityHotelSerializer(serializers.ModelSerializer):
    """Сериализатор Удобств для отеля"""

    class Meta:
        model = HotelAmenity
        fields = ("id", "name",)


class HotelPhotoSerializer(serializers.ModelSerializer):
    """Сериализатор фотографий отеля"""
    photo = serializers.ImageField()

    class Meta:
        model = HotelPhoto
        fields = ("photo",)

class HotelBaseSerializer(serializers.ModelSerializer):
    amenities = AmenityHotelSerializer(many=True,)
    photo = HotelPhotoSerializer(source="hotel_photos", many=True, required=False)
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
    amenities = AmenityHotelSerializer(many=True, read_only=True, )
    rooms = RoomBaseSerializer(many=True, read_only=True,)
    photo = HotelPhotoSerializer(source="hotel_photos", many=True, read_only=True,)
    user_rating = serializers.FloatField(read_only=True,)

    class Meta:
        model = Hotel
        fields = HotelBaseSerializer.Meta.fields + ("rooms",)