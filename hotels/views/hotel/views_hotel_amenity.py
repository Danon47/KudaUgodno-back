from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import viewsets
from hotels.models.hotel.models_hotel_amenity import (HotelAmenityCommon, HotelAmenityForChildren,
                                                      HotelAmenityInTheRoom, HotelAmenitySportsAndRecreation)
from hotels.serializers.hotel.serializers_hotel_amenity import HotelAmenityCommonSerializer, \
    HotelAmenityInTheRoomSerializer, HotelAmenitySportsAndRecreationSerializer, HotelAmenityForChildrenSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список удобств в отеле",
        description="Получение списка всех удобств в отеле",
        responses={
            200: HotelAmenityCommonSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
    create=extend_schema(
        summary="Добавление удобство в отеле",
        description="Создание нового удобства в отеле",
        request=HotelAmenityCommonSerializer,
        responses={
            201: HotelAmenityCommonSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
    retrieve=extend_schema(
        summary="Детали удобств в отеле",
        description="Получение полной информации удобств в отеле",
        responses={
            200: HotelAmenityCommonSerializer,
            404: OpenApiResponse(description="Удобство в отеле не найдено"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
    update=extend_schema(
        summary="Полное обновление удобств в отеле",
        description="Обновление всех полей удобств в отеле",
        request=HotelAmenityCommonSerializer,
        responses={
            200: HotelAmenityCommonSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Удобство в отеле не найдено"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление удобств в отеле",
        description="Обновление отдельных полей удобств в отеле",
        request=HotelAmenityCommonSerializer,
        responses={
            200: HotelAmenityCommonSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Удобство в отеле не найдено"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
    destroy=extend_schema(
        summary="Удаление удобств в отеле",
        description="Полное удаление удобств в отеле",
        responses={
            204: OpenApiResponse(description="Удобство в отеле удалено"),
            404: OpenApiResponse(description="Удобство в отеле не найдено"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
)
class HotelAmenityCommonViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenityCommon.objects.all()
    serializer_class = HotelAmenityCommonSerializer
    pagination_class = None


class HotelAmenityInTheRoomViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenityInTheRoom.objects.all()
    serializer_class = HotelAmenityInTheRoomSerializer
    pagination_class = None


class HotelAmenitySportsAndRecreationViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenitySportsAndRecreation.objects.all()
    serializer_class = HotelAmenitySportsAndRecreationSerializer
    pagination_class = None


class HotelAmenityForChildrenViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenityForChildren.objects.all()
    serializer_class = HotelAmenityForChildrenSerializer
    pagination_class = None

