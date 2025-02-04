from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from rest_framework import viewsets
from hotels.models.room.models_room_amenity import RoomAmenity
from hotels.serializers.room.serializers_room import AmenityRoomSerializer


# Удобства в номере
@extend_schema_view(
    list=extend_schema(
        summary="Список удобств в номере",
        description="Получение списка всех удобств в номере с пагинацией",
        responses={
            200: AmenityRoomSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["Удобства в номере"],
    ),
    create=extend_schema(
        summary="Добавление удобства в номере",
        description="Создание нового удобства в номере",
        request=AmenityRoomSerializer,
        responses={
            201: AmenityRoomSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["Удобства в номере"],
    ),
    retrieve=extend_schema(
        summary="Детали удобства в номере",
        description="Получение информации удобства в номере",
        responses={
            200: AmenityRoomSerializer,
            404: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["Удобства в номере"],
    ),
    update=extend_schema(
        summary="Полное обновление удобства в номере",
        description="Обновление всех полей удобств в номере",
        request=AmenityRoomSerializer,
        responses={
            200: AmenityRoomSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Удобство в номере не найдено"),
        },
        tags=["Удобства в номере"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление удобства в номере",
        description="Обновление отдельных полей удобств в номере",
        request=AmenityRoomSerializer,
        responses={
            200: AmenityRoomSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Удобство в номере не найдено"),
        },
        tags=["Удобства в номере"],
    ),
    destroy=extend_schema(
        summary="Удаление удобства в номере",
        description="Полное удаление удобства в номере",
        responses={
            204: OpenApiResponse(description="Удобство в номере удалено"),
            404: OpenApiResponse(description="Удобство в номере не найдено"),
        },
        tags=["Удобства в номере"],
    ),
)
class RoomAmenityViewSet(viewsets.ModelViewSet):
    queryset = RoomAmenity.objects.all()
    serializer_class = AmenityRoomSerializer
    pagination_class = None

