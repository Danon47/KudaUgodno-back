from django.db.models import Min
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_photo import HotelPhoto


class HotelWhatAboutSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чего насчёт ...
    От дазайнера будет добавлена
    """

    hotel_id = serializers.IntegerField(source="id")
    photo = serializers.SerializerMethodField()
    user_rating = serializers.FloatField()
    min_price = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = (
            "hotel_id",
            "photo",
            "country",
            "city",
            "user_rating",
            "star_category",
            "name",
            "distance_to_the_sea",
            "min_price",
        )

    @extend_schema_field(serializers.IntegerField)
    def get_min_price(self, obj: Hotel) -> int:
        return obj.rooms.aggregate(min_price=Min("price"))["min_price"]

    def get_photo(self, obj: HotelPhoto) -> str:
        if obj.hotel_photos.exists():
            first_photo = obj.hotel_photos.first()
            return self.context["request"].build_absolute_uri(first_photo.photo.url)
        return None
