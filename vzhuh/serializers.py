from rest_framework import serializers

from hotels.models.hotel.models_hotel import Hotel
from tours.models import Tour
from vzhuh.models import Vzhuh


class HotelShortSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = (
            "id",
            "photo",  # ← теперь OK
            "country",
            "city",
            "star_category",
            "user_rating",
            "name",
            "distance_to_the_sea",
            "price",
        )

    def get_photo(self, obj):
        """Возвращает URL первой фотографии отеля (если есть)"""
        first_photo = obj.hotel_photos.first()
        return first_photo.photo.url if first_photo and first_photo.photo else None

    def get_price(self, obj):
        tours = obj.tours.filter(price__isnull=False)
        return min(t.price for t in tours) if tours.exists() else None


class TourShortSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    country = serializers.CharField(source="hotel.country")
    city = serializers.CharField(source="hotel.city")
    star_category = serializers.IntegerField(source="hotel.star_category")
    user_rating = serializers.DecimalField(source="hotel.user_rating", max_digits=3, decimal_places=1)
    name = serializers.CharField(source="hotel.name")
    sale = serializers.SerializerMethodField()
    number_of_days = serializers.SerializerMethodField()

    class Meta:
        model = Tour
        fields = (
            "id",
            "photo",
            "country",
            "city",
            "star_category",
            "user_rating",
            "name",
            "sale",
            "price",
            "start_date",
            "end_date",
            "number_of_days",
        )

    def get_photo(self, obj):
        hotel = obj.hotel
        if not hotel:
            return None

        photo_obj = hotel.hotel_photos.first()
        return photo_obj.photo.url if photo_obj and photo_obj.photo else None

    def get_sale(self, obj):
        if obj.stock and obj.stock.active_stock:
            return obj.stock.discount_amount
        return None

    def get_number_of_days(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return None


class VzhuhSerializer(serializers.ModelSerializer):
    route = serializers.SerializerMethodField()
    tours = TourShortSerializer(many=True)
    hotels = HotelShortSerializer(many=True)

    class Meta:
        model = Vzhuh
        fields = (
            "id",
            "departure_city",
            "arrival_city",
            "route",
            "description",
            "best_time_to_travel",
            "suitable_for_whom",
            "description_hotel",
            "description_blog",
            "tours",  # ← вложенный сериализатор
            "hotels",  # ← вложенный сериализатор
            "created_at",
            "is_published",
        )

    def get_route(self, obj):
        return obj.route
