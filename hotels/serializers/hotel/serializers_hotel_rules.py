from rest_framework import serializers

from hotels.models.hotel.models_hotel_rules import HotelRules


class HotelRulesSerializer(serializers.ModelSerializer):
    """Сериализатор правил в отеле"""

    class Meta:
        model = HotelRules
        fields = (
            "name",
            "description",
        )
