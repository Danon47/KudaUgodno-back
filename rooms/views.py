from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.fixture_views import (
    hotel_id,
    id_room,
    limit,
    offset,
    room_date_id,
    room_date_settings,
    room_id,
    room_id_photo,
    room_photo_settings,
    room_settings,
)
from all_fixture.pagination import CustomLOPagination
from hotels.models import Hotel
from rooms.models import Room, RoomDate, RoomPhoto, RoomRules
from rooms.serializers import (
    RoomBaseSerializer,
    RoomDateListSerializer,
    RoomDetailSerializer,
    RoomPhotoSerializer,
    RoomRulesSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Список номеров",
        description="Получение списка всех номеров с пагинацией",
        parameters=[hotel_id, limit, offset],
        responses={
            200: RoomDetailSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление номера",
        description="Создание нового номера",
        request=RoomBaseSerializer,
        parameters=[hotel_id],
        responses={
            201: RoomBaseSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали номера",
        description="Получение информации о номере",
        parameters=[hotel_id, id_room],
        responses={
            200: RoomDetailSerializer,
            404: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_settings["name"]],
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
        tags=[room_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление номера",
        description="Полное удаление номера",
        parameters=[hotel_id, id_room],
        responses={
            204: OpenApiResponse(description="Номер удален"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=[room_settings["name"]],
    ),
)
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.none()
    pagination_class = CustomLOPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = None

    def get_serializer_class(self):
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
        hotel = get_object_or_404(Hotel, id=self.kwargs["hotel_id"])
        # Сохраняем Room с привязкой к Hotel
        serializer.save(hotel=hotel)


@extend_schema_view(
    list=extend_schema(
        summary="Список номеров",
        description="Получение списка всех номеров с пагинацией",
        parameters=[limit, offset, hotel_id],
        responses={
            200: RoomDateListSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_date_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление номера",
        description="Создание нового номера",
        request=RoomDateListSerializer,
        parameters=[hotel_id],
        responses={
            201: RoomDateListSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_date_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали номера",
        description="Получение информации о номере",
        parameters=[hotel_id, room_date_id],
        responses={
            200: RoomDateListSerializer,
            404: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[room_date_settings["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление номера",
        description="Обновление всех полей номера",
        request=RoomDateListSerializer,
        parameters=[hotel_id, room_date_id],
        responses={
            200: RoomDateListSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=[room_date_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление номера",
        description="Полное удаление номера",
        parameters=[hotel_id, room_date_id],
        responses={
            204: OpenApiResponse(description="Номер удален"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=[room_date_settings["name"]],
    ),
)
class RoomDateViewSet(viewsets.ModelViewSet):
    queryset = RoomDate.objects.none()
    pagination_class = CustomLOPagination
    serializer_class = RoomDateListSerializer

    def get_queryset(self):
        # Получаем ID отеля из URL параметров
        hotel_id = self.kwargs["hotel_id"]

        # Фильтруем Room по связи с Hotel
        return RoomDate.objects.filter(categories__room__hotel_id=hotel_id).distinct()


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
class RoomPhotoViewSet(viewsets.ModelViewSet):
    queryset = RoomPhoto.objects.none()
    serializer_class = RoomPhotoSerializer
    pagination_class = CustomLOPagination

    def get_queryset(self):
        room_id = self.kwargs["room_id"]
        return RoomPhoto.objects.filter(room_id=room_id)

    def perform_create(self, serializer):
        room = get_object_or_404(Room, id=self.kwargs["room_id"])
        serializer.save(room=room)


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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
