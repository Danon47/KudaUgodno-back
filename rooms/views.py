from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.pagination import CustomLOPagination
from all_fixture.views_fixture import (
    HOTEL_ID,
    ID_ROOM,
    LIMIT,
    OFFSET,
    ROOM_ID,
    ROOM_ID_PHOTO,
    ROOM_PHOTO_SETTINGS,
    ROOM_SETTINGS,
)
from hotels.models import Hotel
from rooms.filters import RoomFilter
from rooms.models import Room, RoomPhoto, RoomRules
from rooms.serializers import (
    RoomBaseSerializer,
    RoomDetailSerializer,
    RoomPhotoSerializer,
    RoomRulesSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Список номеров",
        description="Получение списка всех номеров с пагинацией",
        parameters=[HOTEL_ID, LIMIT, OFFSET],
        responses={
            200: RoomDetailSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[ROOM_SETTINGS["name"]],
    ),
    create=extend_schema(
        summary="Добавление номера",
        description="Создание нового номера",
        request=RoomBaseSerializer,
        parameters=[HOTEL_ID],
        responses={
            201: RoomBaseSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[ROOM_SETTINGS["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали номера",
        description="Получение информации о номере",
        parameters=[HOTEL_ID, ID_ROOM],
        responses={
            200: RoomDetailSerializer,
            404: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[ROOM_SETTINGS["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление номера",
        description="Обновление всех полей номера",
        request=RoomBaseSerializer,
        parameters=[HOTEL_ID, ID_ROOM],
        responses={
            200: RoomBaseSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=[ROOM_SETTINGS["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление номера",
        description="Полное удаление номера",
        parameters=[HOTEL_ID, ID_ROOM],
        responses={
            204: OpenApiResponse(description="Номер удален"),
            404: OpenApiResponse(description="Номер не найден"),
        },
        tags=[ROOM_SETTINGS["name"]],
    ),
)
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.none()
    pagination_class = CustomLOPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RoomFilter

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
        summary="Список фотографий номера",
        description="Получение списка всех фотографий номера с пагинацией",
        parameters=[LIMIT, OFFSET, ROOM_ID],
        responses={
            200: RoomPhotoSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[ROOM_PHOTO_SETTINGS["name"]],
    ),
    create=extend_schema(
        summary="Добавление фотографии номера",
        description="Создание новой фотографии номера",
        parameters=[ROOM_ID],
        request={
            "multipart/form-data": RoomPhotoSerializer,  # Указываем формат данных
        },
        responses={
            201: RoomPhotoSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[ROOM_PHOTO_SETTINGS["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление фотографии номера",
        description="Полное удаление фотографии номера",
        parameters=[ROOM_ID, ROOM_ID_PHOTO],
        responses={
            204: OpenApiResponse(description="Фотография номера удалена"),
            404: OpenApiResponse(description="Фотография номера не найдена"),
        },
        tags=[ROOM_PHOTO_SETTINGS["name"]],
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
        parameters=[LIMIT, OFFSET],
        responses={
            200: RoomRulesSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[ROOM_PHOTO_SETTINGS["name"]],
    ),
    create=extend_schema(
        summary="Добавление фотографии номера",
        description="Создание новой фотографии номера",
        parameters=[ROOM_ID],
        request={
            "multipart/form-data": RoomRulesSerializer,  # Указываем формат данных
        },
        responses={
            201: RoomRulesSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[ROOM_PHOTO_SETTINGS["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление фотографии номера",
        description="Полное удаление фотографии номера",
        parameters=[],
        responses={
            204: OpenApiResponse(description="Фотография номера удалена"),
            404: OpenApiResponse(description="Фотография номера не найдена"),
        },
        tags=[ROOM_PHOTO_SETTINGS["name"]],
    ),
)
class RoomRulesViewSet(viewsets.ModelViewSet):
    queryset = RoomRules.objects.all()
    serializer_class = RoomRulesSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
