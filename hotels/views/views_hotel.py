from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from hotels.models.models_hotel import Hotel
from hotels.models.models_hotel_amenity import HotelAmenity
from hotels.models.models_hotel_photo import HotelPhoto
from hotels.serializers.serializers_hotel import (
    AmenityHotelSerializer,
    HotelPhotoSerializer,
    HotelBaseSerializer,
    HotelDetailSerializer
)


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
                name="hotel_pk",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_STRING,
                description="ID комнаты в базе данных",
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

    def perform_create(self, serializer):
        hotel = Hotel.objects.get(pk=self.kwargs['hotel_pk'])
        serializer.save(hotel=hotel)

