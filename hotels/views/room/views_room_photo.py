from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from hotels.models.room.models_room import Room
from hotels.models.room.models_room_photo import RoomPhoto
from hotels.serializers.room.serializers_room import RoomPhotoSerializer

@extend_schema_view(
    list=extend_schema(
        summary="Список фотографий номера",
        description="Получение списка всех фотографий номера с пагинацией",
        parameters=[
            OpenApiParameter(
                name="room_id",
                type=int,
                location=OpenApiParameter.PATH,  # Параметр передается в URL
                description="ID номера, у которого получаем список всех фотографий",
                required=True,
            ),
        ],
        responses={
            200: RoomPhotoSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["3.2.3 Фотографии номера"],
    ),
    create=extend_schema(
        summary="Добавление фотографии номера",
        description="Создание новой фотографии номера",
        parameters=[
            OpenApiParameter(
                name="room_id",
                type=int,
                location=OpenApiParameter.PATH,  # Параметр передается в URL
                description="ID номера, к которому добавляется фотография",
                required=True,
            ),
        ],
        request={
            "multipart/form-data": RoomPhotoSerializer,  # Указываем формат данных
        },
        responses={
            201: RoomPhotoSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["3.2.3 Фотографии номера"],
    ),
    destroy=extend_schema(
        summary="Удаление фотографии номера",
        description="Полное удаление фотографии номера",
        parameters=[
            OpenApiParameter(
                name="room_id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID номера, у которого удаляется фотография",
                required=True,
            ),
            OpenApiParameter(
                name="id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID фотографий номера, которая удаляется",
                required=True,
            ),
        ],
        responses={
            204: OpenApiResponse(description="Фотография номера удалена"),
            404: OpenApiResponse(description="Фотография номера не найдена"),
        },
        tags=["3.2.3 Фотографии номера"],
    ),
)
class RoomPhotoViewSet(CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = RoomPhotoSerializer
    pagination_class = None

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return RoomPhoto.objects.filter(room_id=room_id)

    def perform_create(self, serializer):
        room = get_object_or_404(Room, id=self.kwargs["room_id"])
        serializer.save(room=room)
