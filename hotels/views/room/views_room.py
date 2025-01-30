from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from hotels.models.room.models_room import Room
from hotels.serializers.room.serializers_room import RoomBaseSerializer, RoomDetailSerializer


# Номер
@extend_schema_view(
    list=extend_schema(
        summary="Список номеров",
        description="Получение списка всех номеров с пагинацией",
        parameters=[
            OpenApiParameter(
                name="limit",
                type=int,
                description="Количество номеров для возврата на страницу",
                required=False,
                examples=[
                    OpenApiExample("Пример 1", value=10),
                    OpenApiExample("Пример 2", value=20),
                ],
            ),
            OpenApiParameter(
                name="offset",
                type=int,
                description="Начальный индекс для пагинации",
                required=False,
            ),
        ],
        responses={
            200: RoomDetailSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["3.2 Номер"],
    ),
    create=extend_schema(
        summary="Добавление номера",
        description="Создание нового отеля",
        request=RoomBaseSerializer,
        responses={
            201: RoomBaseSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["3.2 Номер"],
    ),
    retrieve=extend_schema(
        summary="Детали номера",
        description="Получение информации о номере",
        responses={
            200: RoomDetailSerializer,
            404: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["3.2 Номер"],
    ),
    update=extend_schema(
        summary="Полное обновление номера",
        description="Обновление всех полей номера",
        request=RoomBaseSerializer,
        responses={
            200: RoomBaseSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=["3.2 Номер"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление номера",
        description="Обновление отдельных полей номера",
        request=RoomBaseSerializer,
        responses={
            200: RoomBaseSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=["3.2 Номер"],
    ),
    destroy=extend_schema(
        summary="Удаление номера",
        description="Полное удаление номера",
        responses={
            204: OpenApiResponse(description="Номер удален"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=["3.2 Номер"],
    ),
)
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related("category", "hotel").prefetch_related("amenities", "meal", "room_photos")
    # parser_classes = [MultiPartParser, FormParser]

    def get_serializer_class(self):
        if self.action == ["create", "update", "partial_update"]:
            return RoomBaseSerializer
        return RoomDetailSerializer
