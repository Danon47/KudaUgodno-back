from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets

from all_fixture.fixture_views import application_guest_id, application_guest_settings, limit, offset
from guests.models import Guest
from guests.serializers import GuestDetailSerializer, GuestSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список гостей",
        description="Получение списка всех гостей",
        tags=[application_guest_settings["name"]],
        parameters=[limit, offset],
        responses={200: GuestSerializer(many=True), 400: OpenApiResponse(description="Ошибка запроса")},
    ),
    create=extend_schema(
        summary="Добавление Гостя",
        description="Создание нового Гостя",
        request=GuestDetailSerializer,
        tags=[application_guest_settings["name"]],
        responses={201: GuestDetailSerializer, 400: OpenApiResponse(description="Ошибка валидации")},
    ),
    retrieve=extend_schema(
        summary="Информация о Госте",
        description="Получение информации о Госте через идентификатор",
        tags=[application_guest_settings["name"]],
        parameters=[application_guest_id],
        responses={200: GuestSerializer, 404: OpenApiResponse(description="Гость не найден")},
    ),
    update=extend_schema(
        summary="Полное обновление Гостя",
        description="Обновление всех полей Гостя",
        request=GuestDetailSerializer,
        tags=[application_guest_settings["name"]],
        parameters=[application_guest_id],
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
        parameters=[application_guest_id],
        responses={
            204: OpenApiResponse(description="Гость удален"),
            404: OpenApiResponse(description="Гость не найден"),
        },
    ),
)
class GuestViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "put", "delete", "head", "options", "trace"]  # Исключаем 'patch'

    def get_queryset(self):
        if self.request.user.is_superuser:
            # Админ видит всех гостей
            return Guest.objects.all()
            # Обычные пользователи видят только своих гостей
        return Guest.objects.filter(user_owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return GuestDetailSerializer
        return GuestSerializer

    def perform_create(self, serializer):
        serializer.save(user_owner=self.request.user)
