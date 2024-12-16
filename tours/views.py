from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from tours.models import Tour
from tours.serializers import TourSerializer


class TourListCreateView(ListCreateAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    @swagger_auto_schema(
        operation_description="Получение списка туров",
        operation_summary="Список туров",
        tags=["2. Тур"],
        responses={
            200: openapi.Response(
                description="Успешное получение списка туров",
                schema=TourSerializer(many=True),
            ),
            400: "Ошибка запроса",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создание тура",
        operation_summary="Добавление тура",
        request_body=TourSerializer,
        tags=["2. Тур"],
        responses={
            201: openapi.Response(
                description="Успешное создание тура", schema=TourSerializer()
            ),
            400: "Ошибка валидации",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        tour = serializer.save()
        tour.name = tour.hotel.name
        tour.country = tour.hotel.country
        tour.city = tour.hotel.city
        tour.type_of_holiday = tour.hotel.type_of_holiday
        tour.price = ((tour.end_date - tour.start_date) * tour.room.price
                      + tour.flight_to.price + tour.flight_from.price + tour.meal_cost)
        tour.save()


class TourDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    @swagger_auto_schema(
        operation_summary="Получение детальной информации о туре",
        operation_description="Возвращает полную информацию о туре по его идентификатору",
        tags=["2. Тур"],
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_PATH,
                type=openapi.TYPE_INTEGER,
                description="Уникальный идентификатор тура в базе данных",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Успешное получение информации о туре",
                schema=TourSerializer(),
            ),
            404: "Тур не найден",
        },
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Полное обновление информации о туре",
        operation_description="Обновляет все поля тура",
        tags=["2. Тур"],
        request_body=TourSerializer,
        responses={
            200: openapi.Response(
                description="Тур успешно обновлен", schema=TourSerializer()
            ),
            400: "Ошибка валидации",
            404: "Тур не найден",
        },
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Частичное обновление информации о туре",
        operation_description="Обновляет указанные поля тура",
        tags=["2. Тур"],
        request_body=TourSerializer,
        responses={
            200: openapi.Response(
                description="Тур успешно обновлен", schema=TourSerializer()
            ),
            400: "Ошибка валидации",
            404: "Тур не найден",
        },
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Удаление тура",
        operation_description="Полное удаление тура по его идентификатору",
        tags=["2. Тур"],
        responses={204: "Тур успешно удален", 404: "Тур не найден"},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
