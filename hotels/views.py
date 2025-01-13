from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser

from .models import (
    Hotel,
    Room,
    RoomAmenity,
    HotelAmenity,
    RoomCategory,
    HotelPhoto,
    RoomPhoto,
)
from .serializers import (
    HotelBaseSerializer,
    HotelDetailSerializer,
    HotelPhotoSerializer,
    AmenityHotelSerializer,
    RoomBaseSerializer,
    RoomDetailSerializer,
    RoomPhotoSerializer,
    AmenityRoomSerializer,
    CategoryRoomSerializer,
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


class HotelListCreateAPIView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return HotelBaseSerializer
        return HotelDetailSerializer

    @swagger_auto_schema(
        operation_description="Получение списка всех отелей",
        operation_summary="Список отелей",
        tags=["3. Отель"],
        manual_parameters=[
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Количество отелей для возврата на страницу",
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
                description="Успешное получение списка отелей",
                schema=HotelDetailSerializer(many=True),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание нового отеля",
        operation_summary="Добавление отеля",
        request_body=HotelBaseSerializer,
        tags=["3. Отель"],
        responses={
            201: openapi.Response(
                description="Отель успешно создан", schema=HotelBaseSerializer()
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class HotelDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return HotelBaseSerializer
        return HotelDetailSerializer

    @swagger_auto_schema(
        operation_summary="Получение детальной информации об отеле",
        operation_description="Возвращает полную информацию о конкретном отеле по его идентификатору",
        tags=["3. Отель"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор отеля в базе данных",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение информации об отеле",
                schema=HotelDetailSerializer(),
            ),
            404: "Отель не найден",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление информации об отеле",
        operation_description="Обновляет все поля отеля целиком",
        tags=["3. Отель"],
        request_body=HotelBaseSerializer,
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
                description="Отель успешно обновлен", schema=HotelBaseSerializer()
            ),
            400: "Ошибка валидации",
            404: "Отель не найден",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление информации об отеле",
        operation_description="Обновляет указанные поля отеля",
        tags=["3. Отель"],
        request_body=HotelBaseSerializer,
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
                description="Отель успешно обновлен", schema=HotelBaseSerializer()
            ),
            400: "Ошибка валидации",
            404: "Отель не найден",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление отеля",
        operation_description="Полное удаление отеля по его идентификатору",
        tags=["3. Отель"],
        responses={204: "Отель успешно удален", 404: "Отель не найден"},
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


class HotelAmenityCreateAPIView(generics.CreateAPIView):
    queryset = HotelAmenity.objects.all()
    serializer_class = AmenityHotelSerializer

    @swagger_auto_schema(
        operation_description="Создание нового удобства в отеле",
        operation_summary="Добавление удобств в отеле",
        request_body=AmenityHotelSerializer,
        tags=["3. Отель"],
        responses={
            201: openapi.Response(
                description="Удобство в отеле успешно создано",
                schema=AmenityHotelSerializer(),
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class HotelPhotoCreateAPIView(generics.CreateAPIView):
    queryset = HotelPhoto.objects.all()
    serializer_class = HotelPhotoSerializer
    parser_classes = (
        MultiPartParser,
        FormParser,
    )

    @swagger_auto_schema(
        operation_description="Создание новых фотографий отеля",
        operation_summary="Добавление фотографий отеля",
        request_body=HotelPhotoSerializer,
        tags=["3. Отель"],
        manual_parameters=[
            openapi.Parameter(
                name="hotel",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                description="ID Отеля в базе данных",
                required=True,
            )
        ],
        responses={
            201: openapi.Response(
                description="Фотографии отеля успешно созданы",
                schema=HotelPhotoSerializer(),
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
                name="room",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
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
