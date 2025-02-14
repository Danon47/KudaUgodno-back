from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import viewsets

from all_fixture.fixture_views import id_room_category, room_category_settings, limit, offset
from all_fixture.pagination import CustomLOPagination
from hotels.models.room.models_room_category import RoomCategory
from hotels.serializers.room.serializers_room_category import RoomCategorySerializer


# Категории номеров
@extend_schema_view(
    list=extend_schema(
        summary="Список категорий номеров",
        description="Получение списка всех категорий в номере",
        parameters=[limit, offset],
        responses={
            200: RoomCategorySerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_category_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление категории номера",
        description="Создание новой категории номера",
        request=RoomCategorySerializer,
        responses={
            201: RoomCategorySerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_category_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали категорий номеров",
        description="Получение информации категорий номеров",
        parameters=[id_room_category],
        responses={
            200: RoomCategorySerializer,
            404: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_category_settings["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление категорий в номере",
        description="Обновление всех полей категорий в номере",
        request=RoomCategorySerializer,
        responses={
            200: RoomCategorySerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Категория номера не найдена"),
        },
        tags=[room_category_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление категории номера",
        description="Полное удаление категории номера",
        responses={
            204: OpenApiResponse(description="Категория номера удалено"),
            404: OpenApiResponse(description="Категория номера не найдена"),
        },
        tags=[room_category_settings["name"]],
    ),
)
class RoomCategoryViewSet(viewsets.ModelViewSet):
    queryset = RoomCategory.objects.all()
    serializer_class = RoomCategorySerializer
    pagination_class = CustomLOPagination
    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']  # Исключаем 'patch'
