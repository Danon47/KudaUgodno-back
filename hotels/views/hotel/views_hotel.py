from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from all_fixture.fixture_views import (
    filter_city,
    filter_place,
    filter_star_category,
    filter_type_of_rest,
    filter_user_rating,
    hotel_check_in,
    hotel_check_in_optional,
    hotel_check_out,
    hotel_check_out_optional,
    hotel_city,
    hotel_guests,
    hotel_guests_optional,
    hotel_price_gte,
    hotel_price_lte,
    hotel_settings,
    id_hotel,
    limit,
    offset,
)
from all_fixture.pagination import CustomLOPagination
from hotels.filters.hotel.filters_hotel import HotelExtendedFilter, HotelSearchFilter
from hotels.models.hotel.models_hotel import Hotel
from hotels.serializers.hotel.serializers_hotel import (
    HotelBaseSerializer,
    HotelDetailSerializer,
    HotelFiltersRequestSerializer,
    HotelListRoomAndPhotoSerializer,
    HotelSearchRequestSerializer,
    HotelSearchResponseSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Список отелей",
        description="Получение списка всех отелей с пагинацией",
        parameters=[offset, limit],
        responses={
            200: HotelListRoomAndPhotoSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[hotel_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление отеля",
        description="Создание нового отеля",
        request=HotelBaseSerializer,
        responses={
            201: HotelBaseSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=[hotel_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали отеля",
        description="Получение полной информации об отеле",
        parameters=[id_hotel],
        responses={
            200: HotelListRoomAndPhotoSerializer,
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=[hotel_settings["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление отеля",
        description="Обновление всех полей отеля",
        parameters=[id_hotel],
        request=HotelDetailSerializer,
        responses={
            200: HotelDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=[hotel_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление отеля",
        description="Полное удаление отеля",
        parameters=[id_hotel],
        responses={
            204: OpenApiResponse(description="Отель удален"),
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=[hotel_settings["name"]],
    ),
)
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    pagination_class = CustomLOPagination
    http_method_names = ["get", "post", "put", "delete", "head", "options", "trace"]  # Исключаем 'patch'

    def get_serializer_class(self):
        if self.action == "create":
            return HotelBaseSerializer
        elif self.action in ["list", "retrieve"]:
            return HotelListRoomAndPhotoSerializer
        else:
            return HotelDetailSerializer


@extend_schema_view(
    search=extend_schema(
        summary="Поиск отелей",
        description="Поиск отелей по названию, датам и кол-ву гостей",
        parameters=[hotel_city, hotel_check_in, hotel_check_out, hotel_guests, limit, offset],
        tags=[hotel_settings["name"]],
        responses={
            200: HotelSearchResponseSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
)
class HotelSearchView(viewsets.ModelViewSet):
    """Поиск комнат отелей с учетом фильтров(ночи, гости) и рассчет стоимости номера."""

    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelSearchResponseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelSearchFilter
    pagination_class = CustomLOPagination
    http_method_names = ["get"]

    def get_serializer_context(self):
        """Передача данных в сериализатор для обработки перед response."""
        context = super().get_serializer_context()
        context.update(
            {
                "guests": self.request.query_params.get("guests", 1),
                "check_in_date": self.request.query_params["check_in_date"],
                "check_out_date": self.request.query_params["check_out_date"],
            }
        )
        return context

    @action(detail=False, methods=["get"])
    def search(self, request):
        """Получение данных по поиску."""
        request_serializer = HotelSearchRequestSerializer(data=request.query_params)
        if not request_serializer.is_valid():
            return Response({"errors": request_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return self.list(request)


@extend_schema_view(
    filters=extend_schema(
        summary="Расширенный поиск туров",
        description="Расширенный поиск туров по фильтрам",
        parameters=[
            limit,
            offset,
            hotel_city,
            hotel_check_in_optional,
            hotel_check_out_optional,
            hotel_guests_optional,
            filter_city,
            filter_type_of_rest,
            filter_place,
            hotel_price_gte,
            hotel_price_lte,
            filter_user_rating,
            filter_star_category,
        ],
        tags=[hotel_settings["name"]],
        responses={
            200: HotelSearchResponseSerializer(many=True),
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
)
class HotelFiltersView(viewsets.ModelViewSet):
    """Расширенный поиск туров с дополнительными фильтрами по отелям и другим параметрам."""

    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelSearchResponseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelExtendedFilter
    pagination_class = CustomLOPagination
    http_method_names = ["get"]

    def get_serializer_context(self):
        """Передача данных в сериализатор для обработки перед response."""
        context = super().get_serializer_context()
        context.update(
            {
                "guests": self.request.query_params.get("guests", 1),
                "check_in_date": self.request.query_params.get("check_in_date", None),
                "check_out_date": self.request.query_params.get("check_out_date", None),
            }
        )

        return context

    @action(detail=False, methods=["get"])
    def filters(self, request):
        """Получение данных по фильтрам."""
        request_serializer = HotelFiltersRequestSerializer(data=request.query_params)
        if not request_serializer.is_valid():
            return Response({"errors": request_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return self.list(request)
