from datetime import datetime

from drf_spectacular.utils import extend_schema_field
from rest_framework.serializers import (
    CharField,
    DateField,
    DecimalField,
    FloatField,
    IntegerField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
)

from hotels.models.hotel.models_hotel import Hotel
from hotels.serializers.hotel.photo.serializers_hotel_photo import HotelPhotoSerializer
from hotels.serializers.hotel.rules.serializers_hotel_rules import HotelRulesSerializer
from hotels.serializers.room.serializers_room import RoomDetailSerializer
from hotels.validators.hotel.validators_hotel import DateValidator


class HotelBaseSerializer(ModelSerializer):
    """
    Базовая сериализация для создания отеля
    Метод POST (create)
    """

    class Meta:
        model = Hotel
        fields = (
            "id",
            "name",
        )

    def create(self, validated_data):
        return Hotel.objects.create(**validated_data)


class HotelDetailSerializer(ModelSerializer):
    """
    Сериализация для обновления всех полей отеля
    Метод PUT, DELETE, PATCH - но его не используем, позже будет отдельная сериализация
    по добавлению отеля в архив методом PATCH
    """

    rules = HotelRulesSerializer(many=True, source="hotels_rules", required=False)
    user_rating = FloatField(required=False)
    width = DecimalField(required=False, max_digits=11, decimal_places=6)
    longitude = DecimalField(required=False, max_digits=11, decimal_places=6)

    class Meta:
        model = Hotel
        fields = (
            "id",
            "name",
            "star_category",
            "place",
            "country",
            "city",
            "address",
            "distance_to_the_station",
            "distance_to_the_sea",
            "distance_to_the_center",
            "distance_to_the_metro",
            "distance_to_the_airport",
            "description",
            "check_in_time",
            "check_out_time",
            "amenities_common",
            "amenities_in_the_room",
            "amenities_sports_and_recreation",
            "amenities_for_children",
            "user_rating",
            "type_of_rest",
            "rules",
            "is_active",
            "width",
            "longitude",
        )

    def update(self, instance, validated_data):
        # Удаляем вложенные данные из validated_data
        rules_data = validated_data.pop("hotels_rules", None)

        # Обновляем основные поля
        instance = super().update(instance, validated_data)

        # Обновляем вложенные поля, если они предоставлены
        if rules_data is not None:
            instance.hotels_rules.all().delete()  # Удаляем старые правила
            for rule_data in rules_data:
                instance.hotels_rules.create(**rule_data)

        return instance


class HotelListWithPhotoSerializer(HotelDetailSerializer):
    """
    Промежуточная сериализация, где не нужны номера. Возвращает все поля, и фотографии отеля.
    """

    photo = HotelPhotoSerializer(
        source="hotel_photos",
        many=True,
        read_only=True,
    )

    class Meta(HotelDetailSerializer.Meta):
        fields = HotelDetailSerializer.Meta.fields + ("photo",)


class HotelListRoomAndPhotoSerializer(HotelListWithPhotoSerializer):
    """
    Полная сериализация отеля со всеми вложенными данными.
    Фотографии отеля, номера в отеле.
    Метод GET(list), GET id (retrieve)
    """

    rooms = RoomDetailSerializer(
        many=True,
        read_only=True,
    )
    # created_by = SerializerMethodField()

    class Meta(HotelListWithPhotoSerializer.Meta):
        fields = HotelListWithPhotoSerializer.Meta.fields + (
            "rooms",
            # "created_by",
        )

    # def get_created_by(self, obj):
    #     # Например, возвращаем email пользователя
    #     return obj.created_by.email if obj.created_by else None


class HotelSearchResponseSerializer(HotelListRoomAndPhotoSerializer):
    """Cериализатор отеля для получения ответа из поиска."""

    nights = SerializerMethodField()
    guests = SerializerMethodField()
    rooms = SerializerMethodField()

    class Meta(HotelListRoomAndPhotoSerializer.Meta):
        fields = HotelListRoomAndPhotoSerializer.Meta.fields + ("nights", "guests")

    @extend_schema_field(field=RoomDetailSerializer(many=True))
    def get_rooms(self, obj):
        """Возвращаем только отфильтрованные комнаты по количеству гостей и другим параметрам."""
        rooms = getattr(obj, "filtered_rooms", None)
        if rooms is None:
            return []  # если не было префетча
        return RoomDetailSerializer(rooms, many=True).data

    @extend_schema_field(int)
    def get_nights(self, obj) -> int:
        """Подсчет количества ночей."""
        check_in = self.context.get("check_in_date")
        check_out = self.context.get("check_out_date")
        nights_default = 1
        if not check_in or not check_out:
            return nights_default
        try:
            check_in_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out_date = datetime.strptime(check_out, "%Y-%m-%d").date()
            return max((check_out_date - check_in_date).days, nights_default)
        except (ValueError, TypeError):
            return nights_default

    @extend_schema_field(int)
    def get_guests(self, obj) -> int:
        """Получение количества гостей из контекста."""
        return int(self.context.get("guests", 1))


class HotelSearchRequestSerializer(Serializer):
    """Cериализатор отеля для поиска."""

    city = CharField(required=False)
    check_in_date = DateField(
        required=True,
        input_formats=["%Y-%m-%d"],
        error_messages={"invalid": "Некорректный формат даты. Используйте YYYY-MM-DD"},
    )
    check_out_date = DateField(
        required=True,
        input_formats=["%Y-%m-%d"],
        error_messages={"invalid": "Некорректный формат даты. Используйте YYYY-MM-DD"},
    )
    guests = IntegerField(min_value=1, required=True)
    validators = [DateValidator(check_in_field="check_in_date", check_out_field="check_out_date")]


class HotelFiltersRequestSerializer(Serializer):
    """Сериализатор для параметров расширенного поиска (все поля необязательные)."""

    # Параметры фильтрации верхнего поиска
    hotel_city = CharField(required=False)
    check_in_date = DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        error_messages={"invalid": "Некорректный формат даты. Используйте YYYY-MM-DD"},
    )
    check_out_date = DateField(
        required=False,
        input_formats=["%Y-%m-%d"],
        error_messages={"invalid": "Некорректный формат даты. Используйте YYYY-MM-DD"},
    )
    guests = IntegerField(min_value=1, required=False)

    # Параметры фильтрации отеля
    city = CharField(required=False)
    type_of_rest = CharField(required=False)
    place = CharField(required=False)
    price_gte = IntegerField(min_value=1, required=False)
    price_lte = IntegerField(min_value=0, required=False)
    user_rating = FloatField(min_value=0, max_value=10, required=False)
    star_category = IntegerField(min_value=0, required=False)
    validators = [DateValidator(check_in_field="check_in_date", check_out_field="check_out_date")]
