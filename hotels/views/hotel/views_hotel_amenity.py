from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import viewsets
from hotels.models.hotel.models_hotel_amenity import (HotelAmenityCommon, HotelAmenityForChildren,
                                                      HotelAmenityInTheRoom, HotelAmenitySportsAndRecreation)
from hotels.serializers.hotel.serializers_hotel_amenity import HotelAmenityCommonSerializer, \
    HotelAmenityInTheRoomSerializer, HotelAmenitySportsAndRecreationSerializer, HotelAmenityForChildrenSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список общих удобств в отеле",
        description="Получение списка всех общих удобств в отеле",
        responses={
            200: HotelAmenityCommonSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
    create=extend_schema(
        summary="Добавление общего удобства в отеле",
        description="Создание нового общего удобства в отеле",
        request=HotelAmenityCommonSerializer,
        responses={
            201: HotelAmenityCommonSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
    retrieve=extend_schema(
        summary="Детали общего удобства в отеле",
        description="Получение полной информации общего удобства в отеле",
        responses={
            200: HotelAmenityCommonSerializer,
            404: OpenApiResponse(description="Общее удобство в отеле не найдено"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
    update=extend_schema(
        summary="Полное обновление общего удобства в отеле",
        description="Обновление всех полей общего удобства в отеле",
        request=HotelAmenityCommonSerializer,
        responses={
            200: HotelAmenityCommonSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Общее удобство в отеле не найдено"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление общего удобства в отеле",
        description="Обновление отдельных полей общего удобства в отеле",
        request=HotelAmenityCommonSerializer,
        responses={
            200: HotelAmenityCommonSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Общее удобство в отеле не найдено"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
    destroy=extend_schema(
        summary="Удаление общего удобства в отеле",
        description="Полное удаление общего удобства в отеле",
        responses={
            204: OpenApiResponse(description="Общее удобство в отеле удалено"),
            404: OpenApiResponse(description="Общее удобство в отеле не найдено"),
        },
        tags=["3.1.1.1 Удобства общие в отеле"],
    ),
)
class HotelAmenityCommonViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenityCommon.objects.all()
    serializer_class = HotelAmenityCommonSerializer
    pagination_class = None


@extend_schema_view(
    list=extend_schema(
        summary="Список удобств номера в отеле",
        description="Получение списка всех удобств номера в отеле",
        responses={
            200: HotelAmenityInTheRoomSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["3.1.1.2 Удобства в номере в отеле"],
    ),
    create=extend_schema(
        summary="Добавление удобства номера в отеле",
        description="Создание нового удобства номера в отеле",
        request=HotelAmenityInTheRoomSerializer,
        responses={
            201: HotelAmenityInTheRoomSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=["3.1.1.2 Удобства в номере в отеле"],
    ),
    retrieve=extend_schema(
        summary="Детали удобства номера в отеле",
        description="Получение полной информации удобств номера в отеле",
        responses={
            200: HotelAmenityInTheRoomSerializer,
            404: OpenApiResponse(description="Удобство номера в отеле не найдено"),
        },
        tags=["3.1.1.2 Удобства в номере в отеле"],
    ),
    update=extend_schema(
        summary="Полное обновление удобств номера в отеле",
        description="Обновление всех полей удобств номера в отеле",
        request=HotelAmenityInTheRoomSerializer,
        responses={
            200: HotelAmenityInTheRoomSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Удобство номера в отеле не найдено"),
        },
        tags=["3.1.1.2 Удобства в номере в отеле"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление удобств номера в отеле",
        description="Обновление отдельных полей удобств номера в отеле",
        request=HotelAmenityInTheRoomSerializer,
        responses={
            200: HotelAmenityInTheRoomSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Удобство номера в отеле не найдено"),
        },
        tags=["3.1.1.2 Удобства в номере в отеле"],
    ),
    destroy=extend_schema(
        summary="Удаление удобств номера в отеле",
        description="Полное удаление удобств номера в отеле",
        responses={
            204: OpenApiResponse(description="Удобство номера в отеле удалено"),
            404: OpenApiResponse(description="Удобство номера в отеле не найдено"),
        },
        tags=["3.1.1.2 Удобства в номере в отеле"],
    ),
)
class HotelAmenityInTheRoomViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenityInTheRoom.objects.all()
    serializer_class = HotelAmenityInTheRoomSerializer
    pagination_class = None


@extend_schema_view(
    list=extend_schema(
        summary="Список удобств спорта и отдыха в отеле",
        description="Получение списка всех удобств спорта и отдыха в отеле",
        responses={
            200: HotelAmenitySportsAndRecreationSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["3.1.1.3 Удобства спорт и отдых в отеле"],
    ),
    create=extend_schema(
        summary="Добавление удобства спорт и отдых в отеле",
        description="Создание нового удобства спорт и отдых в отеле",
        request=HotelAmenitySportsAndRecreationSerializer,
        responses={
            201: HotelAmenitySportsAndRecreationSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=["3.1.1.3 Удобства спорт и отдых в отеле"],
    ),
    retrieve=extend_schema(
        summary="Детали удобства спорт и отдых в отеле",
        description="Получение полной информации удобств спорт и отдых в отеле",
        responses={
            200: HotelAmenitySportsAndRecreationSerializer,
            404: OpenApiResponse(description="Удобство спорт и отдых в отеле не найдено"),
        },
        tags=["3.1.1.3 Удобства спорт и отдых в отеле"],
    ),
    update=extend_schema(
        summary="Полное обновление удобств спорт и отдых в отеле",
        description="Обновление всех полей удобств спорт и отдых в отеле",
        request=HotelAmenitySportsAndRecreationSerializer,
        responses={
            200: HotelAmenitySportsAndRecreationSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Удобство спорт и отдых в отеле не найдено"),
        },
        tags=["3.1.1.3 Удобства спорт и отдых в отеле"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление удобств спорт и отдых в отеле",
        description="Обновление отдельных полей удобств спорт и отдых в отеле",
        request=HotelAmenitySportsAndRecreationSerializer,
        responses={
            200: HotelAmenitySportsAndRecreationSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Удобство спорт и отдых в отеле не найдено"),
        },
        tags=["3.1.1.3 Удобства спорт и отдых в отеле"],
    ),
    destroy=extend_schema(
        summary="Удаление удобств спорт и отдых в отеле",
        description="Полное удаление удобств спорт и отдых в отеле",
        responses={
            204: OpenApiResponse(description="Удобство спорт и отдых в отеле удалено"),
            404: OpenApiResponse(description="Удобство спорт и отдых в отеле не найдено"),
        },
        tags=["3.1.1.3 Удобства спорт и отдых в отеле"],
    ),
)
class HotelAmenitySportsAndRecreationViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenitySportsAndRecreation.objects.all()
    serializer_class = HotelAmenitySportsAndRecreationSerializer
    pagination_class = None


@extend_schema_view(
    list=extend_schema(
        summary="Список удобств для детей в отеле",
        description="Получение списка всех удобств для детей в отеле",
        responses={
            200: HotelAmenitySportsAndRecreationSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=["3.1.1.4 Удобства для детей в отеле"],
    ),
    create=extend_schema(
        summary="Добавление удобства для детей в отеле",
        description="Создание нового удобства для детей в отеле",
        request=HotelAmenitySportsAndRecreationSerializer,
        responses={
            201: HotelAmenitySportsAndRecreationSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=["3.1.1.4 Удобства для детей в отеле"],
    ),
    retrieve=extend_schema(
        summary="Детали удобства для детей в отеле",
        description="Получение полной информации удобств для детей в отеле",
        responses={
            200: HotelAmenitySportsAndRecreationSerializer,
            404: OpenApiResponse(description="Удобство для детей в отеле не найдено"),
        },
        tags=["3.1.1.4 Удобства для детей в отеле"],
    ),
    update=extend_schema(
        summary="Полное обновление удобств для детей в отеле",
        description="Обновление всех полей удобств для детей в отеле",
        request=HotelAmenitySportsAndRecreationSerializer,
        responses={
            200: HotelAmenitySportsAndRecreationSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Удобство для детей в отеле не найдено"),
        },
        tags=["3.1.1.4 Удобства для детей в отеле"],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление удобств для детей в отеле",
        description="Обновление отдельных полей удобств для детей в отеле",
        request=HotelAmenitySportsAndRecreationSerializer,
        responses={
            200: HotelAmenitySportsAndRecreationSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Удобство для детей в отеле не найдено"),
        },
        tags=["3.1.1.4 Удобства для детей в отеле"],
    ),
    destroy=extend_schema(
        summary="Удаление удобств для детей в отеле",
        description="Полное удаление удобств для детей в отеле",
        responses={
            204: OpenApiResponse(description="Удобство для детей в отеле удалено"),
            404: OpenApiResponse(description="Удобство для детей в отеле не найдено"),
        },
        tags=["3.1.1.4 Удобства для детей в отеле"],
    ),
)
class HotelAmenityForChildrenViewSet(viewsets.ModelViewSet):
    queryset = HotelAmenityForChildren.objects.all()
    serializer_class = HotelAmenityForChildrenSerializer
    pagination_class = None

