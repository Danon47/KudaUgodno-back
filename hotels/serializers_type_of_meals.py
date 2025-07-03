from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from all_fixture.errors.list_error import TYPE_OF_MEAL_NAME_ERROR
from hotels.models import TypeOfMeal


class TypeOfMealSerializer(ModelSerializer):
    """
    Сериализатор для типов питания в отеле.
    """

    class Meta:
        model = TypeOfMeal
        fields = ("id", "name", "price")

    def validate(self, attrs):
        hotel = self.context["view"].get_hotel()
        name = attrs.get("name")
        if TypeOfMeal.objects.filter(hotel_id=hotel.id, name=name).exists():
            raise ValidationError({"detail": TYPE_OF_MEAL_NAME_ERROR}, code=400)
        return attrs
