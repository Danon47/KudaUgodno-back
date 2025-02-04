import random

from drf_spectacular.utils import (
    extend_schema_view, extend_schema, OpenApiResponse, OpenApiParameter
)
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.response import Response

from config.settings import EMAIL_HOST_USER
from users.models import User
from users.serializers import UserSerializer, AdminSerializer
from users.tasks import clear_user_password, send_message
from users.choices import RoleChoices

# Параметры для документации (drf-spectacular) — используем "id" вместо "pk"
user_parameters = [
    OpenApiParameter(
        name="id",
        type=int,
        location=OpenApiParameter.PATH,
        description="Уникальный идентификатор пользователя",
        required=True,
    )
]

tags_users = ["Пользователи"]


@extend_schema_view(
    list=extend_schema(
        summary="Список пользователей",
        description="Получение списка всех пользователей",
        tags=tags_users,
        parameters=[
            OpenApiParameter(
                name="limit",
                type=int,
                description="Количество пользователей для пагинации",
                required=False
            ),
            OpenApiParameter(
                name="offset",
                type=int,
                description="Смещение для пагинации",
                required=False
            ),
        ],
        responses={
            200: UserSerializer(many=True),
            400: OpenApiResponse(description="Ошибка валидации запроса"),
        },
    ),
    create=extend_schema(
        summary="Создание пользователя",
        description="Создание нового пользователя с генерацией 4-значного пароля и отправкой на email.",
        tags=tags_users,
        request=AdminSerializer,
        responses={
            201: AdminSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
        },
    ),
    retrieve=extend_schema(
        summary="Информация о пользователе",
        description="Получение информации о пользователе по его идентификатору",
        tags=tags_users,
        parameters=user_parameters,
        responses={
            200: UserSerializer,
            404: OpenApiResponse(description="Пользователь не найден"),
        },
    ),
    update=extend_schema(
        summary="Полное обновление пользователя",
        description="Обновление всех полей пользователя по его идентификатору",
        tags=tags_users,
        request=AdminSerializer,
        parameters=user_parameters,
        responses={
            200: AdminSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Пользователь не найден"),
        },
    ),
    partial_update=extend_schema(
        summary="Частичное обновление пользователя",
        description="Обновление отдельных полей пользователя по его идентификатору",
        tags=tags_users,
        request=AdminSerializer,
        parameters=user_parameters,
        responses={
            200: AdminSerializer,
            400: OpenApiResponse(description="Ошибка валидации"),
            404: OpenApiResponse(description="Пользователь не найден"),
        },
    ),
    destroy=extend_schema(
        summary="Удаление пользователя",
        description="Удаление пользователя по его идентификатору",
        tags=tags_users,
        parameters=user_parameters,
        responses={
            204: OpenApiResponse(description="Пользователь удалён"),
            404: OpenApiResponse(description="Пользователь не найден"),
        },
    ),
)
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для CRUD-операций над пользователями.
    """
    queryset = User.objects.all().order_by("-pk")
    serializer_class = UserSerializer

    # Ищем объект по "id", а не по "pk"
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return AdminSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        # 1. Валидируем данные сериализатора (ForbiddenWordValidator и т.д.)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # 2. Вызываем модельную валидацию, чтобы учесть clean()
        try:
            user.full_clean()
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)

        # 3. Генерируем 4-значный код и устанавливаем как пароль
        random_number = random.randint(1000, 9999)
        user.set_password(str(random_number))
        user.save(update_fields=["password"])

        # 4. Отправка email с кодом подтверждения
        send_message.delay(
            "Код для подтверждения входа",
            f"Код для входа в сервис 'Куда Угодно': {random_number}.\n"
            "Никому не сообщайте его! Если вы не запрашивали код, игнорируйте сообщение.",
            EMAIL_HOST_USER,
            [user.email]
        )

        # 5. Планируем задачу очистки пароля через 5 минут
        clear_user_password.apply_async((user.id,), countdown=300)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # Для полного обновления тоже вызываем model clean()
        partial = False
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        try:
            user.full_clean()
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        # Для частичного обновления
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        try:
            user.full_clean()
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)

        return Response(serializer.data, status=status.HTTP_200_OK)
