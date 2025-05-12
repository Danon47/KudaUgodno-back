from rest_framework import serializers

from hotels.models.hotel.type_of_meals.models_type_of_meals import TypeOfMeal


class TypeOfMealSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypeOfMeal
        fields = ("name", "price")
