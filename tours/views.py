from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.fixture_views import limit, offset, tour_id, tour_settings, tour_stock_id, tour_stock_settings
from all_fixture.pagination import CustomLOPagination
from tours.models import Tour, TourStock
from tours.serializers import TourListSerializer, TourPatchSerializer, TourSerializer, TourStockSerializer


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

    def get_serializer_class(self):
        if self.action == "patch":
            return TourPatchSerializer
        elif self.action in ["list", "retrieve"]:
            return TourListSerializer
        else:
            return TourSerializer

    # def perform_create(self, serializer):
    #     tour = serializer.save()
    #     total_price = 0
    #     guests_number = tour.number_of_adults + tour.number_of_children
    #     if tour.number_of_children:
    #         guests_number = tour.number_of_adults + tour.number_of_children
    #     if tour.room and tour.flight_from and tour.flight_to:
    #         for room in tour.room.all():
    #             total_price += (
    #                 tour.end_date - tour.start_date
    #             ).days * room.nightly_price
    #         total_price += (
    #             tour.flight_to.price + tour.flight_from.price
    #         ) * guests_number
    #     tour.price = total_price
    #     tour.save()


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
