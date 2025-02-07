from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiResponse,
)
from rest_framework import viewsets

from all_fixture.fixture_views import (
    application_guest_settings,
    offset,
    limit,
    application_guest_id,
)
from applications.models.models_guest import Guest
from applications.serializers.serializers_guests import (
    GuestSerializer,
    GuestDetailSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="Список гостей",
        description="Получение списка всех гостей",
        tags=[application_guest_settings["name"]],
        parameters=[limit, offset],
        responses={
            200: GuestSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
        },
    ),
    create=extend_schema(
        summary="Добавление Гостя",
        description="Создание нового Гостя",
        request=GuestDetailSerializer,
        tags=[application_guest_settings["name"]],
        responses={
            201: GuestDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о Госте",
        description="Получение информации о Госте через идентификатор",
        tags=[application_guest_settings["name"]],
        parameters=application_guest_id,
        responses={
            200: GuestSerializer,
            404: OpenApiResponse(description="Гость не найден"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление Гостя",
        description="Обновление всех полей Гостя",
        request=GuestDetailSerializer,
        tags=[application_guest_settings["name"]],
        parameters=application_guest_id,
        responses={
            200: GuestDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Гость не найден"),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление Гостя",
        description="Обновление отдельных полей Гостя",
        request=GuestDetailSerializer,
        tags=[application_guest_settings["name"]],
        parameters=application_guest_id,
        responses={
            200: GuestDetailSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Гость не найден"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление Гостя",
        description="Полное удаление Гостя",
        tags=[application_guest_settings["name"]],
        parameters=application_guest_id,
        responses={
            204: OpenApiResponse(description="Гость удален"),
            404: OpenApiResponse(description="Гость не найден"),
        },
    ),
)
class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return GuestDetailSerializer
        return GuestSerializer

    def perform_create(self, serializer):
        serializer.save(user_owner=self.request.user)
