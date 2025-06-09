from django.db.models import Min
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from hotels.models import Hotel
from hotels.serializers import HotelPhotoSerializer
from tours.models import Tour
from vzhuhs.models import Vzhuh, VzhuhPhoto


def get_first_photo(self, obj, related_field="hotel_photos"):
    """
    Вспомогательная функция для получения первой фотографии
    """
    request = getattr(self, "context", {}).get("request")
    related_objects = getattr(obj, related_field, None)
    first_photo = related_objects.first() if related_objects else None
    if first_photo:
        serializer = HotelPhotoSerializer(first_photo, context={"request": request})
        photo_url = serializer.data["photo"]
        return request.build_absolute_uri(photo_url) if request else photo_url
    return None


class VzhuhPhotoSerializer(serializers.ModelSerializer):
    """
    Сериализатор для фотографий Вжуха.
    """

    class Meta:
        model = VzhuhPhoto
        fields = ("photos",)


class VzhuhHotelShortSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода инфы по отелю во Вжухе.
    """

    photo = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model = Hotel
        fields = (
            "id",
            "photo",
            "country",
            "city",
            "star_category",
            "user_rating",
            "name",
            "distance_to_the_sea",
            "price",
        )

    @extend_schema_field(serializers.ImageField(allow_null=True))
    def get_photo(self, obj: Hotel):
        """
        Возвращает первую фотографию отеля, если она доступна.
        """
        return get_first_photo(self, obj, "hotel_photos")

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True))
    def get_price(self, obj: Hotel):
        """
        Вычисляет минимальную цену по связанным турам отеля, если они есть.
        """
        min_price = obj.tours.filter(price__isnull=False).aggregate(Min("price"))["price__min"]
        return min_price


class VzhuhTourShortSerializer(serializers.ModelSerializer):
    """
    Сериализатор для вывода инфы по туру во Вжухе.
    """

    photo = serializers.SerializerMethodField()
    country = serializers.CharField(source="hotel.country")
    city = serializers.CharField(source="hotel.city")
    star_category = serializers.IntegerField(source="hotel.star_category")
    user_rating = serializers.FloatField(source="hotel.user_rating")
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

    @extend_schema_field(serializers.ImageField(allow_null=True))
    def get_photo(self, obj: Tour):
        """
        Возвращает первую фотографию отеля, связанного с туром, если она доступна.
        """
        if obj.hotel:
            return get_first_photo(self, obj.hotel, "hotel_photos")
        return None

    @extend_schema_field(serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True))
    def get_sale(self, obj):
        """
        Возвращает размер скидки, если у тура есть активная акция.
        """
        if obj.stock and obj.stock.active_stock:
            return obj.stock.discount_amount
        return None

    @extend_schema_field(serializers.IntegerField(allow_null=True))
    def get_number_of_days(self, obj):
        """
        Вычисляет количество дней между началом и окончанием тура.
        """
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return None


class VzhuhSerializer(serializers.ModelSerializer):
    """
    Сериализатор Вжуха.
    """

    tours = VzhuhTourShortSerializer(many=True)
    hotels = VzhuhHotelShortSerializer(many=True)
    photos = VzhuhPhotoSerializer(many=True)

    class Meta:
        model = Vzhuh
        fields = (
            "id",
            "departure_city",
            "arrival_city",
            "photos",
            "description",
            "best_time_to_travel",
            "suitable_for_whom",
            "description_hotel",
            "description_blog",
            "tours",
            "hotels",
            "is_published",
        )
