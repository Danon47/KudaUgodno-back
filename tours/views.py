from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.fixture_views import limit, offset, tour_id, tour_settings
from tours.models import Tour
from tours.serializers import TourListSerializer, TourPatchSerializer, TourSerializer


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
