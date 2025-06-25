from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.fixture_views import (
    flight_arrival_city,
    flight_arrival_country,
    flight_arrival_date,
    flight_departure_city,
    flight_departure_country,
    flight_departure_date,
    flight_id,
    flight_settings,
    limit,
    offset,
)
from all_fixture.pagination import CustomLOPagination
from flights.models import Flight
from flights.serializers import FlightSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список рейсов",
        description="Получение списка всех рейсов",
        tags=[flight_settings["name"]],
        parameters=[
            limit,
            offset,
            flight_departure_country,
            flight_departure_city,
            flight_departure_date,
            flight_arrival_country,
            flight_arrival_city,
            flight_arrival_date,
        ],
        responses={
            200: FlightSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
    ),
    create=extend_schema(
        summary="Добавление рейса",
        description="Создание новой рейса",
        request=FlightSerializer,
        tags=[flight_settings["name"]],
        responses={
            201: FlightSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о рейсе",
        description="Получение информации о рейсе через идентификатор",
        tags=[flight_settings["name"]],
        parameters=[flight_id],
        responses={
            200: FlightSerializer,
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление рейса",
        description="Обновление всех полей рейса",
        request=FlightSerializer,
        tags=[flight_settings["name"]],
        parameters=[flight_id],
        responses={
            200: FlightSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Рейс не найден"),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление рейса",
        description="Обновление отдельных полей рейса",
        request=FlightSerializer,
        tags=[flight_settings["name"]],
        parameters=[flight_id],
        responses={
            200: FlightSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Рейс не найден"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление рейса",
        description="Полное удаление рейса",
        tags=[flight_settings["name"]],
        parameters=[flight_id],
        responses={
            204: OpenApiResponse(description="Рейса удален"),
            404: OpenApiResponse(description="Рейс не найден"),
        },
    ),
)
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    pagination_class = CustomLOPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = (
        "departure_country",
        "departure_city",
        "departure_date",
        "arrival_country",
        "arrival_city",
        "arrival_date",
    )
