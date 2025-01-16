from rest_framework import serializers
from hotels.models.models_hotel_meal import MealPlan


class MealSerializer(serializers.ModelSerializer):
    """Сериализатор питания"""

    price_per_person = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = MealPlan
        fields = ("name", "price_per_person",)