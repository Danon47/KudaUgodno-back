import random

from drf_spectacular.utils import (
    extend_schema_view, extend_schema, OpenApiResponse, OpenApiParameter
)
from rest_framework import viewsets, status
from rest_framework.response import Response

from config.settings import EMAIL_HOST_USER
from users.models import User
from users.serializers import UserSerializer, AdminSerializer
from users.tasks import clear_user_password, send_message


# Параметры для документации (для drf_spectacular) — пример с pk/id
user_parameters = [
    OpenApiParameter(
        name="pk",
        type=int,
        location=OpenApiParameter.PATH,
        description="Уникальный идентификатор пользователя",
        required=True,
    )
]

# Тэги, под которыми методы будут отображаться в документации
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
    # По умолчанию будем использовать «узкий» сериализатор
    serializer_class = UserSerializer

    def get_serializer_class(self):
        """
        В зависимости от действия (action) возвращаем тот или иной сериализатор.
        Для создания и обновления используем «полный» AdminSerializer,
        для чтения — «узкий» UserSerializer.
        """
        if self.action in ["create", "update", "partial_update"]:
            return AdminSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Переопределяем логику создания, чтобы:
        - Сгенерировать 4-значный код;
        - Установить его как пароль с хэшированием;
        - Отправить письмо на email;
        - Запустить задачу очистки пароля через 5 минут.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Генерация случайного 4-значного кода
        random_number = random.randint(1000, 9999)
        user.set_password(str(random_number))
        user.save(update_fields=["password"])

        # Отправка email с кодом подтверждения
        send_message.delay(
            "Код для подтверждения входа",
            f"Код для входа в сервис 'Куда Угодно': {random_number}.\n"
            "Никому не сообщайте его! Если вы не запрашивали код, игнорируйте сообщение.",
            EMAIL_HOST_USER,
            [user.email]
        )

        # Планирование задачи очистки пароля через 5 минут (300 секунд)
        clear_user_password.apply_async((user.id,), countdown=300)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
