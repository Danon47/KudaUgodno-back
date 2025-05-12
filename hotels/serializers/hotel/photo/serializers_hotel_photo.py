from rest_framework import serializers

from hotels.models.hotel.photo.models_hotel_photo import HotelPhoto


class HotelPhotoSerializer(serializers.ModelSerializer):
    """Сериализатор фотографий отеля"""

    photo = serializers.ImageField()

    class Meta:
        model = HotelPhoto
        fields = ("id", "photo", "hotel")
        read_only_fields = (
            "id",
            "hotel",
        )
