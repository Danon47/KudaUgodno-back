from rest_framework.serializers import ModelSerializer

from hotels.models import TypeOfMeal


class TypeOfMealSerializer(ModelSerializer):
    """
    Сериализатор для типов питания в отеле
    """

    class Meta:
        model = TypeOfMeal
        fields = ("id", "name", "price")
