from rest_framework import serializers

from hotels.models.hotel.models_hotel import Hotel
from hotels.serializers.hotel.photo.serializers_hotel_photo import HotelPhotoSerializer
from hotels.serializers.hotel.rules.serializers_hotel_rules import HotelRulesSerializer
from hotels.serializers.room.serializers_room import RoomDetailSerializer


class HotelBaseSerializer(serializers.ModelSerializer):
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


class HotelDetailSerializer(serializers.ModelSerializer):
    """
    Сериализация для обновления всех полей отеля
    Метод PUT, DELETE, PATCH - но его не используем, позже будет отдельная сериализация
    по добавлению отеля в архив методом PATCH
    """

    rules = HotelRulesSerializer(many=True, source="hotels_rules", required=False)
    user_rating = serializers.FloatField(required=False)
    width = serializers.DecimalField(required=False, max_digits=11, decimal_places=6)
    longitude = serializers.DecimalField(required=False, max_digits=11, decimal_places=6)

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
    # created_by = serializers.SerializerMethodField()

    class Meta(HotelListWithPhotoSerializer.Meta):
        fields = HotelListWithPhotoSerializer.Meta.fields + (
            "rooms",
            # "created_by",
        )

    # def get_created_by(self, obj):
    #     # Например, возвращаем email пользователя
    #     return obj.created_by.email if obj.created_by else None
