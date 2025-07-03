from random import choice

from django.db.models import Count, F, OuterRef, Subquery, Window
from django.db.models.functions import RowNumber
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from all_fixture.pagination import CustomLOPagination
from all_fixture.views_fixture import (
    FILTER_CITY,
    FILTER_PLACE,
    FILTER_STAR_CATEGORY,
    FILTER_TYPE_OF_REST,
    FILTER_USER_RATING,
    HOTEL_CHECK_IN,
    HOTEL_CHECK_OUT,
    HOTEL_GUESTS,
    HOTEL_ID,
    HOTEL_ID_PHOTO,
    HOTEL_PHOTO_SETTINGS,
    HOTEL_PRICE_GTE,
    HOTEL_PRICE_LTE,
    HOTEL_SETTINGS,
    ID_HOTEL,
    LIMIT,
    OFFSET,
    TYPE_OF_MEAL_ID,
    TYPE_OF_MEAL_SETTINGS,
    WHAT_ABOUT_SETTINGS,
)
from calendars.models import CalendarPrice
from hotels.filters import HotelFilter
from hotels.models import Hotel, HotelPhoto, HotelWhatAbout, TypeOfMeal
from hotels.serializers import (
    HotelBaseSerializer,
    HotelDetailSerializer,
    HotelFiltersRequestSerializer,
    HotelFiltersResponseSerializer,
    HotelListRoomAndPhotoSerializer,
    HotelPhotoSerializer,
    HotelPopularSerializer,
    HotelShortWithPriceSerializer,
    HotelWhatAboutFullSerializer,
)
from hotels.serializers_type_of_meals import TypeOfMealSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список отелей",
        description="Получение списка всех отелей с пагинацией",
        parameters=[OFFSET, LIMIT],
        responses={
            200: HotelListRoomAndPhotoSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[HOTEL_SETTINGS["name"]],
    ),
    create=extend_schema(
        summary="Добавление отеля",
        description="Создание нового отеля",
        request=HotelBaseSerializer,
        responses={
            201: HotelBaseSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=[HOTEL_SETTINGS["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали отеля",
        description="Получение полной информации об отеле",
        parameters=[ID_HOTEL],
        responses={
            200: HotelListRoomAndPhotoSerializer,
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=[HOTEL_SETTINGS["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление отеля",
        description="Обновление всех полей отеля",
        parameters=[ID_HOTEL],
        request=HotelDetailSerializer,
        responses={
            200: HotelDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=[HOTEL_SETTINGS["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление отеля",
        description="Полное удаление отеля",
        parameters=[ID_HOTEL],
        responses={
            204: OpenApiResponse(description="Отель удален"),
            404: OpenApiResponse(description="Отель не найден"),
        },
        tags=[HOTEL_SETTINGS["name"]],
    ),
)
class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    pagination_class = CustomLOPagination
    http_method_names = [
        "get",
        "post",
        "put",
        "delete",
        "head",
        "options",
        "trace",
    ]  # Исключаем 'patch'

    def get_serializer_class(self):
        if self.action == "create":
            return HotelBaseSerializer
        elif self.action in ["list", "retrieve"]:
            return HotelListRoomAndPhotoSerializer
        else:
            return HotelDetailSerializer


@extend_schema_view(
    filters=extend_schema(
        summary="Фильтрация отелей",
        description="Расширенная фильтрация отелей",
        parameters=[
            LIMIT,
            OFFSET,
            HOTEL_CHECK_IN,
            HOTEL_CHECK_OUT,
            HOTEL_GUESTS,
            FILTER_CITY,
            FILTER_TYPE_OF_REST,
            FILTER_PLACE,
            HOTEL_PRICE_GTE,
            HOTEL_PRICE_LTE,
            FILTER_USER_RATING,
            FILTER_STAR_CATEGORY,
        ],
        tags=[HOTEL_SETTINGS["name"]],
        responses={
            200: HotelFiltersResponseSerializer(many=True),
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
)
class HotelFiltersView(viewsets.ModelViewSet):
    """Расширенный поиск отелей с дополнительными фильтрами по отелям и другим параметрам."""

    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelFiltersResponseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter
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
            return Response(
                {"errors": request_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return self.list(request)


@extend_schema_view(
    list=extend_schema(
        summary="Список акционных отелей",
        description="Получение списка всех акционных отелей",
        parameters=[LIMIT, OFFSET],
        tags=[HOTEL_SETTINGS["name"]],
        responses={
            200: HotelShortWithPriceSerializer(many=True),
        },
    )
)
class HotelsHotView(viewsets.ModelViewSet):
    """Горящее предложение от отелей по одному из каждой страны по минимальной цене."""

    serializer_class = HotelShortWithPriceSerializer
    pagination_class = CustomLOPagination
    http_method_names = ["get"]

    def get_queryset(self):
        """Получение запроса с отелями по одному из каждой страны с минимальной ценой."""
        min_price_subquery = (
            CalendarPrice.objects.filter(
                calendar_date__discount=True,
                calendar_date__available_for_booking=True,
                room__hotel=OuterRef("pk"),
            )
            .order_by("price")
            .values("price")[:1]
        )

        queryset = (
            Hotel.objects.filter(is_active=True)
            .annotate(min_price=Subquery(min_price_subquery))
            .exclude(min_price=None)
            .annotate(
                grouped_countries=Window(
                    expression=RowNumber(),
                    partition_by=[F("country")],
                    order_by=F("min_price").asc(),
                )
            )
            .filter(grouped_countries=1)
            .order_by("country")
        )

        return queryset


@extend_schema_view(
    list=extend_schema(
        summary="Список популярных отелей",
        description="Получение списка шести популярных отелей",
        parameters=[LIMIT, OFFSET],
        tags=[HOTEL_SETTINGS["name"]],
        responses={
            200: HotelPopularSerializer(many=True),
        },
    )
)
class HotelsPopularView(viewsets.ModelViewSet):
    """Отели шести стран."""

    serializer_class = HotelPopularSerializer
    pagination_class = CustomLOPagination
    http_method_names = ["get"]

    def get_queryset(self):
        """Получение запроса с отелями по одному из шести стран с минимальной ценой."""
        min_price_subquery = (
            CalendarPrice.objects.filter(calendar_date__available_for_booking=True, room__hotel=OuterRef("pk"))
            .order_by("price")
            .values("price")[:1]
        )
        country_hotel_count = (
            Hotel.objects.filter(is_active=True, country=OuterRef("country"))
            .values("country")
            .annotate(count=Count("id"))
            .values("count")
        )
        queryset = (
            Hotel.objects.filter(is_active=True)
            .annotate(
                hotels_count=Subquery(country_hotel_count),
                min_price=Subquery(min_price_subquery),
            )
            .exclude(min_price=None)
            .annotate(
                grouped_countries=Window(
                    expression=RowNumber(),
                    partition_by=[F("country")],
                    order_by=F("min_price").asc(),
                )
            )
            .filter(grouped_countries=1)
            .order_by("min_price")[:6]
        )

        return queryset


@extend_schema_view(
    list=extend_schema(
        summary="Список типов фотографий отеля",
        description="Получение списка всех фотографий отеля",
        parameters=[HOTEL_ID],
        responses={
            200: HotelPhotoSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[HOTEL_PHOTO_SETTINGS["name"]],
    ),
    create=extend_schema(
        summary="Добавление фотографий отеля",
        description="Создание новых фотографий отеля",
        parameters=[HOTEL_ID],
        request={
            "multipart/form-data": HotelPhotoSerializer,
        },
        responses={
            201: HotelPhotoSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=[HOTEL_PHOTO_SETTINGS["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление фотографий отеля",
        description="Полное удаление фотографий отеля",
        parameters=[HOTEL_ID, HOTEL_ID_PHOTO],
        responses={
            204: OpenApiResponse(description="Тип питания в отеле удален"),
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[HOTEL_PHOTO_SETTINGS["name"]],
    ),
)
class HotelPhotoViewSet(viewsets.ModelViewSet):
    queryset = HotelPhoto.objects.none()
    serializer_class = HotelPhotoSerializer
    http_method_names = [
        "get",
        "post",
        "delete",
        "head",
        "options",
        "trace",
    ]  # исключаем обновления

    def get_queryset(self):
        hotel_id = self.kwargs["hotel_id"]
        return HotelPhoto.objects.filter(hotel_id=hotel_id)

    def perform_create(self, serializer):
        hotel = get_object_or_404(Hotel, id=self.kwargs["hotel_id"])
        serializer.save(hotel=hotel)


@extend_schema_view(
    list=extend_schema(
        summary="Список типов питания в определённом отеле",
        description="Получение списка всех типов питания в определённом отеле",
        parameters=[HOTEL_ID],
        responses={
            200: TypeOfMealSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[TYPE_OF_MEAL_SETTINGS["name"]],
    ),
    create=extend_schema(
        summary="Добавление типа питания в определённый отель",
        description="Создание нового типа питания в определённом отеле",
        parameters=[HOTEL_ID],
        request={
            "multipart/form-data": TypeOfMealSerializer,
        },
        responses={
            201: TypeOfMealSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=[TYPE_OF_MEAL_SETTINGS["name"]],
    ),
    retrieve=extend_schema(
        summary="Получение типа питания в определённом отеле",
        description="Получение типа питания в определённом отеле",
        parameters=[HOTEL_ID, TYPE_OF_MEAL_ID],
        responses={
            200: TypeOfMealSerializer,
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[TYPE_OF_MEAL_SETTINGS["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление типа питания в определённом отеле",
        description="Обновление всех полей типа питания в определённом отеле",
        request=TypeOfMealSerializer,
        parameters=[HOTEL_ID, TYPE_OF_MEAL_ID],
        responses={
            200: TypeOfMealSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[TYPE_OF_MEAL_SETTINGS["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление типа питания в определённом отеле",
        description="Полное удаление типа питания в определённом отеле",
        parameters=[HOTEL_ID, TYPE_OF_MEAL_ID],
        responses={
            204: OpenApiResponse(description="Тип питания в отеле удален"),
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[TYPE_OF_MEAL_SETTINGS["name"]],
    ),
)
class TypeOfMealViewSet(viewsets.ModelViewSet):
    queryset = TypeOfMeal.objects.none()
    serializer_class = TypeOfMealSerializer
    http_method_names = [
        "get",
        "post",
        "delete",
        "put",
        "head",
        "options",
        "trace",
    ]  # исключаем обновления

    def get_queryset(self):
        hotel_id = self.kwargs["hotel_id"]
        return TypeOfMeal.objects.filter(hotel_id=hotel_id)

    def perform_create(self, serializer):
        hotel = get_object_or_404(Hotel, id=self.kwargs["hotel_id"])
        serializer.save(hotel=hotel)


@extend_schema_view(
    list=extend_schema(
        summary="Список подборок что насчёт ...",
        description="Получение списка подборок что насчёт ...",
        responses={
            200: HotelWhatAboutFullSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[WHAT_ABOUT_SETTINGS["name"]],
    )
)
class HotelWarpUpViewSet(viewsets.ModelViewSet):
    queryset = HotelWhatAbout.objects.none()
    serializer_class = HotelWhatAboutFullSerializer

    def get_queryset(self):
        """
        Возвращает случайную подборку
        """
        all_ids = list(HotelWhatAbout.objects.values_list("id", flat=True))
        if not all_ids:
            return HotelWhatAbout.objects.none()
        random_id = choice(all_ids)
        return HotelWhatAbout.objects.filter(id=random_id)
