from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.pagination import CustomLOPagination
from all_fixture.views_fixture import (
    FLIGHT_ARRIVAL_CITY,
    FLIGHT_ARRIVAL_COUNTRY,
    FLIGHT_ARRIVAL_DATE,
    FLIGHT_DEPARTURE_CITY,
    FLIGHT_DEPARTURE_COUNTRY,
    FLIGHT_DEPARTURE_DATE,
    FLIGHT_ID,
    FLIGHT_SETTINGS,
    LIMIT,
    OFFSET,
)
from flights.models import Flight
from flights.serializers import FlightSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список рейсов",
        description="Получение списка всех рейсов",
        tags=[FLIGHT_SETTINGS["name"]],
        parameters=[
            LIMIT,
            OFFSET,
            FLIGHT_DEPARTURE_COUNTRY,
            FLIGHT_DEPARTURE_CITY,
            FLIGHT_DEPARTURE_DATE,
            FLIGHT_ARRIVAL_COUNTRY,
            FLIGHT_ARRIVAL_CITY,
            FLIGHT_ARRIVAL_DATE,
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
        tags=[FLIGHT_SETTINGS["name"]],
        responses={
            201: FlightSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о рейсе",
        description="Получение информации о рейсе через идентификатор",
        tags=[FLIGHT_SETTINGS["name"]],
        parameters=[FLIGHT_ID],
        responses={
            200: FlightSerializer,
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление рейса",
        description="Обновление всех полей рейса",
        request=FlightSerializer,
        tags=[FLIGHT_SETTINGS["name"]],
        parameters=[FLIGHT_ID],
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
        tags=[FLIGHT_SETTINGS["name"]],
        parameters=[FLIGHT_ID],
        responses={
            200: FlightSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Рейс не найден"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление рейса",
        description="Полное удаление рейса",
        tags=[FLIGHT_SETTINGS["name"]],
        parameters=[FLIGHT_ID],
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
        "flight_number",
    )
