from rest_framework import serializers

from hotels.models.hotel.models_hotel_photo import HotelPhoto


class HotelPhotoSerializer(serializers.ModelSerializer):
    """Сериализатор фотографий отеля"""

    photo = serializers.ImageField()

    class Meta:
        model = HotelPhoto
        fields = "__all__"
        read_only_fields = (
            "id",
            "hotel",
        )
