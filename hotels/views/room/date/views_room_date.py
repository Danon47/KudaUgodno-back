from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.fixture_views import hotel_id, limit, offset, room_date_id, room_date_settings
from all_fixture.pagination import CustomLOPagination
from hotels.models.room.date.models_room_date import RoomDate
from hotels.serializers.room.date.serializers_room_date import RoomDateDetailSerializer, RoomDateListSerializer


# Номер
@extend_schema_view(
    list=extend_schema(
        summary="Список номеров",
        description="Получение списка всех номеров с пагинацией",
        parameters=[limit, offset, hotel_id],
        responses={
            200: RoomDateListSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_date_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление номера",
        description="Создание нового номера",
        request=RoomDateListSerializer,
        parameters=[hotel_id],
        responses={
            201: RoomDateListSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_date_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали номера",
        description="Получение информации о номере",
        parameters=[hotel_id, room_date_id],
        responses={
            200: RoomDateListSerializer,
            404: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_date_settings["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление номера",
        description="Обновление всех полей номера",
        request=RoomDateListSerializer,
        parameters=[hotel_id, room_date_id],
        responses={
            200: RoomDateListSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=[room_date_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление номера",
        description="Полное удаление номера",
        parameters=[hotel_id, room_date_id],
        responses={
            204: OpenApiResponse(description="Номер удален"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=[room_date_settings["name"]],
    ),
)
class RoomDateViewSet(viewsets.ModelViewSet):
    pagination_class = CustomLOPagination

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return RoomDateListSerializer
        return RoomDateDetailSerializer

    def get_queryset(self):
        # Получаем ID отеля из URL параметров
        hotel_id = self.kwargs["hotel_id"]

        # Фильтруем Room по связи с Hotel
        return RoomDate.objects.filter(categories__room__hotel_id=hotel_id).distinct()
