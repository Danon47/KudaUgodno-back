from django.db.models import Min
from rest_framework import serializers

from hotels.models.hotel.models_hotel import Hotel
from hotels.models.hotel.models_hotel_what_about import HotelWhatAbout


class HotelShortSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = (
            "id",
            "photo",
            "country",
            "city",
            "star_category",
            "name",
            "distance_to_the_center",
            "min_price",
            "user_rating",
        )

    def get_photo(self, obj: Hotel) -> str:
        request = self.context.get("request")
        first_photo = obj.hotel_photos.first()
        if first_photo:
            return request.build_absolute_uri(first_photo.photo.url) if request else first_photo.photo.url
        return None

    def get_min_price(self, obj: Hotel) -> int:
        return obj.rooms.aggregate(min_price=Min("price"))["min_price"]


class HotelWhatAboutFullSerializer(serializers.ModelSerializer):
    hotel = HotelShortSerializer(many=True, read_only=True)
    name_set = serializers.CharField(read_only=True)

    class Meta:
        model = HotelWhatAbout
        fields = (
            "name_set",
            "hotel",
        )
