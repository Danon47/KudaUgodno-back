from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
)
from rest_framework import viewsets
from all_fixture.fixture_views import id_room_amenity, tags_room_amenity_settings
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
        tags=[tags_room_amenity_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление удобства в номере",
        description="Создание нового удобства в номере",
        request=AmenityRoomSerializer,
        responses={
            201: AmenityRoomSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[tags_room_amenity_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали удобства в номере",
        description="Получение информации удобства в номере",
        parameters=[id_room_amenity],
        responses={
            200: AmenityRoomSerializer,
            404: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[tags_room_amenity_settings["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление удобства в номере",
        description="Обновление всех полей удобств в номере",
        parameters=[id_room_amenity],
        request=AmenityRoomSerializer,
        responses={
            200: AmenityRoomSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Удобство в номере не найдено"),
        },
        tags=[tags_room_amenity_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление удобства в номере",
        description="Полное удаление удобства в номере",
        parameters=[id_room_amenity],
        responses={
            204: OpenApiResponse(description="Удобство в номере удалено"),
            404: OpenApiResponse(description="Удобство в номере не найдено"),
        },
        tags=[tags_room_amenity_settings["name"]],
    ),
)
class RoomAmenityViewSet(viewsets.ModelViewSet):
    queryset = RoomAmenity.objects.all()
    serializer_class = AmenityRoomSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']  # Исключаем 'patch'
