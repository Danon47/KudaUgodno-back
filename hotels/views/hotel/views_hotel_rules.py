from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import viewsets
from hotels.models.hotel.models_hotel_rules import HotelRules
from hotels.serializers.hotel.serializers_hotel_rules import HotelRulesSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список правил в отеле",
        description="Получение списка всех правил с пагинацией",
        responses={
            200: HotelRulesSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["Правила в отеле"],
    ),
    create=extend_schema(
        summary="Добавление правила в отель",
        description="Создание нового правила в отель",
        request=HotelRulesSerializer,
        responses={
            201: HotelRulesSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=["Правила в отеле"],
    ),
    retrieve=extend_schema(
        summary="Детали правил в отеле",
        description="Получение полной информации о правилах в отеле",
        responses={
            200: HotelRulesSerializer,
            404: OpenApiResponse(description="Правило в отеле не найдено"),
        },
        tags=["Правила в отеле"],
    ),
    update=extend_schema(
        summary="Полное обновление правил в отеле",
        description="Обновление всех полей правил в отеле",
        request=HotelRulesSerializer,
        responses={
            200: HotelRulesSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Правило в отеле не найдено"),
        },
        tags=["Правила в отеле"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление правил в отеле",
        description="Обновление отдельных полей правил в отеле",
        request=HotelRulesSerializer,
        responses={
            200: HotelRulesSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Правило в отеле не найдено"),
        },
        tags=["Правила в отеле"],
    ),
    destroy=extend_schema(
        summary="Удаление правила в отеле",
        description="Полное удаление правила в отеле",
        responses={
            204: OpenApiResponse(description="Правило в отеле удалено"),
            404: OpenApiResponse(description="Правило в отеле не найдено"),
        },
        tags=["Правила в отеле"],
    ),
)
class HotelRulesViewSet(viewsets.ModelViewSet):
    queryset = HotelRules.objects.all()
    serializer_class = HotelRulesSerializer
    pagination_class = None
