from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
)
from rest_framework import viewsets

from applications.models.models_application import Application
from applications.serializers.serializers_applications import (
    ApplicationSerializer,
    ApplicationDetailSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Список заявок",
        description="Получение списка всех заявок",
        tags=["5. Заявки"],
        parameters=[
            OpenApiParameter(
                name="limit",
                type=int,
                description="Количество Заявок для возврата на страницу",
                required=False,
                examples=[
                    OpenApiExample("Пример 1", value=10),
                    OpenApiExample("Пример 2", value=20),
                ],
            ),
            OpenApiParameter(
                name="offset",
                type=int,
                description="Начальный индекс для пагинации",
                required=False,
            ),
        ],
        responses={
            200: ApplicationSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
    ),
    create=extend_schema(
        summary="Добавление заявки",
        description="Создание новой заявки",
        request=ApplicationDetailSerializer,
        tags=["5. Заявки"],
        responses={
            201: ApplicationDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о заявке",
        description="Получение информации о заявке через идентификатор",
        tags=["5. Заявки"],
        responses={
            200: ApplicationSerializer,
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление заявки",
        description="Обновление всех полей заявки",
        request=ApplicationDetailSerializer,
        tags=["5. Заявки"],
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
        tags=["5. Заявки"],
        responses={
            200: ApplicationDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Заявка не найдена"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление заявки",
        description="Полное удаление заявки",
        tags=["5. Заявки"],
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
