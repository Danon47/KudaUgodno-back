from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.fixture_views import application_id, application_settings, limit, offset
from applications.models import ApplicationHotel, ApplicationTour
from applications.serializers import (
    ApplicationHotelListSerializer,
    ApplicationHotelSerializer,
    ApplicationTourListSerializer,
    ApplicationTourSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Список заявок на тур",
        description="Получение списка всех заявок на тур",
        tags=[application_settings["name"]],
        parameters=[limit, offset],
        responses={
            200: ApplicationTourListSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
    ),
    create=extend_schema(
        summary="Добавление заявки на тур",
        description="Создание новой заявки на тур",
        request=ApplicationTourSerializer,
        tags=[application_settings["name"]],
        responses={
            201: ApplicationTourListSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о заявке на тур",
        description="Получение информации о заявке на тур через идентификатор",
        tags=[application_settings["name"]],
        parameters=[application_id],
        responses={
            200: ApplicationTourListSerializer,
            404: OpenApiResponse(description="Заявка на тур не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление заявки на тур",
        description="Обновление всех полей заявки",
        request=ApplicationTourSerializer,
        tags=[application_settings["name"]],
        parameters=[application_id],
        responses={
            200: ApplicationTourSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Заявка не найден"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление заявки на тур",
        description="Полное удаление заявки на тур",
        tags=[application_settings["name"]],
        parameters=[application_id],
        responses={
            204: OpenApiResponse(description="Заявка на тур удалена"),
            404: OpenApiResponse(description="Заявка на тур не найдена"),
        },
    ),
)
class ApplicationTourViewSet(viewsets.ModelViewSet):
    queryset = ApplicationTour.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ApplicationTourSerializer
        return ApplicationTourListSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user_owner=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary="Список заявок на отель",
        description="Получение списка заявок на отель",
        tags=[application_settings["name"]],
        parameters=[limit, offset],
        responses={
            200: ApplicationHotelListSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
    ),
    create=extend_schema(
        summary="Добавление заявки на отель",
        description="Создание новой заявки на отель",
        request=ApplicationHotelSerializer,
        tags=[application_settings["name"]],
        responses={
            201: ApplicationHotelSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о заявке на отель",
        description="Получение информации о заявке на отель через идентификатор",
        tags=[application_settings["name"]],
        parameters=[application_id],
        responses={
            200: ApplicationHotelListSerializer,
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление заявки на отель",
        description="Обновление всех полей заявки на отель",
        request=ApplicationHotelSerializer,
        tags=[application_settings["name"]],
        parameters=[application_id],
        responses={
            200: ApplicationHotelSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление заявки на отель",
        description="Полное удаление заявки на отель",
        tags=[application_settings["name"]],
        parameters=[application_id],
        responses={
            204: OpenApiResponse(description="Заявка удалена"),
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
)
class ApplicationHotelViewSet(viewsets.ModelViewSet):
    queryset = ApplicationHotel.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ApplicationHotelSerializer
        return ApplicationHotelListSerializer
