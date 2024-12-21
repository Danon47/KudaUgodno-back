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
            'start_date',
            'end_date',
            'flight_to',
            'flight_to',
            'tour_operator',
            'hotel',
            'room',
            'meal_cost',
            'price'
        )
        read_only_fields = ('price', 'meal_cost')

