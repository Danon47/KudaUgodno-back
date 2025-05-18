from random import choice

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.fixture_views import what_about_settings
from hotels.models.hotel.what_about.models_hotel_what_about import HotelWhatAbout
from hotels.serializers.hotel.what_about.serializers_hotel_what_about import HotelWhatAboutFullSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список подборок что насчёт ...",
        description="Получение списка подборок что насчёт ...",
        responses={
            200: HotelWhatAboutFullSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[what_about_settings["name"]],
    )
)
class HotelWarpUpViewSet(viewsets.ModelViewSet):
    queryset = HotelWhatAbout.objects.none()
    serializer_class = HotelWhatAboutFullSerializer

    def get_queryset(self):
        """
        Возвращает случайную подборку
        """
        all_ids = list(HotelWhatAbout.objects.values_list("id", flat=True))
        if not all_ids:
            return HotelWhatAbout.objects.none()
        random_id = choice(all_ids)
        return HotelWhatAbout.objects.filter(id=random_id)
