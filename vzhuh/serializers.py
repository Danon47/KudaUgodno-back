from rest_framework import serializers

from vzhuh.models import Vzhuh


class VzhuhSerializer(serializers.ModelSerializer):
    route = serializers.SerializerMethodField()

    class Meta:
        model = Vzhuh
        fields = (
            "id",
            "departure_city",
            "arrival_city",
            "route",
            "description",
            "best_time_to_travel",
            "suitable_for_whom",
            "description_tour",
            "description_hotel",
            "description_blog",
            "tours",
            "hotels",
            "created_at",
            "is_published",
        )

    def get_route(self, obj):
        return obj.route
