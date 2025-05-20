from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from all_fixture.fixture_views import limit, offset, room_id, room_photo_settings
from hotels.models.room.rules.models_room_rules import RoomRules
from hotels.serializers.room.rules.serializers_room_rules import RoomRulesSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список фотографий номера",
        description="Получение списка всех фотографий номера с пагинацией",
        parameters=[limit, offset],
        responses={
            200: RoomRulesSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_photo_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление фотографии номера",
        description="Создание новой фотографии номера",
        parameters=[room_id],
        request={
            "multipart/form-data": RoomRulesSerializer,  # Указываем формат данных
        },
        responses={
            201: RoomRulesSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_photo_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление фотографии номера",
        description="Полное удаление фотографии номера",
        parameters=[],
        responses={
            204: OpenApiResponse(description="Фотография номера удалена"),
            404: OpenApiResponse(description="Фотография номера не найдена"),
        },
        tags=[room_photo_settings["name"]],
    ),
)
class RoomRulesViewSet(viewsets.ModelViewSet):
    queryset = RoomRules.objects.all()
    serializer_class = RoomRulesSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
