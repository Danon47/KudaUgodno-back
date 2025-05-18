from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from all_fixture.fixture_views import limit, offset, room_id, room_id_photo, room_photo_settings
from all_fixture.pagination import CustomLOPagination
from hotels.models.room.models_room import Room
from hotels.models.room.photo.models_room_photo import RoomPhoto
from hotels.serializers.room.serializers_room import RoomPhotoSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список фотографий номера",
        description="Получение списка всех фотографий номера с пагинацией",
        parameters=[limit, offset, room_id],
        responses={
            200: RoomPhotoSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_photo_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление фотографии номера",
        description="Создание новой фотографии номера",
        parameters=[room_id],
        request={
            "multipart/form-data": RoomPhotoSerializer,  # Указываем формат данных
        },
        responses={
            201: RoomPhotoSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_photo_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление фотографии номера",
        description="Полное удаление фотографии номера",
        parameters=[room_id, room_id_photo],
        responses={
            204: OpenApiResponse(description="Фотография номера удалена"),
            404: OpenApiResponse(description="Фотография номера не найдена"),
        },
        tags=[room_photo_settings["name"]],
    ),
)
class RoomPhotoViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = RoomPhoto.objects.none()
    serializer_class = RoomPhotoSerializer
    pagination_class = CustomLOPagination

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return RoomPhoto.objects.filter(room_id=room_id)

    def perform_create(self, serializer):
        room = get_object_or_404(Room, id=self.kwargs["room_id"])
        serializer.save(room=room)
