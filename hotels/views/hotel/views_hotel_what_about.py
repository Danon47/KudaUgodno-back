from random import choice

from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.fixture_views import limit, offset, warm_up_settings
from all_fixture.pagination import CustomLOPagination
from hotels.models.hotel.models_hotel import Hotel
from hotels.serializers.what_about.serializers_hotel_warm_up import HotelWhatAboutSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список что на счёт погреться",
        description="Получение списка трёх  отелей в определённом городе",
        parameters=[offset, limit],
        responses={
            200: HotelWhatAboutSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[warm_up_settings["name"]],
    )
)
class HotelWarpUpViewSet(viewsets.ModelViewSet):
    serializer_class = HotelWhatAboutSerializer
    pagination_class = CustomLOPagination

    def get_queryset(self):
        # Получаем все отели с warm=True
        warm_hotels = Hotel.objects.filter(warm=True)
        # Если нет отелей в тёплых странах, возвращаем пустой queryset
        if not warm_hotels.exists():
            return Hotel.objects.none()
        # Выбираем случайный отель из списка тёплых отелей
        selected_hotel = choice(list(warm_hotels))
        # Фильтруем отели по стране выбранного отеля сортировка пока не согласована
        queryset = Hotel.objects.filter(country=selected_hotel.country).order_by("?")
        return queryset
