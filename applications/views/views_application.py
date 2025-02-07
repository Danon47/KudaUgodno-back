from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from rest_framework import viewsets

from all_fixture.fixture_views import (
    application_settings,
    offset,
    limit,
    application_id,
)
from applications.models.models_application import Application
from applications.serializers.serializers_applications import (
    ApplicationSerializer,
    ApplicationDetailSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Список заявок",
        description="Получение списка всех заявок",
        tags=[application_settings["name"]],
        parameters=[limit, offset],
        responses={
            200: ApplicationSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
    ),
    create=extend_schema(
        summary="Добавление заявки",
        description="Создание новой заявки",
        request=ApplicationDetailSerializer,
        tags=[application_settings["name"]],
        responses={
            201: ApplicationDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о заявке",
        description="Получение информации о заявке через идентификатор",
        tags=[application_settings["name"]],
        parameters=application_id,
        responses={
            200: ApplicationSerializer,
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление заявки",
        description="Обновление всех полей заявки",
        request=ApplicationDetailSerializer,
        tags=[application_settings["name"]],
        parameters=application_id,
        responses={
            200: ApplicationDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Заявка не найден"),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление заявки",
        description="Обновление отдельных полей заявки",
        request=ApplicationDetailSerializer,
        tags=[application_settings["name"]],
        parameters=application_id,
        responses={
            200: ApplicationDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление заявки",
        description="Полное удаление заявки",
        tags=[application_settings["name"]],
        parameters=application_id,
        responses={
            204: OpenApiResponse(description="Заявка удалена"),
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
)
class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ApplicationDetailSerializer
        return ApplicationSerializer

    def perform_create(self, serializer):
        serializer.save(user_owner=self.request.user)
