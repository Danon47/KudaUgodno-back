from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .models import (
    Hotel,
    Room,
    AmenityRoom,
    AmenityHotel,
    CategoryRoom,
)
from .pagination import MyPagination
from .serializers import (
    HotelSerializer,
    RoomSerializer,
    AmenityRoomSerializer,
    AmenityHotelSerializer,
    CategoryRoomSerializer,
)


class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = MyPagination

    @swagger_auto_schema(
        operation_description="Получение списка всех номеров",
        operation_summary="Список номеров",
        tags=["1. Номер"],
        responses={
            200: openapi.Response(
                description="Успешное получение списка номеров",
                schema=RoomSerializer(many=True),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание нового номера",
        operation_summary="Добавление номера",
        request_body=RoomSerializer,
        tags=["1. Номер"],
        responses={
            201: openapi.Response(
                description="Отель успешно номера", schema=RoomSerializer()
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    pagination_class = MyPagination

    @swagger_auto_schema(
        operation_summary="Получение детальной информации о номере",
        operation_description="Возвращает полную информацию о конкретном номере по его идентификатору",
        tags=["1. Номер"],
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
                schema=HotelSerializer(),
            ),
            404: "Номер не найден",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление информации о номере",
        operation_description="Обновляет все поля номера целиком",
        tags=["1. Номер"],
        request_body=RoomSerializer,
        responses={
            200: openapi.Response(
                description="Номер успешно обновлен", schema=RoomSerializer()
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
        tags=["1. Номер"],
        request_body=RoomSerializer,
        responses={
            200: openapi.Response(
                description="Номер успешно обновлен", schema=RoomSerializer()
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
        tags=["1. Номер"],
        responses={204: "Номер успешно удален", 404: "Номер не найден"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class AmenityRoomCreateAPIView(generics.CreateAPIView):
    queryset = AmenityRoom.objects.all()
    serializer_class = AmenityRoomSerializer

    @swagger_auto_schema(
        operation_description="Создание нового удобства в номере",
        operation_summary="Добавление удобства в номере",
        request_body=AmenityRoomSerializer,
        tags=["1. Номер"],
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


class CategoryRoomCreateAPIView(generics.CreateAPIView):
    queryset = CategoryRoom.objects.all()
    serializer_class = CategoryRoomSerializer

    @swagger_auto_schema(
        operation_description="Создание новой категории номера",
        operation_summary="Добавление категории номера",
        request_body=CategoryRoomSerializer,
        tags=["1. Номер"],
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


class HotelListCreateView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    pagination_class = MyPagination

    @swagger_auto_schema(
        operation_description="Получение списка всех отелей",
        operation_summary="Список отелей",
        tags=["2. Отель"],
        responses={
            200: openapi.Response(
                description="Успешное получение списка отелей",
                schema=HotelSerializer(many=True),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание нового отеля",
        operation_summary="Добавление отеля",
        request_body=HotelSerializer,
        tags=["2. Отель"],
        responses={
            201: openapi.Response(
                description="Отель успешно создан", schema=HotelSerializer()
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    pagination_class = MyPagination

    @swagger_auto_schema(
        operation_summary="Получение детальной информации об отеле",
        operation_description="Возвращает полную информацию о конкретном отеле по его идентификатору",
        tags=["2. Отель"],
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
                schema=HotelSerializer(),
            ),
            404: "Отель не найден",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление информации об отеле",
        operation_description="Обновляет все поля отеля целиком",
        tags=["2. Отель"],
        request_body=HotelSerializer,
        responses={
            200: openapi.Response(
                description="Отель успешно обновлен", schema=HotelSerializer()
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
        tags=["2. Отель"],
        request_body=HotelSerializer,
        responses={
            200: openapi.Response(
                description="Отель успешно обновлен", schema=HotelSerializer()
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
        tags=["2. Отель"],
        responses={204: "Отель успешно удален", 404: "Отель не найден"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class AmenityHotelCreateAPIView(generics.CreateAPIView):
    queryset = AmenityHotel.objects.all()
    serializer_class = AmenityHotelSerializer

    @swagger_auto_schema(
        operation_description="Создание нового удобства в отеле",
        operation_summary="Добавление удобства в отеле",
        request_body=AmenityHotelSerializer,
        tags=["2. Отель"],
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
