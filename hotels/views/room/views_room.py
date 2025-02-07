from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
)
from rest_framework import viewsets
from hotels.models.hotel.models_hotel import Hotel
from all_fixture.fixture_views import (
    hotel_id,
    offset,
    limit,
    id_room,
    tags_room_settings,
)
from hotels.models.room.models_room import Room
from hotels.serializers.room.serializers_room import (
    RoomBaseSerializer,
    RoomDetailSerializer,
)


# Номер
@extend_schema_view(
    list=extend_schema(
        summary="Список номеров",
        description="Получение списка всех номеров с пагинацией",
        parameters=[limit, offset, hotel_id],
        responses={
            200: RoomDetailSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[tags_room_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление номера",
        description="Создание нового отеля",
        request=RoomBaseSerializer,
        parameters=[hotel_id],
        responses={
            201: RoomBaseSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[tags_room_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали номера",
        description="Получение информации о номере",
        parameters=[hotel_id, id_room],
        responses={
            200: RoomDetailSerializer,
            404: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[tags_room_settings["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление номера",
        description="Обновление всех полей номера",
        request=RoomBaseSerializer,
        parameters=[hotel_id, id_room],
        responses={
            200: RoomBaseSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=[tags_room_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление номера",
        description="Полное удаление номера",
        parameters=[hotel_id, id_room],
        responses={
            204: OpenApiResponse(description="Номер удален"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=[tags_room_settings["name"]],
    ),
)
class RoomViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        # Исправляем проверку действия
        if self.action in ["create", "update", "partial_update"]:
            return RoomBaseSerializer
        return RoomDetailSerializer

    def get_queryset(self):
        # Получаем ID отеля из URL параметров
        hotel_id = self.kwargs["hotel_id"]

        # Фильтруем Room по связи с Hotel
        return Room.objects.filter(hotel__id=hotel_id)

    def perform_create(self, serializer):
        # Получаем объект Hotel по ID
        hotel = Hotel.objects.get(id=self.kwargs["hotel_id"])
        # Сохраняем Room с привязкой к Hotel
        serializer.save(hotel=hotel)
