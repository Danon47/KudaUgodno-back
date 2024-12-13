from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from .models import (
    Hotel,
    HotelRoom,
    AmenityRoom,
    AmenityHotel,
    CategoryHotelRoom,
)
from .pagination import MyPagination
from .serializers import (
    HotelSerializer,
    HotelRoomSerializer,
    AmenityRoomSerializer,
    AmenityHotelSerializer,
    CategoryHotelRoomSerializer,
)


class HotelRoomListCreateView(generics.ListCreateAPIView):
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer
    pagination_class = MyPagination

    @swagger_auto_schema(
        operation_description="Получение списка всех номеров",
        operation_summary="Список номеров",
        tags=["1. Номер"],
        responses={
            200: openapi.Response(
                description="Успешное получение списка номеров",
                schema=HotelRoomSerializer(many=True),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание нового номера",
        operation_summary="Добавление номера",
        request_body=HotelRoomSerializer,
        tags=["1. Номер"],
        responses={
            201: openapi.Response(
                description="Отель успешно номера", schema=HotelRoomSerializer()
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class HotelRoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer
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
        request_body=HotelRoomSerializer,
        responses={
            200: openapi.Response(
                description="Номер успешно обновлен", schema=HotelRoomSerializer()
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
        request_body=HotelRoomSerializer,
        responses={
            200: openapi.Response(
                description="Номер успешно обновлен", schema=HotelRoomSerializer()
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


class AmenityRoomListCreateView(generics.ListCreateAPIView):
    queryset = AmenityRoom.objects.all()
    serializer_class = AmenityRoomSerializer
    pagination_class = MyPagination

    @swagger_auto_schema(
        operation_description="Получение списка всех удобств в номере",
        operation_summary="Список удобств в номере",
        tags=["1.1 Удобства в номере"],
        responses={
            200: openapi.Response(
                description="Успешное получение списка удобств в номере",
                schema=AmenityRoomSerializer(many=True),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание нового удобства в номере",
        operation_summary="Добавление удобства в номере",
        request_body=AmenityRoomSerializer,
        tags=["1.1 Удобства в номере"],
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


class AmenityRoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AmenityRoom.objects.all()
    serializer_class = AmenityRoomSerializer
    pagination_class = MyPagination

    @swagger_auto_schema(
        operation_summary="Получение детальной информации о удобстве в номере",
        operation_description="Возвращает полную информацию о конкретном удобстве в номере по его идентификатору",
        tags=["1.1 Удобства в номере"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор удобства в номера в базе данных",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение информации о удобстве в номере",
                schema=HotelSerializer(),
            ),
            404: "Удобство в номере не найдено",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление информации удобства в номере",
        operation_description="Обновляет все поля удовства в номере целиком",
        tags=["1.1 Удобства в номере"],
        request_body=AmenityRoomSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор удобства в номера в базе данных",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Удобство в номере успешно обновлен",
                schema=AmenityRoomSerializer(),
            ),
            400: "Ошибка валидации",
            404: "Удобство в номере не найдено",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление информации удобства в номере",
        operation_description="Обновляет указанные поля удобства в номере",
        tags=["1.1 Удобства в номере"],
        request_body=AmenityRoomSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор удобства в номера в базе данных",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Удоства в номере успешно обновлен",
                schema=AmenityRoomSerializer(),
            ),
            400: "Ошибка валидации",
            404: "Удобство в номере не найдено",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление удобства в номере",
        operation_description="Полное удаление удобства в номере по его идентификатору",
        tags=["1.1 Удобства в номере"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор удобства в номера в базе данных",
                required=True,
            )
        ],
        responses={
            204: "Удобство в номере успешно удалено",
            404: "Удобство в номере не найдено",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


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


class AmenityHotelListCreateView(generics.ListCreateAPIView):
    queryset = AmenityHotel.objects.all()
    serializer_class = AmenityHotelSerializer
    pagination_class = MyPagination

    @swagger_auto_schema(
        operation_description="Получение списка всех удобств в отеле",
        operation_summary="Список удобств в отеле",
        tags=["2.1 Удобства в отеле"],
        responses={
            200: openapi.Response(
                description="Успешное получение списка удобств в отеле",
                schema=AmenityHotelSerializer(many=True),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание нового удобства в отеле",
        operation_summary="Добавление удобства в отеле",
        request_body=AmenityHotelSerializer,
        tags=["2.1 Удобства в отеле"],
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


class AmenityHotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AmenityHotel.objects.all()
    serializer_class = AmenityHotelSerializer
    pagination_class = MyPagination

    @swagger_auto_schema(
        operation_summary="Получение детальной информации удобств в отеле",
        operation_description="Возвращает полную информацию о конкретном удобстве в отеле по его идентификатору",
        tags=["2.1 Удобства в отеле"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор удобства в отеле в базе данных",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение информации удобства в отеле",
                schema=AmenityHotelSerializer(),
            ),
            404: "Удобство в отеле не найдено",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление информации удобства в отеле",
        operation_description="Обновляет все поля удобства в отеле целиком",
        tags=["2.1 Удобства в отеле"],
        request_body=AmenityHotelSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор удобства в отеле в базе данных",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Удобство в отеле успешно обновлено",
                schema=AmenityHotelSerializer(),
            ),
            400: "Ошибка валидации",
            404: "Удобство в отеле не найдено",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление информации удобства в отеле",
        operation_description="Обновляет указанные поля удобства в отеле",
        tags=["2.1 Удобства в отеле"],
        request_body=AmenityHotelSerializer,
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор удобства в отеле в базе данных",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Удобство в отеле успешно обновлено",
                schema=AmenityHotelSerializer(),
            ),
            400: "Ошибка валидации",
            404: "Удобство в отеле не найдено",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление удобства в отеле",
        operation_description="Полное удаление удобства в отеле по его идентификатору",
        tags=["2.1 Удобства в отеле"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор удобства в отеле в базе данных",
                required=True,
            )
        ],
        responses={
            204: "Удобство в отеле успешно удалено",
            404: "Удобство в отеле не найдено",
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class CategoryHotelRoomListCreateView(generics.ListCreateAPIView):
    queryset = CategoryHotelRoom.objects.all()
    serializer_class = CategoryHotelRoomSerializer
    pagination_class = MyPagination

    @swagger_auto_schema(
        operation_description="Получение списка всех категорий номера",
        operation_summary="Список категорий номера",
        tags=["1.2 Категории номера"],
        responses={
            200: openapi.Response(
                description="Успешное получение списка категорий номера",
                schema=CategoryHotelRoomSerializer(many=False),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание новой категории номера",
        operation_summary="Добавление категории номера",
        request_body=CategoryHotelRoomSerializer,
        tags=["1.2 Категории номера"],
        responses={
            201: openapi.Response(
                description="Категория номера успешно создана",
                schema=CategoryHotelRoomSerializer(),
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
