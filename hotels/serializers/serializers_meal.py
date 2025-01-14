from rest_framework import serializers
from hotels.models import MealPlan


class MealSerializer(serializers.ModelSerializer):
    """Сериализатор питания"""

    price_per_person = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = MealPlan
        fields = ("name", "price_per_person",)