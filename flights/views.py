from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import viewsets

from flights.models import Flight
from flights.serializers import FlightSerializer

parameters_tour = [
    OpenApiParameter(
        location=OpenApiParameter.PATH,
        name="id",
        type=int,
        description="Уникальное целочисленное значение, идентифицирующее данный Рейс",
        required=True,
    ),
]

tags_flight = ["Рейсы"]


@extend_schema_view(
    list=extend_schema(
        summary="Список рейсов",
        description="Получение списка всех рейсов",
        tags=tags_flight,
        parameters=[
            OpenApiParameter(
                name="limit",
                type=int,
                description="Количество рейсов для возврата на страницу",
                required=False,
            ),
            OpenApiParameter(
                name="offset",
                type=int,
                description="Начальный индекс для пагинации",
                required=False,
            ),
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
        tags=tags_flight,
        responses={
            201: FlightSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о рейсе",
        description="Получение информации о рейсе через идентификатор",
        tags=tags_flight,
        parameters=parameters_tour,
        responses={
            200: FlightSerializer,
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление рейса",
        description="Обновление всех полей рейса",
        request=FlightSerializer,
        tags=tags_flight,
        parameters=parameters_tour,
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
        tags=tags_flight,
        parameters=parameters_tour,
        responses={
            200: FlightSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Рейс не найден"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление рейса",
        description="Полное удаление рейса",
        tags=tags_flight,
        parameters=parameters_tour,
        responses={
            204: OpenApiResponse(description="Рейса удален"),
            404: OpenApiResponse(description="Рейс не найден"),
        },
    ),
)
class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
