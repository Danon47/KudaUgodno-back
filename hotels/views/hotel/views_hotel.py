from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
from rest_framework import viewsets
from hotels.models.hotel.models_hotel import Hotel
from hotels.serializers.hotel.serializers_hotel import HotelBaseSerializer, HotelDetailSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список отелей",
        description="Получение списка всех отелей с пагинацией",
        parameters=[
            OpenApiParameter(
                name="limit",
                type=int,
                description="Количество отелей для возврата на страницу",
                required=False,
                examples=[
                    OpenApiExample("Пример 1", value=10),
                    OpenApiExample("Пример 2", value=20),
                ],
            ),
            OpenApiParameter(
                name="offset",
                type=int,
                description="Начальный индекс для пагинации",
                required=False,
            ),
        ],
        responses={
            200: HotelDetailSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["Отель"],
    ),
    create=extend_schema(
        summary="Добавление отеля",
        description="Создание нового отеля",
        request=HotelBaseSerializer,
        responses={
            201: HotelBaseSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=["Отель"],
    ),
    retrieve=extend_schema(
        summary="Детали отеля",
        description="Получение полной информации об отеле",
        responses={
            200: HotelDetailSerializer,
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=["Отель"],
    ),
    update=extend_schema(
        summary="Полное обновление отеля",
        description="Обновление всех полей отеля",
        request=HotelDetailSerializer,
        responses={
            200: HotelDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=["Отель"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление отеля",
        description="Обновление отдельных полей отеля",
        request=HotelDetailSerializer,
        responses={
            200: HotelDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=["Отель"],
    ),
    destroy=extend_schema(
        summary="Удаление отеля",
        description="Полное удаление отеля",
        responses={
            204: OpenApiResponse(description="Отель удален"),
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=["Отель"],
    ),
)
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return HotelBaseSerializer
        else:
            return HotelDetailSerializer
