from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import viewsets
from hotels.models.room.models_room_category import RoomCategory
from hotels.serializers.room.serializers_room_category import CategoryRoomSerializer

# Категории номеров
@extend_schema_view(
    list=extend_schema(
        summary="Список категорий номеров",
        description="Получение списка всех категорий в номере с пагинацией",
        responses={
            200: CategoryRoomSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["Категории номера"],
    ),
    create=extend_schema(
        summary="Добавление категории номера",
        description="Создание новой категории номера",
        request=CategoryRoomSerializer,
        responses={
            201: CategoryRoomSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["Категории номера"],
    ),
    retrieve=extend_schema(
        summary="Детали категорий номеров",
        description="Получение информации категорий номеров",
        responses={
            200: CategoryRoomSerializer,
            404: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["Категории номера"],
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
        tags=["Категории номера"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление категории в номере",
        description="Обновление отдельных полей категории в номере",
        request=CategoryRoomSerializer,
        responses={
            200: CategoryRoomSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Категория номера не найдена"),
        },
        tags=["Категории номера"],
    ),
    destroy=extend_schema(
        summary="Удаление категории номера",
        description="Полное удаление категории номера",
        responses={
            204: OpenApiResponse(description="Категория номера удалено"),
            404: OpenApiResponse(description="Категория номера не найдена"),
        },
        tags=["Категории номера"],
    ),
)
class RoomCategoryViewSet(viewsets.ModelViewSet):
    queryset = RoomCategory.objects.all()
    serializer_class = CategoryRoomSerializer
    pagination_class = None
