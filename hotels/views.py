from random import choice

from django.db.models import F, OuterRef, Subquery, Window
from django.db.models.functions import RowNumber
from django.shortcuts import get_object_or_404
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
    hotel_id,
    hotel_id_photo,
    hotel_photo_settings,
    hotel_price_gte,
    hotel_price_lte,
    hotel_settings,
    id_hotel,
    limit,
    offset,
    type_of_meal_id,
    type_of_meal_settings,
    what_about_settings,
)
from all_fixture.pagination import CustomLOPagination
from hotels.filters import HotelExtendedFilter, HotelSearchFilter
from hotels.models import Hotel, HotelPhoto, HotelWhatAbout, TypeOfMeal
from hotels.serializers import (
    HotelBaseSerializer,
    HotelDetailSerializer,
    HotelFiltersRequestSerializer,
    HotelListRoomAndPhotoSerializer,
    HotelPhotoSerializer,
    HotelSearchRequestSerializer,
    HotelSearchResponseSerializer,
    HotelShortWithPriceSerializer,
    HotelWhatAboutFullSerializer,
)
from hotels.serializers_type_of_meals import TypeOfMealSerializer
from rooms.models import CalendarPrice


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
        responses={201: HotelBaseSerializer, 400: OpenApiResponse(description="Ошибка валидации")},
        tags=[hotel_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Детали отеля",
        description="Получение полной информации об отеле",
        parameters=[id_hotel],
        responses={200: HotelListRoomAndPhotoSerializer, 404: OpenApiResponse(description="Отель не найден")},
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
        summary="Фильтрация отелей",
        description="Расширенная фильтрация отелей",
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


@extend_schema_view(
    list=extend_schema(
        summary="Список акционных отелей",
        description="Получение списка всех акционных отелей",
        parameters=[limit, offset],
        tags=[hotel_settings["name"]],
        responses={
            200: HotelShortWithPriceSerializer(many=True),
        },
    )
)
class HotelsHotView(viewsets.ModelViewSet):
    """Горящие туры по одному из каждой страны по минимальной цене."""

    serializer_class = HotelShortWithPriceSerializer
    pagination_class = CustomLOPagination
    http_method_names = ["get"]

    def get_queryset(self):
        """Получение запроса с отелями по одному из каждой страны с минимальной ценой."""
        min_price_subquery = (
            CalendarPrice.objects.filter(
                room_date__stock=True, room_date__available_for_booking=True, room__hotel=OuterRef("pk")
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
                    expression=RowNumber(), partition_by=[F("country")], order_by=F("min_price").asc()
                )
            )
            .filter(grouped_countries=1)
            .order_by("country")
        )

        return queryset


@extend_schema_view(
    list=extend_schema(
        summary="Список типов фотографий отеля",
        description="Получение списка всех фотографий отеля",
        parameters=[hotel_id],
        responses={
            200: HotelPhotoSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[hotel_photo_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление фотографий отеля",
        description="Создание новых фотографий отеля",
        parameters=[hotel_id],
        request={
            "multipart/form-data": HotelPhotoSerializer,
        },
        responses={
            201: HotelPhotoSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=[hotel_photo_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление фотографий отеля",
        description="Полное удаление фотографий отеля",
        parameters=[hotel_id, hotel_id_photo],
        responses={
            204: OpenApiResponse(description="Тип питания в отеле удален"),
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[hotel_photo_settings["name"]],
    ),
)
class HotelPhotoViewSet(viewsets.ModelViewSet):
    queryset = HotelPhoto.objects.none()
    serializer_class = HotelPhotoSerializer
    http_method_names = ["get", "post", "delete", "head", "options", "trace"]  # исключаем обновления

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
        parameters=[hotel_id],
        responses={
            200: TypeOfMealSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
        tags=[type_of_meal_settings["name"]],
    ),
    create=extend_schema(
        summary="Добавление типа питания в определённый отель",
        description="Создание нового типа питания в определённом отеле",
        parameters=[hotel_id],
        request={
            "multipart/form-data": TypeOfMealSerializer,
        },
        responses={
            201: TypeOfMealSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
        tags=[type_of_meal_settings["name"]],
    ),
    retrieve=extend_schema(
        summary="Получение типа питания в определённом отеле",
        description="Получение типа питания в определённом отеле",
        parameters=[hotel_id, type_of_meal_id],
        responses={
            200: TypeOfMealSerializer,
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[type_of_meal_settings["name"]],
    ),
    update=extend_schema(
        summary="Полное обновление типа питания в определённом отеле",
        description="Обновление всех полей типа питания в определённом отеле",
        request=TypeOfMealSerializer,
        parameters=[hotel_id, type_of_meal_id],
        responses={
            200: TypeOfMealSerializer,
            400: OpenApiResponse(description="Ошибка запроса"),
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[type_of_meal_settings["name"]],
    ),
    destroy=extend_schema(
        summary="Удаление типа питания в определённом отеле",
        description="Полное удаление типа питания в определённом отеле",
        parameters=[hotel_id, type_of_meal_id],
        responses={
            204: OpenApiResponse(description="Тип питания в отеле удален"),
            404: OpenApiResponse(description="Тип питания в отеле не найден"),
        },
        tags=[type_of_meal_settings["name"]],
    ),
)
class TypeOfMealViewSet(viewsets.ModelViewSet):
    queryset = TypeOfMeal.objects.none()
    serializer_class = TypeOfMealSerializer
    http_method_names = ["get", "post", "delete", "put", "head", "options", "trace"]  # исключаем обновления

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
        tags=[what_about_settings["name"]],
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
