from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from all_fixture.fixture_views import application_guest_id, application_guest_settings
from guests.models import Guest
from guests.serializers import GuestDetailSerializer, GuestSerializer


@extend_schema_view(
    list=extend_schema(
        summary="Список гостей",
        description="Получение списка всех гостей. Доступен только авторизованным пользователям.",
        tags=[application_guest_settings["name"]],
        responses={
            200: GuestSerializer(many=True),
            400: OpenApiResponse(description="Ошибка запроса"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
        },
    ),
    create=extend_schema(
        summary="Добавление Гостя",
        description="Создание нового Гостя. Доступно только авторизованным пользователям.",
        request=GuestDetailSerializer,
        tags=[application_guest_settings["name"]],
        responses={
            201: GuestSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о Госте",
        description="Получение информации о Госте через идентификатор. Доступно только авторизованным пользователям.",
        tags=[application_guest_settings["name"]],
        parameters=[application_guest_id],
        responses={
            200: GuestSerializer,
            404: OpenApiResponse(description="Гость не найден"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление Гостя",
        description="Обновление всех полей Гостя. Доступно только авторизованным пользователям.",
        request=GuestDetailSerializer,
        tags=[application_guest_settings["name"]],
        parameters=[application_guest_id],
        responses={
            200: GuestSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Гость не найден"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление Гостя",
        description="Полное удаление Гостя. Доступно только авторизованным пользователям.",
        tags=[application_guest_settings["name"]],
        parameters=[application_guest_id],
        responses={
            204: OpenApiResponse(description="Гость удален"),
            404: OpenApiResponse(description="Гость не найден"),
            401: OpenApiResponse(description="Пользователь не авторизован"),
        },
    ),
)
class GuestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Guest.objects.none()

    http_method_names = ["get", "post", "put", "delete", "head", "options", "trace"]

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")

        if self.request.user.is_superuser:
            # Админ может видеть всех гостей, опционально по user_id
            if user_id is not None:
                return Guest.objects.filter(user_owner_id=user_id)
            return Guest.objects.all()

        # Обычный пользователь видит только своих гостей
        if user_id is not None and int(user_id) != self.request.user.id:
            return Guest.objects.none()  # Нельзя получить чужих гостей

        return Guest.objects.filter(user_owner=self.request.user)

    def get_object(self):
        try:
            return Guest.objects.get(pk=self.kwargs["pk"], user_owner_id=self.kwargs["user_id"])
        except Guest.DoesNotExist:
            raise NotFound("Гость не найден")

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return GuestDetailSerializer
        return GuestSerializer

    def perform_create(self, serializer):
        # Привязываем к user_id из URL (если админ) или к текущему пользователю
        user_id = self.kwargs.get("user_id")

        # Безопасность: обычные пользователи не могут создавать гостя другому юзеру
        if not self.request.user.is_superuser and int(user_id) != self.request.user.id:
            raise PermissionDenied("Нельзя создавать гостя другому пользователю")

        serializer.save(user_owner_id=user_id)
