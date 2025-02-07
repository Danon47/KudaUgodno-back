from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import viewsets

from all_fixture.fixture_views import id_room_category, tags_room_category_settings
from hotels.models.room.models_room_category import RoomCategory
from hotels.serializers.room.serializers_room_category import CategoryRoomSerializer


# Категории номеров
@extend_schema_view(
    list=extend_schema(
        summary="Список категорий номеров",
        description="Получение списка всех категорий в номере",
        responses={
            200: CategoryRoomSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[tags_room_category_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление категории номера",
        description="Создание новой категории номера",
        request=CategoryRoomSerializer,
        responses={
            201: CategoryRoomSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[tags_room_category_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали категорий номеров",
        description="Получение информации категорий номеров",
        parameters=[id_room_category],
        responses={
            200: CategoryRoomSerializer,
            404: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[tags_room_category_settings["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление категорий в номере",
        description="Обновление всех полей категорий в номере",
        request=CategoryRoomSerializer,
        responses={
            200: CategoryRoomSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Категория номера не найдена"),
        },
        tags=[tags_room_category_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление категории номера",
        description="Полное удаление категории номера",
        responses={
            204: OpenApiResponse(description="Категория номера удалено"),
            404: OpenApiResponse(description="Категория номера не найдена"),
        },
        tags=[tags_room_category_settings["name"]],
    ),
)
class RoomCategoryViewSet(viewsets.ModelViewSet):
    queryset = RoomCategory.objects.all()
    serializer_class = CategoryRoomSerializer
    pagination_class = None
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']  # Исключаем 'patch'
