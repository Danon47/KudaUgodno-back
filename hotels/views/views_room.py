from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from hotels.models.models_room import Room
from hotels.models.models_room_amenity import RoomAmenity
from hotels.models.models_room_caterogy import RoomCategory
from hotels.models.models_room_photo import RoomPhoto
from hotels.serializers.serializers_room import (
    AmenityRoomSerializer,
    CategoryRoomSerializer,
    RoomPhotoSerializer,
    RoomBaseSerializer,
    RoomDetailSerializer,
)


class RoomListCreateAPIView(generics.ListCreateAPIView):
    queryset = Room.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return RoomBaseSerializer
        return RoomDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @swagger_auto_schema(
        operation_description="Получение списка всех номеров",
        operation_summary="Список номеров",
        tags=["3.1 Номер"],
        manual_parameters=[
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Количество номеров для возврата на страницу",
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Начальный индекс, из которого возвращаются результаты",
            ),
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение списка номеров",
                schema=RoomDetailSerializer(many=True),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание нового номера",
        operation_summary="Добавление номера",
        tags=["3.1 Номер"],
        request_body=RoomBaseSerializer,
        responses={
            201: openapi.Response(
                description="Отель успешно номера", schema=RoomDetailSerializer()
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RoomDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return RoomBaseSerializer
        return RoomDetailSerializer

    @swagger_auto_schema(
        operation_summary="Получение детальной информации о номере",
        operation_description="Возвращает полную информацию о конкретном номере по его идентификатору",
        tags=["3.1 Номер"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор номера в базе данных",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение информации о номере",
                schema=RoomDetailSerializer(),
            ),
            404: "Номер не найден",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление информации о номере",
        operation_description="Обновляет все поля номера целиком",
        tags=["3.1 Номер"],
        request_body=RoomBaseSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор номера в базе данных",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Номер успешно обновлен", schema=RoomBaseSerializer()
            ),
            400: "Ошибка валидации",
            404: "Номер не найден",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление информации о номере",
        operation_description="Обновляет указанные поля номера",
        tags=["3.1 Номер"],
        request_body=RoomBaseSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор номера в базе данных",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Номер успешно обновлен", schema=RoomBaseSerializer()
            ),
            400: "Ошибка валидации",
            404: "Номер не найден",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление номера",
        operation_description="Полное удаление номера по его идентификатору",
        tags=["3.1 Номер"],
        responses={204: "Номер успешно удален", 404: "Номер не найден"},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор отеля в базе данных",
                required=True,
            )
        ],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class RoomAmenityCreateAPIView(generics.CreateAPIView):
    queryset = RoomAmenity.objects.all()
    serializer_class = AmenityRoomSerializer

    @swagger_auto_schema(
        operation_description="Создание нового удобства в номере",
        operation_summary="Добавление удобств в номере",
        request_body=AmenityRoomSerializer,
        tags=["3.1 Номер"],
        responses={
            201: openapi.Response(
                description="Удобство в номере успешно создан",
                schema=AmenityRoomSerializer(),
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RoomCategoryCreateAPIView(generics.CreateAPIView):
    queryset = RoomCategory.objects.all()
    serializer_class = CategoryRoomSerializer

    @swagger_auto_schema(
        operation_description="Создание новой категории номера",
        operation_summary="Добавление категории номера",
        request_body=CategoryRoomSerializer,
        tags=["3.1 Номер"],
        responses={
            201: openapi.Response(
                description="Категория номера успешно создана",
                schema=CategoryRoomSerializer(),
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RoomPhotoCreateAPIView(generics.CreateAPIView):
    queryset = RoomPhoto.objects.all()
    serializer_class = RoomPhotoSerializer
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    @swagger_auto_schema(
        operation_description="Создание новых фотографий номера",
        operation_summary="Добавление фотографий номера",
        request_body=RoomPhotoSerializer,
        tags=["3.1 Номер"],
        manual_parameters=[
            openapi.Parameter(
                name="room_pk",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description="ID комнаты в базе данных",
                required=True,
            )
        ],
        responses={
            201: openapi.Response(
                description="Фотографии номера успешно созданы",
                schema=RoomPhotoSerializer(),
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        room = Room.objects.get(pk=self.kwargs['room_pk'])
        serializer.save(room=room)
