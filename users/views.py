import random
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.mail import EmailMessage
from rest_framework import status, viewsets, mixins
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse
)
from config.settings import EMAIL_HOST_USER
from users.models import User
from users.serializers import (
    AdminSerializer,
    EmailLoginSerializer,
    UserSerializer,
    VerifyCodeSerializer
)
from users.tasks import clear_user_password


# 📌 Настройки API-документирования
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
)
class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления пользователями (CRUD).
    """
    queryset = User.objects.all().order_by("-pk")
    serializer_class = UserSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от действия."""
        if self.action in ["create", "update", "partial_update"]:
            return AdminSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        """
        Создание нового пользователя:
        - Проверка валидности данных
        - Генерация 4-значного кода
        - Отправка кода на email
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        try:
            user.full_clean()
        except DjangoValidationError as e:
            raise DRFValidationError(e.message_dict)

        random_number = random.randint(1000, 9999)
        user.set_password(str(random_number))
        user.save(update_fields=["password"])

        # 📩 Отправляем HTML-письмо с кодом
        email_message = EmailMessage(
            subject="Ваш код для входа",
            body=f"""
                <html>
                    <body>
                        <p>Код для входа в сервис <strong>'Куда Угодно'</strong>: 
                        <strong style="font-size:18px;color:#007bff;">{random_number}</strong>.</p>
                        <p><strong>Никому не сообщайте его!</strong> Если вы не запрашивали код, просто проигнорируйте это сообщение.</p>
                    </body>
                </html>
            """,
            from_email=EMAIL_HOST_USER,
            to=[user.email],
        )
        email_message.content_subtype = "html"  # Указываем HTML-формат
        email_message.send()

        # Очистка пароля через 5 минут
        clear_user_password.apply_async((user.id,), countdown=300)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    create=extend_schema(
        summary="Запросить код для входа",
        description="Отправляет 4-значный код на email пользователя для входа в систему.",
        request=EmailLoginSerializer,
        responses={200: OpenApiResponse(description="Код отправлен на email")},
    ),
    partial_update=extend_schema(
        summary="Подтвердить код и получить токен",
        description="Пользователь вводит email и код, получает JWT-токены.",
        request=VerifyCodeSerializer,
        responses={200: OpenApiResponse(description="JWT-токены получены")},
    ),
)
class AuthViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    ViewSet для аутентификации по email-коду.
    """
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Отправляет код для входа по email:
        - Проверяет, существует ли пользователь
        - Генерирует 4-значный код
        - Отправляет код на почту в HTML-формате
        """
        serializer = EmailLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

        code = random.randint(1000, 9999)
        user.set_password(str(code))
        user.save(update_fields=["password"])

        # 📩 Отправляем email с HTML-кодом
        email_message = EmailMessage(
            subject="Ваш код для входа",
            body=f"""
                <html>
                    <body>
                        <p>Код для входа в сервис <strong>'Куда Угодно'</strong>: 
                        <strong style="font-size:18px;color:#007bff;">{code}</strong>.</p>
                        <p><strong>Никому не сообщайте его!</strong> Если вы не запрашивали код, просто проигнорируйте это сообщение.</p>
                    </body>
                </html>
            """,
            from_email=EMAIL_HOST_USER,
            to=[user.email],
        )
        email_message.content_subtype = "html"
        email_message.send()

        # Очищаем пароль через 5 минут
        clear_user_password.apply_async((user.id,), countdown=300)

        return Response({"message": "Код отправлен на email"}, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        """
        Проверяет код и возвращает JWT-токены + роль пользователя.
        """
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        user = authenticate(email=email, password=str(code))
        if user:
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "role": user.role,  # 🔹 Добавляем роль пользователя в ответ
            }, status=status.HTTP_200_OK)

        return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
