from rest_framework.serializers import ModelSerializer

from tours.models import Tour


class TourSerializer(ModelSerializer):
    """
    Сериализатор для модели Tour.
    """

    class Meta:
        model = Tour
        fields = (
            'id',
            'name',
            'start_date',
            'end_date',
            'flight_to',
            'flight_to',
            'tour_operator',
            'hotel',
            'room',
            'country',
            'city',
            'type_of_holiday',
            'meal_cost',
            'price'
        )

