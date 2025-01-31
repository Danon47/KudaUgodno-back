from rest_framework import serializers
from hotels.models.hotel.models_hotel_amenity import HotelAmenityCommon, HotelAmenityForChildren, \
    HotelAmenitySportsAndRecreation, HotelAmenityInTheRoom


class HotelAmenityCommonSerializer(serializers.ModelSerializer):
    """Сериализатор Удобств для отеля"""

    name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = HotelAmenityCommon
        fields = ("name",)

    # def validate_name(self, value):
    #     print("Validating name:", value)
    #     if not value:
    #         raise serializers.ValidationError("Удобство должно иметь имя.")
    #     return value

class HotelAmenityInTheRoomSerializer(serializers.ModelSerializer):
    """Сериализатор Удобств для отеля"""

    name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = HotelAmenityInTheRoom
        fields = ("name",)


class HotelAmenitySportsAndRecreationSerializer(serializers.ModelSerializer):
    """Сериализатор Удобств для отеля"""

    name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = HotelAmenitySportsAndRecreation
        fields = ("name",)


class HotelAmenityForChildrenSerializer(serializers.ModelSerializer):
    """Сериализатор Удобств для отеля"""

    name = serializers.CharField(max_length=50, required=True)

    class Meta:
        model = HotelAmenityForChildren
        fields = ("name",)


