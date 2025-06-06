from dal import autocomplete
from django.db.models import F, OuterRef, Subquery, Window
from django.db.models.functions import RowNumber
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from all_fixture.fixture_views import (
    filter_city,
    filter_distance_to_the_airport,
    filter_place,
    filter_star_category,
    filter_tour_operator,
    filter_type_of_rest,
    filter_user_rating,
    limit,
    offset,
    tour_arrival_city,
    tour_arrival_city_optional,
    tour_departure_city,
    tour_departure_city_optional,
    tour_guests,
    tour_guests_optional,
    tour_id,
    tour_nights,
    tour_nights_optional,
    tour_price_gte,
    tour_price_lte,
    tour_settings,
    tour_start_date,
    tour_start_date_optional,
    tour_stock_id,
    tour_stock_settings,
)
from all_fixture.pagination import CustomLOPagination
from hotels.models import Hotel, TypeOfMeal
from rooms.models import Room, RoomCategory
from tours.filters import TourExtendedFilter, TourSearchFilter
from tours.models import Tour, TourStock
from tours.serializers import (
    TourFiltersRequestSerializer,
    TourListSerializer,
    TourPatchSerializer,
    TourSearchRequestSerializer,
    TourSerializer,
    TourShortSerializer,
    TourStockSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Список туров",
        description="Получение списка всех туров",
        tags=[tour_settings["name"]],
        parameters=[limit, offset],
        responses={
            200: TourListSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
    ),
    create=extend_schema(
        summary="Добавление тура",
        description="Создание нового тура",
        request=TourSerializer,
        tags=[tour_settings["name"]],
        responses={
            201: TourSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о туре",
        description="Получение информации о туре через идентификатор",
        tags=[tour_settings["name"]],
        parameters=[tour_id],
        responses={
            200: TourListSerializer,
            404: OpenApiResponse(description="Тур не найден"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление тура",
        description="Обновление всех полей тура",
        request=TourSerializer,
        tags=[tour_settings["name"]],
        parameters=[tour_id],
        responses={
            200: TourSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Тур не найден"),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление тура",
        description="Обновление отдельных полей тура",
        request=TourPatchSerializer,
        tags=[tour_settings["name"]],
        parameters=[tour_id],
        responses={
            200: TourPatchSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Тур не найден"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление тура",
        description="Полное удаление тура",
        tags=[tour_settings["name"]],
        parameters=[tour_id],
        responses={
            204: OpenApiResponse(description="Тур удален"),
            404: OpenApiResponse(description="Тур не найден"),
        },
    ),
)
class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    pagination_class = CustomLOPagination

    def get_serializer_class(self):
        if self.action == "partial_update":
            return TourPatchSerializer
        elif self.action in ["list", "retrieve"]:
            return TourListSerializer
        else:
            return TourSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список всех акций в турах",
        description="Получение списка всех акций в турах",
        tags=[tour_stock_settings["name"]],
        parameters=[limit, offset],
        responses={
            200: TourStockSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
    ),
    create=extend_schema(
        summary="Добавление акции в туре",
        description="Создание новой акции в туре",
        request={"multipart/form-data": TourSerializer},
        tags=[tour_stock_settings["name"]],
        responses={
            201: TourStockSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о акции в туре",
        description="Получение информации о акции в туре через идентификатор",
        tags=[tour_stock_settings["name"]],
        parameters=[tour_stock_id],
        responses={
            200: TourStockSerializer,
            404: OpenApiResponse(description="Акция в туре не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление акции в туре",
        description="Обновление всех полей акции в туре",
        request=TourStockSerializer,
        tags=[tour_stock_settings["name"]],
        parameters=[tour_stock_id],
        responses={
            200: TourStockSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Акция в туре не найдена"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление акции в туре",
        description="Полное удаление акции в туре",
        tags=[tour_stock_settings["name"]],
        parameters=[tour_stock_id],
        responses={
            204: OpenApiResponse(description="Акция в туре удалена"),
            404: OpenApiResponse(description="Акция в туре не найдена"),
        },
    ),
)
class TourStockViewSet(viewsets.ModelViewSet):
    queryset = TourStock.objects.all()
    serializer_class = TourStockSerializer
    pagination_class = CustomLOPagination
    http_method_names = ["get", "post", "put", "delete", "head", "options", "trace"]


@extend_schema_view(
    search=extend_schema(
        summary="Поиск туров",
        description="Поиск туров по городам вылета/прилета, дате вылета, количеству ночей и гостей.",
        parameters=[tour_departure_city, tour_arrival_city, tour_start_date, tour_nights, tour_guests, limit, offset],
        tags=[tour_settings["name"]],
        responses={
            200: TourShortSerializer(many=True),
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    )
)
class TourSearchView(viewsets.ModelViewSet):
    """Поиск туров с учетом фильтров город вылета/прилёта, даты вылета, кол-ва ночей/гостей."""

    queryset = Tour.objects.none
    serializer_class = TourShortSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TourSearchFilter
    pagination_class = CustomLOPagination
    http_method_names = ["get"]

    def get_queryset(self):
        """Получение доступного тура с максимальным количеством гостей в комнате."""
        guests_subquery = (
            RoomCategory.objects.filter(
                room__tours=OuterRef("pk"),
                room_date__available_for_booking=True,
            )
            .annotate(total_guests=F("room__number_of_adults") + F("room__number_of_children"))
            .order_by("-total_guests")
            .values("room__number_of_adults", "room__number_of_children")[:1]
        )

        queryset = (
            Tour.objects.filter(is_active=True)
            .annotate(
                number_of_adults=Subquery(guests_subquery.values("room__number_of_adults")),
                number_of_children=Subquery(guests_subquery.values("room__number_of_children")),
            )
            .order_by("arrival_country")
        )

        return queryset

    @action(detail=False, methods=["get"])
    def search(self, request):
        request_serializer = TourSearchRequestSerializer(data=request.query_params)
        if not request_serializer.is_valid():
            return Response({"errors": request_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return self.list(request)


@extend_schema_view(
    filters=extend_schema(
        summary="Расширенный поиск туров",
        description="Расширенный поиск туров по фильтрам.",
        parameters=[
            tour_departure_city_optional,
            tour_arrival_city_optional,
            tour_start_date_optional,
            tour_nights_optional,
            tour_guests_optional,
            filter_city,
            filter_type_of_rest,
            filter_place,
            tour_price_gte,
            tour_price_lte,
            filter_user_rating,
            filter_star_category,
            filter_distance_to_the_airport,
            filter_tour_operator,
            limit,
            offset,
        ],
        tags=[tour_settings["name"]],
        responses={
            200: TourShortSerializer(many=True),
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
)
class TourFiltersView(viewsets.ModelViewSet):
    """Расширенный поиск туров с дополнительными фильтрами по отелям и другим параметрам."""

    queryset = Tour.objects.none
    serializer_class = TourShortSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TourExtendedFilter
    pagination_class = CustomLOPagination
    http_method_names = ["get"]

    def get_queryset(self):
        """Получение доступного тура с максимальным количеством гостей в комнате."""
        guests_subquery = (
            RoomCategory.objects.filter(
                room__tours=OuterRef("pk"),
                room_date__available_for_booking=True,
            )
            .annotate(total_guests=F("room__number_of_adults") + F("room__number_of_children"))
            .order_by("-total_guests")
            .values("room__number_of_adults", "room__number_of_children")[:1]
        )

        queryset = (
            Tour.objects.filter(is_active=True)
            .annotate(
                number_of_adults=Subquery(guests_subquery.values("room__number_of_adults")),
                number_of_children=Subquery(guests_subquery.values("room__number_of_children")),
            )
            .order_by("arrival_country")
        )

        return queryset

    @action(detail=False, methods=["get"])
    def filters(self, request):
        request_serializer = TourFiltersRequestSerializer(data=request.query_params)
        if not request_serializer.is_valid():
            return Response({"errors": request_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return self.list(request)


@extend_schema_view(
    list=extend_schema(
        summary="Список горящих туров",
        description="Получение списка всех горящих туров",
        parameters=[limit, offset],
        tags=[tour_settings["name"]],
        responses={
            200: TourShortSerializer(many=True),
        },
    )
)
class TourHotView(viewsets.ModelViewSet):
    """Горящие туры по одному из каждой страны по минимальной цене."""

    serializer_class = TourShortSerializer
    pagination_class = CustomLOPagination
    http_method_names = ["get"]

    def get_queryset(self):
        """Получение тура по одному из каждой страны с минимальной ценой."""
        guests_subquery = (
            RoomCategory.objects.filter(
                room_date__stock=True, room_date__available_for_booking=True, room__tours=OuterRef("pk")
            )
            .order_by("price")
            .values("room__number_of_adults", "room__number_of_children")[:1]
        )

        queryset = (
            Tour.objects.filter(is_active=True, stock__active_stock=True)
            .annotate(
                number_of_adults=Subquery(guests_subquery.values("room__number_of_adults")),
                number_of_children=Subquery(guests_subquery.values("room__number_of_children")),
                country_rank=Window(
                    expression=RowNumber(), partition_by=[F("arrival_country")], order_by=F("price").asc()
                ),
            )
            .filter(country_rank=1)
            .order_by("arrival_country")
        )

        return queryset


class HotelAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Hotel.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


class RoomAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Получаем отель из параметров запроса
        hotel_id = self.forwarded.get("hotel", None)
        qs = Room.objects.all()

        if hotel_id:
            # Фильтруем номера только для выбранного отеля
            qs = qs.filter(hotel_id=hotel_id)

        if self.q:
            # Добавляем поиск по категории номера
            qs = qs.filter(category__icontains=self.q)

        return qs


class TypeOfMealAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Получаем отель из параметров запроса
        hotel_id = self.forwarded.get("hotel", None)
        qs = TypeOfMeal.objects.all()

        if hotel_id:
            # Фильтруем типы питания только для выбранного отеля
            qs = qs.filter(hotel_id=hotel_id)

        if self.q:
            # Добавляем поиск по названию типа питания
            qs = qs.filter(name__icontains=self.q)

        return qs.order_by("price")
